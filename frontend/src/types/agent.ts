import type { Task } from './task';

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };
export type JsonObject = { [key: string]: JsonValue };

export type AgentActorRole = 'pm' | 'worker' | 'verifier';
export type AgentAssignmentPurpose = 'execution' | 'verification';
export type AgentAssignmentQueueClass = 'normal' | 'rework' | 'recovery';
export type AgentAssignmentState = 'queued' | 'accepted' | 'fulfilled' | 'cancelled';
export type AgentModelBindingStatus = 'not_selected' | 'current' | 'stale' | 'unresolved';
export type AgentModelTrustState = 'matched' | 'mismatch' | 'unreported' | 'unverifiable';
export type AgentModelMatchBasis = 'configured_alias' | 'catalog_key';

export type ModelReasoningTier = 1 | 2 | 3;
export type ModelContextTier = 'small' | 'medium' | 'large';
export type ModelCostTier = 'low' | 'medium' | 'high';
export type ModelLatencyTier = 'fast' | 'balanced' | 'slow';
export type TaskDifficultyScore = 1 | 2 | 3;
export type TaskSkillLevel = 1 | 2 | 3 | 4 | 5;
export type TaskDifficultyBand = 'routine' | 'standard' | 'advanced';
export type TaskReviewMode = 'none' | 'standard' | 'independent' | 'specialist-independent';

export type AssessmentReasonCode =
    | 'novel-architecture'
    | 'material-ambiguity'
    | 'broad-context'
    | 'security'
    | 'authorization'
    | 'migration'
    | 'data-integrity'
    | 'concurrency'
    | 'production'
    | 'irreversible-change'
    | 'independent-verification'
    | 'specialist-verification';

export type RoutingBlockerCode =
    | 'assignment_purpose_queue_class_incompatible'
    | 'assessment_missing'
    | 'assessment_stale'
    | 'assessment_policy_mismatch'
    | 'assessment_low_confidence'
    | 'task_definition_not_ready'
    | 'task_status_incompatible'
    | 'task_deferred'
    | 'task_composite'
    | 'task_dependency_unresolved'
    | 'actor_disabled'
    | 'actor_role_incompatible'
    | 'actor_scope_missing'
    | 'actor_policy_incompatible'
    | 'actor_topology_incompatible'
    | 'actor_profile_missing'
    | 'capacity_owner_missing'
    | 'capacity_owner_profile_missing'
    | 'actor_capacity_profile_mismatch'
    | 'profile_kind_human'
    | 'profile_kind_unsupported'
    | 'profile_automation_disabled'
    | 'profile_assignment_mode_missing'
    | 'required_skill_missing'
    | 'required_skill_level_insufficient'
    | 'required_skill_blocking_weakness'
    | 'model_binding_missing'
    | 'model_binding_disabled'
    | 'model_binding_stale'
    | 'model_catalog_missing'
    | 'model_catalog_disabled'
    | 'model_reasoning_tier_insufficient'
    | 'model_context_tier_insufficient'
    | 'model_modality_missing'
    | 'model_tool_missing'
    | 'model_data_policy_missing'
    | 'capacity_unavailable'
    | 'workload_limit_exceeded'
    | 'vacation_conflict'
    | 'schedule_missing'
    | 'schedule_conflict'
    | 'queue_limit_exceeded'
    | 'current_work_conflict'
    | 'reviewer_profile_missing'
    | 'reviewer_profile_mismatch'
    | 'verification_actor_not_independent'
    | 'verification_profile_not_independent'
    | 'verification_independence_unverifiable'
    | 'verification_specialist_skill_missing'
    | 'preview_not_found'
    | 'preview_stale'
    | 'preview_expired'
    | 'preview_digest_mismatch'
    | 'no_eligible_candidate';

export interface AgentCommandMetadata {
    idempotencyKey: string;
    rationale: string;
    correlationId: string;
}

export interface AgentActor {
    id: number;
    name: string;
    display_name: string;
    scopes: string[];
    enabled: boolean;
    lifecycle_state?: 'active' | 'onboarding' | 'disabled';
    role: AgentActorRole | string;
    profile_id: number | null;
    work_policy: string;
    max_parallel_work: number;
    queue_revision: number;
    created_at: string;
    last_seen_at: string | null;
}

