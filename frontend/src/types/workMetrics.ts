export interface WorkMetrics {
    metric_contract_version?: number;
    total_tasks?: number;
    required_tasks?: number;
    optional_tasks?: number;
    structural_tasks?: number;
    implemented_tasks?: number;
    accepted_tasks?: number;
    overdue_tasks?: number;
    late_start_tasks?: number;
    iteration_overflow_tasks?: number;
    project_target_overflow_tasks?: number;
    acceptance_unknown_tasks?: number;
    accepted_percent?: number;
}
