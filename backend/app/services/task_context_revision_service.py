"""Atomic task-version fencing for relationship-backed execution context."""

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.commands import command_transaction
from app.models.agent import TaskEvent
from app.models.task import Task


class TaskContextVersionConflictError(RuntimeError):
    """Raised when another transaction reserves the task context version first."""


async def lock_task_context(db: AsyncSession, task_id: int) -> bool:
    """Lock the iteration before task context, including SQLite's writer reservation."""
    from app.services.task_service import TaskService
    async with command_transaction(db, commit=False):
        await TaskService(db)._lock_task_scope(task_id)
        return await db.scalar(select(Task.id).where(Task.id == task_id).with_for_update()) is not None


async def reserve_task_context_revision(
    db: AsyncSession,
    task_id: int,
    *,
    context_kind: str,
    action: str,
    details: dict[str, Any] | None = None,
) -> int | None:
    """Reserve the shared task version and append context evidence under its command owner."""
    from app.services.task_service import TaskService, TaskVersionConflictError
    from app.services.snapshot_service import SnapshotService
    async with command_transaction(db, commit=False):
        if not await lock_task_context(db, task_id):
            return None
        task = await db.scalar(select(Task).where(Task.id == task_id).with_for_update().execution_options(populate_existing=True))
        if task is None:
            return None
        await SnapshotService(db).create_snapshot(task.iteration_id, "before_context_change")
        try:
            version = await TaskService(db).reserve_task_version(task, task.version)
        except TaskVersionConflictError as exc:
            raise TaskContextVersionConflictError("Task context version changed while locked") from exc
        db.add(TaskEvent(task_id=task_id, actor_type="system", event_type="task_context_changed", payload=json.dumps({
            "context_kind": context_kind, "action": action, "details": details or {}, "version": version,
        }, ensure_ascii=False, default=str)))
        return version
