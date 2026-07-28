"""Agent integration API schemas."""
import json
import re
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.agent_routing import AgentModelBindingResponse
from app.schemas.project import ProjectHealth, ProjectUpdateEntryResponse
from app.schemas.request_source import RequestSourceLinkWithSourceResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from app.schemas.triage import TriageItemResponse
from app.services.agent_routing_policy import (
    SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS,
    assignment_intent,
    validate_routing_packet_size,
)
from app.utils.url_policy import URLPolicyError, normalize_stored_display_url


MAX_AGENT_JSON_BYTES = 32_768
MAX_AGENT_JSON_FIELDS = 100
MAX_AGENT_TEXT_LENGTH = 8_000
MAX_AGENT_EVENT_MESSAGE_LENGTH = 4_000
MAX_AGENT_ARTIFACT_LINKS = 50
MAX_AGENT_URL_LENGTH = 2_000
ALLOWED_AGENT_NAMESPACED_TASK_EVENTS = {
    "agent.progress",
    "agent.checkpoint",
    "agent.blocker",
}
SUPPORTED_AGENT_SCOPES = frozenset(
    {
        "admin",
        "tasks:read",
        "tasks:write",
        "events:write",
        "runs:write",
        "triage:write",
        "skills:read",
        "planning:read",
        "planning:write",
        "team:read",
        "team:write",
        "assignments:read",
        "assignments:write",
        "work:execute",
        "verification:read",
        "verification:write",
        "reports:write",
        "recovery:read",
        "recovery:write",
    }
)


def _validate_actor_scopes(value: list[str]) -> list[str]:
    if len(value) != len(set(value)):
        raise ValueError("Actor scopes must be unique")
    unknown = sorted(set(value).difference(SUPPORTED_AGENT_SCOPES))
    if unknown:
        raise ValueError("Unsupported actor scopes: " + ", ".join(unknown))
    return value


def _validate_bounded_json(value: dict[str, Any], *, label: str) -> dict[str, Any]:
    """Reject persistence packets that can amplify storage and webhook payloads."""
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    if len(encoded) > MAX_AGENT_JSON_BYTES:
        raise ValueError(f"{label} must not exceed {MAX_AGENT_JSON_BYTES} bytes")
    return value


