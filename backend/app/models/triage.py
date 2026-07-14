"""Triage item model."""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, CheckConstraint, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.iteration import Iteration
    from app.models.project import Project
    from app.models.request_source import RequestSourceLink
    from app.models.task import Task
    from app.models.team_member import TeamMember


class TriageItemStatus(str, Enum):
    """Triage item lifecycle status."""
    NEW = "new"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    DUPLICATE = "duplicate"
    SNOOZED = "snoozed"
    CONVERTED = "converted"


class TriageItem(Base):
    """Raw inbound work item before it becomes scheduled task work."""
    __tablename__ = "triage_items"
    __table_args__ = (
        CheckConstraint(
            "duplicate_of_id IS NULL OR duplicate_task_id IS NULL",
            name="ck_triage_items_one_duplicate_target",
        ),
        CheckConstraint(
            "priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)",
            name="ck_triage_items_priority_hint_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    external_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    status: Mapped[str] = mapped_column(
        String(50), default=TriageItemStatus.NEW.value, nullable=False, index=True
    )
    priority_hint: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    assignee_hint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    labels: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    snoozed_until: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True
    )

    project_hint_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True
    )
    iteration_hint_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("iterations.id", ondelete="SET NULL"), nullable=True, index=True
    )
    duplicate_of_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("triage_items.id", ondelete="SET NULL"), nullable=True, index=True
    )
    duplicate_task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True
    )
    converted_task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True
    )

    project_hint: Mapped[Optional["Project"]] = relationship(
        "Project", foreign_keys=[project_hint_id]
    )
    iteration_hint: Mapped[Optional["Iteration"]] = relationship(
        "Iteration", foreign_keys=[iteration_hint_id]
    )
    duplicate_of: Mapped[Optional["TriageItem"]] = relationship(
        "TriageItem",
        remote_side=[id],
        foreign_keys=[duplicate_of_id],
        back_populates="duplicate_items",
    )
    duplicate_items: Mapped[list["TriageItem"]] = relationship(
        "TriageItem",
        foreign_keys=[duplicate_of_id],
        back_populates="duplicate_of",
    )
    duplicate_task: Mapped[Optional["Task"]] = relationship(
        "Task", foreign_keys=[duplicate_task_id]
    )
    converted_task: Mapped[Optional["Task"]] = relationship(
        "Task", foreign_keys=[converted_task_id]
    )
    request_source_links: Mapped[list["RequestSourceLink"]] = relationship(
        "RequestSourceLink",
        back_populates="triage_item",
        passive_deletes=True,
        order_by="RequestSourceLink.created_at, RequestSourceLink.id",
    )
    classification_suggestions: Mapped[list["TriageClassificationSuggestion"]] = relationship(
        "TriageClassificationSuggestion",
        back_populates="triage_item",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by=(
            "TriageClassificationSuggestion.created_at.desc(), "
            "TriageClassificationSuggestion.id.desc()"
        ),
    )

    @property
    def request_count(self) -> int:
        """Return loaded direct request-source link count without triggering IO."""
        from sqlalchemy.orm import attributes

        state = attributes.instance_state(self)
        return len(state.dict.get("request_source_links", []))


class TriageClassificationSuggestion(Base):
    """Stored advisory AI classification for a triage item."""
    __tablename__ = "triage_classification_suggestions"
    __table_args__ = (
        CheckConstraint(
            "suggested_priority IS NULL OR "
            "(suggested_priority >= 1 AND suggested_priority <= 10)",
            name="ck_triage_classification_suggestions_priority_range",
        ),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_triage_classification_suggestions_confidence_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    triage_item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("triage_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    suggested_type_label_slug: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    suggested_area_label_slug: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    suggested_priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    suggested_label_slugs: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    unmatched_label_text: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    suggested_assignee_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("team_members.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    suggested_assignee_hint: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    suggested_project_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    duplicate_candidates: Mapped[list[dict]] = mapped_column(
        JSON, default=list, nullable=False
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_fallback: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    raw_response_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )

    triage_item: Mapped["TriageItem"] = relationship(
        "TriageItem", back_populates="classification_suggestions"
    )
    suggested_assignee: Mapped[Optional["TeamMember"]] = relationship("TeamMember")
    suggested_project: Mapped[Optional["Project"]] = relationship("Project")

    @property
    def language(self) -> Optional[str]:
        """Return the stored AI output language when available."""
        value = self.raw_response_json.get("_language") if isinstance(self.raw_response_json, dict) else None
        return str(value) if value in {"en", "ru"} else None
