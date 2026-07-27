"""Agent integration and tracing models."""
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    event,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.project import ProjectUpdateEntry
    from app.models.task import Task
    from app.models.team_member import TeamMember, TeamMemberProfile


class AgentActor(Base):
    """Automated agent identity authorized to operate on tasks."""
    __tablename__ = "agent_actors"
    __table_args__ = (
        CheckConstraint(
            "work_policy = 'assigned_only'",
            name="ck_agent_actors_supported_work_policy",
        ),
        CheckConstraint(
            "max_parallel_work = 1",
            name="ck_agent_actors_supported_parallel_work",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    scopes: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="worker", nullable=False)
    profile_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("team_member_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    work_policy: Mapped[str] = mapped_column(
        String(40), default="assigned_only", nullable=False
    )
    max_parallel_work: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    queue_revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)

    claimed_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="claimed_agent"
    )
    task_events: Mapped[list["TaskEvent"]] = relationship(
        "TaskEvent", back_populates="actor"
    )
    runs: Mapped[list["AgentRun"]] = relationship(
        "AgentRun", back_populates="actor"
    )
    project_updates_authored: Mapped[list["ProjectUpdateEntry"]] = relationship(
        "ProjectUpdateEntry", back_populates="created_by_actor"
    )
    profile: Mapped[Optional["TeamMemberProfile"]] = relationship(
        "TeamMemberProfile", back_populates="agent_actors"
    )
    assignments: Mapped[list["AgentTaskAssignment"]] = relationship(
        "AgentTaskAssignment",
        foreign_keys="AgentTaskAssignment.actor_id",
        back_populates="actor",
    )
    assignments_created: Mapped[list["AgentTaskAssignment"]] = relationship(
        "AgentTaskAssignment",
        foreign_keys="AgentTaskAssignment.assigned_by_actor_id",
        back_populates="assigned_by_actor",
    )
    model_bindings: Mapped[list["AgentModelBinding"]] = relationship(
        "AgentModelBinding",
        back_populates="actor",
        passive_deletes=True,
    )
    routing_assessments_created: Mapped[list["TaskRoutingAssessment"]] = relationship(
        "TaskRoutingAssessment",
        back_populates="assessor_actor",
        passive_deletes=True,
    )


