import api from './api';
import type {
    Iteration,
    IterationCreate,
    IterationPlanningReadinessSummary,
    IterationSeriesCreate,
    IterationSeriesResponse,
    IterationSummary,
    IterationUpdate,
} from '../types/iteration';

export const iterationService = {
    getAll: async (context?: { signal?: AbortSignal }) => {
        const iterations: Iteration[] = [];
        let after_id = 0;
        let upper_id: number | undefined;
        while (true) {
            const page = (await api.get<{ items: Iteration[]; has_more: boolean; next_after_id: number | null; upper_id: number }>('/iterations/page',
                { params: { limit: 100, after_id, upper_id }, signal: context?.signal })).data;
            iterations.push(...page.items);
            if (!Array.isArray(page.items) || typeof page.has_more !== 'boolean' || !Number.isSafeInteger(page.upper_id)) throw new Error('Incomplete iteration page');
            upper_id ??= page.upper_id;
            if (!page.has_more) break;
            if (page.next_after_id === null || page.next_after_id <= after_id || page.next_after_id > upper_id) throw new Error('Invalid iteration page cursor');
            after_id = page.next_after_id;
        }
        return iterations.sort((a, b) => b.start_date.localeCompare(a.start_date) || b.id - a.id);
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

    update: async (id: number, data: IterationUpdate) => {
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
    },

    getPlanningReadiness: async (id: number) => {
        const response = await api.get<IterationPlanningReadinessSummary>(
            `/iterations/${id}/planning-readiness`,
        );
        return response.data;
    },
};
