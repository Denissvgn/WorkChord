export interface AnalyticsScope {
    project_id?: number;
    iteration_id?: number;
    backlog?: boolean;
    all_projects?: boolean;
    all_projects_backlog?: boolean;
    lookback_days: number;
}