export type ModelAwareRoutingMode = 'off' | 'shadow' | 'enforced';

export type ModelAwareRoutingTopologyStatus =
    | 'unavailable'
    | 'not_ready'
    | 'ready';

export type ModelAwareRoutingTopologySource =
    | 'unavailable'
    | 'agent-team-master-v1';

export interface ModelAwareRoutingTopologyReadiness {
    schema_version: 'model-aware-routing-topology-readiness-v1';
    status: ModelAwareRoutingTopologyStatus;
    source: ModelAwareRoutingTopologySource;
    topology_id: string | null;
    topology_revision: number | null;
    blocker_codes: string[];
}

export interface ModelAwareRoutingStatus {
    configured_mode: ModelAwareRoutingMode;
    effective_mode: ModelAwareRoutingMode;
    feature_advertised: boolean;
    blocker_codes: string[];
    topology_readiness: ModelAwareRoutingTopologyReadiness;
}

export interface AgentCapabilities {
    server_version: string;
    api_contract: string;
    actor: AgentActor;
    scopes: string[];
    lease_limits: Record<string, number>;
    features: string[];
    model_aware_routing: ModelAwareRoutingStatus;
    recommended_skills: Record<string, string>;
    lifecycle_actions: string[];
    skill_catalog_version: string | null;
    skill_catalog_url: string | null;
    skill_discovery_url: string | null;
}

export interface AgentProfileSkillCatalogItem {
    skill_key: string;
    skill_name: string;
    category: string;
    keywords: string[];
}

export interface AgentActorRosterProfileSkill {
    id: number;
    skill_key: string;
    skill_name: string;
    category: string | null;
    level: number;
    interest: number;
    is_weakness: boolean;
    updated_at: string;
}

export interface AgentActorRosterProfile {
    id: number;
    revision: string;
    display_name: string;
    automation_enabled: boolean;
    profile_kind: string;
    assignment_modes: string[];
    skills: AgentActorRosterProfileSkill[];
    updated_at: string;
}

export interface AgentModelCatalogEntry {
    id: number;
    key: string;
    provider: string;
    configured_model_alias: string;
    reasoning_tier: ModelReasoningTier;
    context_tier: ModelContextTier;
    modality_tags: string[];
    cost_tier: ModelCostTier;
    latency_tier: ModelLatencyTier;
    enabled: boolean;
    revision: number;
    last_verified_at: string | null;
    created_at: string;
    updated_at: string;
}

export interface AgentModelCatalogCreate {
    key: string;
    provider: string;
    configured_model_alias: string;
    reasoning_tier: ModelReasoningTier;
    context_tier: ModelContextTier;
    modality_tags?: string[];
    cost_tier: ModelCostTier;
    latency_tier: ModelLatencyTier;
    enabled?: boolean;
    revision?: 1;
    last_verified_at?: string | null;
}

export interface AgentModelCatalogUpdate {
    expected_revision: number;
    provider?: string;
    configured_model_alias?: string;
    reasoning_tier?: ModelReasoningTier;
    context_tier?: ModelContextTier;
    modality_tags?: string[];
    cost_tier?: ModelCostTier;
    latency_tier?: ModelLatencyTier;
    enabled?: true;
    last_verified_at?: string | null;
    reconcile_live_assignments?: boolean;
}

export interface AgentModelCatalogDisable {
    expected_revision: number;
    reconcile_live_assignments?: boolean;
}

export interface AgentModelBinding {
    id: number;
    actor_id: number;
    model_catalog_id: number;
    is_default: boolean;
    enabled: boolean;
    tool_tags: string[];
    data_policy_tags: string[];
    revision: number;
    model_catalog_key: string | null;
    selectable: boolean;
    model_catalog: AgentModelCatalogEntry | null;
    live_assignment_count: number;
    historical_assignment_count: number;
    run_reference_count: number;
    created_at: string;
    updated_at: string;
}

export interface AgentModelBindingCreate {
    actor_id: number;
    model_catalog_id: number;
    is_default?: boolean;
    enabled?: boolean;
    tool_tags?: string[];
    data_policy_tags?: string[];
    revision?: 1;
}

