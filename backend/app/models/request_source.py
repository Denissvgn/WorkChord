"""Request source models for customer and intake traceability."""
from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.task import Task
    from app.models.triage import TriageItem


class RequestSourceType(str, Enum):
    """Supported lightweight request intake source types."""

    CUSTOMER = "customer"
    INTERNAL = "internal"
    SUPPORT = "support"
    EMAIL = "email"
    WEB = "web"
    IMPORT = "import"


class RequestSource(Base):
    """Free-text source record that can be linked to work entities."""

    __tablename__ = "request_sources"
    __table_args__ = (
        CheckConstraint(
            "source_type IN ('customer', 'internal', 'support', 'email', 'web', 'import')",
            name="ck_request_sources_source_type",
        ),
        CheckConstraint(
            "priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)",
            name="ck_request_sources_priority_hint_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, index=True)
    external_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    priority_hint: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
        index=True,
    )

    links: Mapped[list["RequestSourceLink"]] = relationship(
        "RequestSourceLink",
        back_populates="request_source",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="RequestSourceLink.created_at, RequestSourceLink.id",
    )


class RequestSourceLink(Base):
    """Link from one request source to exactly one supported target."""

    __tablename__ = "request_source_links"
    __table_args__ = (
        CheckConstraint(
            "("
            "CASE WHEN triage_item_id IS NOT NULL THEN 1 ELSE 0 END + "
            "CASE WHEN task_id IS NOT NULL THEN 1 ELSE 0 END + "
            "CASE WHEN project_id IS NOT NULL THEN 1 ELSE 0 END"
            ") = 1",
            name="ck_request_source_links_exactly_one_target",
        ),
        UniqueConstraint(
            "request_source_id",
            "triage_item_id",
            name="uq_request_source_links_source_triage_item",
        ),
        UniqueConstraint(
            "request_source_id",
            "task_id",
            name="uq_request_source_links_source_task",
        ),
        UniqueConstraint(
            "request_source_id",
            "project_id",
            name="uq_request_source_links_source_project",
        ),
        Index("ix_request_source_links_request_source_id", "request_source_id"),
        Index("ix_request_source_links_triage_item_id", "triage_item_id"),
        Index("ix_request_source_links_task_id", "task_id"),
        Index("ix_request_source_links_project_id", "project_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    request_source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("request_sources.id", ondelete="CASCADE"),
        nullable=False,
    )
    triage_item_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("triage_items.id", ondelete="CASCADE"),
        nullable=True,
    )
    task_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True,
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
    )

    request_source: Mapped["RequestSource"] = relationship(
        "RequestSource",
        back_populates="links",
    )
    triage_item: Mapped[Optional["TriageItem"]] = relationship(
        "TriageItem",
        back_populates="request_source_links",
    )
    task: Mapped[Optional["Task"]] = relationship(
        "Task",
        back_populates="request_source_links",
    )
    project: Mapped[Optional["Project"]] = relationship(
        "Project",
        back_populates="request_source_links",
    )