def _normalize_optional_url(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    try:
        return normalize_stored_display_url(value)
    except URLPolicyError as exc:
        raise ValueError(str(exc)) from exc


def _normalize_url_list(values: list[str]) -> list[str]:
    if len(values) > MAX_AGENT_ARTIFACT_LINKS:
        raise ValueError(
            f"At most {MAX_AGENT_ARTIFACT_LINKS} artifact links are allowed"
        )
    normalized: list[str] = []
    for value in values:
        url = _normalize_optional_url(value)
        if url is not None:
            if len(url) > MAX_AGENT_URL_LENGTH:
                raise ValueError(
                    f"Artifact links must not exceed {MAX_AGENT_URL_LENGTH} characters"
                )
            normalized.append(url)
    return normalized


class AgentActorModelBindingCreate(BaseModel):
    """Secret-free model binding optionally created with a new actor."""

    model_config = ConfigDict(extra="forbid")

    model_catalog_key: str = Field(..., min_length=1, max_length=120)
    is_default: bool = True
    tool_tags: list[str] = Field(default_factory=list, max_length=32)
    data_policy_tags: list[str] = Field(default_factory=list, max_length=32)

    @field_validator("model_catalog_key")
    @classmethod
    def normalize_catalog_key(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(
            r"[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?",
            normalized,
        ):
            raise ValueError("model_catalog_key must be a stable lowercase key")
        return normalized

    @field_validator("tool_tags", "data_policy_tags")
    @classmethod
    def normalize_tags(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            tag = value.strip().lower()
            if not re.fullmatch(
                r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?",
                tag,
            ):
                raise ValueError("Model binding tags must be stable lowercase keys")
            normalized.append(tag)
        if len(normalized) != len(set(normalized)):
            raise ValueError("Model binding tags must be unique")
        return sorted(normalized)


class AgentActorCreate(BaseModel):
    """Request for creating an agent actor."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=255)
    scopes: list[str] = Field(
        default_factory=list, max_length=len(SUPPORTED_AGENT_SCOPES)
    )
    enabled: bool = True
    role: Literal["pm", "worker", "verifier"] = "worker"
    profile_id: Optional[int] = None
    work_policy: Literal["assigned_only"] = "assigned_only"
    max_parallel_work: Literal[1] = 1
    model_binding: Optional[AgentActorModelBindingCreate] = None

    @field_validator("scopes")
    @classmethod
    def validate_scopes(cls, value: list[str]) -> list[str]:
        return _validate_actor_scopes(value)


class AgentActorUpdate(BaseModel):
    """Administrative update for a provisioned actor."""

    display_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    scopes: Optional[list[str]] = Field(
        default=None, max_length=len(SUPPORTED_AGENT_SCOPES)
    )
    enabled: Optional[bool] = None
    role: Optional[Literal["pm", "worker", "verifier"]] = None
    profile_id: Optional[int] = None
    work_policy: Optional[Literal["assigned_only"]] = None
    max_parallel_work: Optional[Literal[1]] = None

    @field_validator("scopes")
    @classmethod
    def validate_scopes(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        return _validate_actor_scopes(value) if value is not None else None

    @model_validator(mode="after")
    def reject_null_for_non_nullable_fields(self):
        """Use [] to clear scopes; explicit null is invalid for required columns."""
        non_nullable = {
            "display_name",
            "scopes",
            "enabled",
            "role",
            "work_policy",
            "max_parallel_work",
        }
        invalid = sorted(
            field_name
            for field_name in self.model_fields_set.intersection(non_nullable)
            if getattr(self, field_name) is None
        )
        if invalid:
            raise ValueError(
                "Actor fields cannot be null: " + ", ".join(invalid)
            )
        return self


class AgentActorResponse(BaseModel):
    """Agent actor response."""
    id: int
    name: str
    display_name: str
    scopes: list[str] = []
    enabled: bool
    lifecycle_state: Literal["active", "onboarding", "disabled"] = "active"
    role: str = "worker"
    profile_id: Optional[int] = None
    work_policy: str = "assigned_only"
    max_parallel_work: int = 1
    queue_revision: int = 1
    created_at: datetime
    last_seen_at: Optional[datetime] = None


class AgentActorCreatedResponse(AgentActorResponse):
    """Agent actor creation response including the one-time API key."""

    api_key: str
    model_binding_id: Optional[int] = None
    model_binding_revision: Optional[int] = None
    model_catalog_key: Optional[str] = None


class AgentTaskCreate(TaskCreate):
    """Agent task creation request."""
    pass


class AgentTaskPatch(TaskUpdate):
    """Agent task patch request with optimistic concurrency."""
    expected_version: int = Field(..., ge=1)
    claim_id: Optional[str] = Field(default=None, min_length=16, max_length=64)
    claim_generation: Optional[int] = Field(default=None, ge=1)


class TaskClaimRequest(BaseModel):
    """Request to claim or renew a task lease."""
    lease_seconds: int = Field(default=3600, ge=60, le=86400)
    trace_id: Optional[str] = Field(default=None, max_length=255)
    span_id: Optional[str] = Field(default=None, max_length=255)
    correlation_id: Optional[str] = Field(default=None, max_length=255)
    claim_id: Optional[str] = Field(default=None, min_length=16, max_length=64)
    claim_generation: Optional[int] = Field(default=None, ge=1)


class TaskClaimResponse(BaseModel):
    """Response for task lease operations."""
    task: TaskResponse
    claim_expires_at: datetime
    claim_id: str
    claim_generation: int


class TaskEventCreate(BaseModel):
    """Request to append a task event."""
    model_config = ConfigDict(extra="forbid")

    event_type: str = Field(..., min_length=1, max_length=100)
    payload: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )
    trace_id: Optional[str] = Field(default=None, max_length=255)
    span_id: Optional[str] = Field(default=None, max_length=255)
    correlation_id: Optional[str] = Field(default=None, max_length=255)
    claim_id: Optional[str] = Field(default=None, min_length=16, max_length=64)
    claim_generation: Optional[int] = Field(default=None, ge=1)

    @field_validator("event_type")
    @classmethod
    def validate_authored_event_type(cls, value: str) -> str:
        """Keep server-owned lifecycle/audit namespaces unavailable to workers."""
        if value not in ALLOWED_AGENT_NAMESPACED_TASK_EVENTS:
            raise ValueError(
                "Agent-authored task events must use agent.progress, "
                "agent.checkpoint, or agent.blocker"
            )
        return value

    @field_validator("payload")
    @classmethod
    def validate_payload_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Task event payload")


class TaskEventResponse(BaseModel):
    """Task event response."""
    id: int
    task_id: Optional[int]
    actor_type: str
    actor_id: Optional[int]
    event_type: str
    payload: dict[str, Any]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    correlation_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    created_at: datetime


class AgentRunCreate(BaseModel):
    """Request to start an agent run."""
    task_id: Optional[int] = None
    assignment_id: Optional[int] = None
    claim_generation: Optional[int] = Field(default=None, ge=1)
    trace_id: Optional[str] = Field(default=None, max_length=255)
    model: Optional[str] = Field(default=None, max_length=255)
    tool_name: Optional[str] = Field(default=None, max_length=255)
    metadata: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )
    artifact_links: list[str] = Field(
        default_factory=list, max_length=MAX_AGENT_ARTIFACT_LINKS
    )
    commit_url: Optional[str] = Field(default=None, max_length=1000)
    pr_url: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("artifact_links")
    @classmethod
    def validate_artifact_links(cls, value: list[str]) -> list[str]:
        return _normalize_url_list(value)

    @field_validator("commit_url", "pr_url")
    @classmethod
    def validate_urls(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Run metadata")


class AgentRunEventCreate(BaseModel):
    """Request to append an agent run event."""
    model_config = ConfigDict(extra="forbid")

    event_type: str = Field(..., min_length=1, max_length=100)
    message: Optional[str] = Field(
        default=None, max_length=MAX_AGENT_EVENT_MESSAGE_LENGTH
    )
    payload: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )
    trace_id: Optional[str] = Field(default=None, max_length=255)
    span_id: Optional[str] = Field(default=None, max_length=255)
    correlation_id: Optional[str] = Field(default=None, max_length=255)
    idempotency_key: Optional[str] = Field(default=None, max_length=255)
    claim_id: Optional[str] = Field(default=None, min_length=16, max_length=64)
    claim_generation: Optional[int] = Field(default=None, ge=1)

    @field_validator("payload")
    @classmethod
    def validate_payload_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Run event payload")


class AgentRunFinish(BaseModel):
    """Request to finish an agent run."""
    status: Literal["succeeded", "failed", "canceled"]
    summary: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    error: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    artifact_links: list[str] = Field(
        default_factory=list, max_length=MAX_AGENT_ARTIFACT_LINKS
    )
    commit_url: Optional[str] = Field(default=None, max_length=1000)
    pr_url: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("artifact_links")
    @classmethod
    def validate_artifact_links(cls, value: list[str]) -> list[str]:
        return _normalize_url_list(value)

    @field_validator("commit_url", "pr_url")
    @classmethod
    def validate_urls(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)


class AgentRunEventResponse(BaseModel):
    """Agent run event response."""
    id: int
    run_id: int
    event_type: str
    message: Optional[str] = None
    payload: dict[str, Any]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    correlation_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    created_at: datetime


class AgentRunResponse(BaseModel):
    """Agent run response."""
    id: int
    task_id: Optional[int]
    actor_id: int
    assignment_id: Optional[int] = None
    claim_generation: Optional[int] = None
    status: str
    trace_id: Optional[str] = None
    model_binding_id: Optional[int] = None
    model_binding_revision: Optional[int] = None
    configured_model_alias: Optional[str] = None
    resolved_model_id: Optional[str] = None
    model_trust_state: Literal[
        "matched",
        "mismatch",
        "unreported",
        "unverifiable",
    ] = Field(
        default="unreported",
        description=(
            "Configured-versus-reported comparison only; matched worker "
            "self-report is not launcher attestation."
        ),
    )
    model_match_basis: Optional[
        Literal["configured_alias", "catalog_key"]
    ] = None
    model: Optional[str] = None
    tool_name: Optional[str] = None
    metadata: dict[str, Any]
    artifact_links: list[str]
    commit_url: Optional[str] = None
    pr_url: Optional[str] = None
    summary: Optional[str] = None
    error: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    heartbeat_at: Optional[datetime] = None


class TaskTimelineItem(BaseModel):
    """Merged timeline item for a task."""
    item_type: Literal["task_event", "status_log", "agent_run", "agent_run_event"]
    timestamp: datetime
    title: str
    payload: dict[str, Any] = Field(default_factory=dict)
    actor_type: Optional[str] = None
    actor_id: Optional[int] = None
    trace_id: Optional[str] = None


class TaskTimelineResponse(BaseModel):
    """Merged task timeline response."""
    task_id: int
    items: list[TaskTimelineItem]


class AgentPipelineResponse(BaseModel):
    """Segmented task list representing the agent supervision pipeline board."""
    needs_definition: list[TaskResponse]
    ready_for_agent: list[TaskResponse]
    definition_ready_unassigned: list[TaskResponse] = []
    assigned_waiting: list[TaskResponse] = []
    start_ready: list[TaskResponse] = []
    executing: list[TaskResponse]
    verification_required: list[TaskResponse]
    recovery_required: list[TaskResponse] = []


class AgentRunDetailResponse(AgentRunResponse):
    """Full detail of an agent run including its list of chronological trace events."""
    events: list[AgentRunEventResponse] = []


# These literals are external assignment-contract vocabularies and intentionally
# remain closed so PM and worker clients fail fast on unsupported state.
AgentAssignmentPurpose = Literal["execution", "verification"]
AgentAssignmentQueueClass = Literal["normal", "rework", "recovery"]
AgentAssignmentState = Literal["queued", "accepted", "fulfilled", "cancelled"]


class AgentTaskAssignmentCreate(BaseModel):
    """PM command to dispatch a task to an exact actor."""
    model_config = ConfigDict(extra="forbid")


    task_id: int
    actor_id: int
    team_member_id: Optional[int] = None
    purpose: AgentAssignmentPurpose = "execution"
    queue_class: AgentAssignmentQueueClass = "normal"
    queue_rank: int = Field(default=1000, ge=0)
    not_before: Optional[datetime] = None
    reviewer_profile_id: Optional[int] = None
    routing_snapshot: dict[str, Any] = Field(
        default_factory=dict,
        max_length=MAX_AGENT_JSON_FIELDS,
    )
    reason: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    expected_task_version: int = Field(..., ge=1)

    @field_validator("routing_snapshot")
    @classmethod
    def validate_routing_snapshot_size(
        cls, value: dict[str, Any]
    ) -> dict[str, Any]:
        """Keep assignment routing evidence bounded in durable queue responses."""
        schema_version = value.get("schema_version")
        if (
            isinstance(schema_version, str)
            and schema_version in SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS
        ):
            raise ValueError(
                "Model-aware routing snapshot schemas are server-owned"
            )
        return validate_routing_packet_size(
            value,
            label="Assignment routing snapshot",
        )

    @model_validator(mode="after")
    def validate_assignment_intent(self) -> "AgentTaskAssignmentCreate":
        """Freeze the four supported purpose/queue-class combinations."""

        assignment_intent(self.purpose, self.queue_class)
        return self


class ModelAwareAgentTaskAssignmentCreate(BaseModel):
    """PM command to dispatch one preview-selected actor/model binding."""

    model_config = ConfigDict(extra="forbid")

    task_id: int = Field(..., ge=1)
    actor_id: int = Field(..., ge=1)
    expected_task_version: int = Field(..., ge=1)
    purpose: AgentAssignmentPurpose
    assessment_id: int = Field(..., ge=1)
    model_binding_id: int = Field(..., ge=1)
    model_binding_revision: int = Field(..., ge=1)
    routing_preview_id: str = Field(..., min_length=1, max_length=255)
    routing_preview_digest: str = Field(..., min_length=64, max_length=64)
    team_member_id: Optional[int] = Field(default=None, ge=1)
    reviewer_profile_id: Optional[int] = Field(default=None, ge=1)
    queue_class: AgentAssignmentQueueClass = "normal"
    queue_rank: int = Field(default=1000, ge=0)
    not_before: Optional[datetime] = None
    reason: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)

    @field_validator("routing_preview_id")
    @classmethod
    def normalize_routing_preview_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("routing_preview_id must not be blank")
        return normalized

    @field_validator("routing_preview_digest")
    @classmethod
    def normalize_routing_preview_digest(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-f0-9]{64}", normalized):
            raise ValueError("routing_preview_digest must be a SHA-256 digest")
        return normalized

    @model_validator(mode="after")
    def validate_assignment_intent(
        self,
    ) -> "ModelAwareAgentTaskAssignmentCreate":
        assignment_intent(self.purpose, self.queue_class)
        return self


class AgentTaskAssignmentUpdate(BaseModel):
    """PM command to reorder, reassign, or cancel a queued assignment."""
    model_config = ConfigDict(extra="forbid")


    actor_id: Optional[int] = None
    queue_rank: Optional[int] = Field(default=None, ge=0)
    not_before: Optional[datetime] = None
    reviewer_profile_id: Optional[int] = None
    state: Optional[Literal["queued", "cancelled"]] = None
    reason: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    expected_queue_revision: int = Field(..., ge=1)


class ModelAwareAgentTaskAssignmentUpdate(BaseModel):
    """PM command to reroute queued work through a fresh routing preview."""

    model_config = ConfigDict(extra="forbid")

    expected_queue_revision: int = Field(..., ge=1)
    assessment_id: int = Field(..., ge=1)
    model_binding_id: int = Field(..., ge=1)
    model_binding_revision: int = Field(..., ge=1)
    routing_preview_id: str = Field(..., min_length=1, max_length=255)
    routing_preview_digest: str = Field(..., min_length=64, max_length=64)
    actor_id: Optional[int] = Field(default=None, ge=1)
    reviewer_profile_id: Optional[int] = Field(default=None, ge=1)
    queue_rank: Optional[int] = Field(default=None, ge=0)
    not_before: Optional[datetime] = None
    state: Optional[Literal["queued", "cancelled"]] = None
    reason: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)

    @field_validator("routing_preview_id")
    @classmethod
    def normalize_routing_preview_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("routing_preview_id must not be blank")
        return normalized

    @field_validator("routing_preview_digest")
    @classmethod
    def normalize_routing_preview_digest(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-f0-9]{64}", normalized):
            raise ValueError("routing_preview_digest must be a SHA-256 digest")
        return normalized


class AgentTaskAssignmentResponse(BaseModel):
    """Durable agent task assignment response."""

    id: int
    task_id: int
    actor_id: int
    team_member_id: Optional[int] = None
    purpose: str
    queue_class: str
    state: str
    queue_rank: int
    not_before: Optional[datetime] = None
    assigned_by_actor_id: Optional[int] = None
    reviewer_profile_id: Optional[int] = None
    task_version: int
    model_binding_id: Optional[int] = None
    model_binding_revision: Optional[int] = None
    model_binding_status: Literal[
        "not_selected",
        "current",
        "stale",
        "unresolved",
    ] = "not_selected"
    model_binding_stale_reasons: list[str] = Field(default_factory=list)
    routing_snapshot: dict[str, Any] = Field(default_factory=dict)
    reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AgentRoutingTopologyReadinessResponse(BaseModel):
    """Bounded server-owned topology readiness exposed to agent clients."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["model-aware-routing-topology-readiness-v1"]
    status: Literal["unavailable", "not_ready", "ready"]
    source: Literal["unavailable", "agent-team-master-v1"]
    topology_id: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,99}$",
    )
    topology_revision: Optional[int] = Field(default=None, ge=1)
    blocker_codes: list[str] = Field(default_factory=list, max_length=20)


class AgentRoutingRolloutStatusResponse(BaseModel):
    """Explicit configured and effective model-aware routing rollout state."""

    model_config = ConfigDict(extra="forbid")

    configured_mode: Literal["off", "shadow", "enforced"]
    effective_mode: Literal["off", "shadow", "enforced"]
    feature_advertised: bool
    blocker_codes: list[str] = Field(default_factory=list, max_length=20)
    topology_readiness: AgentRoutingTopologyReadinessResponse


class AgentCapabilitiesResponse(BaseModel):
    """Authenticated compatibility and actor capability handshake."""

    server_version: str
    api_contract: str
    actor: AgentActorResponse
    scopes: list[str]
    lease_limits: dict[str, int]
    features: list[str]
    recommended_skills: dict[str, str]
    lifecycle_actions: list[str] = Field(default_factory=list)
    skill_catalog_version: Optional[str] = None
    skill_catalog_url: Optional[str] = None
    skill_discovery_url: Optional[str] = None
    model_aware_routing: AgentRoutingRolloutStatusResponse


class AgentActorRosterProfileSkill(BaseModel):
    """Bounded capability evidence attached to one roster profile."""

    id: int
    skill_key: str
    skill_name: str
    category: Optional[str] = None
    level: int
    interest: int
    is_weakness: bool
    updated_at: datetime


class AgentActorRosterProfile(BaseModel):
    """Secret-free profile projection used for exact-actor routing."""

    id: int
    revision: str
    display_name: str
    automation_enabled: bool
    profile_kind: str
    assignment_modes: list[str] = Field(default_factory=list)
    skills: list[AgentActorRosterProfileSkill] = Field(default_factory=list)
    updated_at: datetime


class AgentActorRosterItem(AgentActorResponse):
    """Secret-free actor dispatch roster item."""

    actor_revision: int = 1
    profile_revision: Optional[str] = None
    profile: Optional[AgentActorRosterProfile] = None
    eligible_model_bindings: list[AgentModelBindingResponse] = Field(
        default_factory=list
    )
    queued_assignments: int = 0
    accepted_assignments: int = 0
    running_runs: int = 0


class AgentDependencyContext(BaseModel):
    """Dependency state returned in complete worker context."""

    task_id: int
    title: str
    status: str
    version: int


class AgentTaskContextResponse(BaseModel):
    """Complete task context for an assigned worker."""

    task: TaskResponse
    assignment: Optional[AgentTaskAssignmentResponse] = None
    task_brief: dict[str, str] = Field(default_factory=dict)
    parent_chain: list[dict[str, Any]] = Field(default_factory=list)
    dependencies: list[AgentDependencyContext] = Field(default_factory=list)
    request_sources: list[RequestSourceLinkWithSourceResponse] = Field(
        default_factory=list
    )
    timeline: list[TaskTimelineItem] = Field(default_factory=list)
    definition_ready: bool = False
    start_ready: bool = False
    blocker_codes: list[str] = Field(default_factory=list)


class AgentWorkItem(BaseModel):
    """One ordered assigned-work item."""

    assignment: AgentTaskAssignmentResponse
    task: TaskResponse
    queue_position: int
    selection_key: list[Any] = Field(default_factory=list)
    selection_reason: str
    blocker_codes: list[str] = Field(default_factory=list)
    claim: Optional[dict[str, Any]] = None
    run: Optional[AgentRunResponse] = None


class AgentPaginationMetadata(BaseModel):
    """Opaque snapshot-bound pagination metadata shared by REST and MCP."""

    snapshot_revision: str
    page_size: int = Field(..., ge=1, le=200)
    returned: int = Field(..., ge=0)
    has_more: bool = False
    next_cursor: Optional[str] = None


class AgentCollectionPageMetadata(BaseModel):
    """Per-collection counts for compound assigned-work pages."""

    returned: int = Field(..., ge=0)
    has_more: bool = False


class AgentWorkPaginationMetadata(AgentPaginationMetadata):
    """Pagination metadata for ready and blocked assigned-work collections."""

    queue: AgentCollectionPageMetadata
    blocked_assigned: AgentCollectionPageMetadata


class AgentWorkDecisionResponse(BaseModel):
    """Server-authoritative current/next work decision."""

    actor: AgentActorResponse
    server_time: datetime
    selection_policy: str = "assigned-work/v1"
    queue_revision: int
    pagination: AgentWorkPaginationMetadata
    cursor: Optional[str] = None
    state: Literal["resume", "start_assigned", "wait", "no_work", "attention_required"]
    current: Optional[AgentWorkItem] = None
    next: Optional[AgentWorkItem] = None
    queue: list[AgentWorkItem] = Field(default_factory=list)
    blocked_assigned: list[AgentWorkItem] = Field(default_factory=list)
    recovery_codes: list[str] = Field(default_factory=list)
    next_poll_after: Optional[datetime] = None


class AgentReviewQueueResponse(BaseModel):
    """Paginated verifier queue projection."""

    items: list[AgentWorkItem] = Field(default_factory=list)
    pagination: AgentPaginationMetadata


class AgentWorkBegin(BaseModel):
    """Atomically accept and start a server-selected work assignment."""
    model_config = ConfigDict(extra="forbid")


    assignment_id: int
    queue_revision: int = Field(..., ge=1)
    lease_seconds: int = Field(default=3600, ge=60, le=86400)
    trace_id: Optional[str] = Field(default=None, max_length=255)
    model: Optional[str] = Field(default=None, max_length=255)
    tool_name: Optional[str] = Field(default=None, max_length=255)
    metadata: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Work metadata")


class ModelAwareAgentWorkBegin(BaseModel):
    """Atomically begin only the model binding selected by routing."""

    model_config = ConfigDict(extra="forbid")

    assignment_id: int = Field(..., ge=1)
    queue_revision: int = Field(..., ge=1)
    model_binding_id: int = Field(..., ge=1)
    model_binding_revision: int = Field(..., ge=1)
    resolved_model_id: str = Field(..., min_length=1, max_length=255)
    lease_seconds: int = Field(default=3600, ge=60, le=86400)
    trace_id: Optional[str] = Field(default=None, max_length=255)
    tool_name: Optional[str] = Field(default=None, max_length=255)
    metadata: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )

    @field_validator("resolved_model_id")
    @classmethod
    def normalize_resolved_model_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("resolved_model_id must not be blank")
        return normalized

    @field_validator("metadata")
    @classmethod
    def validate_metadata_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Work metadata")


