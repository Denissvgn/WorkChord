"""Atomic task-version fencing for relationship-backed execution context."""

import json
from typing import Any

from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import attributes

from app.models.agent import TaskEvent
from app.models.task import Task


class TaskContextVersionConflictError(RuntimeError):
    """Raised when another transaction reserves the task context version first."""


async def lock_task_context(db: AsyncSession, task_id: int) -> bool:
    """Serialize one task-context mutation without changing its version."""
    if db.get_bind().dialect.name == "sqlite":
        # SQLite ignores SELECT ... FOR UPDATE, so reserve the database writer
        # before reading any relationship-backed context state.
        await db.execute(
            text("UPDATE tasks SET id = id WHERE id = :task_id"),
            {"task_id": task_id},
        )
    result = await db.execute(
        select(Task.id).where(Task.id == task_id).with_for_update()
    )
    return result.scalar_one_or_none() is not None


async def reserve_task_context_revision(
    db: AsyncSession,
    task_id: int,
    *,
    context_kind: str,
    action: str,
    details: dict[str, Any] | None = None,
) -> int | None:
    """Lock a task, increment its version, and append a server-owned audit event."""
    if not await lock_task_context(db, task_id):
        return None
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    task = result.scalar_one_or_none()
    if task is None:
        return None
    expected_version = task.version
    version_result = await db.execute(
        update(Task)
        .where(Task.id == task_id, Task.version == expected_version)
        .values(version=Task.version + 1)
        .returning(Task.version, Task.updated_at)
        .execution_options(synchronize_session=False)
    )
    version_row = version_result.one_or_none()
    if version_row is None:
        raise TaskContextVersionConflictError(
            "Task context version changed while locked"
        )
    attributes.set_committed_value(task, "version", version_row.version)
    if version_row.updated_at is not None:
        attributes.set_committed_value(task, "updated_at", version_row.updated_at)
    db.add(
        TaskEvent(
            task_id=task_id,
            actor_type="system",
            event_type="task_context_changed",
            payload=json.dumps(
                {
                    "context_kind": context_kind,
                    "action": action,
                    "details": details or {},
                    "version": version_row.version,
                },
                ensure_ascii=False,
                default=str,
            ),
        )
    )
    return int(version_row.version)