export interface AgentModelBindingUpdate {
    expected_revision: number;
    is_default?: boolean;
    enabled?: true;
    tool_tags?: string[];
    data_policy_tags?: string[];
    reconcile_live_assignments?: boolean;
}

export interface AgentModelBindingDisable {
    expected_revision: number;
    reconcile_live_assignments?: boolean;
}

export interface AgentModelMutationReceipt<
    TResult extends AgentModelCatalogEntry | AgentModelBinding =
        AgentModelCatalogEntry | AgentModelBinding,
> {
    operation: string;
    actor_id: number;
    target_type: 'model_catalog' | 'model_binding';
    target_id: number;
    idempotency_key: string;
    rationale: string;
    correlation_id: string;
    authoritative_revision: number;
    invalidated_assignment_ids: number[];
    audit_event_ids: number[];
    result: TResult;
}

export interface AgentActorRosterItem extends AgentActor {
    actor_revision: number;
    profile_revision: string | null;
    profile: AgentActorRosterProfile | null;
    eligible_model_bindings: AgentModelBinding[];
    queued_assignments: number;
    accepted_assignments: number;
    running_runs: number;
}

export interface TaskDifficultyAxes {
    reasoning: TaskDifficultyScore;
    ambiguity: TaskDifficultyScore;
    context_breadth: TaskDifficultyScore;
    risk: TaskDifficultyScore;
    verification_burden: TaskDifficultyScore;
}

export interface RequiredModelEnvelope {
    minimum_reasoning_tier: ModelReasoningTier;
    minimum_context_tier: ModelContextTier;
    modality_tags: string[];
    tool_tags: string[];
    data_policy_tags: string[];
}

export interface TaskRoutingAssessmentCommand {
    expected_task_version: number;
    band: TaskDifficultyBand;
    axes: TaskDifficultyAxes;
    required_skill_levels: Record<string, TaskSkillLevel>;
    required_model: RequiredModelEnvelope;
    review_mode: TaskReviewMode;
    confidence: number;
    reason_codes: AssessmentReasonCode[];
    rationale: string;
}

export interface TaskRoutingAssessment {
    id: number;
    task_id: number;
    task_version: number;
    policy_version: 'model-aware-routing-v1';
    band: TaskDifficultyBand;
    axes: TaskDifficultyAxes;
    required_skill_levels: Record<string, number>;
    required_model: RequiredModelEnvelope;
    review_mode: TaskReviewMode;
    confidence: number;
    reason_codes: string[];
    rationale: string;
    assessor: string;
    assessor_actor_id: number | null;
    created_at: string;
    policy_conformant: boolean;
    is_current: boolean;
}

export interface TaskRoutingAssessmentState {
    task_id: number;
    current_task_version: number;
    state: 'none' | 'current' | 'stale';
    assessment: TaskRoutingAssessment | null;
}

export interface TaskRoutingAssessmentHistory {
    task_id: number;
    current_task_version: number;
    assessments: TaskRoutingAssessment[];
    total_count: number;
    omitted_count: number;
}

export interface TaskRoutingAssessmentMutationReceipt {
    operation: 'routing.assessment.create';
    actor_id: number;
    target_type: 'task_routing_assessment';
    target_id: number;
    task_id: number;
    idempotency_key: string;
    rationale: string;
    correlation_id: string;
    authoritative_task_version: number;
    assessment: TaskRoutingAssessment;
    audit_event_ids: number[];
}

export interface AgentRoutingPreviewCreate {
    purpose: AgentAssignmentPurpose;
    assessment_id: number;
    expected_task_version: number;
    reviewer_profile_id?: number | null;
}

