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
    TaskTextContext,
    TaskBatchUpdateRequest,
    TaskBatchUpdateResponse,
} from '../types/task';
import type { TaskActions, TaskCommand, TaskDetail, TaskBrief, CriterionProgress, TaskReferencePage } from '../types/task';
import type { AssigneeRecommendation } from '../types/team';

export const taskService = {
    ownerOptions: async (projectId?: number) => (await api.get<{ items: { id: number; name: string }[]; has_more: boolean }>("/tasks/owner-options", { params: { project_id: projectId } })).data,
    getDetail: async (taskId: number, params: { limit?: number; children_after_id?: number; dependencies_after_id?: number } = {}, signal?: AbortSignal) => (await api.get<TaskDetail>(`/tasks/${taskId}/detail`, { params, signal })).data,
    lookup: async (params: { project_id?: number; iteration_id?: number; q?: string; backlog_only?: boolean; after_id?: number; limit?: number; task_status?: string; parent_id?: number; roots_only?: boolean }, signal?: AbortSignal) => {
        const page = (await api.get<TaskReferencePage>('/tasks/lookup', { params, signal })).data;
        if (!Array.isArray(page.items) || typeof page.has_more !== 'boolean'
            || page.items.some(item => !Number.isSafeInteger(item.id) || item.id <= (params.after_id ?? 0))
            || (page.has_more && (!Number.isSafeInteger(page.next_after_id) || (page.next_after_id ?? 0) <= (params.after_id ?? 0)))) {
            throw new Error('Incomplete or invalid task page. Refresh the workset.');
        }
        return page;
    },
    actions: async (taskId: number) => (await api.get<TaskActions>(`/tasks/${taskId}/actions`)).data,
    command: async (taskId: number, data: TaskCommand) => (await api.post<Task>(`/tasks/${taskId}/commands`, data)).data,
    convertBrief: async (taskId: number, expected_version: number, apply: boolean) => (await api.post<{ brief: TaskBrief; notes: string[]; already_converted: boolean }>(`/tasks/${taskId}/brief/convert`, { expected_version, apply })).data,
    progress: async (taskId: number, data: { expected_version: number; criteria: CriterionProgress[]; artifacts: string[] }) => (await api.post<Task>(`/tasks/${taskId}/progress`, data)).data,
    review: async (taskId: number, data: { expected_version: number; brief_revision: number; artifact_revision: number; verdict: 'accept' | 'reject'; reason: string; evidence?: string }) => (await api.post<Task>(`/tasks/${taskId}/review`, data)).data,

    getByIteration: async (iterationId: number) => {
        const response = await api.get<Task[]>(`/iterations/${iterationId}/tasks`);
        return response.data;
    },

    getById: async (taskId: number) => {
        const detail = (await api.get<TaskDetail>(`/tasks/${taskId}/detail`)).data;
        return { ...detail.task, dependencies: detail.dependencies.items.map(item => item.id), detail_context: detail };
    },

    create: async (iterationId: number | null, data: TaskCreate) => {
        const response = await api.post<Task>(iterationId ? `/iterations/${iterationId}/tasks` : `/projects/${data.project_id}/backlog`, data);
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

    delete: async (taskId: number, expectedVersion?: number, expectedRevision?: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/tasks/${taskId}`, { params: { expected_version: expectedVersion, expected_revision: expectedRevision } });
        return response.data;
    },

    addDependency: async (taskId: number, dependsOnId: number, expectedVersion: number) => {
        const response = await api.post(`/tasks/${taskId}/dependencies`, { depends_on_id: dependsOnId, expected_version: expectedVersion });
        return response.data;
    },

    removeDependency: async (taskId: number, dependsOnId: number, expectedVersion: number) => {
        const response = await api.delete(`/tasks/${taskId}/dependencies/${dependsOnId}`, { params: { expected_version: expectedVersion } });
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

    reorder: async (data: { taskIds: number[]; iterationId: number; parentId?: number | null; expectedRevision?: number }) => {
        const response = await api.post(`/tasks/reorder`, {
            task_ids: data.taskIds,
            iteration_id: data.iterationId,
            parent_id: data.parentId ?? null,
            expected_revision: data.expectedRevision,
        });
        return { ...response.data, iteration_revision: Number(response.headers["x-iteration-revision"]) || undefined };
    },

    mergeTasks: async (iterationId: number, data: TaskMergeRequest) => {
        const response = await api.post<Task>(`/iterations/${iterationId}/tasks/merge`, data);
        return response.data;
    },

    unmergeTask: async (taskId: number, deleteParent: boolean = true, expectedRevision?: number) => {
        const response = await api.post<Task[]>(`/tasks/${taskId}/unmerge`, { delete_parent: deleteParent, expected_revision: expectedRevision });
        return response.data;
    },

    runBulkOperation: async (data: TaskBulkOperationRequest) => {
        const response = await api.post<TaskBulkOperationResponse>('/tasks/bulk-operations', data);
        return response.data;
    },

    importFromText: async (
        iterationId: number,
        text: string,
        options: { destination?: TaskImportDestination; expectedRevision?: number } = {}
    ) => {
        const payload: TasksImportRequest = { text, destination: options.destination, expected_revision: options.expectedRevision };
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

    getTasksTextContext: async (iterationId: number) => (
        await api.get<TaskTextContext>(`/iterations/${iterationId}/tasks/text-context`)
    ).data,

    bulkUpdateTasks: async (
        iterationId: number,
        text: string,
        options: { destination?: TaskImportDestination; expectedRevision?: number } = {}
    ) => {
        const payload: TasksImportRequest = { text, destination: options.destination, expected_revision: options.expectedRevision };
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

    getTimelinePage: async (taskId: number, cursor?: string) => (await api.get<TaskTimelineResponse & { has_more: boolean; next_cursor: string | null; limit: number; consistency: string }>(`/tasks/${taskId}/timeline/page`, { params: { cursor, limit: 50 } })).data,

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