class AgentModelCatalogEntry(Base):
    """Secret-free provider-neutral model capability declaration."""

    __tablename__ = "agent_model_catalog_entries"
    __table_args__ = (
        CheckConstraint(
            "reasoning_tier >= 1 AND reasoning_tier <= 3",
            name="ck_agent_model_catalog_reasoning_tier",
        ),
        CheckConstraint(
            "context_tier IN ('small', 'medium', 'large')",
            name="ck_agent_model_catalog_context_tier",
        ),
        CheckConstraint(
            "cost_tier IN ('low', 'medium', 'high')",
            name="ck_agent_model_catalog_cost_tier",
        ),
        CheckConstraint(
            "latency_tier IN ('fast', 'balanced', 'slow')",
            name="ck_agent_model_catalog_latency_tier",
        ),
        CheckConstraint(
            "revision >= 1",
            name="ck_agent_model_catalog_revision",
        ),
        CheckConstraint(
            "length(trim(key)) > 0",
            name="ck_agent_model_catalog_key_not_blank",
        ),
        CheckConstraint(
            "key = lower(trim(key))",
            name="ck_agent_model_catalog_key_canonical",
        ),
        CheckConstraint(
            "length(trim(provider)) > 0",
            name="ck_agent_model_catalog_provider_not_blank",
        ),
        CheckConstraint(
            "length(trim(configured_model_alias)) > 0",
            name="ck_agent_model_catalog_alias_not_blank",
        ),
        Index("ix_agent_model_catalog_enabled", "enabled"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(120), nullable=False)
    configured_model_alias: Mapped[str] = mapped_column(String(255), nullable=False)
    reasoning_tier: Mapped[int] = mapped_column(Integer, nullable=False)
    context_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    modality_tags: Mapped[list[Any]] = mapped_column(
        JSON, default=lambda: ["text"], nullable=False
    )
    cost_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    latency_tier: Mapped[str] = mapped_column(String(20), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(
        UTCDateTime(), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    bindings: Mapped[list["AgentModelBinding"]] = relationship(
        "AgentModelBinding",
        back_populates="model_catalog",
        passive_deletes=True,
    )


class AgentModelBinding(Base):
    """Versioned runtime capability binding owned by one exact actor."""

    __tablename__ = "agent_model_bindings"
    __table_args__ = (
        CheckConstraint(
            "revision >= 1",
            name="ck_agent_model_bindings_revision",
        ),
        CheckConstraint(
            "(NOT is_default) OR enabled",
            name="ck_agent_model_bindings_default_enabled",
        ),
        UniqueConstraint(
            "actor_id",
            "model_catalog_id",
            name="uq_agent_model_bindings_actor_catalog",
        ),
        Index(
            "ix_agent_model_bindings_actor_enabled",
            "actor_id",
            "enabled",
        ),
        Index(
            "ix_agent_model_bindings_catalog_enabled",
            "model_catalog_id",
            "enabled",
        ),
        Index(
            "uq_agent_model_bindings_default_enabled",
            "actor_id",
            unique=True,
            sqlite_where=text("is_default AND enabled"),
            postgresql_where=text("is_default AND enabled"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="CASCADE"),
        nullable=False,
    )
    model_catalog_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agent_model_catalog_entries.id", ondelete="RESTRICT"),
        nullable=False,
    )
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tool_tags: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    data_policy_tags: Mapped[list[Any]] = mapped_column(
        JSON, default=list, nullable=False
    )
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    actor: Mapped["AgentActor"] = relationship(
        "AgentActor", back_populates="model_bindings"
    )
    model_catalog: Mapped["AgentModelCatalogEntry"] = relationship(
        "AgentModelCatalogEntry", back_populates="bindings"
    )
    assignments: Mapped[list["AgentTaskAssignment"]] = relationship(
        "AgentTaskAssignment",
        back_populates="model_binding",
        passive_deletes=True,
    )
    runs: Mapped[list["AgentRun"]] = relationship(
        "AgentRun",
        back_populates="model_binding",
        passive_deletes=True,
    )

    @property
    def model_catalog_key(self) -> Optional[str]:
        """Expose the stable catalog key without duplicating it in the binding."""

        return self.model_catalog.key if self.model_catalog is not None else None

    @property
    def selectable(self) -> bool:
        """Return whether current metadata permits this binding to be selected."""

        return bool(
            self.enabled
            and self.model_catalog is not None
            and self.model_catalog.enabled
        )


class TaskRoutingAssessment(Base):
    """Append-only routing assessment for one concrete task version."""

    __tablename__ = "task_routing_assessments"
    __table_args__ = (
        CheckConstraint(
            "task_version >= 1",
            name="ck_task_routing_assessments_task_version",
        ),
        CheckConstraint(
            "policy_version = 'model-aware-routing-v1'",
            name="ck_task_routing_assessments_policy_version",
        ),
        CheckConstraint(
            "band IN ('routine', 'standard', 'advanced')",
            name="ck_task_routing_assessments_band",
        ),
        CheckConstraint(
            "reasoning_axis BETWEEN 1 AND 3 "
            "AND ambiguity_axis BETWEEN 1 AND 3 "
            "AND context_breadth_axis BETWEEN 1 AND 3 "
            "AND risk_axis BETWEEN 1 AND 3 "
            "AND verification_burden_axis BETWEEN 1 AND 3",
            name="ck_task_routing_assessments_axes",
        ),
        CheckConstraint(
            "band <> 'routine' OR (reasoning_axis = 1 "
            "AND ambiguity_axis = 1 AND context_breadth_axis = 1 "
            "AND risk_axis = 1 AND verification_burden_axis = 1)",
            name="ck_task_routing_assessments_routine_band",
        ),
        CheckConstraint(
            "band <> 'standard' OR (reasoning_axis < 3 "
            "AND ambiguity_axis < 3 AND context_breadth_axis < 3 "
            "AND risk_axis < 3 AND verification_burden_axis < 3)",
            name="ck_task_routing_assessments_standard_band",
        ),
        CheckConstraint(
            "review_mode IN ('none', 'standard', 'independent', "
            "'specialist-independent')",
            name="ck_task_routing_assessments_review_mode",
        ),
        CheckConstraint(
            "risk_axis < 3 OR review_mode IN "
            "('independent', 'specialist-independent')",
            name="ck_task_routing_assessments_risk_review",
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_task_routing_assessments_confidence",
        ),
        UniqueConstraint(
            "task_id",
            "task_version",
            "policy_version",
            name="uq_task_routing_assessments_task_version_policy",
        ),
        Index(
            "ix_task_routing_assessments_task_version",
            "task_id",
            "task_version",
        ),
        Index(
            "ix_task_routing_assessments_policy_band",
            "policy_version",
            "band",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )
    task_version: Mapped[int] = mapped_column(Integer, nullable=False)
    policy_version: Mapped[str] = mapped_column(
        String(80), default="model-aware-routing-v1", nullable=False
    )
    band: Mapped[str] = mapped_column(String(20), nullable=False)
    reasoning_axis: Mapped[int] = mapped_column(Integer, nullable=False)
    ambiguity_axis: Mapped[int] = mapped_column(Integer, nullable=False)
    context_breadth_axis: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_axis: Mapped[int] = mapped_column(Integer, nullable=False)
    verification_burden_axis: Mapped[int] = mapped_column(Integer, nullable=False)
    required_skill_levels: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    required_model: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    review_mode: Mapped[str] = mapped_column(String(40), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reason_codes: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    assessor: Mapped[str] = mapped_column(String(255), nullable=False)
    assessor_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )

    task: Mapped["Task"] = relationship(
        "Task", back_populates="routing_assessments"
    )
    assessor_actor: Mapped[Optional["AgentActor"]] = relationship(
        "AgentActor", back_populates="routing_assessments_created"
    )

    @property
    def axes(self) -> dict[str, int]:
        """Return the normalized contract shape for the five stored axes."""

        return {
            "reasoning": self.reasoning_axis,
            "ambiguity": self.ambiguity_axis,
            "context_breadth": self.context_breadth_axis,
            "risk": self.risk_axis,
            "verification_burden": self.verification_burden_axis,
        }

    def is_current_for(self, task_version: int) -> bool:
        """Determine staleness without mutable flags or timestamps."""

        return self.task_version == task_version


class ImmutableRoutingAssessmentError(RuntimeError):
    """Raised when application code attempts to mutate append-only evidence."""


@event.listens_for(TaskRoutingAssessment, "before_update")
@event.listens_for(TaskRoutingAssessment, "before_delete")
def _reject_routing_assessment_mutation(*_args: Any, **_kwargs: Any) -> None:
    raise ImmutableRoutingAssessmentError(
        "Task routing assessments are immutable; append a new task-version assessment"
    )


class AgentTaskAssignment(Base):
    """Durable delegation of task execution or verification to one actor."""

    __tablename__ = "agent_task_assignments"
    __table_args__ = (
        CheckConstraint(
            "purpose IN ('execution', 'verification')",
            name="ck_agent_task_assignments_purpose",
        ),
        CheckConstraint(
            "queue_class IN ('normal', 'rework', 'recovery')",
            name="ck_agent_task_assignments_queue_class",
        ),
        CheckConstraint(
            "state IN ('queued', 'accepted', 'fulfilled', 'cancelled')",
            name="ck_agent_task_assignments_state",
        ),
        CheckConstraint(
            "(model_binding_id IS NULL AND model_binding_revision IS NULL) OR "
            "(model_binding_id IS NOT NULL AND model_binding_revision IS NOT NULL "
            "AND model_binding_revision >= 1)",
            name="ck_agent_task_assignments_model_binding_pair",
        ),
        Index(
            "ix_agent_task_assignments_actor_queue",
            "actor_id",
            "purpose",
            "state",
            "queue_rank",
        ),
        Index(
            "ix_agent_task_assignments_task_state",
            "task_id",
            "purpose",
            "state",
        ),
        Index(
            "uq_agent_task_assignments_live_purpose",
            "task_id",
            "purpose",
            unique=True,
            sqlite_where=text("state IN ('queued', 'accepted')"),
            postgresql_where=text("state IN ('queued', 'accepted')"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    actor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agent_actors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    team_member_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("team_members.id", ondelete="SET NULL"), nullable=True
    )
    purpose: Mapped[str] = mapped_column(String(30), default="execution", nullable=False)
    queue_class: Mapped[str] = mapped_column(String(30), default="normal", nullable=False)
    state: Mapped[str] = mapped_column(String(30), default="queued", nullable=False)
    queue_rank: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    not_before: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    assigned_by_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id", ondelete="SET NULL"), nullable=True
    )
    reviewer_profile_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("team_member_profiles.id", ondelete="SET NULL"), nullable=True
    )
    task_version: Mapped[int] = mapped_column(Integer, nullable=False)
    model_binding_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_model_bindings.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    model_binding_revision: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    routing_snapshot: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    task: Mapped["Task"] = relationship("Task", back_populates="agent_assignments")
    actor: Mapped["AgentActor"] = relationship(
        "AgentActor", foreign_keys=[actor_id], back_populates="assignments"
    )
    assigned_by_actor: Mapped[Optional["AgentActor"]] = relationship(
        "AgentActor", foreign_keys=[assigned_by_actor_id], back_populates="assignments_created"
    )
    team_member: Mapped[Optional["TeamMember"]] = relationship("TeamMember")
    reviewer_profile: Mapped[Optional["TeamMemberProfile"]] = relationship(
        "TeamMemberProfile", foreign_keys=[reviewer_profile_id]
    )
    model_binding: Mapped[Optional["AgentModelBinding"]] = relationship(
        "AgentModelBinding", back_populates="assignments"
    )
    runs: Mapped[list["AgentRun"]] = relationship(
        "AgentRun", back_populates="assignment"
    )


class AgentIdempotencyRecord(Base):
    """Replay-safe record for agent and PM mutations."""

    __tablename__ = "agent_idempotency_records"
    __table_args__ = (
        UniqueConstraint(
            "actor_id",
            "operation",
            "target_type",
            "target_id",
            "idempotency_key",
            name="uq_agent_idempotency_operation",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agent_actors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    operation: Mapped[str] = mapped_column(String(100), nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    response_payload: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )


class TaskEvent(Base):
    """Append-only ledger entry for task mutations and agent checkpoints."""
    __tablename__ = "task_events"
    __table_args__ = (
        Index(
            "uq_task_events_agent_idempotency_key",
            "task_id",
            "actor_id",
            "event_type",
            "idempotency_key",
            unique=True,
            sqlite_where=text(
                "idempotency_key IS NOT NULL AND actor_id IS NOT NULL "
                "AND task_id IS NOT NULL"
            ),
            postgresql_where=text(
                "idempotency_key IS NOT NULL AND actor_id IS NOT NULL "
                "AND task_id IS NOT NULL"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_type: Mapped[str] = mapped_column(String(50), default="user", nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    payload: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    span_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )

    task: Mapped[Optional["Task"]] = relationship("Task", back_populates="events")
    actor: Mapped[Optional["AgentActor"]] = relationship(
        "AgentActor", back_populates="task_events"
    )


class AgentRun(Base):
    """Trace record for one automated agent execution."""
    __tablename__ = "agent_runs"
    __table_args__ = (
        CheckConstraint(
            "(model_binding_id IS NULL AND model_binding_revision IS NULL) OR "
            "(model_binding_id IS NOT NULL AND model_binding_revision IS NOT NULL "
            "AND model_binding_revision >= 1)",
            name="ck_agent_runs_model_binding_pair",
        ),
        CheckConstraint(
            "model_trust_state IN "
            "('matched', 'mismatch', 'unreported', 'unverifiable')",
            name="ck_agent_runs_model_trust_state",
        ),
        CheckConstraint(
            "(model_trust_state = 'matched' AND "
            "model_match_basis IS NOT NULL AND "
            "model_match_basis IN ('configured_alias', 'catalog_key')) OR "
            "(model_trust_state <> 'matched' AND model_match_basis IS NULL)",
            name="ck_agent_runs_model_match_basis",
        ),
        Index(
            "uq_agent_runs_running_assignment",
            "assignment_id",
            unique=True,
            sqlite_where=text("assignment_id IS NOT NULL AND status = 'running'"),
            postgresql_where=text("assignment_id IS NOT NULL AND status = 'running'"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True
    )
    actor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=False, index=True
    )
    assignment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_task_assignments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    claim_generation: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="running", nullable=False, index=True)
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    model_binding_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_model_bindings.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    model_binding_revision: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    configured_model_alias: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    resolved_model_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    model_trust_state: Mapped[str] = mapped_column(
        String(30),
        default="unreported",
        server_default="unreported",
        nullable=False,
    )
    model_match_basis: Mapped[Optional[str]] = mapped_column(
        String(40), nullable=True
    )
    model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tool_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    run_metadata: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    artifact_links: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    commit_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    pr_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    started_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    heartbeat_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)

    task: Mapped[Optional["Task"]] = relationship("Task", back_populates="agent_runs")
    actor: Mapped["AgentActor"] = relationship("AgentActor", back_populates="runs")
    assignment: Mapped[Optional["AgentTaskAssignment"]] = relationship(
        "AgentTaskAssignment", back_populates="runs"
    )
    model_binding: Mapped[Optional["AgentModelBinding"]] = relationship(
        "AgentModelBinding", back_populates="runs"
    )
    events: Mapped[list["AgentRunEvent"]] = relationship(
        "AgentRunEvent",
        back_populates="run",
        cascade="all, delete-orphan",
        order_by="AgentRunEvent.created_at"
    )


class AgentRunEvent(Base):
    """Append-only event emitted during an agent run."""
    __tablename__ = "agent_run_events"
    __table_args__ = (
        Index(
            "uq_agent_run_events_run_id_idempotency_key",
            "run_id",
            "idempotency_key",
            unique=True,
            sqlite_where=text("idempotency_key IS NOT NULL"),
            postgresql_where=text("idempotency_key IS NOT NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    span_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )

    run: Mapped["AgentRun"] = relationship("AgentRun", back_populates="events")