export interface AgentRoutingCandidate {
    actor_id: number;
    actor_revision: number;
    actor_queue_revision: number;
    profile_id: number;
    profile_revision: string;
    capacity_owner_id: number | null;
    capacity_owner_profile_id: number | null;
    model_binding_id: number;
    model_binding_revision: number;
    model_catalog_id: number;
    model_catalog_key: string;
    model_catalog_revision: number;
    configured_model_alias: string;
    eligible: true;
    hard_blocker_codes: RoutingBlockerCode[];
    matched_skill_levels: Record<string, TaskSkillLevel>;
    missing_skill_keys: string[];
    blocking_weakness_keys: string[];
    reasoning_tier: ModelReasoningTier;
    context_tier: ModelContextTier;
    modality_tags: string[];
    tool_tags: string[];
    data_policy_tags: string[];
    cost_tier: ModelCostTier;
    latency_tier: ModelLatencyTier;
    available_capacity_days: number;
    committed_effort_days: number;
    workload_ratio: number;
    vacation_conflict: false;
    queued_assignments: number;
    accepted_assignments: number;
    running_runs: number;
    schedule_delay_days: number;
    schedule_eligible: true;
    adequacy_class: number;
    rank: number;
    confidence: number;
    rationale: string;
}

export interface AgentRoutingExclusion {
    actor_id: number;
    actor_revision: number;
    actor_queue_revision: number;
    profile_id: number | null;
    profile_revision: string | null;
    capacity_owner_id: number | null;
    capacity_owner_profile_id: number | null;
    model_binding_id: number | null;
    model_binding_revision: number | null;
    model_catalog_id: number | null;
    model_catalog_key: string | null;
    model_catalog_revision: number | null;
    configured_model_alias: string | null;
    eligible: false;
    hard_blocker_codes: RoutingBlockerCode[];
    matched_skill_levels: Record<string, TaskSkillLevel>;
    missing_skill_keys: string[];
    insufficient_skill_keys: string[];
    blocking_weakness_keys: string[];
    reasoning_tier: ModelReasoningTier | null;
    context_tier: ModelContextTier | null;
    cost_tier: ModelCostTier | null;
    latency_tier: ModelLatencyTier | null;
    missing_modality_tags: string[];
    missing_tool_tags: string[];
    missing_data_policy_tags: string[];
    available_capacity_days: number | null;
    committed_effort_days: number | null;
    workload_ratio: number | null;
    vacation_conflict: boolean | null;
    queued_assignments: number | null;
    accepted_assignments: number | null;
    running_runs: number | null;
    schedule_delay_days: number | null;
    schedule_eligible: boolean | null;
    rationale: string;
}

export interface AgentRoutingPreviewResponse {
    preview_id: string;
    preview_digest: string;
    input_digest: string;
    task_id: number;
    topology_key: string | null;
    topology_revision: number | null;
    purpose: AgentAssignmentPurpose;
    assessment_id: number;
    assessment_task_version: number;
    current_task_version: number;
    policy_version: 'model-aware-routing-v1';
    review_mode: TaskReviewMode;
    reviewer_profile_id: number | null;
    generated_at: string;
    expires_at: string;
    recommended_candidate: AgentRoutingCandidate | null;
    eligible_candidates: AgentRoutingCandidate[];
    exclusions: AgentRoutingExclusion[];
    eligible_candidates_omitted: number;
    exclusions_omitted: number;
    hard_blocker_codes: RoutingBlockerCode[];
}

export interface ModelAwareAgentTaskAssignmentCreate {
    task_id: number;
    actor_id: number;
    expected_task_version: number;
    purpose: AgentAssignmentPurpose;
    assessment_id: number;
    model_binding_id: number;
    model_binding_revision: number;
    routing_preview_id: string;
    routing_preview_digest: string;
    team_member_id?: number | null;
    reviewer_profile_id?: number | null;
    queue_class?: AgentAssignmentQueueClass;
    queue_rank?: number;
    not_before?: string | null;
    reason?: string | null;
}

export interface ModelAwareAgentTaskAssignmentUpdate {
    expected_queue_revision: number;
    assessment_id: number;
    model_binding_id: number;
    model_binding_revision: number;
    routing_preview_id: string;
    routing_preview_digest: string;
    actor_id?: number | null;
    reviewer_profile_id?: number | null;
    queue_rank?: number | null;
    not_before?: string | null;
    state?: 'queued' | 'cancelled' | null;
    reason?: string | null;
}

