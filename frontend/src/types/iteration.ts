import type { TaskDisplayedState } from './task';
import type { WorkMetrics } from './workMetrics';
export interface IterationProject {
    id: number;
    name: string;
    status: string;
    health: string;
}

export interface Iteration {
    nominal_day_hours?: number;
    revision?: number;
    id: number;
    name: string;
    calendar_id: number;
    additional_calendar_ids?: number[];
    missing_calendar_years?: number[];
    project_id?: number | null;
    project?: IterationProject | null;
    start_date: string; // ISO
    end_date: string; // ISO
    manager_email?: string;
    working_days: number;
}

export interface IterationCreate {
    name: string;
    calendar_id?: number | null;
    additional_calendar_ids?: number[];
    project_id?: number | null;
    start_date: string;
    end_date: string;
    manager_email?: string;
}

export interface IterationUpdate {
    name?: string;
    calendar_id?: number | null;
    additional_calendar_ids?: number[];
    project_id?: number | null;
    start_date?: string;
    end_date?: string;
    manager_email?: string | null;
}

export type IterationSeriesStop =
    | { mode: 'count'; count: number }
    | { mode: 'until_date'; until_date: string };

export interface IterationSeriesCreate {
    base_name: string;
    calendar_id?: number | null;
    additional_calendar_ids?: number[];
    project_id?: number | null;
    start_date: string;
    duration_days: number;
    stop: IterationSeriesStop;
    manager_email?: string;
}

export interface IterationSeriesResponse {
    iterations: Iteration[];
}

export interface IterationSummary extends WorkMetrics {
    missing_calendar_years?: number[];
    id: number;
    name: string;
    project_id?: number | null;
    project?: IterationProject | null;
    start_date: string;
    end_date: string;
    working_days: number;
    total_tasks: number;
    completed_tasks: number;
    total_effort_days: number;
    team_capacity_days: number;
    overdue_tasks_count: number;
    /** Leaf counts by status, from the same aggregate as the other counts. */
    status_counts?: Partial<Record<TaskDisplayedState, number>>;
    blocked_tasks?: number;
    remaining_effort_days?: number;
    unknown_estimate_tasks?: number;
    /** Latest scheduled end of the included work; null before the iteration is scheduled. */
    scheduled_finish?: string | null;
    remaining_working_days?: number | null;
}

export interface IterationPlanningReadinessSummary {
    iteration_id: number;
    calendar_name?: string | null;
    additional_calendar_ids?: number[];
    missing_calendar_years?: number[];
    team_member_count: number;
    team_capacity_hours: number;
    /** Effort of the iteration's planning leaves, and the part assigned to a capacity row. */
    planned_hours?: number;
    assigned_hours?: number;
    team_members_no_capacity: number;
    task_count: number;
    tasks_without_assignee: number;
    tasks_without_effort: number;
    tasks_agent_without_capacity?: number;
    team_agent_count?: number;
    has_schedule: boolean;
    risk_count: number;
    /** Saved dependency pairs whose dates start the dependent on or before its prerequisite ends. */
    inverted_dependencies?: Array<{
        task_id: number;
        task_title: string;
        task_start_date: string;
        prerequisite_id: number;
        prerequisite_title: string;
        prerequisite_end_date: string;
    }>;
    /** The six plan checkpoints, derived on the server; the PM agent reads the same list. */
    checkpoints?: PlanCheckpoint[];
    checkpoints_done?: number;
    checkpoints_total?: number;
}

export interface PlanCheckpoint {
    id: 'iteration' | 'team' | 'work' | 'blockers' | 'schedule' | 'review';
    state: 'done' | 'warn' | 'todo' | 'blocked';
    reason_codes: string[];
    counts: Record<string, number>;
}
