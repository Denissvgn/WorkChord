export type SavedViewType = 'tasks' | 'projects' | 'triage';
export type SavedViewScope = 'personal' | 'shared' | 'system';

export interface SavedView {
    id: number;
    name: string;
    description?: string | null;
    seed_key?: string | null;
    view_type: SavedViewType;
    scope: SavedViewScope;
    filters_json: Record<string, unknown>;
    sort_json: Record<string, unknown>;
    columns_json: Record<string, unknown>;
    created_by_session_id?: number | null;
    schema_version: number;
    is_valid: boolean;
    invalid_reason?: string | null;
    created_at: string;
    updated_at: string;
}

export interface SavedViewDashboardCard {
    saved_view_id: number;
    seed_key: string;
    name: string;
    description?: string | null;
    view_type: SavedViewType;
    scope: SavedViewScope;
    count: number;
    target_path: string;
    is_valid: boolean;
    invalid_reason?: string | null;
}

export interface SavedViewListParams {
    view_type: SavedViewType;
}

export interface SavedViewCreate {
    name: string;
    description?: string | null;
    view_type: SavedViewType;
    scope?: Exclude<SavedViewScope, 'system'>;
    filters_json?: Record<string, unknown>;
    sort_json?: Record<string, unknown>;
    columns_json?: Record<string, unknown>;
    schema_version?: number;
}

export interface SavedViewUpdate {
    name?: string;
    description?: string | null;
    view_type?: SavedViewType;
    scope?: Exclude<SavedViewScope, 'system'>;
    filters_json?: Record<string, unknown>;
    sort_json?: Record<string, unknown>;
    columns_json?: Record<string, unknown>;
    schema_version?: number;
}

export interface SavedViewDuplicate {
    name?: string;
    description?: string | null;
    scope?: Exclude<SavedViewScope, 'system'>;
}
