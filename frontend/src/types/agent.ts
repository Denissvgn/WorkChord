import type { Task } from './task';

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };
export type JsonObject = { [key: string]: JsonValue };

export interface AgentRunEvent {
    id: number;
    run_id: number;
    event_type: string;
    message?: string | null;
    payload: JsonObject;
    trace_id?: string | null;
    span_id?: string | null;
    created_at: string;
}

export interface AgentRun {
    id: number;
    task_id?: number | null;
    actor_id: number;
    status: 'running' | 'succeeded' | 'failed' | 'canceled' | string;
    trace_id?: string | null;
    model?: string | null;
    tool_name?: string | null;
    metadata: JsonObject;
    artifact_links: string[];
    commit_url?: string | null;
    pr_url?: string | null;
    summary?: string | null;
    error?: string | null;
    started_at: string;
    ended_at?: string | null;
    events?: AgentRunEvent[];
}

export interface AgentPipeline {
    needs_definition: Task[];
    ready_for_agent: Task[];
    definition_ready_unassigned: Task[];
    assigned_waiting: Task[];
    start_ready: Task[];
    executing: Task[];
    verification_required: Task[];
    recovery_required: Task[];
}

export interface TaskTimelineItem {
    item_type: 'task_event' | 'status_log' | 'agent_run' | 'agent_run_event';
    timestamp: string;
    title: string;
    payload: JsonObject;
    actor_type?: string | null;
    actor_id?: number | null;
    trace_id?: string | null;
}

export interface TaskTimelineResponse {
    task_id: number;
    items: TaskTimelineItem[];
}
