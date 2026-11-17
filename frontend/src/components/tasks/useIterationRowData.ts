import { useMemo } from 'react';
import { useQueries } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import type { Task } from '../../types/task';
import type { TaskRowAssigneeOption } from './TaskRow';

const flatten = (tasks: Task[]): Task[] => tasks.flatMap(task => [task, ...flatten(task.children ?? [])]);

/**
 * What rows of several iterations need that a task reference does not carry, loaded the way the
 * Tasks list loads it: each iteration's tasks and the people and agents it can assign to.
 * `loadTasks` is left off when the caller already holds full tasks.
 */
export const useIterationRowData = (iterationIds: (number | null | undefined)[], { loadTasks = true }: { loadTasks?: boolean } = {}) => {
    // The list is rebuilt on every render; its content, as one string, says when it changed.
    const key = [...new Set(iterationIds.filter((id): id is number => id !== null && id !== undefined))].sort((a, b) => a - b).join(',');
    const ids = useMemo(() => (key === '' ? [] : key.split(',').map(Number)), [key]);
    // feedback-policy: query loading,error,retry,empty - the rows stay usable without these; the page shows the load failure with a retry and the pickers keep Unassigned and the current assignee.
    const taskQueries = useQueries({
        queries: ids.map(id => ({ queryKey: ['tasks', id], queryFn: () => taskService.getByIteration(id), enabled: loadTasks })),
    });
    // feedback-policy: query loading,error,retry,empty - the rows stay usable without these; the page shows the load failure with a retry and the pickers keep Unassigned and the current assignee.
    const teamQueries = useQueries({
        queries: ids.map(id => ({ queryKey: ['team', id], queryFn: () => teamService.getByIteration(id) })),
    });

    // The query arrays are new on every render; the time of the last load says when their data changed.
    const tasksStamp = taskQueries.map(query => query.dataUpdatedAt).join(',');
    const teamStamp = teamQueries.map(query => query.dataUpdatedAt).join(',');
    const tasksById = useMemo(() => {
        const map = new Map<number, Task>();
        taskQueries.forEach(query => flatten(query.data ?? []).forEach(task => map.set(task.id, task)));
        return map;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [tasksStamp]);
    const optionsByIteration = useMemo(() => {
        const map = new Map<number, TaskRowAssigneeOption[]>();
        teamQueries.forEach((query, index) => map.set(ids[index], (query.data ?? []).map(member => ({ id: member.id, name: member.name, kind: member.profile?.profile_kind, profileId: member.profile_id ?? member.profile?.id ?? null }))));
        return map;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [teamStamp, ids]);
    const failed = [...taskQueries, ...teamQueries].find(query => query.isError);

    return {
        tasksById,
        optionsByIteration,
        error: failed?.error ?? null,
        refetch: () => { [...taskQueries, ...teamQueries].filter(query => query.isError).forEach(query => void query.refetch()); },
    };
};
