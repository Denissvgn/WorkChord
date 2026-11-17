export interface AnalyticsScope {
    project_id?: number;
    iteration_id?: number;
    backlog?: boolean;
    all_projects?: boolean;
    lookback_days: number;
}
