import api from './api';
import type {
    AgentActorRosterItem,
    AgentAssignmentListParams,
    AgentCapabilities,
    AgentCommandMetadata,
    AgentModelBinding,
    AgentModelBindingCreate,
    AgentModelBindingDisable,
    AgentModelBindingListParams,
    AgentModelBindingUpdate,
    AgentModelCatalogCreate,
    AgentModelCatalogDisable,
    AgentModelCatalogEntry,
    AgentModelCatalogUpdate,
    AgentModelMutationReceipt,
    AgentPipeline,
    AgentProfileSkillCatalogItem,
    AgentRoutingPreviewCreate,
    AgentRoutingPreviewResponse,
    AgentRun,
    AgentTaskAssignment,
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentTaskAssignmentUpdate,
    TaskRoutingAssessmentCommand,
    TaskRoutingAssessmentHistory,
    TaskRoutingAssessmentMutationReceipt,
    TaskRoutingAssessmentState,
    TaskTimelineResponse,
} from '../types/agent';

const commandHeaders = (metadata: AgentCommandMetadata) => ({
    'Idempotency-Key': metadata.idempotencyKey,
    'X-Agent-Rationale': metadata.rationale,
    'X-Correlation-ID': metadata.correlationId,
});

export const agentService = {
    async getCapabilities(): Promise<AgentCapabilities> {
        const response = await api.get<AgentCapabilities>('/agent/capabilities');
        return response.data;
    },

    async getActorRoster(includeDisabled = false): Promise<AgentActorRosterItem[]> {
        const response = await api.get<AgentActorRosterItem[]>('/agent/actors', {
            params: { include_disabled: includeDisabled },
        });
        return response.data;
    },

    async getProfileSkillCatalog(): Promise<AgentProfileSkillCatalogItem[]> {
        const response = await api.get<AgentProfileSkillCatalogItem[]>(
            '/agent/profile-skill-catalog',
        );
        return response.data;
    },

    async getModelCatalog(includeDisabled = false): Promise<AgentModelCatalogEntry[]> {
        const response = await api.get<AgentModelCatalogEntry[]>('/agent/model-catalog', {
            params: { include_disabled: includeDisabled },
        });
        return response.data;
    },

    async getModelCatalogEntry(catalogKey: string): Promise<AgentModelCatalogEntry> {
        const response = await api.get<AgentModelCatalogEntry>(
            `/agent/model-catalog/${encodeURIComponent(catalogKey)}`,
        );
        return response.data;
    },

    async createModelCatalogEntry(
        data: AgentModelCatalogCreate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelCatalogEntry>> {
        const response = await api.post<AgentModelMutationReceipt<AgentModelCatalogEntry>>(
            '/agent/model-catalog',
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async updateModelCatalogEntry(
        catalogId: number,
        data: AgentModelCatalogUpdate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelCatalogEntry>> {
        const response = await api.patch<AgentModelMutationReceipt<AgentModelCatalogEntry>>(
            `/agent/model-catalog/${catalogId}`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async disableModelCatalogEntry(
        catalogId: number,
        data: AgentModelCatalogDisable,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelCatalogEntry>> {
        const response = await api.post<AgentModelMutationReceipt<AgentModelCatalogEntry>>(
            `/agent/model-catalog/${catalogId}/disable`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async getModelBindings(
        filters: AgentModelBindingListParams = {},
    ): Promise<AgentModelBinding[]> {
        const response = await api.get<AgentModelBinding[]>('/agent/model-bindings', {
            params: {
                actor_id: filters.actorId,
                include_disabled: filters.includeDisabled ?? false,
            },
        });
        return response.data;
    },

    async getModelBinding(bindingId: number): Promise<AgentModelBinding> {
        const response = await api.get<AgentModelBinding>(
            `/agent/model-bindings/${bindingId}`,
        );
        return response.data;
    },

    async createModelBinding(
        data: AgentModelBindingCreate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelBinding>> {
        const response = await api.post<AgentModelMutationReceipt<AgentModelBinding>>(
            '/agent/model-bindings',
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async updateModelBinding(
        bindingId: number,
        data: AgentModelBindingUpdate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelBinding>> {
        const response = await api.patch<AgentModelMutationReceipt<AgentModelBinding>>(
            `/agent/model-bindings/${bindingId}`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async disableModelBinding(
        bindingId: number,
        data: AgentModelBindingDisable,
        metadata: AgentCommandMetadata,
    ): Promise<AgentModelMutationReceipt<AgentModelBinding>> {
        const response = await api.post<AgentModelMutationReceipt<AgentModelBinding>>(
            `/agent/model-bindings/${bindingId}/disable`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async getTaskRoutingAssessment(taskId: number): Promise<TaskRoutingAssessmentState> {
        const response = await api.get<TaskRoutingAssessmentState>(
            `/agent/planning/tasks/${taskId}/routing-assessment`,
        );
        return response.data;
    },

    async getTaskRoutingAssessmentHistory(
        taskId: number,
        limit = 100,
    ): Promise<TaskRoutingAssessmentHistory> {
        const response = await api.get<TaskRoutingAssessmentHistory>(
            `/agent/planning/tasks/${taskId}/routing-assessments`,
            { params: { limit } },
        );
        return response.data;
    },

    async createTaskRoutingAssessment(
        taskId: number,
        data: TaskRoutingAssessmentCommand,
        metadata: AgentCommandMetadata,
    ): Promise<TaskRoutingAssessmentMutationReceipt> {
        const response = await api.post<TaskRoutingAssessmentMutationReceipt>(
            `/agent/planning/tasks/${taskId}/routing-assessment`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async previewTaskRouting(
        taskId: number,
        data: AgentRoutingPreviewCreate,
    ): Promise<AgentRoutingPreviewResponse> {
        const response = await api.post<AgentRoutingPreviewResponse>(
            `/agent/tasks/${taskId}/routing-preview`,
            data,
        );
        return response.data;
    },

    async createAssignment(
        data: ModelAwareAgentTaskAssignmentCreate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentTaskAssignment> {
        const response = await api.post<AgentTaskAssignment>(
            '/agent/assignments',
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async updateAssignment(
        assignmentId: number,
        data: ModelAwareAgentTaskAssignmentUpdate,
        metadata: AgentCommandMetadata,
    ): Promise<AgentTaskAssignment> {
        const response = await api.patch<AgentTaskAssignment>(
            `/agent/assignments/${assignmentId}`,
            data,
            { headers: commandHeaders(metadata) },
        );
        return response.data;
    },

    async listAssignments(
        filters: AgentAssignmentListParams = {},
    ): Promise<AgentTaskAssignment[]> {
        const response = await api.get<AgentTaskAssignment[]>('/agent/assignments', {
            params: {
                task_id: filters.taskId,
                actor_id: filters.actorId,
                purpose: filters.purpose,
                state: filters.state,
                limit: filters.limit ?? 200,
            },
        });
        return response.data;
    },

    async getPipeline(): Promise<AgentPipeline> {
        const response = await api.get<AgentPipeline>('/agent/pipeline');
        return response.data;
    },

    async getRunDetail(runId: number): Promise<AgentRun> {
        const response = await api.get<AgentRun>(`/agent/runs/${runId}`);
        return response.data;
    },

    async getTaskTimeline(taskId: number): Promise<TaskTimelineResponse> {
        const response = await api.get<TaskTimelineResponse>(`/tasks/${taskId}/timeline`);
        return response.data;
    }
};
