import type { TriageItem } from './triage';
import type { AssigneeRecommendation } from './team';

export interface TaskAssignee {
    id: number;
    name: string;
}

export interface TaskClaimedBy {
    id: number;
    name: string;
    display_name: string;
}

export interface TaskProject {
    id: number;
    name: string;
    status: string;
    health: string;
}

export interface TaskMilestone {
    id: number;
    project_id: number;
    name: string;
    status: string;
    target_date?: string | null;
}

export interface TaskAgentReadinessCriterion {
    key: string;
    label: string;
    passed: boolean;
    reason: string;
}

export interface TaskAgentReadiness {
    blocker_codes?: string[];
    is_ready: boolean;
    blockers: string[];
    warnings: string[];
    criteria: TaskAgentReadinessCriterion[];
}

export type TaskStatus = 'planned' | 'active' | 'resolved' | 'closed';
export type ExternalLinkProvider = 'github' | 'gitlab' | 'figma' | 'sentry' | 'custom' | string;

export interface ExternalLink {
    id?: number | null;
    entity_type: 'task' | 'project' | 'release' | string;
    entity_id: number;
    provider: ExternalLinkProvider;
    external_key?: string | null;
    url?: string | null;
    title?: string | null;
    status?: string | null;
    metadata_json: Record<string, unknown>;
    is_legacy: boolean;
    created_at?: string | null;
    updated_at?: string | null;
}

export interface ExternalLinkCreate {
    provider: ExternalLinkProvider;
    external_key?: string | null;
    url?: string | null;
    title?: string | null;
    status?: string | null;
    metadata_json?: Record<string, unknown>;
}

export interface GitHubExternalLinkCreate {
    url: string;
}

export interface ExternalLinkUpdate {
    provider?: ExternalLinkProvider;
    external_key?: string | null;
    url?: string | null;
    title?: string | null;
    status?: string | null;
    metadata_json?: Record<string, unknown>;
}

export interface Task {
    iteration_revision?: number;
    effective_is_deferred?: boolean;
    effective_is_optional?: boolean;
    metric_contract_version?: number;
    is_late_start?: boolean;
    is_iteration_overflow?: boolean;
    is_project_target_overflow?: boolean;
    is_implemented?: boolean;
    is_accepted?: boolean;
    acceptance_unknown?: boolean;
    owner_profile_id?: number | null;
    owner?: TaskAssignee | null;
    ownership_provenance?: string;
    nominal_day_hours?: number;
    estimate_provenance?: string;
    brief?: TaskBrief | null;
    brief_revision?: number;
    brief_provenance?: string;
    legacy_description?: string | null;
    brief_migration_notes?: string[];
    progress?: TaskProgress | null;
    artifact_revision?: number;
    execution_mode?: 'manual' | 'scheduled';
    blocked_reason?: string | null;
    canceled_at?: string | null;
    canceled_reason?: string | null;
    detail_context?: TaskDetail;
    baseline_start_date?: string | null;
    baseline_end_date?: string | null;
    baseline_revision?: number;
    baseline_provenance?: string;
    started_at?: string | null;
    resolved_at?: string | null;
    accepted_at?: string | null;

    id: number;
    iteration_id: number | null;
    project_id?: number | null;
    milestone_id?: number | null;
    parent_id?: number | null;
    title: string;
    description?: string;
    priority: number;
    effort_days: number | null;
    effort_hours: number | null;
    project?: TaskProject | null;
    milestone?: TaskMilestone | null;
    assignee?: TaskAssignee | null;
    status: TaskStatus;
    start_date?: string | null;
    end_date?: string | null;
    actual_start_date?: string | null;
    actual_end_date?: string | null;
    min_start_date?: string | null;
    max_end_date?: string | null;
    is_overdue: boolean;
    is_delayed: boolean;
    is_composite: boolean;
    is_optional: boolean;
    is_deferred: boolean;
    is_outside_constraints?: boolean;
    tags: string[];
    sort_order: number;
    external_key?: string | null;
    source?: string | null;
    source_url?: string | null;
    external_links: ExternalLink[];
    request_count: number;
    agent_readiness: TaskAgentReadiness;
    version: number;
    claimed_by?: TaskClaimedBy | null;
    claim_expires_at?: string | null;
    updated_at?: string | null;
    children: Task[];
    dependencies: number[];
}

