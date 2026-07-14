"""GitHub integration models."""
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


GITHUB_STATUS_AUTOMATION_EVENT_TYPES = (
    "github_pr_opened",
    "github_pr_reopened",
    "github_pr_ready_for_review",
    "github_pr_synchronize",
    "github_pr_closed",
    "github_pr_merged",
)
GITHUB_STATUS_AUTOMATION_FROM_STATUSES = ("planned", "active", "resolved", "closed")
GITHUB_STATUS_AUTOMATION_TARGET_STATUSES = ("active", "resolved", "closed")


class GitHubStatusAutomationRule(Base):
    """Opt-in rule that maps GitHub PR activity to task status changes."""

    __tablename__ = "github_status_automation_rules"
    __table_args__ = (
        CheckConstraint(
            "github_event_type IN ("
            "'github_pr_opened', 'github_pr_reopened', 'github_pr_ready_for_review', "
            "'github_pr_synchronize', 'github_pr_closed', 'github_pr_merged'"
            ")",
            name="ck_github_status_rules_event_type",
        ),
        CheckConstraint(
            "from_status IS NULL OR from_status IN ('planned', 'active', 'resolved', 'closed')",
            name="ck_github_status_rules_from_status",
        ),
        CheckConstraint(
            "target_status IN ('active', 'resolved', 'closed')",
            name="ck_github_status_rules_target_status",
        ),
        Index("ix_github_status_rules_event_enabled", "github_event_type", "enabled"),
        Index("ix_github_status_rules_sort", "sort_order", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    github_event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    from_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_status: Mapped[str] = mapped_column(String(50), nullable=False)
    reason_template: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
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
