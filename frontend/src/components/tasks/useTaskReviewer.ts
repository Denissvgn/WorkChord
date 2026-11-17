import { useQuery } from '@tanstack/react-query';
import type { Task } from '../../types/task';
import { taskService } from '../../services/taskService';

/** The reviewer detail of a submitted task; shared by every part of the page that names who decides acceptance. */
// feedback-policy: query loading,error,retry,empty - consumers show loading, an error with retry, and fall back to the "anyone" wording only once data is known.
export const useTaskReviewer = (task: Task) => useQuery({
    queryKey: ['taskReviewer', task.id, task.version],
    queryFn: () => taskService.getDetail(task.id, { limit: 1 }),
    enabled: task.status === 'resolved',
    staleTime: 30_000,
});