export interface AgentTaskAssignment {
    id: number;
    task_id: number;
    actor_id: number;
    team_member_id: number | null;
    purpose: AgentAssignmentPurpose | string;
    queue_class: AgentAssignmentQueueClass | string;
    state: AgentAssignmentState | string;
    queue_rank: number;
    not_before: string | null;
    assigned_by_actor_id: number | null;
    reviewer_profile_id: number | null;
    task_version: number;
    model_binding_id: number | null;
    model_binding_revision: number | null;
    model_binding_status: AgentModelBindingStatus;
    model_binding_stale_reasons: string[];
    routing_snapshot: JsonObject;
    reason: string | null;
    created_at: string;
    updated_at: string;
}

export interface AgentAssignmentListParams {
    taskId?: number;
    actorId?: number;
    purpose?: AgentAssignmentPurpose;
    state?: AgentAssignmentState;
    limit?: number;
}

export interface AgentModelBindingListParams {
    actorId?: number;
    includeDisabled?: boolean;
}

export interface AgentRunEvent {
    id: number;
    run_id: number;
    event_type: string;
    message?: string | null;
    payload: JsonObject;
    trace_id?: string | null;
    span_id?: string | null;
    correlation_id?: string | null;
    idempotency_key?: string | null;
    created_at: string;
}

export interface AgentRun {
    id: number;
    task_id?: number | null;
    actor_id: number;
    assignment_id?: number | null;
    claim_generation?: number | null;
    status: 'running' | 'succeeded' | 'failed' | 'canceled' | string;
    trace_id?: string | null;
    model_binding_id?: number | null;
    model_binding_revision?: number | null;
    configured_model_alias?: string | null;
    resolved_model_id?: string | null;
    model_trust_state: AgentModelTrustState;
    model_match_basis?: AgentModelMatchBasis | null;
    model?: string | null;
    tool_name?: string | null;
    metadata: JsonObject;
    artifact_links: string[];
    commit_url?: string | null;
    pr_url?: string | null;
    summary?: string | null;
    error?: string | null;
    started_at: string;
    ended_at?: string | null;
    heartbeat_at?: string | null;
    events?: AgentRunEvent[];
}

export interface AgentPipeline {
    needs_definition: Task[];
    ready_for_agent: Task[];
    definition_ready_unassigned: Task[];
    assigned_waiting: Task[];
    start_ready: Task[];
    executing: Task[];
    verification_required: Task[];
    recovery_required: Task[];
}

export interface TaskTimelineItem {
    item_type: 'task_event' | 'status_log' | 'agent_run' | 'agent_run_event';
    timestamp: string;
    title: string;
    payload: JsonObject;
    actor_type?: string | null;
    actor_id?: number | null;
    trace_id?: string | null;
}

export interface TaskTimelineResponse {
    task_id: number;
    items: TaskTimelineItem[];
}

export type AgentTeamRole = 'pm' | 'worker' | 'verifier';
export type AgentTeamStepState = 'done' | 'warn' | 'blocked' | 'todo';
export type AgentTeamLifecycle =
    | 'desired'
    | 'configured'
    | 'credential_delivered'
    | 'onboarding'
    | 'connected'
    | 'runtime_ready'
    | 'disabled';

export interface AgentTeamSkillPackage {
    name: string;
    version: string;
    sha256: string;
}

export interface AgentTeamMemberSpec {
    actor_key: string;
    actor_name: string;
    display_name: string;
    role: AgentTeamRole;
    scope_preset: 'pm-v1' | 'worker-v1' | 'verifier-v1';
    profile_key: string;
    skill_package: AgentTeamSkillPackage;
    assignment_modes: string[];
    model_binding_keys: string[];
    default_model_binding_key: string;
    runtime_ref: string;
    credential_ref: string;
}

export interface AgentTeamMaster {
    schema_version: 'agent-team-master-v1';
    topology_key: string;
    server_url: string;
    credential_sink_ref: string;
    required_server_features: string[];
    controller: AgentTeamMemberSpec;
    workers: AgentTeamMemberSpec[];
    verifiers: AgentTeamMemberSpec[];
    readiness_policy: {
        minimum_execution_workers: number;
        require_independent_verifier_when_assessed: boolean;
        maximum_runtime_staleness_seconds: number;
    };
}

export interface AgentTeamValidation {
    schema_version: 'agent-team-validation-v1';
    valid: boolean;
    manifest_digest: string;
    normalized_manifest: AgentTeamMaster;
    blocker_codes: string[];
}

