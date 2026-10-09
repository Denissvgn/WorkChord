import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';

export const readTaskEditorSnapshot = async (taskId: number, signal: AbortSignal): Promise<Task> => {
    const detail = await taskService.getDetail(taskId, {}, signal);
    if (detail.task.id !== taskId || !Number.isSafeInteger(detail.task.version) || detail.task.version <= 0) {
        throw new Error('Task identity or version is unavailable. Reload the task before editing.');
    }
    return { ...detail.task, dependencies: detail.dependencies.items.map(item => item.id), detail_context: detail };
};

export const keepNewestTaskSnapshot = (previous: unknown, next: unknown) => {
    const before = previous as Task | undefined;
    const after = next as Task;
    return before && before.id === after.id && before.version > after.version ? before : after;
};
