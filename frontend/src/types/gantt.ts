import type { Iteration } from './iteration';
import type { TaskUpdate } from './task';

// TaskAssignee removed as it is not used anymore

export interface GanttTask {
    id: number;
    title: string;
    description?: string;
    project_id?: number | null;
    milestone_id?: number | null;
    start_date: string | null;
    end_date: string | null;
    actual_start_date?: string | null;  // When status changed to ACTIVE
    actual_end_date?: string | null;    // When status changed to CLOSED
    min_start_date?: string | null;
    max_end_date?: string | null;
    effort_days: number;
    effort_hours?: number;
    calculated_effort_days: number | null;  // Effort after applying coefficients
    progress: number;
    priority: number;
    status: 'planned' | 'active' | 'resolved' | 'closed';
    is_composite: boolean;
    is_overdue: boolean;
    is_delayed: boolean;  // start_date < today and status == PLANNED
    is_optional: boolean;
    is_deferred?: boolean;
    is_outside_constraints: boolean;
    tags: string[];
    milestone?: {
        id: number;
        project_id: number;
        name: string;
        status: string;
        target_date?: string | null;
    } | null;
    assignee?: { id: number; name: string } | null;
    assignees: Array<{ id: number; name: string }>;
    children: GanttTask[];
    dependencies: number[];
    version?: number;  // Optimistic-concurrency version, sent by the Gantt API
    /** Complete local draft used when applying sandbox edits atomically. */
    sandbox_update?: TaskUpdate;
    isSandboxModified?: boolean;
    schedule_result?: {
        scheduled_start: string;
        scheduled_end: string;
        issues: Array<{
            is_overload: boolean;
            description: string;
        }>;
    };
}

export interface GanttResponse {
    iteration: Iteration;
    tasks: GanttTask[];
    overdue_task_ids: number[];
    holidays: string[];
    weekends: string[];
    member_vacations: Record<number, string[]>;
    schedule_result?: ScheduleResult | null;
}

export interface ScheduleResult {
    success: boolean;
    decisions: SchedulingDecision[];
    workload_balanced: boolean;
    workload_issues: WorkloadIssue[];
}

/** Server dry-run of sandbox edits through the real scheduler (nothing persisted). */
export interface SchedulePreviewResponse {
    tasks: GanttTask[];
    overdue_task_ids: number[];
    schedule_result?: ScheduleResult | null;
}

export interface SchedulingDecision {
    task_id: number;
    task_title: string;
    decision_type: 'scheduled' | 'reordered' | 'delayed' | 'overdue';
    reason: string;
    affected_tasks: number[];
}

export interface WorkloadIssue {
    member_id: number;
    member_name: string;
    issue: string;
}

export type ExplainScheduleDetailLevel = 'brief' | 'full';

export interface ExplainScheduleRequest {
    detail_level?: ExplainScheduleDetailLevel;
}

export interface ScheduleDecisionExplanation {
    task_id: number;
    task_title: string;
    decision_type: string;
    explanation: string;
}

export interface WorkloadAnalysis {
    balanced: boolean;
    issues: string[];
}

export interface ExplainScheduleResponse {
    summary: string;
    decisions: ScheduleDecisionExplanation[];
    workload_analysis: WorkloadAnalysis;
    provider?: string | null;
    model?: string | null;
    language?: 'en' | 'ru';
    is_fallback?: boolean;
    finish_reason?: string | null;
    is_truncated?: boolean;
    warnings?: string[];
}