export type AgentTeamReconciliationClass =
    | 'create'
    | 'safe_update'
    | 'no_change'
    | 'blocked_conflict'
    | 'requires_replacement'
    | 'propose_disable'
    | 'unmanaged';

export interface AgentTeamPlanAction {
    action_id: string;
    action_digest: string;
    reconciliation_class: AgentTeamReconciliationClass;
    operation: string;
    actor_key: string;
    target_actor_id: number | null;
    expected_object_revision: number | null;
    expected_actor_revision: number | null;
    before: Record<string, JsonValue> | null;
    after: Record<string, JsonValue> | null;
    preconditions: Record<string, JsonValue>;
    blocker_code: string | null;
    requires_explicit_confirmation: boolean;
    authority_change: boolean;
}

export interface AgentTeamPlan {
    schema_version: 'agent-team-reconciliation-plan-v1';
    topology_key: string;
    expected_topology_revision: number;
    manifest_digest: string;
    plan_digest: string;
    actions: AgentTeamPlanAction[];
    blocker_codes: string[];
}

export interface AgentTeamActionReceipt {
    action_id: string;
    action_digest: string;
    reconciliation_class: AgentTeamReconciliationClass;
    operation: string;
    actor_key: string;
    status: 'pending' | 'applied' | 'no_change' | 'blocked';
    target_actor_id: number | null;
    before_revision: number | null;
    after_revision: number | null;
    blocker_code: string | null;
    next_action: string | null;
}

export interface AgentTeamApplyResponse {
    schema_version: 'agent-team-apply-receipt-v1';
    apply_id: string;
    topology_key: string;
    manifest_digest: string;
    plan_digest: string;
    expected_topology_revision: number;
    resulting_topology_revision: number;
    status: 'completed' | 'partial' | 'blocked';
    replayed: boolean;
    receipts: AgentTeamActionReceipt[];
    pending_action_ids: string[];
    blocker_codes: string[];
}

export interface AgentTeamRuntimeHandoff {
    schema_version: 'agent-team-runtime-handoff-v1';
    topology_key: string;
    topology_revision: number;
    actor_key: string;
    actor_id: number;
    role: AgentTeamRole;
    server_url: string;
    required_server_features: string[];
    skill_package: AgentTeamSkillPackage;
    profile_key: string;
    profile_revision: string;
    model_binding_revisions: Record<string, number>;
    supported_assignment_modes: string[];
    startup_instructions: string[];
    credential_ref: string;
}

export interface AgentTeamMemberStatus {
    actor_key: string;
    actor_id: number | null;
    actor_name: string;
    display_name: string;
    role: AgentTeamRole;
    desired: boolean;
    configured: boolean;
    lifecycle_state: AgentTeamLifecycle;
    enabled: boolean;
    profile_key: string;
    profile_revision: string | null;
    binding_revisions: Record<string, number>;
    skill_package: AgentTeamSkillPackage;
    package_acknowledged: boolean;
    credential_delivery_state: 'pending' | 'delivered' | 'uncertain' | 'not_required';
    connection_state: 'unobserved' | 'observed' | 'stale';
    last_seen_at: string | null;
    queued_assignments: number | null;
    accepted_assignments: number | null;
    running_runs: number | null;
    runtime_ready: boolean;
    availability: 'availability_unknown';
    blocker_codes: string[];
    handoff: AgentTeamRuntimeHandoff | null;
}

export interface AgentTeamSetupStep {
    id: 'authority' | 'master' | 'controller' | 'workers' | 'bindings' | 'verifier' | 'review';
    state: AgentTeamStepState;
    blocker_codes: string[];
    next_action: string | null;
}

export interface AgentTeamStatus {
    schema_version: 'agent-team-status-v1';
    topology_key: string | null;
    topology_revision: number | null;
    manifest_digest: string | null;
    topology_state: 'absent' | 'configured' | 'onboarding' | 'runtime_ready' | 'blocked' | 'disabled';
    runtime_ready: boolean;
    availability: 'availability_unknown';
    blocker_codes: string[];
    steps: AgentTeamSetupStep[];
    members: AgentTeamMemberStatus[];
    pending_action_ids: string[];
    can_mutate: boolean;
    next_action: string | null;
}
