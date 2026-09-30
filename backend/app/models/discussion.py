"""Attributable discussion, personal subscriptions and durable inbox receipts."""

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, event, inspect
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class TaskComment(Base):
    __tablename__ = "task_comments"
    __table_args__ = (CheckConstraint("version >= 1", name="ck_task_comment_version"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    original_task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    body: Mapped[str] = mapped_column(Text, nullable=False)
    mentions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now, onupdate=utc_now)


class TaskCommentRevision(Base):
    __tablename__ = "task_comment_revisions"
    __table_args__ = (UniqueConstraint("comment_id", "version", name="uq_task_comment_revision"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("task_comments.id", ondelete="RESTRICT"), index=True)
    original_task_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    mentions: Mapped[list] = mapped_column(JSON, nullable=False)
    deleted: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)


class TaskSubscription(Base):
    __tablename__ = "task_subscriptions"
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), primary_key=True)
    enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    events: Mapped[list] = mapped_column(JSON, nullable=False, default=lambda: ["discussion", "mention", "review", "block"])
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class InboxNotification(Base):
    __tablename__ = "inbox_notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), index=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey("outbound_webhook_deliveries.id", ondelete="RESTRICT"), unique=True)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    read: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)


@event.listens_for(Session, "do_orm_execute")
def prevent_comment_history_rewrite(state):
    if (state.is_update or state.is_delete) and getattr(getattr(state.statement, "table", None), "name", None) == "task_comment_revisions":
        raise ValueError("Comment history is append-only")


@event.listens_for(Session, "before_flush")
def protect_discussion_history(session, _flush_context, _instances):
    for obj in list(session.dirty) + list(session.deleted):
        if isinstance(obj, TaskCommentRevision) and (obj in session.deleted or session.is_modified(obj)):
            raise ValueError("Comment history is append-only")
    if session.info.get("command") is None:
        return
    from app.models.task import Task
    for obj in session.dirty:
        if not isinstance(obj, Task) or not obj.id:
            continue
        changed = {attribute.key for attribute in inspect(obj).attrs if attribute.history.has_changes()}
        kind = "review" if "status" in changed and obj.status in {"resolved", "closed"} else "block" if "blocked_reason" in changed else None
        if kind:
            session.info.setdefault("discussion_events", set()).add((obj.id, obj.version, kind))
