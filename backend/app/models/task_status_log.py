"""Task status log model for audit trail."""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.task import Task


class TaskStatusLog(Base):
    """Audit log for task status changes.

    Records all status transitions with timestamp, reason, and affected tasks.
    """
    __tablename__ = "task_status_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Task reference
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    # Status transition
    from_status: Mapped[str] = mapped_column(String(50), nullable=False)
    to_status: Mapped[str] = mapped_column(String(50), nullable=False)

    # Timestamp
    changed_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )

    # Optional reason for status change
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Who triggered the change
    triggered_by: Mapped[str] = mapped_column(
        String(50), default="user", nullable=False
    )  # "user" | "system"

    # JSON list of affected dependent task IDs (for cascading updates)
    affected_task_ids: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    task: Mapped["Task"] = relationship("Task", back_populates="status_logs")
