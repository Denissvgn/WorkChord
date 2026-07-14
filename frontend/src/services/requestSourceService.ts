import api from './api';
import type {
    RequestSource,
    RequestSourceLinkCreate,
    RequestSourceLinkWithSource,
    RequestSourceTargetType,
    RequestSourceType,
} from '../types/requestSource';

const buildSearchQuery = (params: {
    q?: string;
    source_type?: RequestSourceType | '';
    limit?: number;
}) => {
    const searchParams = new URLSearchParams();
    if (params.q?.trim()) {
        searchParams.set('q', params.q.trim());
    }
    if (params.source_type) {
        searchParams.set('source_type', params.source_type);
    }
    if (params.limit !== undefined) {
        searchParams.set('limit', String(params.limit));
    }
    const query = searchParams.toString();
    return query ? `?${query}` : '';
};

export const requestSourceService = {
    search: async (params: { q?: string; source_type?: RequestSourceType | ''; limit?: number } = {}) => {
        const response = await api.get<RequestSource[]>(`/request-sources${buildSearchQuery(params)}`);
        return response.data;
    },

    getLinks: async (targetType: RequestSourceTargetType, targetId: number) => {
        const response = await api.get<RequestSourceLinkWithSource[]>('/request-source-links', {
            params: {
                target_type: targetType,
                target_id: targetId,
            },
        });
        return response.data;
    },

    createLink: async (data: RequestSourceLinkCreate) => {
        const response = await api.post<RequestSourceLinkWithSource>('/request-source-links', data);
        return response.data;
    },

    deleteLink: async (linkId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/request-source-links/${linkId}`);
        return response.data;
    },
};
