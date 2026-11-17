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
import type { Task, TaskStatus } from '../../types/task';
import type { TaskRowAssigneeOption } from './TaskRow';

/** How many submitted tasks one reviewer read covers; a longer list is read in several pages. */
export const REVIEWER_PAGE_SIZE = 20;

/** A row the page shows: only its id and status decide whether a Reviewer is read for it. */
export interface DisplayedTask { id: number; status: TaskStatus }

export interface AgentRowFacts {
    /** Reviewer per submitted task that has been read: the agent holding the review, or null when any authorized person reviews. */
    reviewerById: Map<number, string | null>;
    /** True while any displayed task is submitted, so every row keeps a Reviewer cell and the columns line up. */
    reviewerColumn: boolean;
    /** Profiles with an enabled agent bound; null when this reader may not read the agent roster. */
    boundProfileIds: Set<number> | null;
}

/**
 * What a task row needs beside the task to show the agent status line and the Reviewer.
 *
 * The Reviewer of each displayed submitted task comes from the task detail read, which names the
 * agent holding the live review. Reads go only for the tasks shown, in pages of
 * REVIEWER_PAGE_SIZE ids, so a long list is covered without one unbounded request. `known` holds
 * reviewers a page already read in its own list (My Work returns them), which are not read again.
 * Whether an agent is bound to a profile comes from the agent roster, for readers allowed it.
 */
export const useAgentRowFacts = (tasks: DisplayedTask[], known?: ReadonlyMap<number, string | null>): AgentRowFacts => {
    const submittedKey = [...new Set(tasks.filter(task => task.status === 'resolved').map(task => task.id))].sort((a, b) => a - b).join(',');
    const submittedIds = useMemo(() => (submittedKey === '' ? [] : submittedKey.split(',').map(Number)), [submittedKey]);
    const toRead = useMemo(() => submittedIds.filter(id => !known?.has(id)), [submittedIds, known]);
    const pages = useMemo(() => {
        const chunks: number[][] = [];
        for (let start = 0; start < toRead.length; start += REVIEWER_PAGE_SIZE) chunks.push(toRead.slice(start, start + REVIEWER_PAGE_SIZE));
        return chunks;
    }, [toRead]);
    const identity = useIdentity()?.identity;
    const { hasAgentKey } = useAgentAccess();
    // The roster is for workspace operators and agent or admin keys; others are not asked.
    const mayReadRoster = identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator' || hasAgentKey || hasAdminApiKey();

    // feedback-policy: query loading,error,retry,empty - optional row detail: while loading or after a failure the row keeps an empty Reviewer cell instead of guessing a name.
    const reviewerQueries = useQueries({
        queries: pages.map(ids => ({
            queryKey: ['tasks', 'reviewers', ids.join(',')],
            queryFn: async ({ signal }: { signal: AbortSignal }) => {
                // One task that cannot be read leaves only its own cell empty.
                const reads = await Promise.allSettled(ids.map(id => taskService.getDetail(id, { limit: 1 }, signal)));
                return reads.flatMap((read, index) => read.status === 'fulfilled' ? [[ids[index], read.value.reviewer_name ?? null] as const] : []);
            },
            staleTime: 30_000,
        })),
    });
    // feedback-policy: query loading,error,retry,empty - optional row detail: without the roster the line says the agent status is unknown.
    const roster = useQuery({
        queryKey: ['agent-actor-roster', false],
        queryFn: () => agentService.getActorRoster(false, { optional: true }),
        enabled: mayReadRoster,
        retry: protectedQueryRetry,
        staleTime: 60_000,
    });

    // The query array is new on every render; the time of the last load says when its data changed.
    const reviewerStamp = reviewerQueries.map(query => query.dataUpdatedAt).join(',');
    const reviewerById = useMemo(() => {
        const map = new Map<number, string | null>();
        submittedIds.forEach(id => { if (known?.has(id)) map.set(id, known.get(id) ?? null); });
        reviewerQueries.forEach(query => query.data?.forEach(([id, name]) => map.set(id, name)));
        return map;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [reviewerStamp, submittedIds, known]);
    const rosterData = roster.data;
    const boundProfileIds = useMemo(() => rosterData
        ? new Set(rosterData.filter(actor => actor.enabled && actor.lifecycle_state !== 'disabled' && actor.profile_id !== null).map(actor => actor.profile_id as number))
        : null, [rosterData]);

    return { reviewerById, reviewerColumn: submittedIds.length > 0, boundProfileIds };
};

/**
 * The agent status line and the Reviewer for one row. The status line is for an agent
 * assignee only; the Reviewer is named once the task is submitted. While any displayed task is
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
    const reviewer = !facts.reviewerColumn ? undefined
        : task.status === 'resolved' && facts.reviewerById.has(task.id) ? { name: facts.reviewerById.get(task.id) ?? null } : null;
    return { dispatch, reviewer };
};
