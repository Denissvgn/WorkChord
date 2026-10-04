import api from './api';
import type { DeliveryMetrics } from '../types/deliveryMetrics';

export const deliveryMetricsService = {
    get: async (scope: { project_id?: number; iteration_id?: number; lookback_days: number }) => (
        await api.get<DeliveryMetrics>('/tasks/delivery-metrics', { params: scope })
    ).data,
};
