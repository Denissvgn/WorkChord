"""Agent integration and tracing models."""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
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
