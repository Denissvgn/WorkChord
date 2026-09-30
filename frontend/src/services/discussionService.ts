import api from './api';

export interface TaskComment {
    id: number; task_id: number; principal_id: number; author_name: string;
    body: string; mentions: number[]; version: number; deleted: boolean;
    created_at: string; updated_at: string;
}
export interface CommentRevision { version: number; body: string; principal_id: number; deleted: boolean; created_at: string }
export interface Subscription { enabled: boolean; events: string[]; version: number }
export interface InboxItem { id: number; task_id: number; title: string; event_type: string; read: boolean; created_at: string }
export interface NotificationDelivery { id: number; task_id: number; title: string; status: string; attempt_count: number; max_attempts: number }
export interface Page<T> { items: T[]; has_more: boolean; next_after_id: number | null }

export const discussionService = {
    list: async (taskId: number, afterId = 0) => (await api.get<Page<TaskComment>>(`/tasks/${taskId}/comments`, { params: { after_id: afterId } })).data,
    mentions: async (taskId: number, q: string) => (await api.get<Page<{ id: number; name: string }>>(`/tasks/${taskId}/mention-options`, { params: { q } })).data,
    save: async (taskId: number, body: string, mentions: number[], comment?: { id: number; version: number }, deleted = false) => comment
        ? (await api.put<TaskComment>(`/tasks/${taskId}/comments/${comment.id}`, { body: body || 'Removed', mentions, expected_version: comment.version, deleted })).data
        : (await api.post<TaskComment>(`/tasks/${taskId}/comments`, { body, mentions })).data,
    history: async (taskId: number, commentId: number, afterVersion = 0) => (await api.get<{ items: CommentRevision[]; has_more: boolean; next_after_version: number | null }>(`/tasks/${taskId}/comments/${commentId}/history`, { params: { after_version: afterVersion } })).data,
    subscription: async (taskId: number) => (await api.get<Subscription>(`/tasks/${taskId}/subscription`)).data,
    subscribe: async (taskId: number, current: Subscription, enabled: boolean, events = current.events) => (await api.put<Subscription>(`/tasks/${taskId}/subscription`, { enabled, events, expected_version: current.version })).data,
    inbox: async (afterId = 0) => (await api.get<Page<InboxItem>>('/notifications', { params: { after_id: afterId } })).data,
    read: async (id: number, read: boolean) => (await api.put(`/notifications/${id}`, { read })).data,
    deliveries: async (afterId = 0) => (await api.get<Page<NotificationDelivery>>('/notifications/deliveries', { params: { after_id: afterId } })).data,
    retry: async (id: number) => (await api.post(`/notifications/deliveries/${id}/retry`)).data,
};
