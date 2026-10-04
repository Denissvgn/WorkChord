"""Immutable workflow observations with scope captured at the event boundary."""

from datetime import datetime
import json

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, UniqueConstraint, event, select
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.agent import TaskEvent
from app.models.task import Task
from app.models.task_brief import TaskReviewRecord
from app.utils.time import UTCDateTime, utc_now


class DeliveryObservation(Base):
    """Retain delivery identity and scope independently of later hierarchy edits."""
    __tablename__ = "delivery_observations"
    __table_args__ = (
        UniqueConstraint("original_task_id", "task_version", "kind", name="uq_delivery_observation_fact"),
        CheckConstraint("task_version >= 1", name="ck_delivery_observation_version"),
        Index("ix_delivery_observations_scope_time", "project_id", "iteration_id", "observed_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_task_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    task_version: Mapped[int] = mapped_column(Integer, nullable=False)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    iteration_id: Mapped[int | None] = mapped_column(ForeignKey("iterations.id", ondelete="SET NULL"))
    original_project_id: Mapped[int | None] = mapped_column(Integer)
    original_iteration_id: Mapped[int | None] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)


def _record(connection, row, kind, at, source, *, version=None, structural=False):
    """Join the owning transaction without exposing a client-authored ledger write."""
    if row is None or version is not None and version < 1:
        return
    if not structural and (row["is_summary"] or connection.scalar(select(Task.id).where(Task.parent_id == row["id"]).limit(1)) is not None):
        return
    if connection.dialect.name == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    else:
        from sqlalchemy.dialects.sqlite import insert
    connection.execute(insert(DeliveryObservation.__table__).values(
        original_task_id=row["id"], task_version=row["version"] if version is None else version,
        project_id=row["project_id"], iteration_id=row["iteration_id"],
        original_project_id=row["project_id"], original_iteration_id=row["iteration_id"],
        kind=kind, source=source, observed_at=at,
    ).on_conflict_do_nothing(index_elements=["original_task_id", "task_version", "kind"]))


def _task_row(connection, task_id):
    return connection.execute(select(Task.__table__).where(Task.id == task_id)).mappings().first()


def observe_task_insert(_mapper, connection, task):
    from app.models.recovery import TaskDeletionFence
    row = _task_row(connection, task.id)
    restored = task.baseline_provenance == "restored" or connection.scalar(
        select(TaskDeletionFence.original_task_id).where(TaskDeletionFence.original_task_id == task.id)) is not None
    kind = "restored" if restored else "captured" if task.status == "planned" and task.domain_backfill_version >= 1 else "imported_state"
    _record(connection, row, kind, utc_now(), "database_insert")
    if task.parent_id is not None:
        _record(connection, _task_row(connection, task.parent_id), "structural", utc_now(), "hierarchy", structural=True)


def observe_task_event(_mapper, connection, item):
    if item.task_id is None:
        return
    row = _task_row(connection, item.task_id)
    if row is None:
        return
    kind = {"task_cancel": "canceled", "execution_canceled": "canceled",
            "task_reopen": "reopened", "backlog_snapshot_restored": "restored", "snapshot_task_restored": "restored"}.get(item.event_type)
    if item.event_type == "task_reopen" and row["status"] == "planned":
        kind = "reopened_planned"
    if item.event_type == "status_changed":
        payload = json.loads(item.payload)
        transition = (payload.get("from_status"), payload.get("to_status"))
        if row["status"] != transition[1]:
            return
        kind = {("planned", "active"): "started", ("active", "resolved"): "resolved",
                ("resolved", "active"): "rework_started", ("closed", "active"): "reopened"}.get(transition)
    if kind:
        _record(connection, row, kind, item.created_at, "task_event")


def observe_review(_mapper, connection, review):
    if review.task_id is None:
        return
    row = _task_row(connection, review.task_id)
    if row is None:
        return
    if review.verdict == "accept":
        confirmed = (review.principal_id is not None and row["status"] == "closed"
                     and row["accepted_version"] == row["version"]
                     and review.task_version == row["accepted_version"]
                     and review.brief_revision == row["brief_revision"]
                     and review.artifact_revision == row["artifact_revision"]
                     and row["accepted_by_principal_id"] == review.principal_id)
        kind = "accepted" if confirmed else "acceptance_unknown"
    else:
        kind = "rejected"
    _record(connection, row, kind, review.created_at, "review_record", version=review.task_version)


event.listen(Task, "after_insert", observe_task_insert)
event.listen(TaskEvent, "after_insert", observe_task_event)
event.listen(TaskReviewRecord, "after_insert", observe_review)


def observe_task_update(_mapper, connection, task):
    row = _task_row(connection, task.id)
    if row["is_summary"] or connection.scalar(select(Task.id).where(Task.parent_id == task.id).limit(1)) is not None:
        _record(connection, row, "structural", utc_now(), "hierarchy", structural=True)


def observe_task_delete(_mapper, connection, task):
    _record(connection, _task_row(connection, task.id), "removed", utc_now(), "database_delete")


event.listen(Task, "after_update", observe_task_update)
event.listen(Task, "before_delete", observe_task_delete)


def immutable_observation(*_args):
    raise ValueError("Delivery observations are append-only")


event.listen(DeliveryObservation, "before_update", immutable_observation)
event.listen(DeliveryObservation, "before_delete", immutable_observation)
