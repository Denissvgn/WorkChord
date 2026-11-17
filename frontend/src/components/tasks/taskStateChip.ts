import type { Task, TaskStatus } from '../../types/task';

/** The one state a row names, chosen by priority: Blocked, Needs definition, Waits for n, Ready to start, In review. */
export type TaskStateChip =
    | { kind: 'blocked' }
    | { kind: 'needsDefinition' }
    | { kind: 'waits'; count: number }
    | { kind: 'ready' }
    | { kind: 'inReview' };

export const isDone = (status: TaskStatus | undefined) => status === 'resolved' || status === 'closed';

/** Chooses the single state chip for a task; `taskMap` lets Waits count only the dependencies still open. */
export const taskStateChip = (task: Task, taskMap?: Map<number, Task>): TaskStateChip | null => {
    if (task.status === 'closed') return null;
    if (task.blocked_reason) return { kind: 'blocked' };
    const startReady = task.agent_readiness.start_ready ?? task.agent_readiness.is_ready;
    if (task.status === 'planned' && !startReady && !task.agent_readiness.definition_ready) return { kind: 'needsDefinition' };
    if (task.status === 'planned' || task.status === 'active') {
        const waiting = startReady && task.status === 'planned' ? 0
            : task.dependencies.filter(id => !isDone(taskMap?.get(id)?.status)).length;
        if (waiting > 0) return { kind: 'waits', count: waiting };
    }
    if (task.status === 'planned' && startReady) return { kind: 'ready' };
    if (task.status === 'resolved') return { kind: 'inReview' };
    return null;
};
