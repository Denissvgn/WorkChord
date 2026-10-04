import api from './api';
import type { ExecutionUsageSummary } from '../types/executionUsage';

export const executionUsageService = {
    get: async (scope: { project_id?: number; iteration_id?: number; lookback_days: number; budget_amount?: string; budget_currency?: string }) => (
        await api.get<ExecutionUsageSummary>('/tasks/execution-usage', { params: scope })
    ).data,
};
