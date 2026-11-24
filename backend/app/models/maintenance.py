"""Coordinated control-plane maintenance windows and their attributable receipts."""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class MaintenanceWindow(Base):
    """One bounded deployment window an operator announces, begins, and closes.

    ``active_slot`` is 1 only while the window is announced or in progress, so a
    unique constraint allows at most one open window on every database.
    """

    __tablename__ = "maintenance_windows"
    __table_args__ = (
        CheckConstraint(
            "state IN ('announced', 'in_progress', 'completed', 'canceled')",
            name="ck_maintenance_windows_state",
        ),
        CheckConstraint(
            "(state IN ('announced', 'in_progress') AND active_slot = 1)"
            " OR (state IN ('completed', 'canceled') AND active_slot IS NULL)",
            name="ck_maintenance_windows_active_slot",
        ),
        CheckConstraint(
            "outcome IS NULL OR outcome IN ('completed', 'rolled_back', 'canceled')",
            name="ck_maintenance_windows_outcome",
        ),
        CheckConstraint("planned_end_at > planned_start_at", name="ck_maintenance_windows_bounds"),
        CheckConstraint(
            "max_outage_seconds >= 1 AND expiry_margin_seconds >= 60",
            name="ck_maintenance_windows_margins",
        ),
        UniqueConstraint("active_slot", name="uq_maintenance_windows_active_slot"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    state: Mapped[str] = mapped_column(String(20), nullable=False, default="announced")
    active_slot: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)
    release_label: Mapped[str] = mapped_column(String(120), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    planned_start_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    planned_end_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    max_outage_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_margin_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    announced_by_principal_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("principals.id", ondelete="SET NULL"), nullable=True
    )
    announced_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)
    started_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    outcome: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    closing_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    protected_claims: Mapped[Optional[list[Any]]] = mapped_column(JSON(none_as_null=True), nullable=True)
    resumption: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON(none_as_null=True), nullable=True)


class MaintenanceWindowReceipt(Base):
    """A run owner's acknowledgement of a window or a PM's notice of it.

    ``receipt_key`` names the claim generation (owner) or the PM, so a repeated
    acknowledgement returns the original receipt instead of adding another.
    """

    __tablename__ = "maintenance_window_receipts"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('owner_acknowledgement', 'pm_notice')",
            name="ck_maintenance_window_receipts_kind",
        ),
        CheckConstraint(
            "source IN ('agent', 'operator')",
            name="ck_maintenance_window_receipts_source",
        ),
        CheckConstraint(
            "kind = 'pm_notice' OR source = 'agent'",
            name="ck_maintenance_window_receipts_owner_consent",
        ),
        UniqueConstraint("window_id", "receipt_key", name="uq_maintenance_window_receipts_key"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    window_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("maintenance_windows.id", ondelete="CASCADE"), nullable=False, index=True
    )
    kind: Mapped[str] = mapped_column(String(30), nullable=False)
    receipt_key: Mapped[str] = mapped_column(String(120), nullable=False)
    actor_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("agent_actors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(20), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    run_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    assignment_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    claim_generation: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    claim_expires_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    channel: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    reference: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    recorded_by_principal_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("principals.id", ondelete="SET NULL"), nullable=True
    )
    recorded_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)
