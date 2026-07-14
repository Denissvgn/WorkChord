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
    id: number;
    iteration_id: number;
    project_id?: number | null;
    milestone_id?: number | null;
    parent_id?: number | null;
    title: string;
    description?: string;
    priority: number;
    effort_days: number;
    effort_hours: number;
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
    parent_id?: number | null;
    title: string;
    description?: string;
    priority: number;
    effort_days: number;
    effort_hours?: number;
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
    tasks: TaskBatchUpdateItem[];
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
