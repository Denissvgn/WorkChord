import type { Task } from './task';
import type { TeamMemberOption, TeamMemberProfileCompact } from './team';

export type ProjectStatus = 'proposed' | 'planned' | 'active' | 'paused' | 'completed' | 'canceled';
export type ProjectHealth = 'unknown' | 'on_track' | 'at_risk' | 'off_track';
export type ProjectTargetDateRisk = 'unknown' | 'on_track' | 'at_risk' | 'off_track';
export type ProjectUpdateFreshness = 'fresh' | 'stale' | 'missing' | 'not_required';
export type ProjectMilestoneStatus = 'planned' | 'active' | 'completed' | 'canceled';
export type ProjectOwner = TeamMemberOption;
export type ProjectProfileOwner = TeamMemberProfileCompact;

export interface Initiative {
    id: number;
    name: string;
    description?: string | null;
    owner_id: number | null;
    owner: ProjectOwner | null;
    owner_profile_id: number | null;
    owner_profile: ProjectProfileOwner | null;
    health: ProjectHealth;
    target_date?: string | null;
    created_at: string;
    updated_at: string;
}

export interface InitiativeCreate {
    name: string;
    description?: string | null;
    owner_id?: number | null;
    owner_profile_id?: number | null;
    health: ProjectHealth;
    target_date?: string | null;
}

export interface InitiativeUpdate {
    name?: string;
    description?: string | null;
    owner_id?: number | null;
    owner_profile_id?: number | null;
    health?: ProjectHealth;
    target_date?: string | null;
}

export interface ProjectInitiativeSummary {
    id: number;
    name: string;
    owner_id: number | null;
    owner: ProjectOwner | null;
    owner_profile_id: number | null;
    owner_profile: ProjectProfileOwner | null;
    health: ProjectHealth;
    target_date?: string | null;
}

export interface Project {
    id: number;
    name: string;
    description?: string | null;
    status: ProjectStatus;
    health: ProjectHealth;
    owner_id: number | null;
    owner: ProjectOwner | null;
    owner_profile_id: number | null;
    owner_profile: ProjectProfileOwner | null;
    initiative_id?: number | null;
    initiative?: ProjectInitiativeSummary | null;
    start_date?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    sort_order: number;
    created_at: string;
    updated_at: string;
}

export interface ProjectCreate {
    name: string;
    description?: string | null;
    status: ProjectStatus;
    health: ProjectHealth;
    owner_id?: number | null;
    owner_profile_id?: number | null;
    initiative_id?: number | null;
    start_date?: string | null;
    target_date?: string | null;
    sort_order: number;
}

export interface ProjectUpdate {
    name?: string;
    description?: string | null;
    status?: ProjectStatus;
    health?: ProjectHealth;
    owner_id?: number | null;
    owner_profile_id?: number | null;
    initiative_id?: number | null;
    start_date?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    sort_order?: number;
}

export interface ProjectUpdateEntry {
    id: number;
    project_id: number;
    health: ProjectHealth;
    summary: string;
    progress_text?: string | null;
    risks_text?: string | null;
    decisions_text?: string | null;
    next_steps_text?: string | null;
    created_by_session_id?: number | null;
    created_at: string;
}

export interface ProjectUpdateEntryCreate {
    health: ProjectHealth;
    summary: string;
    progress_text?: string | null;
    risks_text?: string | null;
    decisions_text?: string | null;
    next_steps_text?: string | null;
}

export interface ProjectMilestone {
    id: number;
    project_id: number;
    name: string;
    description?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    sort_order: number;
    status: ProjectMilestoneStatus;
    created_at: string;
    updated_at: string;
}

export interface RoadmapMilestonePage {
    items: ProjectMilestone[];
    next_cursor: number | null;
}

export interface ProjectMilestoneCreateRequest {
    name: string;
    description?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    sort_order?: number;
    status?: ProjectMilestoneStatus;
}

export interface ProjectMilestoneUpdateRequest {
    name?: string;
    description?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    sort_order?: number;
    status?: ProjectMilestoneStatus;
}

export interface ProjectMilestoneDeleteResponse {
    success: boolean;
    message: string;
    detached_task_count: number;
}

export interface ProjectMilestoneSummary {
    id: number;
    project_id: number;
    name: string;
    status: ProjectMilestoneStatus;
    target_date?: string | null;
    sort_order: number;
}

export interface ProjectMilestoneTaskGroup {
    milestone_id?: number | null;
    milestone?: ProjectMilestoneSummary | null;
    name: string;
    task_count: number;
    completed_tasks: number;
    completion_percent: number;
    status_counts: Record<string, number>;
    total_effort_days: number;
    remaining_effort_days: number;
}

export interface ProjectPortfolioSummary {
    project_id: number;
    total_tasks: number;
    completed_tasks: number;
    total_effort_days: number;
    remaining_effort_days: number;
    blocked_tasks: number;
    overdue_tasks: number;
    target_date_risk: ProjectTargetDateRisk;
}

export interface ProjectSummary {
    id: number;
    name: string;
    status: ProjectStatus;
    health: ProjectHealth;
    owner_id: number | null;
    owner: ProjectOwner | null;
    owner_profile_id: number | null;
    owner_profile: ProjectProfileOwner | null;
    initiative_id?: number | null;
    start_date?: string | null;
    target_date?: string | null;
    completed_at?: string | null;
    total_tasks: number;
    completed_tasks: number;
    completion_percent: number;
    active_tasks: number;
    blocked_tasks: number;
    overdue_tasks: number;
    target_date_risk: ProjectTargetDateRisk;
    target_date_risk_reason?: string | null;
    target_date_slip_days: number;
    days_until_target?: number | null;
    status_counts: Record<string, number>;
    total_effort_days: number;
    remaining_effort_days: number;
    milestone_groups: ProjectMilestoneTaskGroup[];
    request_count: number;
    task_start_date?: string | null;
    task_end_date?: string | null;
    latest_update?: ProjectUpdateEntry | null;
    latest_update_at?: string | null;
    days_since_latest_update?: number | null;
    update_freshness: ProjectUpdateFreshness;
    is_update_stale: boolean;
    stale_update_threshold_days: number;
}

export type ProjectTask = Task;
