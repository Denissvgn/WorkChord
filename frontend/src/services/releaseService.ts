import api from './api';
import type {
    Release,
    ReleaseCreateRequest,
    ReleaseUpdateRequest,
} from '../types/release';

export const releaseService = {
    getForProject: async (projectId: number) => {
        const response = await api.get<Release[]>(`/projects/${projectId}/releases`);
        return response.data;
    },

    createForProject: async (projectId: number, data: ReleaseCreateRequest) => {
        const response = await api.post<Release>(`/projects/${projectId}/releases`, data);
        return response.data;
    },

    getById: async (releaseId: number) => {
        const response = await api.get<Release>(`/releases/${releaseId}`);
        return response.data;
    },

    update: async (releaseId: number, data: ReleaseUpdateRequest) => {
        const response = await api.put<Release>(`/releases/${releaseId}`, data);
        return response.data;
    },
};
