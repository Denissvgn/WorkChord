import api from './api';
import type { ExecutionUsageSummary } from '../types/executionUsage';
import type { AnalyticsScope } from '../types/analyticsScope';

export const executionUsageService = {
    get: async (scope: AnalyticsScope & { budget_amount?: string; budget_currency?: string }) => (
        await api.get<ExecutionUsageSummary>('/tasks/execution-usage', { params: scope })
    ).data,
};