export interface TaskCreate {
    owner_profile_id?: number | null;
    brief?: TaskBrief;
    estimate_provenance?: "unknown" | "assumed" | "estimated";
    expected_revision?: number;
    parent_id?: number | null;
    title: string;
    description?: string;
    priority: number;
    effort_days: number | null;
    effort_hours?: number | null;
    assignee_id?: number | null;
    project_id?: number | null;
    milestone_id?: number | null;
    depends_on: number[];
    is_optional?: boolean;
    is_deferred?: boolean;
    tags?: string[];
    sort_order?: number;
    min_start_date?: string | null;
    max_end_date?: string | null;
    external_key?: string | null;
    source?: string | null;
    source_url?: string | null;
}

export interface TaskUpdate extends Partial<TaskCreate> {
    status?: string;
    /** Rendered task version used for optimistic concurrency. */
    expected_version?: number;
}

export interface TaskMoveRequest {
    expected_revisions?: Record<number, number>;
    iteration_id: number;
    parent_id?: number | null;
    expected_version?: number;
}

export interface TaskVersionConflictDetail {
    code: 'task_version_conflict';
    message: string;
    expected_version: number;
    current_task: Pick<Task, 'id' | 'version' | 'title' | 'status' | 'updated_at'>;
}

export interface SuggestedSubtask {
    title: string;
    effort_days: number;
}

export interface TaskFormalizeResponse {
    original_title: string;
    formalized_title: string;
    suggested_description: string;
    language?: 'en' | 'ru';
    suggested_effort_days?: number | null;
    suggested_subtasks: SuggestedSubtask[];
}

export interface TaskImproveDescriptionResponse {
    improved_description: string;
    language?: 'en' | 'ru';
}

export interface GroundedFact {
    claim: string;
    source: string;
}

export interface TaskAISuggestRequest {
    brief?: TaskBrief | null;
    title: string;
    description?: string | null;
    priority?: number | null;
    effort_days?: number | null;
    effort_hours?: number | null;
    assignee_id?: number | null;
    project_id?: number | null;
    milestone_id?: number | null;
    parent_id?: number | null;
    depends_on?: number[];
    tags?: string[];
    is_optional?: boolean | null;
    is_deferred?: boolean | null;
    min_start_date?: string | null;
    max_end_date?: string | null;
    source?: string | null;
    source_url?: string | null;
    external_key?: string | null;
    template_id?: number | null;
    user_context?: string | null;
    extra_context?: Record<string, unknown>;
}

export interface GroundedAISuggestionResponse {
    provider?: string | null;
    model?: string | null;
    language?: 'en' | 'ru';
    is_fallback: boolean;
    finish_reason?: string | null;
    is_truncated: boolean;
    suggested_title?: string | null;
    suggested_description: string;
    acceptance_criteria: string[];
    implementation_notes: string[];
    risks: string[];
    open_questions: string[];
    grounded_facts: GroundedFact[];
    ungrounded_suggestions: string[];
    warnings: string[];
}

export type TaskImportDestination = 'tasks' | 'triage' | 'auto';

export interface TasksImportRequest {
    text: string;
    destination?: TaskImportDestination;
}

export interface TasksImportResponse {
    imported_count: number;
    task_count: number;
    triage_count: number;
    tasks: Task[];
    triage_items: TriageItem[];
}

export interface TaskMergeRequest {
    expected_revision?: number;
    task_ids: number[];
    parent_title: string;
    parent_description?: string;
}

export type TaskBulkAction =
    | 'set_assignee'
    | 'clear_assignee'
    | 'auto_assign'
    | 'set_project'
    | 'clear_project'
    | 'set_milestone'
    | 'clear_milestone'
    | 'set_priority'
    | 'add_labels'
    | 'remove_labels'
    | 'set_flags'
    | 'change_status'
    | 'delete';

export type TaskBulkOutcome = 'updated' | 'deleted' | 'skipped' | 'failed' | 'would_update' | 'would_delete';

export interface TaskBulkOperationRequest {
    expected_versions?: Record<number, number>;
    expected_revisions?: Record<number, number>;
    task_ids: number[];
    action: TaskBulkAction;
    payload?: Record<string, unknown>;
    dry_run?: boolean;
}

