import { useMemo } from 'react';
import { useQueries, useQuery } from '@tanstack/react-query';
import { agentService } from '../../services/agentService';
import { taskService } from '../../services/taskService';
import { useIdentity } from '../../features/identity/identityContext';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { hasAdminApiKey } from '../../utils/adminAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { taskAgentDispatchState } from '../../features/agentDispatch';
import type { AgentDispatchState } from '../../features/agentDispatch';
import type { Task } from '../../types/task';
import type { TaskRowAssigneeOption } from './TaskRow';

/** Sorted distinct iteration ids as one string, so a list rebuilt on every render keeps one query set. */
const iterationKey = (iterationIds: (number | null | undefined)[]) =>
    [...new Set(iterationIds.filter((id): id is number => id !== null && id !== undefined))].sort((a, b) => a - b).join(',');

export interface AgentRowFacts {
    /** The agent that holds a submitted task's review; null when any authorized person reviews. */
    reviewerById: Map<number, string | null>;
    /** Profiles with an enabled agent bound; null when this reader may not read the agent roster. */
    boundProfileIds: Set<number> | null;
}

/**
 * What a task row needs beside the task to show the agent status line and the Reviewer:
 * reviewer names of the iterations' submitted tasks, and which profiles have an agent bound.
 */
export const useAgentRowFacts = (iterationIds: (number | null | undefined)[]): AgentRowFacts => {
    const key = iterationKey(iterationIds);
    const ids = useMemo(() => (key === '' ? [] : key.split(',').map(Number)), [key]);
    const identity = useIdentity()?.identity;
    const { hasAgentKey } = useAgentAccess();
    // The roster is for workspace operators and agent or admin keys; others are not asked.
    const mayReadRoster = identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator' || hasAgentKey || hasAdminApiKey();

    // feedback-policy: query loading,error,retry,empty - optional row detail: while loading or after a failure the row leaves the Reviewer name out instead of guessing it.
    const reviewerQueries = useQueries({
        queries: ids.map(id => ({
            queryKey: ['tasks', id, 'resolved-reviewers'],
            queryFn: ({ signal }: { signal: AbortSignal }) => taskService.lookup({ iteration_id: id, task_status: 'resolved', limit: 100 }, signal),
            staleTime: 30_000,
        })),
    });
    // feedback-policy: query loading,error,retry,empty - optional row detail: without the roster the row does not claim that no agent is connected.
    const roster = useQuery({
        queryKey: ['agent-actor-roster', false],
        queryFn: () => agentService.getActorRoster(false, { quiet: true }),
        enabled: mayReadRoster,
        retry: protectedQueryRetry,
        staleTime: 60_000,
    });

    // The query array is new on every render; the time of the last load says when its data changed.
    const reviewerStamp = reviewerQueries.map(query => query.dataUpdatedAt).join(',');
    const reviewerById = useMemo(() => {
        const map = new Map<number, string | null>();
        reviewerQueries.forEach(query => query.data?.items.forEach(item => map.set(item.id, item.reviewer_name ?? null)));
        return map;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [reviewerStamp]);
    const rosterData = roster.data;
    const boundProfileIds = useMemo(() => rosterData
        ? new Set(rosterData.filter(actor => actor.enabled && actor.lifecycle_state !== 'disabled' && actor.profile_id !== null).map(actor => actor.profile_id as number))
        : null, [rosterData]);

    return { reviewerById, boundProfileIds };
};

/**
 * The agent status line and the Reviewer for one row. The status line is for an agent
 * assignee only; the Reviewer is named once the task is submitted. While any loaded task is
 * submitted, other rows keep an empty reviewer cell so the columns line up; with none, the
 * cell is left out and the title keeps the room.
 */
export const agentRowValues = (
    task: Pick<Task, 'id' | 'status' | 'agent_working' | 'claimed_by'> & { assignee?: { id: number } | null },
    options: TaskRowAssigneeOption[] | undefined,
    facts: AgentRowFacts,
): { dispatch: AgentDispatchState | null; reviewer: { name: string | null } | null | undefined } => {
    const option = task.assignee ? options?.find(candidate => candidate.id === task.assignee?.id) : undefined;
    const profileId = option?.profileId ?? null;
    const agentBound = facts.boundProfileIds && profileId !== null ? facts.boundProfileIds.has(profileId) : undefined;
    const dispatch = option?.kind === 'agent' ? taskAgentDispatchState(task, agentBound) : null;
    const reviewer = facts.reviewerById.size === 0 ? undefined
        : task.status === 'resolved' && facts.reviewerById.has(task.id) ? { name: facts.reviewerById.get(task.id) ?? null } : null;
    return { dispatch, reviewer };
};
