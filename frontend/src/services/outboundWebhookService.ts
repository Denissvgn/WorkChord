import api from './api';
import type {
    OutboundWebhookDelivery,
    OutboundWebhookDeliveryListParams,
    OutboundWebhookRetryResponse,
    OutboundWebhookTarget,
    OutboundWebhookTargetCreate,
    OutboundWebhookTargetUpdate,
} from '../types/outboundWebhook';

const buildDeliveryQuery = (params?: OutboundWebhookDeliveryListParams) => {
    const search = new URLSearchParams();
    if (params?.target_id) {
        search.set('target_id', String(params.target_id));
    }
    if (params?.status) {
        search.set('status', params.status);
    }
    if (params?.limit) {
        search.set('limit', String(params.limit));
    }
    const value = search.toString();
    return value ? `?${value}` : '';
};

export const outboundWebhookService = {
    getTargets: async () => {
        const response = await api.get<OutboundWebhookTarget[]>('/outbound-webhooks/targets');
        return response.data;
    },

    createTarget: async (data: OutboundWebhookTargetCreate) => {
        const response = await api.post<OutboundWebhookTarget>('/outbound-webhooks/targets', data);
        return response.data;
    },

    updateTarget: async (targetId: number, data: OutboundWebhookTargetUpdate) => {
        const response = await api.put<OutboundWebhookTarget>(`/outbound-webhooks/targets/${targetId}`, data);
        return response.data;
    },

    deleteTarget: async (targetId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(
            `/outbound-webhooks/targets/${targetId}`
        );
        return response.data;
    },

    testTarget: async (targetId: number) => {
        const response = await api.post<OutboundWebhookRetryResponse>(
            `/outbound-webhooks/targets/${targetId}/test`
        );
        return response.data;
    },

    getDeliveries: async (params?: OutboundWebhookDeliveryListParams) => {
        const response = await api.get<OutboundWebhookDelivery[]>(
            `/outbound-webhooks/deliveries${buildDeliveryQuery(params)}`
        );
        return response.data;
    },

    retryDelivery: async (deliveryId: number) => {
        const response = await api.post<OutboundWebhookRetryResponse>(
            `/outbound-webhooks/deliveries/${deliveryId}/retry`
        );
        return response.data;
    },
};