class AgentWorkBeginResponse(BaseModel):
    """Atomic begin result containing all new authoritative state."""

    assignment: AgentTaskAssignmentResponse
    task: TaskResponse
    run: AgentRunResponse
    claim_id: str
    claim_generation: int
    claim_expires_at: datetime
    queue_revision: int


class AgentWorkRenew(BaseModel):
    """Renew the live fence for one accepted assignment and running run."""
    model_config = ConfigDict(extra="forbid")


    assignment_id: int
    run_id: int
    claim_id: str = Field(..., min_length=16, max_length=64)
    claim_generation: int = Field(..., ge=1)
    expected_task_version: int = Field(..., ge=1)
    lease_seconds: int = Field(default=3600, ge=60, le=86400)


class AgentWorkSubmit(BaseModel):
    """Atomically submit an active assignment for verification."""
    model_config = ConfigDict(extra="forbid")


    assignment_id: int
    run_id: int
    claim_id: str = Field(..., min_length=16, max_length=64)
    claim_generation: int = Field(..., ge=1)
    expected_task_version: int = Field(..., ge=1)
    summary: str = Field(..., min_length=1, max_length=MAX_AGENT_TEXT_LENGTH)
    evidence: dict[str, Any] = Field(
        ..., min_length=1, max_length=MAX_AGENT_JSON_FIELDS
    )
    artifact_links: list[str] = Field(
        default_factory=list, max_length=MAX_AGENT_ARTIFACT_LINKS
    )
    commit_url: Optional[str] = Field(default=None, max_length=1000)
    pr_url: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("artifact_links")
    @classmethod
    def validate_artifact_links(cls, value: list[str]) -> list[str]:
        return _normalize_url_list(value)

    @field_validator("commit_url", "pr_url")
    @classmethod
    def validate_urls(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_url(value)

    @field_validator("evidence")
    @classmethod
    def validate_evidence_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Submission evidence")


class AgentWorkTerminal(BaseModel):
    """Atomically fail or cancel an active assignment."""
    model_config = ConfigDict(extra="forbid")


    assignment_id: int
    run_id: int
    claim_id: str = Field(..., min_length=16, max_length=64)
    claim_generation: int = Field(..., ge=1)
    expected_task_version: int = Field(..., ge=1)
    status: Literal["failed", "canceled"]
    summary: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    error: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    evidence: dict[str, Any] = Field(
        ..., min_length=1, max_length=MAX_AGENT_JSON_FIELDS
    )

    @field_validator("evidence")
    @classmethod
    def validate_evidence_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Failure evidence")


class AgentWorkTerminalResponse(BaseModel):
    """Atomic submit/fail result."""

    assignment: AgentTaskAssignmentResponse
    task: TaskResponse
    run: AgentRunResponse
    recovery_required: bool = False


class AgentReviewVerdict(BaseModel):
    """Verifier-scoped pass or rejection command."""
    model_config = ConfigDict(extra="forbid")


    assignment_id: int
    verdict: Literal["pass", "reject"]
    expected_task_version: int = Field(..., ge=1)
    evidence: dict[str, Any] = Field(..., min_length=1, max_length=100)
    reason: Optional[str] = Field(default=None, max_length=4000)
    rework_actor_id: Optional[int] = None
    rework_queue_rank: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_verification_packet(self):
        """Require bounded evidence and a reason for every rejection."""
        if self.verdict == "reject" and not (self.reason or "").strip():
            raise ValueError("A rejection reason is required")
        _validate_bounded_json(self.evidence, label="Verification evidence")
        return self


class AgentReviewVerdictResponse(BaseModel):
    """Verification result plus optional rework assignment."""

    review_assignment: AgentTaskAssignmentResponse
    task: TaskResponse
    rework_assignment: Optional[AgentTaskAssignmentResponse] = None


class AgentRecoveryRequeue(BaseModel):
    """PM command to replace stale execution ownership with recovery work."""
    model_config = ConfigDict(extra="forbid")


    actor_id: int
    expected_task_version: int = Field(..., ge=1)
    expected_live_assignment_ids: list[int] = Field(..., max_length=20)
    expected_running_run_ids: list[int] = Field(..., max_length=20)
    expected_claim_generation: int = Field(..., ge=0)
    queue_rank: int = Field(default=0, ge=0)
    reason: str = Field(..., min_length=1, max_length=MAX_AGENT_TEXT_LENGTH)


class AgentRecoveryItem(BaseModel):
    """Typed PM recovery diagnosis and optimistic ownership tuple."""

    task: TaskResponse
    recovery_codes: list[str] = Field(..., min_length=1)
    live_assignments: list[AgentTaskAssignmentResponse] = Field(default_factory=list)
    recent_runs: list[AgentRunResponse] = Field(default_factory=list)
    running_run_ids: list[int] = Field(default_factory=list)
    claim_actor_id: Optional[int] = None
    claim_present: bool = False
    claim_generation: int = 0
    claim_expires_at: Optional[datetime] = None
    server_time: datetime


class AgentRecoveryListResponse(BaseModel):
    """Paginated PM recovery projection."""

    items: list[AgentRecoveryItem] = Field(default_factory=list)
    pagination: AgentPaginationMetadata


class AgentRecoveryRequeueResponse(BaseModel):
    """Authoritative result of stale-work reconciliation and requeue."""

    task: TaskResponse
    assignment: AgentTaskAssignmentResponse
    cancelled_assignment_ids: list[int] = Field(default_factory=list)
    cancelled_run_ids: list[int] = Field(default_factory=list)


class AgentProjectUpdateCreate(BaseModel):
    """Agent-authored append-only project status report."""
    model_config = ConfigDict(extra="forbid")


    health: ProjectHealth
    summary: str = Field(..., min_length=1, max_length=MAX_AGENT_TEXT_LENGTH)
    progress_text: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    risks_text: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    decisions_text: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    next_steps_text: Optional[str] = Field(default=None, max_length=MAX_AGENT_TEXT_LENGTH)
    evidence: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )
    correlation_id: Optional[str] = Field(default=None, max_length=255)

    @field_validator("evidence")
    @classmethod
    def validate_evidence_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        if "_agent_audit" in value:
            raise ValueError("Project update evidence key _agent_audit is reserved")
        return _validate_bounded_json(value, label="Project update evidence")


class AgentProjectUpdateResponse(ProjectUpdateEntryResponse):
    """Agent project-update response with attribution and evidence."""


class AgentDiscoveryTriageCreate(BaseModel):
    """Claim-bound report of work discovered outside the assigned scope."""
    model_config = ConfigDict(extra="forbid")

    task_id: int
    assignment_id: int
    run_id: int
    claim_id: str = Field(..., min_length=16, max_length=64)
    claim_generation: int = Field(..., ge=1)
    expected_task_version: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1, max_length=12_000)
    blocking: bool = False
    evidence: dict[str, Any] = Field(
        default_factory=dict, max_length=MAX_AGENT_JSON_FIELDS
    )
    suggested_labels: list[str] = Field(default_factory=list, max_length=50)
    priority_hint: Optional[int] = Field(default=None, ge=1, le=10)

    @field_validator("evidence")
    @classmethod
    def validate_evidence_size(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _validate_bounded_json(value, label="Discovery evidence")


class AgentDiscoveryTriageResponse(TriageItemResponse):
    """Created discovery Triage item with source linkage metadata."""
