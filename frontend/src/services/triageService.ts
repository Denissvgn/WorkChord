import api from './api';
import type {
    TriageActionRequest,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageDuplicateSuggestionsResponse,
    TriageItem,
    TriageItemCreate,
    TriageItemUpdate,
    TriageListParams,
    TriageSnoozeRequest,
    TriageTaskDraftRequest,
    TriageTaskDraftResponse,
} from '../types/triage';
import type { AssigneeRecommendation } from '../types/team';

const buildTriageListQuery = (params?: TriageListParams) => {
    const searchParams = new URLSearchParams();

    if (!params) {
        return '';
    }

    if (params.active !== undefined) {
        searchParams.set('active', String(params.active));
    }
    params.statuses?.forEach(status => searchParams.append('status', status));
    if (params.q?.trim()) {
        searchParams.set('q', params.q.trim());
    }
    if (params.source?.trim()) {
        searchParams.set('source', params.source.trim());
    }
    if (params.limit !== undefined) {
        searchParams.set('limit', String(params.limit));
    }
    if (params.offset !== undefined) {
        searchParams.set('offset', String(params.offset));
    }

    const query = searchParams.toString();
    return query ? `?${query}` : '';
};

export interface FrontendTriageService {
    getAll: (params?: TriageListParams) => Promise<TriageItem[]>;
    create: (data: TriageItemCreate) => Promise<TriageItem>;
    getById: (triageItemId: number) => Promise<TriageItem>;
    update: (triageItemId: number, data: TriageItemUpdate) => Promise<TriageItem>;
    accept: (triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>;
    decline: (triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>;
    snooze: (triageItemId: number, data: TriageSnoozeRequest) => Promise<TriageItem>;
    markDuplicate: (triageItemId: number, data: TriageDuplicateRequest) => Promise<TriageItem>;
    getDuplicateSuggestions: (
        triageItemId: number,
        params?: { limitPerType?: number; minScore?: number }
    ) => Promise<TriageDuplicateSuggestionsResponse>;
    getAssigneeRecommendations: (
        triageItemId: number,
        iterationId?: number | null
    ) => Promise<AssigneeRecommendation[]>;
    draftTask: (triageItemId: number, data?: TriageTaskDraftRequest) => Promise<TriageTaskDraftResponse>;
    convertToTask: (triageItemId: number, data: TriageConvertToTaskRequest) => Promise<TriageConvertToTaskResponse>;
}

export const triageService: FrontendTriageService = {
    getAll: async (params?: TriageListParams) => {
        const response = await api.get<TriageItem[]>(`/triage${buildTriageListQuery(params)}`);
        return response.data;
    },

    create: async (data: TriageItemCreate) => {
        const response = await api.post<TriageItem>('/triage', data);
        return response.data;
    },

    getById: async (triageItemId: number) => {
        const response = await api.get<TriageItem>(`/triage/${triageItemId}`);
        return response.data;
    },

    update: async (triageItemId: number, data: TriageItemUpdate) => {
        const response = await api.put<TriageItem>(`/triage/${triageItemId}`, data);
        return response.data;
    },

    accept: async (triageItemId: number, data: TriageActionRequest = {}) => {
        const response = await api.post<TriageItem>(`/triage/${triageItemId}/accept`, data);
        return response.data;
    },

    decline: async (triageItemId: number, data: TriageActionRequest = {}) => {
        const response = await api.post<TriageItem>(`/triage/${triageItemId}/decline`, data);
        return response.data;
    },

    snooze: async (triageItemId: number, data: TriageSnoozeRequest) => {
        const response = await api.post<TriageItem>(`/triage/${triageItemId}/snooze`, data);
        return response.data;
    },

    markDuplicate: async (triageItemId: number, data: TriageDuplicateRequest) => {
        const response = await api.post<TriageItem>(`/triage/${triageItemId}/mark-duplicate`, data);
        return response.data;
    },

    getDuplicateSuggestions: async (
        triageItemId: number,
        params: { limitPerType?: number; minScore?: number } = {}
    ) => {
        const searchParams = new URLSearchParams();
        if (params.limitPerType !== undefined) {
            searchParams.set('limit_per_type', String(params.limitPerType));
        }
        if (params.minScore !== undefined) {
            searchParams.set('min_score', String(params.minScore));
        }
        const query = searchParams.toString();
        const response = await api.get<TriageDuplicateSuggestionsResponse>(
            `/triage/${triageItemId}/duplicate-suggestions${query ? `?${query}` : ''}`
        );
        return response.data;
    },

    getAssigneeRecommendations: async (triageItemId: number, iterationId?: number | null) => {
        const query = iterationId ? `?iteration_id=${iterationId}` : '';
        const response = await api.get<AssigneeRecommendation[]>(
            `/triage/${triageItemId}/assignee-recommendations${query}`
        );
        return response.data;
    },

    draftTask: async (triageItemId: number, data: TriageTaskDraftRequest = {}) => {
        const response = await api.post<TriageTaskDraftResponse>(`/triage/${triageItemId}/draft-task`, data);
        return response.data;
    },

    convertToTask: async (triageItemId: number, data: TriageConvertToTaskRequest) => {
        const response = await api.post<TriageConvertToTaskResponse>(`/triage/${triageItemId}/convert-to-task`, data);
        return response.data;
    },
};
