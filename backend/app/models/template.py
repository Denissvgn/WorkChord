"""Reusable work template model."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Boolean, CheckConstraint, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class TemplateType(str, Enum):
    """Template target type."""
    TASK = "task"
    PROJECT = "project"
    TRIAGE = "triage"


class WorkTemplate(Base):
    """Reusable defaults for creating tasks, projects, or triage items."""
    __tablename__ = "work_templates"
    __table_args__ = (
        CheckConstraint(
            "template_type IN ('task', 'project', 'triage')",
            name="ck_work_templates_template_type",
        ),
        CheckConstraint(
            "default_priority IS NULL OR (default_priority >= 1 AND default_priority <= 10)",
            name="ck_work_templates_default_priority_range",
        ),
        CheckConstraint(
            "default_effort_days IS NULL OR default_effort_days >= 0.1",
            name="ck_work_templates_default_effort_days_min",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    seed_key: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, unique=True, index=True
    )
    template_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    default_title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    default_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_priority: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    default_effort_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    default_labels: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    default_checklist: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    default_payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True
    )
