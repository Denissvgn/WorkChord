"""A recorded decision that stopped a task, and what must be true before it resumes."""

from datetime import date, datetime

from sqlalchemy import JSON, CheckConstraint, Date, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

POSTPONABLE_STATUSES = ("planned", "active", "resolved")
REACTIVATION_STATUSES = ("planned", "resolved")
REQUIREMENT_KINDS = ("predecessor_accepted", "date", "owner_decision", "linked_resolved")


class TaskPostponement(Base):
    """One postponement of one task, kept after reactivation as its history.

    A task has at most one open postponement: the row whose ``reactivated_at``
    is null. ``from_status`` decides where reactivation returns the task:
    resolved work returns to resolved, planned and active work to planned.
    ``released`` lists the claim, assignments and runs the postponement ended.
    """

    __tablename__ = "task_postponements"
    __table_args__ = (
        CheckConstraint("from_status IN ('planned', 'active', 'resolved')", name="ck_task_postponements_from_status"),
        CheckConstraint(
            "(reactivated_at IS NULL AND reactivated_to_status IS NULL AND reactivation_trigger IS NULL)"
            " OR (reactivated_at IS NOT NULL AND reactivated_to_status IN ('planned', 'resolved')"
            " AND reactivation_trigger IS NOT NULL)",
            name="ck_task_postponements_reactivation",
        ),
        Index("ix_task_postponements_task_id", "task_id"),
        Index(
            "uq_task_postponements_open_task",
            "task_id",
            unique=True,
            sqlite_where=text("reactivated_at IS NULL"),
            postgresql_where=text("reactivated_at IS NULL"),
        ),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    from_status: Mapped[str] = mapped_column(String(16), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    postponed_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    postponed_by_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="SET NULL"))
    postponed_by_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))
    # The task version the postponement produced.
    task_version: Mapped[int] = mapped_column(Integer, nullable=False)
    released: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    reactivated_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    reactivated_to_status: Mapped[str | None] = mapped_column(String(16))
    # What returned the task to work: an explicit command today; met requirements can add another.
    reactivation_trigger: Mapped[str | None] = mapped_column(String(32))
    reactivation_reason: Mapped[str | None] = mapped_column(Text)
    reactivated_by_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="SET NULL"))
    reactivated_by_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))


class TaskReactivationRequirement(Base):
    """One condition a postponement waits for.

    ``predecessor_accepted`` names a task that must be accepted, ``date`` a day in
    the task's working time zone, ``owner_decision`` a decision the owner records,
    and ``linked_resolved`` a task or triage item that must be resolved. A named
    task or triage item that is later deleted leaves the requirement with no
    target, so its history stays readable. ``met_at`` stays null until the
    requirement is evaluated as met.
    """

    __tablename__ = "task_reactivation_requirements"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('predecessor_accepted', 'date', 'owner_decision', 'linked_resolved')",
            name="ck_task_reactivation_requirements_kind",
        ),
        CheckConstraint(
            "(kind = 'date' AND on_date IS NOT NULL) OR (kind <> 'date' AND on_date IS NULL)",
            name="ck_task_reactivation_requirements_date",
        ),
        CheckConstraint(
            "kind <> 'owner_decision' OR description IS NOT NULL",
            name="ck_task_reactivation_requirements_decision",
        ),
        CheckConstraint(
            "(target_task_id IS NULL OR kind IN ('predecessor_accepted', 'linked_resolved'))"
            " AND (target_triage_item_id IS NULL OR kind = 'linked_resolved')"
            " AND (target_task_id IS NULL OR target_triage_item_id IS NULL)",
            name="ck_task_reactivation_requirements_target",
        ),
        Index("ix_task_reactivation_requirements_postponement_id", "postponement_id"),
        Index("ix_task_reactivation_requirements_task_id", "task_id"),
        Index("ix_task_reactivation_requirements_target_task_id", "target_task_id"),
        Index("ix_task_reactivation_requirements_target_triage_item_id", "target_triage_item_id"),
        {"sqlite_autoincrement": True},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    postponement_id: Mapped[int] = mapped_column(ForeignKey("task_postponements.id", ondelete="CASCADE"), nullable=False)
    # The postponed task, kept beside the postponement for scoped reads.
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    target_task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"))
    target_triage_item_id: Mapped[int | None] = mapped_column(ForeignKey("triage_items.id", ondelete="SET NULL"))
    on_date: Mapped[date | None] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(Text)
    met_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
