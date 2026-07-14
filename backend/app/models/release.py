"""Release model for shipped-work tracking."""
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    and_,
)
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship

from app.database import Base
from app.models.external_link import ExternalLink
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.task import Task


class ReleaseStatus(str, Enum):
    """Release lifecycle independent of task status."""

    PLANNED = "planned"
    BUILDING = "building"
    SHIPPED = "shipped"
    CANCELED = "canceled"


release_tasks = Table(
    "release_tasks",
    Base.metadata,
    Column(
        "release_id",
        Integer,
        ForeignKey("releases.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "task_id",
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column("created_at", UTCDateTime(), default=utc_now, nullable=False),
    Index("ix_release_tasks_task_id", "task_id"),
)


class Release(Base):
    """Lightweight shipping record scoped to one project."""

    __tablename__ = "releases"
    __table_args__ = (
        CheckConstraint(
            "status IN ('planned', 'building', 'shipped', 'canceled')",
            name="ck_releases_status",
        ),
        Index("ix_releases_project_status_date", "project_id", "status", "target_date", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=ReleaseStatus.PLANNED.value,
        nullable=False,
        index=True,
    )
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    shipped_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    environment: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    project: Mapped["Project"] = relationship("Project", back_populates="releases")
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=release_tasks,
        order_by="Task.sort_order, Task.id",
    )
    external_links: Mapped[list["ExternalLink"]] = relationship(
        "ExternalLink",
        primaryjoin=lambda: and_(
            Release.id == foreign(ExternalLink.entity_id),
            ExternalLink.entity_type == "release",
        ),
        order_by="ExternalLink.created_at, ExternalLink.id",
        viewonly=True,
    )

    @property
    def task_ids(self) -> list[int]:
        """Return linked task IDs for response schemas and future service code."""
        return [task.id for task in self.tasks]
