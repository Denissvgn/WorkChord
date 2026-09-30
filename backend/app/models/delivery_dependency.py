"""Delivery prerequisites are separate from iteration-local scheduling edges."""

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint, event, inspect
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base


class DeliveryDependency(Base):
    __tablename__ = "delivery_dependencies"
    __table_args__ = (
        CheckConstraint("(prerequisite_task_id IS NULL) <> (prerequisite_milestone_id IS NULL)", name="ck_delivery_dependency_target"),
        CheckConstraint("task_id <> prerequisite_task_id", name="ck_delivery_dependency_self"),
        UniqueConstraint("task_id", "prerequisite_task_id", name="uq_delivery_task_target"),
        UniqueConstraint("task_id", "prerequisite_milestone_id", name="uq_delivery_milestone_target"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    prerequisite_task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="RESTRICT"), index=True)
    prerequisite_milestone_id: Mapped[int | None] = mapped_column(ForeignKey("project_milestones.id", ondelete="RESTRICT"), index=True)


@event.listens_for(Session, "before_flush")
def track_delivery_changes(session, _flush_context, _instances):
    """Collect changes for transactional downstream invalidation without rewriting history."""
    if session.info.get("command") is None or session.info.get("delivery_reconciling"):
        return
    from app.models.task import Task, TaskDependency
    from app.models.project import ProjectMilestone
    for obj in list(session.new) + list(session.dirty) + list(session.deleted):
        if isinstance(obj, Task):
            changed = {attr.key for attr in inspect(obj).attrs if attr.history.has_changes()}
            if obj.id and changed.intersection({"status", "accepted_at", "accepted_version", "canceled_at",
                "project_id", "milestone_id", "parent_id", "brief_revision", "context_revision", "artifact_revision"}):
                session.info.setdefault("delivery_changed_nodes", set()).add(("task", obj.id))
            if obj not in session.new and "project_id" in changed:
                session.info.setdefault("delivery_scope_changed", set()).add(obj.id)
            if changed.intersection({"parent_id", "milestone_id"}):
                session.info["delivery_graph_changed"] = True
        elif isinstance(obj, ProjectMilestone) and obj.id:
            session.info.setdefault("delivery_changed_nodes", set()).add(("milestone", obj.id))
        elif isinstance(obj, (TaskDependency, DeliveryDependency)):
            session.info["delivery_graph_changed"] = True
            if obj.task_id:
                session.info.setdefault("delivery_changed_nodes", set()).add(("task", obj.task_id))
