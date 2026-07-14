import type { Task } from './task';

export type TriageItemStatus = 'new' | 'accepted' | 'declined' | 'duplicate' | 'snoozed' | 'converted';

export interface TriageItem {
    id: number;
    title: string;
    description?: string | null;
    source?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    status: TriageItemStatus;
    priority_hint?: number | null;
    assignee_hint?: string | null;
    project_hint_id?: number | null;
    iteration_hint_id?: number | null;
    labels: string[];
    metadata_json: Record<string, unknown>;
    snoozed_until?: string | null;
    duplicate_of_id?: number | null;
    duplicate_task_id?: number | null;
    converted_task_id?: number | null;
    request_count: number;
    created_at: string;
    updated_at: string;
}

export interface TriageItemCreate {
    title: string;
    description?: string | null;
    source?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    priority_hint?: number | null;
    assignee_hint?: string | null;
    project_hint_id?: number | null;
    iteration_hint_id?: number | null;
    labels?: string[];
    metadata_json?: Record<string, unknown>;
}

export type TriageItemUpdate = Partial<TriageItemCreate>;

export interface TriageListParams {
    active?: boolean;
    statuses?: TriageItemStatus[];
    q?: string;
    source?: string;
    limit?: number;
    offset?: number;
}

export interface TriageActionRequest {
    reason?: string | null;
}

export interface TriageSnoozeRequest {
    snoozed_until: string;
    reason?: string | null;
}

export interface TriageDuplicateRequest {
    duplicate_of_id?: number | null;
    duplicate_task_id?: number | null;
    link_request_to_duplicate_task?: boolean;
    reason?: string | null;
}

export interface TriageDuplicateSuggestion {
    target_type: 'triage_item' | 'task';
    target_id: number;
    title: string;
    description?: string | null;
    status?: string | null;
    source?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    labels: string[];
    project_id?: number | null;
    iteration_id?: number | null;
    score: number;
    signals: string[];
}

export interface TriageDuplicateSuggestionsResponse {
    triage_item_id: number;
    triage_items: TriageDuplicateSuggestion[];
    tasks: TriageDuplicateSuggestion[];
}

export interface TriageClassificationSuggestion {
    id: number;
    triage_item_id: number;
    suggested_type_label_slug?: string | null;
    suggested_area_label_slug?: string | null;
    suggested_priority?: number | null;
    suggested_label_slugs: string[];
    unmatched_label_text: string[];
    suggested_assignee_id?: number | null;
    suggested_assignee_hint?: string | null;
    suggested_project_id?: number | null;
    duplicate_candidates: Array<Record<string, unknown>>;
    confidence: number;
    rationale?: string | null;
    language?: string | null;
    provider?: string | null;
    model?: string | null;
    is_fallback: boolean;
    created_at: string;
}

export interface TriageTaskDraftRequest {
    template_id?: number | null;
    classification_suggestion_id?: number | null;
    current_title?: string | null;
    current_description?: string | null;
}

export interface TriageTaskDraftResponse {
    triage_item_id: number;
    suggested_title: string;
    suggested_description: string;
    suggested_checklist: string[];
    acceptance_criteria: string[];
    risks: string[];
    template_id?: number | null;
    classification_suggestion_id?: number | null;
    is_fallback: boolean;
    provider?: string | null;
    model?: string | null;
    language?: 'en' | 'ru';
    finish_reason?: string | null;
    is_truncated?: boolean;
    grounded_facts?: Array<{ claim: string; source: string }>;
    implementation_notes?: string[];
    open_questions?: string[];
    ungrounded_suggestions?: string[];
    warnings?: string[];
    rationale?: string | null;
}

export interface TriageConvertToTaskRequest {
    iteration_id: number;
    title?: string;
    description?: string | null;
    project_id?: number | null;
    assignee_id?: number | null;
    priority?: number;
    tags?: string[];
    effort_days: number;
    effort_hours?: number;
    depends_on: number[];
}

export interface TriageConvertToTaskResponse {
    triage_item: TriageItem;
    task: Task;
}
