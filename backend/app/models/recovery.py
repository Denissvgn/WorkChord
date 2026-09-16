"""Transactional application recovery points and explicit schedule commitments."""

from datetime import date, datetime

from sqlalchemy import ForeignKey, Integer, JSON, String, Text, UniqueConstraint, CheckConstraint, Date, case, event, select
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class ApplicationSnapshot(Base):
    __tablename__ = "application_snapshots"
    __table_args__ = (UniqueConstraint("iteration_id", "filename", name="uq_application_snapshot_filename"),
        UniqueConstraint("project_id", "filename", name="uq_application_snapshot_project_filename"),
        CheckConstraint("iteration_id IS NOT NULL OR project_id IS NOT NULL", name="ck_application_snapshot_scope"))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iteration_id: Mapped[int | None] = mapped_column(ForeignKey("iterations.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    input_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    provenance: Mapped[str] = mapped_column(String(32), default="command", nullable=False)
    created_by_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, index=True)


class LegacySnapshotImport(Base):
    __tablename__ = "legacy_snapshot_imports"
    checksum: Mapped[str] = mapped_column(String(64), primary_key=True)
    iteration_id: Mapped[int] = mapped_column(ForeignKey("iterations.id", ondelete="CASCADE"), index=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    disposition: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    imported_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class TaskScheduleBaseline(Base):
    __tablename__ = "task_schedule_baselines"
    __table_args__ = (UniqueConstraint("task_id", "revision", name="uq_task_schedule_baseline_revision"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class TaskDeletionFence(Base):
    """Retain the highest deleted task version independently of task lifetime."""
    __tablename__ = "task_deletion_fences"
    __table_args__ = (CheckConstraint("last_version >= 1", name="ck_task_deletion_fence_version"),)
    original_task_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    last_version: Mapped[int] = mapped_column(Integer, nullable=False)


def record_task_deletion_fence(_mapper, connection, task):
    """Join the authorized ORM deletion transaction, including cascaded children."""
    from app.models.task import Task
    if connection.dialect.name == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    else:
        from sqlalchemy.dialects.sqlite import insert
    persisted = connection.scalar(select(Task.__table__.c.version).where(Task.__table__.c.id == task.id))
    version = max(task.version, persisted or task.version)
    table = TaskDeletionFence.__table__
    statement = insert(table).values(original_task_id=task.id, last_version=version)
    statement = statement.on_conflict_do_update(index_elements=[table.c.original_task_id], set_={
        "last_version": case((statement.excluded.last_version > table.c.last_version, statement.excluded.last_version), else_=table.c.last_version),
    })
    connection.execute(statement)


from app.models.task import Task
event.listen(Task, "before_delete", record_task_deletion_fence)
