import api from './api';
import type { DeliveryMetrics } from '../types/deliveryMetrics';
import type { AnalyticsScope } from '../types/analyticsScope';

export const deliveryMetricsService = {
    get: async (scope: AnalyticsScope) => (
        await api.get<DeliveryMetrics>('/tasks/delivery-metrics', { params: scope })
    ).data,
};
