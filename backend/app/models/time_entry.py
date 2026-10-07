"""Private explicit work records and retained corrections, independent of task state."""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, Index, Integer, String, Text, UniqueConstraint, event, inspect
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class TimeEntry(Base):
    __tablename__ = "time_entries"
    __table_args__ = (
        CheckConstraint("minutes >= 1 AND minutes <= 1440", name="ck_time_entry_minutes"),
        CheckConstraint("version >= 1", name="ck_time_entry_version"),
        UniqueConstraint("principal_id", "request_id", name="uq_time_entry_request"),
        Index("ix_time_entry_author_date", "principal_id", "work_date"),
        Index("ix_time_entry_project_date", "project_id", "work_date"),
        {"sqlite_autoincrement": True},
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Stable recording-scope IDs intentionally survive task/project/account deletion.
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    task_id: Mapped[int | None] = mapped_column(Integer)
    principal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    task_title: Mapped[str | None] = mapped_column(String(500))
    request_id: Mapped[str] = mapped_column(String(36), nullable=False)
    creation_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False, default="")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    voided: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)


class TimeEntryRevision(Base):
    __tablename__ = "time_entry_revisions"
    __table_args__ = (
        UniqueConstraint("entry_id", "version", name="uq_time_entry_revision"),
        CheckConstraint("minutes >= 1 AND minutes <= 1440", name="ck_time_revision_minutes"),
        CheckConstraint("version >= 1", name="ck_time_revision_version"),
        Index("ix_time_revision_entry", "entry_id", "version"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(Integer, nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    principal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    work_date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    voided: Mapped[bool] = mapped_column(nullable=False)
    reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)


@event.listens_for(Session, "before_flush")
def retain_time_entry_history(session, _context, _instances):
    for obj in list(session.dirty) + list(session.deleted):
        if isinstance(obj, TimeEntryRevision) and (obj in session.deleted or session.is_modified(obj)):
            raise ValueError("Time-entry correction history is append-only")
        if isinstance(obj, TimeEntry):
            if obj in session.deleted:
                raise ValueError("Void time entries instead of deleting retained records")
            immutable = {"project_id", "task_id", "principal_id", "task_title", "request_id", "creation_digest", "created_at"}
            if any(inspect(obj).attrs[name].history.has_changes() for name in immutable):
                raise ValueError("Time-entry recording scope and authorship are immutable")
    authorized = session.info.get("time_entry_commands", set())
    for obj in list(session.new) + list(session.dirty):
        if isinstance(obj, (TimeEntry, TimeEntryRevision)) and (obj in session.new or session.is_modified(obj)) and id(obj) not in authorized:
            raise ValueError("Use the versioned time-entry commands")


@event.listens_for(Session, "do_orm_execute")
def reject_time_history_rewrites(state):
    name = getattr(getattr(state.statement, "table", None), "name", None)
    if name == "time_entry_revisions" and (state.is_update or state.is_delete):
        raise ValueError("Time-entry correction history is append-only")
    if name == "time_entries" and (state.is_update or state.is_delete):
        raise ValueError("Use the versioned time-entry commands")
