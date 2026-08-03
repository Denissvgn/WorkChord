import type { Task } from '../types/task';

const doneStatuses = new Set(['resolved', 'closed']);

const workNowRank = (task: Task) => {
    if (task.is_overdue) return 0;
    if (task.status === 'active') return 1;
    if (!task.assignee) return 2;
    return 3;
};

export const selectWorkNowTasks = (tasks: Task[], limit = 3) => (
    tasks
        .filter(task => !doneStatuses.has(task.status))
        .map((task, index) => ({ task, index }))
        .sort((left, right) => (
            workNowRank(left.task) - workNowRank(right.task)
            || left.index - right.index
        ))
        .slice(0, limit)
        .map(({ task }) => task)
);
