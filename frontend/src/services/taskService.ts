import api from './api';
import type {
    Task,
    TaskCreate,
    ExternalLink,
    ExternalLinkCreate,
    ExternalLinkUpdate,
    GitHubExternalLinkCreate,
    GroundedAISuggestionResponse,
    TaskFormalizeResponse,
    TaskAISuggestRequest,
    TaskBulkOperationRequest,
    TaskBulkOperationResponse,
    TaskImportDestination,
    TaskImproveDescriptionResponse,
    TaskMoveRequest,
    TaskUpdate,
    TaskMergeRequest,
    TaskStatus,
    TaskStatusChangeResponse,
    TaskStatusLog,
    TaskTimelineResponse,
    TasksImportRequest,
    TasksImportResponse,
    TaskBatchUpdateRequest,
    TaskBatchUpdateResponse,
} from '../types/task';
import type { AssigneeRecommendation } from '../types/team';

export const taskService = {
    getByIteration: async (iterationId: number) => {
        const response = await api.get<Task[]>(`/iterations/${iterationId}/tasks`);
        return response.data;
    },

    getById: async (taskId: number) => {
        const response = await api.get<Task>(`/tasks/${taskId}`);
        return response.data;
    },

    create: async (iterationId: number, data: TaskCreate) => {
        const response = await api.post<Task>(`/iterations/${iterationId}/tasks`, data);
        return response.data;
    },

    createSubtask: async (parentId: number, data: TaskCreate) => {
        const response = await api.post<Task>(`/tasks/${parentId}/subtasks`, data);
        return response.data;
    },

    update: async (taskId: number, data: TaskUpdate) => {
        const response = await api.put<Task>(`/tasks/${taskId}`, data);
        return response.data;
    },

    move: async (taskId: number, data: TaskMoveRequest) => {
        const response = await api.post<Task>(`/tasks/${taskId}/move`, data);
        return response.data;
    },

    delete: async (taskId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/tasks/${taskId}`);
        return response.data;
    },

    addDependency: async (taskId: number, dependsOnId: number) => {
        const response = await api.post(`/tasks/${taskId}/dependencies`, { depends_on_id: dependsOnId });
        return response.data;
    },

    removeDependency: async (taskId: number, dependsOnId: number) => {
        const response = await api.delete(`/tasks/${taskId}/dependencies/${dependsOnId}`);
        return response.data;
    },

    formalize: async (taskId: number, context?: string) => {
        const response = await api.post<TaskFormalizeResponse>(`/tasks/${taskId}/formalize`, { context });
        return response.data;
    },

    formalizeDraft: async (title: string, description?: string, context?: string) => {
        const response = await api.post<TaskFormalizeResponse>('/tasks/draft/formalize', {
            title,
            description,
            context,
        });
        return response.data;
    },

    improveDescription: async (taskId: number, currentDescription?: string, context?: string) => {
        const response = await api.post<TaskImproveDescriptionResponse>(`/tasks/${taskId}/improve-description`, {
            current_description: currentDescription,
            context,
        });
        return response.data;
    },

    improveDescriptionDraft: async (currentDescription: string, context?: string) => {
        const response = await api.post<TaskImproveDescriptionResponse>('/tasks/draft/improve-description', {
            current_description: currentDescription,
            context,
        });
        return response.data;
    },

    suggestWithAI: async (data: TaskAISuggestRequest, taskId?: number) => {
        const path = taskId ? `/tasks/${taskId}/ai/suggest` : '/tasks/ai/suggest';
        const response = await api.post<GroundedAISuggestionResponse>(path, data);
        return response.data;
    },

    reorder: async (data: { taskIds: number[]; iterationId: number; parentId?: number | null }) => {
        const response = await api.post(`/tasks/reorder`, {
            task_ids: data.taskIds,
            iteration_id: data.iterationId,
            parent_id: data.parentId ?? null,
        });
        return response.data;
    },

    mergeTasks: async (iterationId: number, data: TaskMergeRequest) => {
        const response = await api.post<Task>(`/iterations/${iterationId}/tasks/merge`, data);
        return response.data;
    },

    unmergeTask: async (taskId: number, deleteParent: boolean = true) => {
        const response = await api.post<Task[]>(`/tasks/${taskId}/unmerge`, { delete_parent: deleteParent });
        return response.data;
    },

    runBulkOperation: async (data: TaskBulkOperationRequest) => {
        const response = await api.post<TaskBulkOperationResponse>('/tasks/bulk-operations', data);
        return response.data;
    },

    importFromText: async (
        iterationId: number,
        text: string,
        options: { destination?: TaskImportDestination } = {}
    ) => {
        const payload: TasksImportRequest = { text, destination: options.destination };
        const response = await api.post<TasksImportResponse>(
            `/iterations/${iterationId}/tasks/import`,
            payload
        );
        return response.data;
    },

    getTasksAsText: async (iterationId: number) => {
        const response = await api.get<string>(`/iterations/${iterationId}/tasks/text`);
        return response.data;
    },

    bulkUpdateTasks: async (
        iterationId: number,
        text: string,
        options: { destination?: TaskImportDestination } = {}
    ) => {
        const payload: TasksImportRequest = { text, destination: options.destination };
        const response = await api.post<TasksImportResponse>(
            `/iterations/${iterationId}/tasks/bulk-update`,
            payload
        );
        return response.data;
    },

    changeStatus: async (
        taskId: number,
        status: TaskStatus,
        reason?: string,
        expectedVersion?: number,
    ) => {
        const response = await api.put<TaskStatusChangeResponse>(
            `/tasks/${taskId}/status`,
            { status, reason, expected_version: expectedVersion }
        );
        return response.data;
    },

    getStatusHistory: async (taskId: number) => {
        const response = await api.get<TaskStatusLog[]>(`/tasks/${taskId}/status-history`);
        return response.data;
    },

    getIterationHistory: async (iterationId: number) => {
        const response = await api.get<TaskStatusLog[]>(`/iterations/${iterationId}/history`);
        return response.data;
    },

    getOverdueTasks: async (iterationId: number) => {
        const response = await api.get<Task[]>(`/iterations/${iterationId}/overdue`);
        return response.data;
    },

    getTimeline: async (taskId: number) => {
        const response = await api.get<TaskTimelineResponse>(`/tasks/${taskId}/timeline`);
        return response.data;
    },

    getAssigneeRecommendations: async (taskId: number) => {
        const response = await api.get<AssigneeRecommendation[]>(`/tasks/${taskId}/assignee-recommendations`);
        return response.data;
    },

    getExternalLinks: async (taskId: number) => {
        const response = await api.get<ExternalLink[]>(`/tasks/${taskId}/external-links`);
        return response.data;
    },

    createExternalLink: async (taskId: number, data: ExternalLinkCreate) => {
        const response = await api.post<ExternalLink>(`/tasks/${taskId}/external-links`, data);
        return response.data;
    },

    createGitHubExternalLink: async (taskId: number, data: GitHubExternalLinkCreate) => {
        const response = await api.post<ExternalLink>(`/tasks/${taskId}/external-links/github`, data);
        return response.data;
    },

    refreshGitHubExternalLink: async (linkId: number) => {
        const response = await api.post<ExternalLink>(`/external-links/${linkId}/refresh-github`);
        return response.data;
    },

    updateExternalLink: async (linkId: number, data: ExternalLinkUpdate) => {
        const response = await api.put<ExternalLink>(`/external-links/${linkId}`, data);
        return response.data;
    },

    deleteExternalLink: async (linkId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/external-links/${linkId}`);
        return response.data;
    },

    batchUpdate: async (iterationId: number, data: TaskBatchUpdateRequest) => {
        const response = await api.post<TaskBatchUpdateResponse>(`/iterations/${iterationId}/tasks/batch-update`, data);
        return response.data;
    },
};
