"""Version allocation shared by scheduled and project-backlog recovery."""

from sqlalchemy import func, select

from app.authority import AuthorityError, internal_authority
from app.commands import current_command
from app.models.recovery import TaskDeletionFence
from app.models.task_brief import TaskBriefRevision, TaskProgressRecord, TaskReviewRecord


async def reserve_restored_task_version(db, task_id, task, saved_version):
    """Restore strictly above every retained fence inside the scope's locked command."""
    from app.services.task_service import TaskService
    state = current_command(db)
    if state is None:
        raise RuntimeError("Task recovery requires a command transaction")
    if type(saved_version) is not int or saved_version < 1:
        raise ValueError("Snapshot task version must be a positive integer")
    with internal_authority(db):
        deleted_version = await db.scalar(select(TaskDeletionFence.last_version).where(TaskDeletionFence.original_task_id == task_id))
        versions = [saved_version, task.version if task is not None else 0, deleted_version or 0]
        for model in (TaskBriefRevision, TaskProgressRecord, TaskReviewRecord):
            versions.append(await db.scalar(select(func.max(model.task_version)).where(model.original_task_id == task_id)) or 0)
    if task is None and deleted_version is None:
        raise AuthorityError("snapshot_version_history_unknown",
            "The last deleted task version is unavailable. Restore a complete database backup with its matching application image; this snapshot cannot safely reuse the task ID.", 409)
    next_version = max(versions) + 1
    if next_version > 2_147_483_647:
        raise ValueError("Task version exceeds the supported database range")
    if task is not None:
        await TaskService(db).reserve_task_version(task, task.version)
        task.version = max(task.version, next_version)
        return task.version
    state.tasks[task_id] = next_version - 1
    return next_version
