"""Append-only per-attempt usage report revisions and pricing evidence."""

from datetime import datetime
from sqlalchemy import ForeignKey, Index, Integer, JSON, String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class ExecutionUsageRecord(Base):
    __tablename__ = "execution_usage_records"
    __table_args__ = (
        UniqueConstraint("run_identity", "report_id", name="uq_execution_usage_report"),
        UniqueConstraint("run_identity", "sequence", name="uq_execution_usage_sequence"),
        Index("ix_execution_usage_scope_time", "project_id", "iteration_id", "reported_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int | None] = mapped_column(ForeignKey("agent_runs.id", ondelete="SET NULL"), index=True)
    original_run_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    run_identity: Mapped[str] = mapped_column(String(64), nullable=False)
    original_task_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    iteration_id: Mapped[int | None] = mapped_column(ForeignKey("iterations.id", ondelete="SET NULL"))
    original_project_id: Mapped[int | None] = mapped_column(Integer)
    original_iteration_id: Mapped[int | None] = mapped_column(Integer)
    reporter_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))
    report_id: Mapped[str] = mapped_column(String(128), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    digest: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_digest: Mapped[str | None] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    reported_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


def immutable_usage(*_args):
    raise ValueError("Execution usage and pricing evidence are append-only")


event.listen(ExecutionUsageRecord, "before_update", immutable_usage)
event.listen(ExecutionUsageRecord, "before_delete", immutable_usage)