export interface TaskBulkOperationResult {
    task_id: number;
    outcome: TaskBulkOutcome;
    changes: Record<string, { old: unknown; new: unknown } | unknown>;
    warnings: string[];
    error?: string | null;
    task?: Task | null;
    assignee_recommendation?: AssigneeRecommendation | null;
}

export interface TaskBulkOperationResponse {
    input_revisions?: Record<number, number>;
    task_versions?: Record<number, number>;
    requested_count: number;
    succeeded_count: number;
    failed_count: number;
    dry_run: boolean;
    results: TaskBulkOperationResult[];
}

export interface CascadeUpdateInfo {
    task_id: number;
    task_title: string;
    old_start_date: string | null;
    new_start_date: string | null;
    old_end_date: string | null;
    new_end_date: string | null;
}

export interface TaskStatusChangeResponse {
    task: Task;
    cascade_updates: CascadeUpdateInfo[];
    notifications_sent: boolean;
}

export interface TaskStatusLog {
    id: number;
    task_id: number;
    task_title?: string;
    from_status: TaskStatus;
    to_status: TaskStatus;
    changed_at: string;
    reason?: string;
    triggered_by: string;
    affected_task_ids: number[];
}

export interface TaskStatusStats {
    from_status: TaskStatus;
    to_status: TaskStatus;
    count: number;
}

export interface TaskTimelineItem {
    item_type: 'task_event' | 'status_log' | 'agent_run' | 'agent_run_event';
    timestamp: string;
    title: string;
    payload: Record<string, unknown>;
    actor_type?: string | null;
    actor_id?: number | null;
    trace_id?: string | null;
}

export interface TaskTimelineResponse {
    task_id: number;
    items: TaskTimelineItem[];
}

export interface TaskBatchUpdateItem {
    task_id: number;
    update: TaskUpdate;
    status_reason?: string | null;
    expected_version?: number;
}

export interface TaskBatchUpdateRequest {
    expected_revision?: number;
    tasks: TaskBatchUpdateItem[];
    expected_planning_revision?: number;
}

export interface TaskBatchUpdateResponseItem {
    task_id: number;
    success: boolean;
    error?: string | null;
}

export interface TaskBatchUpdateResponse {
    results: TaskBatchUpdateResponseItem[];
    updated_tasks: Task[];
}


export interface BriefCriterion {
    id: string;
    revision: number;
    text: string;
    verification: string;
}

export interface TaskBrief {
    schema_version: 1;
    goal: string;
    context: string;
    scope: string;
    exclusions: string;
    acceptance_criteria: BriefCriterion[];
    verification: string;
    artifact_expectations: string;
}

export interface CriterionProgress {
    criterion_id: string;
    criterion_revision: number;
    state: 'pending' | 'in_progress' | 'completed';
    evidence: string;
}

export interface TaskProgress {
    criteria: CriterionProgress[];
    artifacts: string[];
    brief_revision: number;
    artifact_revision: number;
}

export interface TaskReference {
    acceptance_current?: boolean;
    project_name?: string | null; iteration_name?: string | null; blocked_reason?: string | null; canceled_at?: string | null;
    id: number; title: string; version: number; status: TaskStatus;
    project_id: number | null; iteration_id: number | null; parent_id: number | null; owner_profile_id: number | null;
}
export interface TaskReferencePage { items: TaskReference[]; has_more: boolean; next_after_id: number | null; limit: number }
export interface TaskDetail {
    task: Task; ancestors: TaskReference[]; ancestors_complete: boolean;
    children: TaskReferencePage; dependencies: TaskReferencePage; execution_context_complete: false;
}
export interface TaskActionAvailability { action: string; allowed: boolean; blockers: { code: string; message: string }[] }
export interface TaskActions {
    task_id: number; version: number; actions: TaskActionAvailability[];
    claim_generation: number; running_run_ids: number[]; live_assignment_ids: number[];
}
export interface TaskCommand {
    action: string; expected_version: number; reason: string; iteration_id?: number;
    expected_claim_generation?: number; expected_running_run_ids?: number[]; expected_live_assignment_ids?: number[];
}
