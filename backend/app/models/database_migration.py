"""Target-owned state for controlled SQLite-to-PostgreSQL transfers."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import CheckConstraint, Index, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class DatabaseMigrationGate(Base):
    """Fail-closed progress for one catalogued database transfer.

    Rows in this table are operational target state. They are deliberately not
    copied from SQLite. Readiness remains false while any row is not fully
    reconciled, so a partially loaded target cannot accidentally serve traffic.
    """

    __tablename__ = "database_migration_gates"
    __table_args__ = (
        CheckConstraint(
            "status IN ('loading', 'loaded', 'reconciling', "
            "'raw_reconciled', 'reconciled', 'failed')",
            name="ck_database_migration_gates_status",
        ),
        Index("ix_database_migration_gates_status", "status"),
    )

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_manifest_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    source_snapshot_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    target_identity_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    completed_tables: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    failure_code: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    raw_report_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    reconciliation_report_sha256: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )
