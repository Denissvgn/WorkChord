"""Calibration contracts that state when performance history may inform routing."""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

CALIBRATION_CONTRACT_STATES = ("submitted", "approved")
CALIBRATION_CONTRACT_ACTIONS = ("submit", "approve")

# A submitted revision carries no approval; an approved one carries all of it.
APPROVAL_CONSISTENCY = (
    "(state = 'approved' AND approved_at IS NOT NULL AND approved_by_actor_type IS NOT NULL "
    "AND approval_reason IS NOT NULL AND approved_as IS NOT NULL) OR (state = 'submitted' AND approved_at IS NULL "
    "AND approved_by_actor_type IS NULL AND approved_by_actor_id IS NULL AND approval_reason IS NULL "
    "AND approved_as IS NULL)"
)

# Only an approve revision names the declared approver it was approved as.
REVISION_APPROVED_AS = (
    "(action = 'approve' AND approved_as IS NOT NULL) OR (action = 'submit' AND approved_as IS NULL)"
)


class RoutingCalibrationContract(Base):
    """The current revision of one named calibration contract.

    Its terms are complete on every revision. Submitting new terms makes the
    contract ``submitted`` again, so an approval always covers exactly the
    terms the approver read.
    """

    __tablename__ = "routing_calibration_contracts"
    __table_args__ = (
        CheckConstraint("state IN ('submitted', 'approved')", name="ck_routing_calibration_contracts_state"),
        CheckConstraint("revision >= 1", name="ck_routing_calibration_contracts_revision"),
        CheckConstraint("length(trim(key)) > 0", name="ck_routing_calibration_contracts_key_not_blank"),
        CheckConstraint("key = lower(trim(key))", name="ck_routing_calibration_contracts_key_canonical"),
        CheckConstraint("length(terms_digest) = 64", name="ck_routing_calibration_contracts_terms_digest"),
        CheckConstraint(APPROVAL_CONSISTENCY, name="ck_routing_calibration_contracts_approval"),
        UniqueConstraint("key", name="uq_routing_calibration_contracts_key"),
        Index("ix_routing_calibration_contracts_state", "state"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(120), nullable=False)
    schema_version: Mapped[str] = mapped_column(String(60), nullable=False)
    state: Mapped[str] = mapped_column(String(20), default="submitted", nullable=False)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    terms: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    terms_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    submitted_by_actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    submitted_by_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True
    )
    submitted_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    approved_by_actor_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    approved_by_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    approval_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # The declared approver the authenticated principal approved as.
    approved_as: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    revisions: Mapped[list["RoutingCalibrationContractRevision"]] = relationship(
        "RoutingCalibrationContractRevision",
        back_populates="contract",
        order_by="RoutingCalibrationContractRevision.revision",
    )


class RoutingCalibrationContractRevision(Base):
    """The terms and state a contract had after one submit or approve command, and why."""

    __tablename__ = "routing_calibration_contract_revisions"
    __table_args__ = (
        UniqueConstraint(
            "contract_id",
            "revision",
            name="uq_routing_calibration_contract_revisions_revision",
        ),
        CheckConstraint(
            "action IN ('submit', 'approve')",
            name="ck_routing_calibration_contract_revisions_action",
        ),
        CheckConstraint(
            "state IN ('submitted', 'approved')",
            name="ck_routing_calibration_contract_revisions_state",
        ),
        CheckConstraint(
            "length(trim(reason)) > 0",
            name="ck_routing_calibration_contract_revisions_reason_not_blank",
        ),
        CheckConstraint(
            REVISION_APPROVED_AS,
            name="ck_routing_calibration_contract_revisions_approved_as",
        ),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("routing_calibration_contracts.id", ondelete="RESTRICT"),
        nullable=False,
    )
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    terms: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    terms_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    approved_as: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True
    )
    correlation_id: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)

    contract: Mapped[RoutingCalibrationContract] = relationship(
        RoutingCalibrationContract,
        back_populates="revisions",
    )
