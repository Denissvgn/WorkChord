export interface IterationProject {
    id: number;
    name: string;
    status: string;
    health: string;
}

export interface Iteration {
    id: number;
    name: string;
    calendar_id: number;
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
    project_id?: number | null;
    start_date: string;
    end_date: string;
    manager_email?: string;
}

export interface IterationUpdate {
    name?: string;
    calendar_id?: number | null;
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
    project_id?: number | null;
    start_date: string;
    duration_days: number;
    stop: IterationSeriesStop;
    manager_email?: string;
}

export interface IterationSeriesResponse {
    iterations: Iteration[];
}

export interface IterationSummary {
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
}
