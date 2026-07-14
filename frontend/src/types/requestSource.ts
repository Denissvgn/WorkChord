export type RequestSourceType = 'customer' | 'internal' | 'support' | 'email' | 'web' | 'import';
export type RequestSourceTargetType = 'task' | 'project' | 'triage_item';

export interface RequestSource {
    id: number;
    title: string;
    description?: string | null;
    source_type: RequestSourceType;
    source_name?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    priority_hint?: number | null;
    created_at: string;
}

export interface RequestSourceCreate {
    title: string;
    description?: string | null;
    source_type: RequestSourceType;
    source_name?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    priority_hint?: number | null;
}

export interface RequestSourceLink {
    id: number;
    request_source_id: number;
    triage_item_id?: number | null;
    task_id?: number | null;
    project_id?: number | null;
    created_at: string;
}

export interface RequestSourceLinkWithSource extends RequestSourceLink {
    request_source: RequestSource;
}

export type RequestSourceLinkCreate =
    | {
        target_type: RequestSourceTargetType;
        target_id: number;
        request_source_id: number;
        request_source?: never;
    }
    | {
        target_type: RequestSourceTargetType;
        target_id: number;
        request_source: RequestSourceCreate;
        request_source_id?: never;
    };
