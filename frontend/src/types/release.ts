import type { TaskStatus } from './task';

export type ReleaseStatus = 'planned' | 'building' | 'shipped' | 'canceled';

export interface ReleaseTaskSummary {
    id: number;
    title: string;
    status: TaskStatus | string;
    project_id?: number | null;
}

export interface Release {
    id: number;
    project_id: number;
    name: string;
    description?: string | null;
    status: ReleaseStatus;
    target_date?: string | null;
    shipped_at?: string | null;
    version?: string | null;
    environment?: string | null;
    task_ids: number[];
    tasks: ReleaseTaskSummary[];
    created_at: string;
    updated_at: string;
}

export interface ReleaseCreateRequest {
    name: string;
    description?: string | null;
    status?: ReleaseStatus;
    target_date?: string | null;
    shipped_at?: string | null;
    version?: string | null;
    environment?: string | null;
    task_ids?: number[];
}

export interface ReleaseUpdateRequest {
    name?: string;
    description?: string | null;
    status?: ReleaseStatus;
    target_date?: string | null;
    shipped_at?: string | null;
    version?: string | null;
    environment?: string | null;
    task_ids?: number[];
}
