import type { Task, TaskDetail } from '../../types/task';

const emptyPage = { items: [], has_more: false, next_after_id: null, limit: 1 };

/**
 * A `GET /tasks/{id}/detail` response as the backend sends it: the task, its bounded context
 * pages, and `reviewer_name`, the agent holding the live review (null when anyone reviews).
 */
export const taskDetailResponse = (task: Partial<Task> & { id: number }, reviewerName: string | null): TaskDetail => ({
    task: task as Task,
    ancestors: [],
    ancestors_complete: true,
    children: emptyPage,
    dependencies: emptyPage,
    execution_context_complete: false,
    reviewer_name: reviewerName,
});
