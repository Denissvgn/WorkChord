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
    effort_days: number | null;
    effort_hours?: number | null;
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
    /** Saved start is on or before a prerequisite's saved end; a schedule preview shows corrected dates. */
    has_inverted_dependency?: boolean;
    tags: string[];
    milestone?: {
        id: number;
        project_id: number;
        name: string;
        status: string;
        target_date?: string | null;
    } | null;
    assignee?: { id: number; name: string; kind?: 'human' | 'agent' | 'hybrid' | null } | null;
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

export interface InvertedDependency {
    task_id: number;
    task_title: string;
    task_start_date: string;
    prerequisite_id: number;
    prerequisite_title: string;
    prerequisite_end_date: string;
}

export interface GanttResponse {
    iteration: Iteration;
    tasks: GanttTask[];
    overdue_task_ids: number[];
    inverted_dependencies?: InvertedDependency[];
    holidays: string[];
    weekends: string[];
    member_vacations: Record<number, string[]>;
    schedule_result?: ScheduleResult | null;
}

export type UnscheduledReason = 'no_assignee' | 'assignee_not_in_iteration' | 'no_estimate' | 'no_capacity'
    | 'prerequisites_pending' | 'predecessor_unscheduled' | 'predecessor_postponed' | 'deferred' | 'blocked' | 'not_placed';

/** A task a planned task waits on: postponed work, or the prerequisite behind idle days. */
export interface WaitingOnTask {
    task_id: number;
    task_title: string;
}

export type DateRule = 'dates_incomplete' | 'dates_inverted' | 'outside_iteration' | 'before_min_start_date';

/** A planned task the scheduler left without dates, with the cause and the server's English hint. */
export interface UnscheduledTask {
    task_id: number;
    task_title: string;
    reason: UnscheduledReason;
    message: string;
    /** The task held dates before this run and the run removed them. */
    dates_cleared?: boolean;
    /** The rule the removed dates broke; only a half-dated task loses its dates. */
    date_rule?: DateRule;
    /** Causes of its own that keep it undated once the main reason is resolved. */
    also?: UnscheduledReason[];
    /** The postponed work it waits on, for reason predecessor_postponed. */
    waiting_on?: WaitingOnTask[];
}

/** A planned task the scheduler could not place; it keeps the dates it already had. */
export interface KeptDatesTask {
    task_id: number;
    task_title: string;
    reason: UnscheduledReason;
    message: string;
    start_date: string;
    end_date: string;
    /** The rule the kept dates break, when they break one. */
    date_rule?: DateRule;
    also?: UnscheduledReason[];
    waiting_on?: WaitingOnTask[];
}

export type IdleReason = 'waits_for_prerequisite' | 'earliest_start' | 'fixed_dates' | 'uninterrupted_slot';

/** Working days an assignee is left idle before the task that follows them on the row. */
export interface IdleGap {
    start_date: string;
    end_date: string;
    working_days: number;
    /** The task that starts after these days, and why it starts no earlier. */
    task_id: number;
    task_title: string;
    reason: IdleReason;
    /** The prerequisite it waits for, for reason waits_for_prerequisite. */
    waiting_on?: WaitingOnTask;
    message: string;
}

/** An assignee's working days left idle inside the scheduled span, before the row's last work. */
export interface AssigneeIdleDays {
    member_id: number;
    member_name: string;
    idle_working_days: number;
    gaps: IdleGap[];
}

export interface ScheduleResult {
    planning_revision?: number;
    capacity_issues?: { profile_id: number | null; code: string; message: string; dates?: string[] }[];
    success: boolean;
    decisions: SchedulingDecision[];
    workload_balanced: boolean;
    workload_issues: WorkloadIssue[];
    unscheduled?: UnscheduledTask[];
    kept_dates?: KeptDatesTask[];
    idle_days?: AssigneeIdleDays[];
}

/** Server dry-run of sandbox edits through the real scheduler (nothing persisted). */
export interface SchedulePreviewResponse {
    input_revision: number;
    input_planning_revision?: number;
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
