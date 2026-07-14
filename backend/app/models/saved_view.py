"""Saved view model for reusable list and dashboard filters."""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.user_session import UserSession


class SavedViewType(str, Enum):
    """Surface that a saved view applies to."""
    TASKS = "tasks"
    PROJECTS = "projects"
    TRIAGE = "triage"


class SavedViewScope(str, Enum):
    """Visibility scope for a saved view."""
    PERSONAL = "personal"
    SHARED = "shared"
    SYSTEM = "system"


class SavedView(Base):
    """Persisted filter, sort, and column configuration for reusable views."""
    __tablename__ = "saved_views"
    __table_args__ = (
        CheckConstraint(
            "view_type IN ('tasks', 'projects', 'triage')",
            name="ck_saved_views_view_type",
        ),
        CheckConstraint(
            "scope IN ('personal', 'shared', 'system')",
            name="ck_saved_views_scope",
        ),
        CheckConstraint(
            "schema_version >= 1",
            name="ck_saved_views_schema_version_min",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    seed_key: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, unique=True, index=True
    )
    view_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    filters_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    sort_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    columns_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_by_session_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("user_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True
    )

    created_by_session: Mapped[Optional["UserSession"]] = relationship(
        "UserSession",
        back_populates="saved_views",
    )
