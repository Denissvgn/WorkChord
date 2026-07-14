import api from './api';
import type {
    Iteration,
    IterationCreate,
    IterationSeriesCreate,
    IterationSeriesResponse,
    IterationSummary,
} from '../types/iteration';

export const iterationService = {
    getAll: async () => {
        const response = await api.get<Iteration[]>('/iterations');
        return response.data;
    },

    getById: async (id: number) => {
        const response = await api.get<Iteration>(`/iterations/${id}`);
        return response.data;
    },

    create: async (data: IterationCreate) => {
        const response = await api.post<Iteration>('/iterations', data);
        return response.data;
    },

    createSeries: async (data: IterationSeriesCreate) => {
        const response = await api.post<IterationSeriesResponse>('/iterations/series', data);
        return response.data;
    },

    update: async (id: number, data: Partial<IterationCreate>) => {
        const response = await api.put<Iteration>(`/iterations/${id}`, data);
        return response.data;
    },

    delete: async (id: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/iterations/${id}`);
        return response.data;
    },

    getSummary: async (id: number) => {
        const response = await api.get<IterationSummary>(`/iterations/${id}/summary`);
        return response.data;
    }
};
