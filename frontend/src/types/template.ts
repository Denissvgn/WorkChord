export type TemplateType = 'task' | 'project' | 'triage';

export interface WorkTemplate {
    id: number;
    name: string;
    description?: string | null;
    seed_key?: string | null;
    template_type: TemplateType;
    default_title?: string | null;
    default_description?: string | null;
    default_priority?: number | null;
    default_effort_days?: number | null;
    default_labels: string[];
    default_checklist: string[];
    default_payload: Record<string, unknown>;
    is_active: boolean;
    sort_order: number;
    created_at: string;
    updated_at: string;
}

export interface WorkTemplateCreate {
    name: string;
    description?: string | null;
    template_type: TemplateType;
    default_title?: string | null;
    default_description?: string | null;
    default_priority?: number | null;
    default_effort_days?: number | null;
    default_labels?: string[];
    default_checklist?: string[];
    default_payload?: Record<string, unknown>;
    is_active?: boolean;
    sort_order?: number;
}

export type WorkTemplateUpdate = Partial<WorkTemplateCreate>;

export interface TemplateListParams {
    template_type?: TemplateType;
    include_inactive?: boolean;
}
