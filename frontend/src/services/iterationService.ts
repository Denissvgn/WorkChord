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
        const pageSize = 500;
        const iterations: Iteration[] = [];
        let cursorStartDate: string | undefined;
        let cursorId: number | undefined;

        while (true) {
            const response = await api.get<Iteration[]>('/iterations', {
                params: {
                    limit: pageSize,
                    cursor_start_date: cursorStartDate,
                    cursor_id: cursorId,
                },
            });
            const page = response.data;
            iterations.push(...page);
            if (page.length < pageSize) break;

            const last = page[page.length - 1];
            cursorStartDate = last.start_date;
            cursorId = last.id;
        }
        return iterations;
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
