"""WorkChord mirror models for autonomous topology and verification state."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    event,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class AgentAutonomyTopology(Base):
    """Applied secret-free topology projection; external receipts stay authoritative."""

    __tablename__ = "agent_autonomy_topologies"
    __table_args__ = (
        CheckConstraint("revision >= 1", name="ck_agent_autonomy_topologies_revision"),
        CheckConstraint(
            "external_journal_revision >= 0",
            name="ck_agent_autonomy_topologies_journal_revision",
        ),
        CheckConstraint(
            "state IN ('planned', 'applying', 'active', 'blocked', 'disabled')",
            name="ck_agent_autonomy_topologies_state",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topology_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    manifest_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    charter_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    primary_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="RESTRICT"),
        nullable=True,
        unique=True,
    )
    state: Mapped[str] = mapped_column(String(30), default="planned", nullable=False)
    external_journal_revision: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    external_journal_head_digest: Mapped[str] = mapped_column(
        String(64), default="0" * 64, nullable=False
    )
    applied_receipt_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    blocker_codes: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    members: Mapped[list["AgentAutonomyTopologyMember"]] = relationship(
        "AgentAutonomyTopologyMember",
        back_populates="topology",
        passive_deletes=True,
    )


class AgentAutonomyTopologyMember(Base):
    """Stable logical-key to actor mapping and non-secret runtime readiness."""

    __tablename__ = "agent_autonomy_topology_members"
    __table_args__ = (
        CheckConstraint("object_revision >= 1", name="ck_agent_autonomy_members_revision"),
        CheckConstraint(
            "lifecycle_state IN ('desired', 'configured', 'credential_delivered', "
            "'onboarding', 'connected', 'runtime_ready', 'disabled')",
            name="ck_agent_autonomy_members_lifecycle",
        ),
        UniqueConstraint(
            "topology_id", "logical_key", name="uq_agent_autonomy_members_logical_key"
        ),
        UniqueConstraint("actor_id", name="uq_agent_autonomy_members_actor"),
        Index(
            "ix_agent_autonomy_members_topology_state",
            "topology_id",
            "lifecycle_state",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topology_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agent_autonomy_topologies.id", ondelete="RESTRICT"),
        nullable=False,
    )
    logical_key: Mapped[str] = mapped_column(String(100), nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="RESTRICT"),
        nullable=True,
    )
    object_revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(40), default="desired", nullable=False)
    desired_member_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    independence_group: Mapped[str] = mapped_column(String(100), nullable=False)
    role_package_checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    external_identity_binding_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    runtime_attestation_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    credential_delivery_receipt_digest: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    runtime_acknowledgement_digest: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    topology: Mapped[AgentAutonomyTopology] = relationship(
        "AgentAutonomyTopology", back_populates="members"
    )


class AgentWorkPackage(Base):
    """Package aggregation is separate from the mutable execution task."""

    __tablename__ = "agent_work_packages"
    __table_args__ = (
        CheckConstraint("package_version >= 1", name="ck_agent_work_packages_version"),
        CheckConstraint(
            "external_journal_revision >= 1",
            name="ck_agent_work_packages_journal_revision",
        ),
        CheckConstraint(
            "state IN ('planned', 'evaluating', 'passed', 'rework_required')",
            name="ck_agent_work_packages_state",
        ),
        UniqueConstraint(
            "package_key", "package_version", name="uq_agent_work_packages_key_version"
        ),
        Index("ix_agent_work_packages_state", "state"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    package_key: Mapped[str] = mapped_column(String(255), nullable=False)
    package_version: Mapped[int] = mapped_column(Integer, nullable=False)
    execution_task_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    predecessor_package_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_work_packages.id", ondelete="RESTRICT"),
        nullable=True,
    )
    state: Mapped[str] = mapped_column(String(30), default="planned", nullable=False)
    artifact_set_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    contract_manifest_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    source_contract_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    creation_request_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    external_journal_revision: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    external_journal_head_digest: Mapped[str] = mapped_column(
        String(64), default="0" * 64, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    requirements: Mapped[list["AgentVerificationRequirement"]] = relationship(
        "AgentVerificationRequirement",
        back_populates="package",
        passive_deletes=True,
    )


class AgentVerificationRequirement(Base):
    """One independently claimable verifier slot with a fenced lifecycle."""

    __tablename__ = "agent_verification_requirements"
    __table_args__ = (
        CheckConstraint(
            "state IN ('planned', 'ready', 'claimed', 'running', 'passed', "
            "'rejected', 'expired')",
            name="ck_agent_verification_requirements_state",
        ),
        CheckConstraint(
            "lease_generation >= 0",
            name="ck_agent_verification_requirements_lease_generation",
        ),
        CheckConstraint(
            "executor_independence_group <> verifier_independence_group",
            name="ck_agent_verification_requirements_independence",
        ),
        CheckConstraint(
            "state NOT IN ('claimed', 'running', 'passed', 'rejected') OR "
            "(assigned_verifier_actor_id IS NOT NULL AND lease_generation >= 1 "
            "AND lease_digest IS NOT NULL AND attempt_start_digest IS NOT NULL "
            "AND lease_expires_at IS NOT NULL)",
            name="ck_agent_verification_requirements_live_fence",
        ),
        UniqueConstraint(
            "package_id", "slot_key", name="uq_agent_verification_requirements_slot"
        ),
        UniqueConstraint(
            "assignment_id", name="uq_agent_verification_requirements_assignment"
        ),
        Index(
            "ix_agent_verification_requirements_actor_state",
            "assigned_verifier_actor_id",
            "state",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    package_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agent_work_packages.id", ondelete="RESTRICT"),
        nullable=False,
    )
    slot_key: Mapped[str] = mapped_column(String(255), nullable=False)
    verifier_logical_key: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(30), default="planned", nullable=False)
    assigned_verifier_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    assignment_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_task_assignments.id", ondelete="RESTRICT"),
        nullable=True,
    )
    criterion_schema: Mapped[str] = mapped_column(String(255), nullable=False)
    artifact_set_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    evaluator_version: Mapped[str] = mapped_column(String(255), nullable=False)
    executor_independence_group: Mapped[str] = mapped_column(String(100), nullable=False)
    verifier_independence_group: Mapped[str] = mapped_column(String(100), nullable=False)
    lease_generation: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lease_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    attempt_start_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    lease_expires_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    heartbeat_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    evidence_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    verdict_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    package: Mapped[AgentWorkPackage] = relationship(
        "AgentWorkPackage", back_populates="requirements"
    )
    events: Mapped[list["AgentVerificationEvent"]] = relationship(
        "AgentVerificationEvent",
        back_populates="requirement",
        passive_deletes=True,
        order_by="AgentVerificationEvent.sequence",
    )


class AgentVerificationEvent(Base):
    """Append-only verifier-slot event projection."""

    __tablename__ = "agent_verification_events"
    __table_args__ = (
        CheckConstraint("sequence >= 1", name="ck_agent_verification_events_sequence"),
        UniqueConstraint(
            "requirement_id", "sequence", name="uq_agent_verification_events_sequence"
        ),
        UniqueConstraint(
            "requirement_id",
            "idempotency_key",
            name="uq_agent_verification_events_idempotency",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    requirement_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agent_verification_requirements.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="RESTRICT"),
        nullable=True,
    )
    lease_generation: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    event_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)

    requirement: Mapped[AgentVerificationRequirement] = relationship(
        "AgentVerificationRequirement", back_populates="events"
    )


class AgentObservationJob(Base):
    """Restart-safe bounded observation/retention job projection."""

    __tablename__ = "agent_observation_jobs"
    __table_args__ = (
        CheckConstraint("job_version >= 1", name="ck_agent_observation_jobs_version"),
        CheckConstraint(
            "state IN ('planned', 'scheduled', 'running', 'met', 'missed', "
            "'failed', 'blocked_external')",
            name="ck_agent_observation_jobs_state",
        ),
        CheckConstraint(
            "minimum_elapsed_seconds >= 1",
            name="ck_agent_observation_jobs_minimum_elapsed",
        ),
        CheckConstraint(
            "starts_at < due_at AND due_at < valid_until",
            name="ck_agent_observation_jobs_time_order",
        ),
        CheckConstraint(
            "external_journal_revision >= 0",
            name="ck_agent_observation_jobs_journal_revision",
        ),
        UniqueConstraint(
            "job_key", "job_version", name="uq_agent_observation_jobs_key_version"
        ),
        Index("ix_agent_observation_jobs_due_state", "due_at", "state"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_key: Mapped[str] = mapped_column(String(255), nullable=False)
    job_version: Mapped[int] = mapped_column(Integer, nullable=False)
    package_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_work_packages.id", ondelete="RESTRICT"),
        nullable=True,
    )
    observation_kind: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(30), default="planned", nullable=False)
    policy_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    trusted_clock_ref_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    minimum_elapsed_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    due_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    valid_until: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    checkpoint_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    credential_lineage_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    result_evidence_digest: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    external_journal_revision: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    external_journal_head_digest: Mapped[str] = mapped_column(
        String(64), default="0" * 64, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )


class ImmutableAutonomyEventError(RuntimeError):
    pass


@event.listens_for(AgentVerificationEvent, "before_update")
@event.listens_for(AgentVerificationEvent, "before_delete")
def _reject_verification_event_mutation(*_args: Any, **_kwargs: Any) -> None:
    raise ImmutableAutonomyEventError(
        "Agent verification events are append-only"
    )
