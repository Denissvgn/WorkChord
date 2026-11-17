import { useMemo } from 'react';
import { useQueries } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
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
}

/**
 * What a task row needs beside the task to show the agent status line and the Reviewer.
 *
 * The Reviewer of each displayed submitted task comes from the task detail read, which names the
 * agent holding the live review. Reads go only for the tasks shown, in pages of
 * REVIEWER_PAGE_SIZE ids, so a long list is covered without one unbounded request. `known` holds
 * reviewers a page already read in its own list (My Work returns them), which are not read again.
 * Whether the agent is connected comes with the assignee options, from the team read every reader has.
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

    // The query array is new on every render; the time of the last load says when its data changed.
    const reviewerStamp = reviewerQueries.map(query => query.dataUpdatedAt).join(',');
    const reviewerById = useMemo(() => {
        const map = new Map<number, string | null>();
        submittedIds.forEach(id => { if (known?.has(id)) map.set(id, known.get(id) ?? null); });
        reviewerQueries.forEach(query => query.data?.forEach(([id, name]) => map.set(id, name)));
        return map;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [reviewerStamp, submittedIds, known]);

    return { reviewerById, reviewerColumn: submittedIds.length > 0 };
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
    const dispatch = option?.kind === 'agent' ? taskAgentDispatchState(task, option.agentConnected) : null;
    const reviewer = !facts.reviewerColumn ? undefined
        : task.status === 'resolved' && facts.reviewerById.has(task.id) ? { name: facts.reviewerById.get(task.id) ?? null } : null;
    return { dispatch, reviewer };
};
