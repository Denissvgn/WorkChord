export type OutboundWebhookDeliveryStatus = 'pending' | 'delivered' | 'failed';

export interface OutboundWebhookTarget {
    id: number;
    name: string;
    description?: string | null;
    url: string;
    enabled: boolean;
    subscribed_events_json: string[];
    has_secret: boolean;
    headers_json: Record<string, string>;
    created_at: string;
    updated_at: string;
}

export interface OutboundWebhookTargetCreate {
    name: string;
    description?: string | null;
    url: string;
    enabled: boolean;
    subscribed_events_json: string[];
    secret?: string | null;
    headers_json?: Record<string, string>;
}

export type OutboundWebhookTargetUpdate = Partial<OutboundWebhookTargetCreate>;

export interface OutboundWebhookEvent {
    id: number;
    event_id: string;
    event_type: string;
    entity_type: string;
    entity_id?: number | null;
    payload_json: Record<string, unknown>;
    occurred_at: string;
}

export interface OutboundWebhookDelivery {
    id: number;
    target_id?: number | null;
    event_id: number;
    target_name?: string | null;
    target_url?: string | null;
    status: OutboundWebhookDeliveryStatus;
    attempt_count: number;
    last_http_status?: number | null;
    last_error?: string | null;
    last_response_body?: string | null;
    last_attempt_at?: string | null;
    next_retry_at?: string | null;
    delivered_at?: string | null;
    created_at: string;
    updated_at: string;
    event: OutboundWebhookEvent;
}

export interface OutboundWebhookRetryResponse {
    delivery: OutboundWebhookDelivery;
}

export interface OutboundWebhookDeliveryListParams {
    target_id?: number | null;
    status?: OutboundWebhookDeliveryStatus | null;
    limit?: number;
}
