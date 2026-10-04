export interface DurationSamples {
    unit: 'elapsed_seconds';
    sample_count: number;
    mean: number | null;
    median: number | null;
    censored_count: number;
    unknown_count: number;
}

export interface DeliveryQueueItem {
    task_id: number;
    title: string;
    reason: string;
    age_seconds: number | null;
}

export interface DeliveryMetrics {
    contract_version: number;
    window_start: string;
    window_end: string;
    scope_basis: string;
    accepted_leaf_tasks: number;
    acceptance_events: number;
    rejection_events: number;
    canceled_leaf_tasks: number;
    reopened_events: number;
    lead_time: DurationSamples;
    cycle_time: DurationSamples;
    review_delay: DurationSamples;
    coverage: Record<string, number | string>;
    review_queue: DeliveryQueueItem[];
    recovery_queue: DeliveryQueueItem[];
    queues_truncated: boolean;
}
