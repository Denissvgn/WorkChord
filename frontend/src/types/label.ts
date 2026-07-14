export interface LabelGroupBrief {
    id: number;
    key: string;
    name: string;
    color: string;
    is_active: boolean;
}

export interface Label {
    id: number;
    slug: string;
    name: string;
    group_id: number;
    group?: LabelGroupBrief | null;
    description?: string | null;
    color: string;
    is_active: boolean;
    sort_order: number;
    seed_key?: string | null;
    created_at: string;
    updated_at: string;
}

export interface LabelGroup {
    id: number;
    key: string;
    name: string;
    description?: string | null;
    color: string;
    is_active: boolean;
    sort_order: number;
    seed_key?: string | null;
    labels: Label[];
    created_at: string;
    updated_at: string;
}

export interface LabelGroupCreate {
    key: string;
    name: string;
    description?: string | null;
    color?: string;
    is_active?: boolean;
    sort_order?: number;
}

export type LabelGroupUpdate = Partial<LabelGroupCreate>;

export interface LabelCreate {
    slug: string;
    name: string;
    group_id: number;
    description?: string | null;
    color?: string;
    is_active?: boolean;
    sort_order?: number;
}

export type LabelUpdate = Partial<LabelCreate>;

export interface LabelGroupListParams {
    include_inactive?: boolean;
}

export interface LabelListParams {
    group_key?: string;
    include_inactive?: boolean;
    q?: string;
}
