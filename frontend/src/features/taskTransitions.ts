import type { TaskStatus } from '../types/task';

/** The direct status moves the server allows (TaskStatusService.VALID_TRANSITIONS). */
export const TASK_TRANSITIONS: Record<TaskStatus, TaskStatus[]> = {
    planned: ['active'],
    active: ['resolved'],
    resolved: ['active', 'closed'],
    closed: [],
};

export const canTransition = (from: TaskStatus, to: TaskStatus) => TASK_TRANSITIONS[from]?.includes(to) ?? false;
