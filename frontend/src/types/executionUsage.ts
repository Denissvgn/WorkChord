export interface ExecutionUsageSummary {
    window_start: string;
    window_end: string;
    window_basis: string;
    expected_runs: number;
    reported_runs: number;
    unreported_runs: number;
    partial_reports: number;
    unavailable_reports: number;
    simulated_reports: number;
    measured_report_count: number;
    provider_reported_cost: Record<string, string | null>;
    estimated_cost: Record<string, string | null>;
    known_cost_reports: Record<string, number>;
    unknown_cost_reports: number;
    accepted_task_identities: number;
    reports_linked_to_accepted_tasks: number;
    reported_human_effort_minutes: string | null;
    human_effort_reports: number;
    reported_units: Record<string, string | null>;
    unit_report_counts: Record<string, number>;
    simulated_reported_cost: Record<string, string>;
    simulated_estimated_cost: Record<string, string>;
    simulated_units: Record<string, string | null>;
    independently_reconciled: false;
    advisory_budget: { amount: string; currency: string; known_reported_cost: string | null;
        known_estimated_cost: string | null; coverage: string; advisory_only: true } | null;
}
