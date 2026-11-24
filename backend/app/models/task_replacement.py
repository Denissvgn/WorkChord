"""An audited disposition that replaces unattributable work with a separate clean task."""

from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class TaskReplacement(Base):
    """Link an original task to the one task that delivers its work instead.

    The original keeps its attempts, artifacts and unknown attribution. Only the
    replacement can be accepted, and only on its own attributable contributions.
    """

    __tablename__ = "task_replacements"
    __table_args__ = (
        CheckConstraint("original_task_id <> replacement_task_id", name="ck_task_replacements_distinct"),
        UniqueConstraint("original_task_id", name="uq_task_replacements_original_task_id"),
        UniqueConstraint("replacement_task_id", name="uq_task_replacements_replacement_task_id"),
        Index("ix_task_replacements_project_id", "project_id"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    original_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False)
    replacement_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    owner_decision: Mapped[str] = mapped_column(Text, nullable=False)
    base_commit_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    # Original runs whose commits the replacement carries; each stays a contributor.
    carried_run_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    moved_dependencies: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    moved_release_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    original_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    review_policy: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    decided_by_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="SET NULL"))
    decided_by_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))
    decided_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
