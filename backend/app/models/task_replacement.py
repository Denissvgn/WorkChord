"""An audited disposition that names the one task delivering another task's work instead."""

from datetime import datetime

from sqlalchemy import JSON, CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint, select
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.database import Base
from app.models.task import Task
from app.utils.time import UTCDateTime, utc_now


class TaskReplacement(Base):
    """Link an original task to the one task that delivers its work instead.

    A ``replacement`` disposition names a fresh task that does unattributable work
    again from a clean base: only the replacement can be accepted, and only on its
    own attributable contributions. A ``supersession`` names work that was already
    closed or accepted when the disposition was recorded; it has no base commit and
    need not cite an owner decision. Either way the original keeps its attempts,
    artifacts and history and is never accepted independently.
    """

    __tablename__ = "task_replacements"
    __table_args__ = (
        CheckConstraint("original_task_id <> replacement_task_id", name="ck_task_replacements_distinct"),
        CheckConstraint("disposition IN ('replacement', 'supersession')", name="ck_task_replacements_disposition"),
        CheckConstraint("disposition = 'supersession' OR (base_commit_url IS NOT NULL AND owner_decision IS NOT NULL)",
                        name="ck_task_replacements_replacement_basis"),
        UniqueConstraint("original_task_id", name="uq_task_replacements_original_task_id"),
        UniqueConstraint("replacement_task_id", name="uq_task_replacements_replacement_task_id"),
        Index("ix_task_replacements_project_id", "project_id"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    original_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False)
    replacement_task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False)
    disposition: Mapped[str] = mapped_column(String(16), nullable=False, default="replacement",
                                             server_default="replacement")
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    # Required for a replacement; a supersession may omit both.
    owner_decision: Mapped[str | None] = mapped_column(Text)
    base_commit_url: Mapped[str | None] = mapped_column(String(1000))
    # Original runs whose commits the replacement carries; each stays a contributor.
    carried_run_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    moved_dependencies: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    moved_release_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    original_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    review_policy: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    decided_by_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="SET NULL"))
    decided_by_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))
    decided_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


# Who delivers a withdrawn task's work, read with the task itself. The subqueries use the table, not
# the entity, so the authority scope on task reads does not apply to them a second time.
_replacements = TaskReplacement.__table__
Task.successor_task_id = column_property(
    select(_replacements.c.replacement_task_id).where(_replacements.c.original_task_id == Task.id).scalar_subquery())
Task.successor_kind = column_property(
    select(_replacements.c.disposition).where(_replacements.c.original_task_id == Task.id).scalar_subquery())
