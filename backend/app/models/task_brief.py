"""Append-only brief, progress and ordinary review history.

These records describe task collaboration. Autonomous work-package verification
continues to require its own trusted evidence and fenced verifier protocol.
"""

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, JSON, String, Text, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class TaskBriefRevision(Base):
    __tablename__ = "task_brief_revisions"
    __table_args__ = (UniqueConstraint("original_task_id", "revision", name="uq_task_brief_revision"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    original_task_id: Mapped[int] = mapped_column(Integer, index=True)
    revision: Mapped[int] = mapped_column(Integer)
    task_version: Mapped[int] = mapped_column(Integer)
    principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    payload: Mapped[dict] = mapped_column(JSON)
    provenance: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class TaskProgressRecord(Base):
    __tablename__ = "task_progress_records"
    __table_args__ = (UniqueConstraint("original_task_id", "artifact_revision", name="uq_task_progress_revision"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    original_task_id: Mapped[int] = mapped_column(Integer, index=True)
    task_version: Mapped[int] = mapped_column(Integer)
    brief_revision: Mapped[int] = mapped_column(Integer)
    artifact_revision: Mapped[int] = mapped_column(Integer)
    principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class TaskReviewRecord(Base):
    __tablename__ = "task_review_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    original_task_id: Mapped[int] = mapped_column(Integer, index=True)
    task_version: Mapped[int] = mapped_column(Integer)
    brief_revision: Mapped[int] = mapped_column(Integer)
    artifact_revision: Mapped[int] = mapped_column(Integer)
    principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    verdict: Mapped[str] = mapped_column(String(16))
    reason: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


def _immutable_history(*_args):
    raise ValueError("Brief, evidence and verdict history is append-only")


for _model in (TaskBriefRevision, TaskProgressRecord, TaskReviewRecord):
    event.listen(_model, "before_update", _immutable_history)
    event.listen(_model, "before_delete", _immutable_history)
