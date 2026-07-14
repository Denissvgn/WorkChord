"""Task status transitions, roll-up reconciliation, and status reporting."""

import json
from datetime import date, timedelta
from typing import Any, Optional, Sequence, TYPE_CHECKING

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.task_status_log import TaskStatusLog
from app.services.language_service import (
    automatic_child_status_reason,
    incomplete_dependency_message,
    resolve_runtime_ui_language,
    task_requires_schedule_message,
)
from app.services.outbound_webhook_service import OutboundWebhookService

if TYPE_CHECKING:
    from app.services.task_service import TaskService


class TaskStatusService:
    """Own status transitions, dependent cascades, and parent reconciliation."""

    VALID_TRANSITIONS = {
        TaskStatus.PLANNED.value: {TaskStatus.ACTIVE.value},
        TaskStatus.ACTIVE.value: {TaskStatus.RESOLVED.value},
        TaskStatus.RESOLVED.value: {TaskStatus.ACTIVE.value, TaskStatus.CLOSED.value},
        TaskStatus.CLOSED.value: set(),
    }
    ROLLUP_TRANSITIONS = {
        status.value: {
            target.value for target in TaskStatus if target.value != status.value
        }
        for status in TaskStatus
    }

    def __init__(self, db: AsyncSession, task_service: "TaskService"):
        self.db = db
        self.task_service = task_service

    @staticmethod
    def derive_parent_status(child_statuses: Sequence[str]) -> str:
        """Derive the complete parent roll-up truth table from child statuses."""
        statuses = list(child_statuses)
        if not statuses:
            raise ValueError("Parent status requires at least one child status.")
        if all(status == TaskStatus.PLANNED.value for status in statuses):
            return TaskStatus.PLANNED.value
        if all(status == TaskStatus.CLOSED.value for status in statuses):
            return TaskStatus.CLOSED.value
        if all(
            status in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}
            for status in statuses
        ):
            return TaskStatus.RESOLVED.value
        return TaskStatus.ACTIVE.value

    async def change_status(
        self,
        task_id: int,
        new_status: TaskStatus | str,
        reason: Optional[str] = None,
        actor_type: str = "user",
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        expected_version: Optional[int] = None,
        commit: bool = True,
        reserve_version: bool = True,
    ) -> tuple[Optional[Task], list[dict], bool]:
        """Apply one valid direct transition and reconcile its ancestor chain."""
        task = await self.task_service.get_by_id(task_id)
        if task is None:
            return None, [], False
        self.task_service.ensure_expected_version(task, expected_version)

        new_status_value = (
            new_status.value if hasattr(new_status, "value") else str(new_status)
        )
        if new_status_value not in self.VALID_TRANSITIONS.get(task.status, set()):
            return None, [], False

        ui_language = await resolve_runtime_ui_language(self.db)
        if task.status == TaskStatus.PLANNED.value:
            if not task.start_date or not task.end_date:
                raise ValueError(task_requires_schedule_message(ui_language))
            for dependency in task.dependencies:
                dependency_task = await self.task_service.get_by_id(
                    dependency.depends_on_id
                )
                if dependency_task and dependency_task.status not in {
                    TaskStatus.RESOLVED.value,
                    TaskStatus.CLOSED.value,
                }:
                    raise ValueError(
                        incomplete_dependency_message(
                            dependency_task.title,
                            dependency_task.status,
                            ui_language,
                        )
                    )

        updated, cascade_updates, notification_sent = await self._apply_transition(
            task,
            new_status_value,
            reason=reason,
            actor_type=actor_type,
            actor_id=actor_id,
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            expected_version=expected_version,
            automatic=False,
            reserve_version=reserve_version,
        )
        if updated.parent_id is not None:
            await self.reconcile_parent_chain(
                updated.parent_id,
                visited={updated.id},
                commit=False,
            )
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        refreshed = await self.task_service.get_by_id(task_id)
        return refreshed, cascade_updates, notification_sent

    async def _apply_transition(
        self,
        task: Task,
        new_status: str,
        *,
        reason: Optional[str],
        actor_type: str,
        actor_id: Optional[int] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        expected_version: Optional[int],
        automatic: bool,
        reserve_version: bool = True,
    ) -> tuple[Task, list[dict], bool]:
        """Run the shared mutation, audit, delivery, and notification semantics."""
        old_status = task.status
        if old_status == new_status:
            return task, [], False
        transition_map = self.ROLLUP_TRANSITIONS if automatic else self.VALID_TRANSITIONS
        if new_status not in transition_map.get(old_status, set()):
            raise ValueError(f"Invalid task status transition: {old_status} -> {new_status}")

        today = date.today()
        original_end_date = task.end_date
        if automatic:
            if new_status == TaskStatus.PLANNED.value:
                task.actual_start_date = None
                task.actual_end_date = None
            elif new_status == TaskStatus.ACTIVE.value:
                task.actual_start_date = task.actual_start_date or today
                task.actual_end_date = None
            elif new_status == TaskStatus.RESOLVED.value:
                task.actual_end_date = None
            elif new_status == TaskStatus.CLOSED.value:
                task.actual_end_date = task.actual_end_date or today
        elif new_status == TaskStatus.ACTIVE.value and old_status == TaskStatus.PLANNED.value:
            task.actual_start_date = today
            if task.start_date and today > task.start_date and task.end_date:
                task.end_date += timedelta(days=(today - task.start_date).days)
            task.start_date = today
        elif new_status == TaskStatus.CLOSED.value:
            task.actual_end_date = today
            task.end_date = today

        task.status = new_status
        if reserve_version:
            await self.task_service.reserve_task_version(task, expected_version)

        cascade_updates: list[dict] = []
        status_log = TaskStatusLog(
            task_id=task.id,
            from_status=old_status,
            to_status=new_status,
            reason=reason,
            triggered_by=actor_type,
        )
        self.db.add(status_log)
        if (
            not automatic
            and original_end_date
            and task.end_date
            and task.end_date != original_end_date
        ):
            cascade_updates = await self.cascade_update_dependents(
                task,
                original_end_date,
                reason=f"Predecessor task '{task.title}' dates updated",
            )
            status_log.affected_task_ids = json.dumps(
                [item["task_id"] for item in cascade_updates]
            )

        await self.task_service.record_task_event(
            task.id,
            "status_changed",
            {
                "from_status": old_status,
                "to_status": new_status,
                "reason": reason,
                "affected_task_ids": [item["task_id"] for item in cascade_updates],
                "version": task.version,
            },
            actor_type=actor_type,
            actor_id=actor_id,
            trace_id=trace_id,
            span_id=span_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        result = await self.db.execute(
            select(Iteration).where(Iteration.id == task.iteration_id)
        )
        iteration = result.scalar_one_or_none()
        event_data = {
            "task_id": task.id,
            "iteration_id": task.iteration_id,
            "project_id": task.project_id,
            "from_status": old_status,
            "to_status": new_status,
            "reason": reason,
            "affected_task_ids": [item["task_id"] for item in cascade_updates],
            "version": task.version,
            "automatic": automatic,
        }
        await OutboundWebhookService(self.db).enqueue_status_change(
            event_type="task.status_changed",
            entity_type="task",
            entity_id=task.id,
            data=event_data,
            email_payload={
                "task_title": task.title,
                "task_id": task.id,
                "old_status": old_status,
                "new_status": new_status,
                "manager_email": iteration.manager_email if iteration else None,
                "assignee_email": task.assignee.email if task.assignee else None,
                "cascade_updates": cascade_updates,
                "reason": reason,
            },
            commit=False,
        )
        # Delivery is intentionally asynchronous. Keep the legacy response field
        # honest: persistence of an intent is not the same as a sent email.
        return task, cascade_updates, False

    async def reconcile_parent_chain(
        self,
        parent_id: int,
        *,
        visited: set[int] | None = None,
        commit: bool = True,
    ) -> None:
        """Reconcile each ancestor at most once through the shared transition operation."""
        visited = set(visited or set())
        if parent_id in visited:
            raise ValueError(f"Task parent cycle detected while reconciling task {parent_id}.")
        visited.add(parent_id)

        parent = await self.task_service.get_by_id(parent_id)
        if parent is None or not parent.children:
            return
        target_status = self.derive_parent_status(
            [child.status for child in parent.children]
        )
        if target_status == parent.status:
            return

        ui_language = await resolve_runtime_ui_language(self.db)
        await self._apply_transition(
            parent,
            target_status,
            reason=automatic_child_status_reason(ui_language),
            actor_type="auto",
            expected_version=parent.version,
            automatic=True,
            reserve_version=True,
        )
        if parent.parent_id is not None:
            await self.reconcile_parent_chain(
                parent.parent_id,
                visited=visited,
                commit=False,
            )
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()

    async def cascade_update_dependents(
        self,
        source_task: Task,
        original_end_date: date,
        reason: str,
    ) -> list[dict]:
        """Shift planned dependent tasks when a predecessor is delayed."""
        if not source_task.end_date:
            return []
        delta = (source_task.end_date - original_end_date).days
        if delta <= 0:
            return []

        result = await self.db.execute(
            select(TaskDependency).where(TaskDependency.depends_on_id == source_task.id)
        )
        cascade_updates: list[dict] = []
        for dependency in result.scalars().all():
            dependent = await self.task_service.get_by_id(dependency.task_id)
            if dependent is None or dependent.status != TaskStatus.PLANNED.value:
                continue
            old_start = dependent.start_date
            old_end = dependent.end_date
            if dependent.start_date:
                dependent.start_date += timedelta(days=delta)
            if dependent.end_date:
                dependent.end_date += timedelta(days=delta)
            dependent.version += 1
            cascade_updates.append(
                {
                    "task_id": dependent.id,
                    "task_title": dependent.title,
                    "old_start_date": old_start,
                    "old_end_date": old_end,
                    "new_start_date": dependent.start_date,
                    "new_end_date": dependent.end_date,
                }
            )
            await self.task_service.record_task_event(
                dependent.id,
                "dates_cascaded",
                {
                    "reason": reason,
                    "source_task_id": source_task.id,
                    "old_start_date": old_start,
                    "old_end_date": old_end,
                    "new_start_date": dependent.start_date,
                    "new_end_date": dependent.end_date,
                    "version": dependent.version,
                },
                actor_type="auto",
            )
            if old_end and dependent.end_date:
                cascade_updates.extend(
                    await self.cascade_update_dependents(
                        dependent,
                        old_end,
                        reason=f"Cascade from '{source_task.title}'",
                    )
                )
        return cascade_updates

    async def get_status_history(self, task_id: int) -> list[Any]:
        """Get status change history for a task."""
        result = await self.db.execute(
            select(TaskStatusLog)
            .where(TaskStatusLog.task_id == task_id)
            .order_by(TaskStatusLog.changed_at.desc())
        )
        return list(result.scalars().all())

    async def get_overdue_tasks(self, iteration_id: int) -> Sequence[Task]:
        """Get planned tasks whose start date has passed."""
        result = await self.db.execute(
            select(Task)
            .where(
                Task.iteration_id == iteration_id,
                Task.status == TaskStatus.PLANNED.value,
                Task.start_date < date.today(),
                Task.start_date.isnot(None),
            )
            .options(selectinload(Task.assignee), selectinload(Task.dependencies))
            .order_by(Task.start_date)
        )
        return result.scalars().all()

    async def get_iteration_status_history(
        self,
        iteration_id: int,
        limit: int = 50,
    ) -> list[Any]:
        """Get recent status history for one iteration."""
        result = await self.db.execute(
            select(TaskStatusLog, Task.title)
            .join(Task, TaskStatusLog.task_id == Task.id)
            .where(Task.iteration_id == iteration_id)
            .order_by(desc(TaskStatusLog.changed_at))
            .limit(limit)
        )
        history = []
        for log, title in result.all():
            log.task_title = title
            history.append(log)
        return history

    async def get_iteration_status_stats(self, iteration_id: int) -> list[dict]:
        """Aggregate transition counts for one iteration."""
        result = await self.db.execute(
            select(
                TaskStatusLog.from_status,
                TaskStatusLog.to_status,
                func.count(TaskStatusLog.id).label("count"),
            )
            .join(Task, TaskStatusLog.task_id == Task.id)
            .where(Task.iteration_id == iteration_id)
            .group_by(TaskStatusLog.from_status, TaskStatusLog.to_status)
        )
        return [
            {"from_status": from_status, "to_status": to_status, "count": count}
            for from_status, to_status, count in result.all()
        ]
