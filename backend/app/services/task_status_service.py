"""Task status transitions, roll-up reconciliation, and status reporting."""

from app.authority import AuthorityError
from app.commands import atomic_command, command_transaction, commit_or_flush, lock_iterations

import json
from collections import deque
from datetime import date, timedelta
from typing import Any, Optional, Sequence, TYPE_CHECKING

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.task_status_log import TaskStatusLog
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
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
        # Postponed work moves only through the postpone and reactivate commands.
        TaskStatus.POSTPONED.value: set(),
    }
    # The only moves into and out of postponed; TaskPostponementService owns them.
    POSTPONEMENT_TRANSITIONS = {
        TaskStatus.PLANNED.value: {TaskStatus.POSTPONED.value},
        TaskStatus.ACTIVE.value: {TaskStatus.POSTPONED.value},
        TaskStatus.RESOLVED.value: {TaskStatus.POSTPONED.value},
        TaskStatus.POSTPONED.value: {TaskStatus.PLANNED.value, TaskStatus.RESOLVED.value},
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
        if all(status == TaskStatus.POSTPONED.value for status in statuses):
            return TaskStatus.POSTPONED.value
        # Beside other work, a postponed leaf is neither started nor done.
        statuses = [TaskStatus.PLANNED.value if status == TaskStatus.POSTPONED.value else status
                    for status in statuses]
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

    @atomic_command
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
        manual_execution: bool = False,
        review_evidence: str = "",
        review_rework: bool = False,
    ) -> tuple[Optional[Task], list[dict], bool]:
        """Apply one valid direct transition and reconcile its ancestor chain."""
        authority = self.db.info.get("authority")
        if authority is not None and authority.kind == "agent":
            if (new_status.value if hasattr(new_status, "value") else str(new_status)) == "closed" and authority.actor_role != "verifier":
                raise AuthorityError("independent_review_required", "Execution cannot accept its own work.")
            if authority.source == "rest":
                raise AuthorityError("agent_protocol_required", "Use the assigned-work command with its current execution fence.")
        from app.commands import PlanningConflict
        from app.services.task_hierarchy_service import TaskTreeIntegrityError
        try:
            await self.task_service._lock_task_scope(task_id)
            task = await self.task_service.get_by_id(task_id)
        except TaskTreeIntegrityError as exc:
            raise PlanningConflict("task_ancestry_invalid", "Reload or repair this task's ancestry before executing work.") from exc
        if task is None:
            return None, [], False
        if task.canceled_at or task.blocked_reason:
            raise ValueError("Canceled or blocked work cannot change lifecycle")
        if task.status == TaskStatus.POSTPONED.value:
            raise ValueError("Postponed work cannot change lifecycle; reactivate it first")
        if manual_execution and authority is not None and authority.kind not in {"human", "local"}:
            raise AuthorityError("human_execution_required", "Manual execution requires a human identity.")
        if task.is_summary or task.children:
            raise ValueError("Summary lifecycle is derived from its leaf work")
        self.task_service.ensure_expected_version(task, expected_version)

        new_status_value = (
            new_status.value if hasattr(new_status, "value") else str(new_status)
        )
        if new_status_value == TaskStatus.POSTPONED.value:
            raise ValueError("Postpone work with the postpone command, which records a reason and reactivation requirements")
        from app.services.work_metrics import effective_work_flags
        if new_status_value in {"active", "resolved"} and not review_rework and effective_work_flags(task)["effective_is_deferred"]:
            raise PlanningConflict("task_deferred", "Remove deferral before executing work.")
        from app.authority import require_project
        from app.commands import current_command
        command = current_command(self.db)
        evidence_return = (authority is not None and command is not None and task.status == "resolved" and
                           new_status_value == "active" and (authority.actor_id, task.id) in command.evidence_returns)
        require_project(self.db, task.project_id, "manage" if evidence_return else
                        "review" if new_status_value == "closed" or review_rework else "execute")
        if review_rework:
            if task.status != "resolved" or new_status_value != "active":
                raise ValueError("Review rework requires a resolved-to-active transition")
            self.db.info.setdefault("review_rework_tasks", set()).add(task.id)
        if new_status_value not in self.VALID_TRANSITIONS.get(task.status, set()):
            return None, [], False

        if new_status_value == "closed":
            from app.services.task_brief_service import TaskBriefService
            await TaskBriefService(self.db).require_review(task, accepting=True)
        ui_language = await resolve_runtime_ui_language(self.db)
        if task.status == TaskStatus.PLANNED.value:
            from app.services.delivery_dependency_service import DeliveryDependencyService
            if not await DeliveryDependencyService(self.db).ready(task.id):
                raise ValueError("Delivery prerequisites must be accepted before starting this work")
            if not manual_execution and (not task.start_date or not task.end_date):
                raise ValueError(task_requires_schedule_message(ui_language))
            for dependency in task.dependencies:
                dependency_task = await self.task_service.get_by_id(
                    dependency.depends_on_id
                )
                if dependency_task and (dependency_task.canceled_at or dependency_task.status not in {
                    TaskStatus.RESOLVED.value,
                    TaskStatus.CLOSED.value,
                }):
                    raise ValueError(
                        incomplete_dependency_message(
                            dependency_task.title,
                            dependency_task.status,
                            ui_language,
                        )
                    )

        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(task.iteration_id, "before_status_change")
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
        if new_status_value == "closed":
            from app.services.task_brief_service import TaskBriefService
            await TaskBriefService(self.db).record_review(updated, verdict="accept", reason=reason or "Independent status review", evidence=review_evidence)
        if updated.parent_id is not None:
            await self.reconcile_parent_chain(
                updated.parent_id,
                visited={updated.id},
                commit=False,
            )
        if commit:
            await commit_or_flush(self.db)
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
        postponement: bool = False,
    ) -> tuple[Task, list[dict], bool]:
        """Run the shared mutation, audit, delivery, and notification semantics."""
        old_status = task.status
        if old_status == new_status:
            return task, [], False
        transition_map = (self.ROLLUP_TRANSITIONS if automatic else
                          self.POSTPONEMENT_TRANSITIONS if postponement else self.VALID_TRANSITIONS)
        if new_status not in transition_map.get(old_status, set()):
            raise ValueError(f"Invalid task status transition: {old_status} -> {new_status}")

        from app.services.work_metrics import working_today
        from app.models.project import Project
        from app.utils.time import utc_now
        from app.models.calendar import Calendar
        timezone = (await self.db.scalar(select(Project.timezone).where(Project.id == task.project_id)) if task.project_id else
                    await self.db.scalar(select(Calendar.timezone).join(Iteration, Iteration.calendar_id == Calendar.id).where(Iteration.id == task.iteration_id)))
        today, now = working_today(timezone), utc_now()
        original_end_date = task.end_date
        authority = self.db.info.get("authority")
        if automatic:
            self.db.info.setdefault("derived_rollups", set()).add(task.id)
            task.is_summary = True
        elif postponement:
            # Stopping and resuming keep the brief, progress, evidence, dates and
            # execution provenance exactly as they were.
            pass
        elif new_status == TaskStatus.ACTIVE.value:
            task.progress = None
            task.started_at = task.started_at or now
            task.actual_start_date = task.actual_start_date or today
            task.resolved_at = task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None
            task.actual_end_date = None
            if old_status == TaskStatus.PLANNED.value and task.execution_mode != "manual":
                # The forecast follows the actual start, earlier or later, and keeps its length.
                if task.start_date and today != task.start_date and task.end_date:
                    task.end_date += timedelta(days=(today - task.start_date).days)
                task.start_date = today
            if task.id not in self.db.info.get("review_rework_tasks", set()):
                task.executed_by_principal_id = getattr(authority, "principal_id", None)
        elif new_status == TaskStatus.RESOLVED.value:
            task.resolved_at = now
            if task.execution_mode != "manual" and task.start_date and task.end_date and task.end_date != today:
                # The forecast ends when the work was really submitted, so its assignee is free from then.
                task.end_date = max(task.start_date, today)
            task.executed_by_principal_id = getattr(authority, "principal_id", None) or task.executed_by_principal_id
            task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None
        elif new_status == TaskStatus.CLOSED.value:
            from app.services.identity_service import acting_principal_id
            acceptor = await acting_principal_id(self.db)
            task.actual_end_date = today
            task.accepted_at = now
            task.accepted_by_principal_id = acceptor

        task.status = new_status
        if reserve_version:
            await self.task_service.reserve_task_version(task, expected_version)
        if new_status == "closed" and not automatic:
            task.accepted_version = task.version

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
            # The caller's own change is authorized as the caller. Moving the dates of
            # the work behind it follows from that change, so the server does it itself;
            # a worker has no planning scope and could otherwise never start late work.
            from app.authority import internal_authority
            await self.db.flush()
            with internal_authority(self.db):
                cascade_updates = await self.cascade_update_dependents(
                    task,
                    original_end_date,
                    reason=f"Predecessor task '{task.title}' dates updated",
                )
                await self.db.flush()
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
                "assignee_email": task.owner_profile.email if task.__dict__.get("owner_profile") else task.assignee.email if task.assignee else None,
                "cascade_updates": cascade_updates,
                "reason": reason,
            },
            commit=False,
        )
        # Delivery is intentionally asynchronous. Keep the legacy response field
        # honest: persistence of an intent is not the same as a sent email.
        return task, cascade_updates, False

    async def apply_postponement_transition(
        self,
        task: Task,
        new_status: str,
        *,
        reason: str,
        expected_version: Optional[int],
        actor_type: str = "user",
    ) -> Task:
        """Move one locked leaf into or out of postponed, with the usual audit.

        The caller has checked manage authority, the lifecycle and the
        postponement record; this writes the status, version, status log, event
        and webhook, then reconciles the ancestor chain. The command records the
        task so the write is authorized as the planning decision it is.
        """
        from app.commands import current_command
        command = current_command(self.db)
        if command is None:
            raise RuntimeError("Postponement transitions require a command transaction")
        command.postponement_transitions.add(task.id)
        updated, _, _ = await self._apply_transition(
            task, new_status, reason=reason, actor_type=actor_type, expected_version=expected_version,
            automatic=False, postponement=True,
        )
        if updated.parent_id is not None:
            await self.reconcile_parent_chain(updated.parent_id, visited={updated.id}, commit=False)
        return updated

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
        if parent is None:
            return
        children = list(parent.children)
        target_status = self.derive_parent_status([child.status for child in children]) if children else "planned"
        target_priority = min(child.priority for child in children) if children else parent.priority
        structural_change = not parent.is_summary or parent.priority != target_priority or parent.effort_days != 0 or parent.effort_hours != 0 or parent.assignee_id is not None
        self.db.info.setdefault("derived_rollups", set()).add(parent.id)
        parent.is_summary = True
        parent.effort_days = parent.effort_hours = 0.0
        parent.assignee_id = None
        parent.priority = target_priority
        parent.accepted_at = parent.accepted_by_principal_id = parent.accepted_version = None
        if target_status != parent.status:
            ui_language = await resolve_runtime_ui_language(self.db)
            await self._apply_transition(parent, target_status, reason=automatic_child_status_reason(ui_language),
                actor_type="auto", expected_version=parent.version, automatic=True, reserve_version=True)
        elif structural_change:
            await self.task_service.reserve_task_version(parent, parent.version)
            await self.task_service.record_task_event(parent.id, "summary_reconciled", {"priority": target_priority, "status": target_status}, actor_type="auto")
        await self.db.flush()
        if parent.parent_id is not None:
            await self.reconcile_parent_chain(parent.parent_id, visited=visited, commit=False)
        if commit:
            await commit_or_flush(self.db)

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

        # Every planned task reached moves by the same delta, so each one is
        # visited and moved exactly once, however many dependency paths lead to
        # it. Walking every path instead moved a task once per path.
        cascade_updates: list[dict] = []
        seen: set[int] = {source_task.id}
        pending: deque[tuple[Task, str]] = deque([(source_task, reason)])
        while pending:
            predecessor, step_reason = pending.popleft()
            result = await self.db.execute(
                select(TaskDependency)
                .where(TaskDependency.depends_on_id == predecessor.id)
                .order_by(TaskDependency.task_id)
            )
            for dependency in result.scalars().all():
                if dependency.task_id in seen:
                    continue
                seen.add(dependency.task_id)
                shifted = await self._shift_dependent(
                    dependency.task_id, predecessor, delta, step_reason
                )
                if shifted is None:
                    continue
                dependent, update = shifted
                cascade_updates.append(update)
                if update["old_end_date"] and update["new_end_date"]:
                    pending.append((dependent, f"Cascade from '{predecessor.title}'"))
        return cascade_updates

    async def _shift_dependent(
        self,
        dependent_id: int,
        predecessor: Task,
        delta: int,
        reason: str,
    ) -> tuple[Task, dict] | None:
        """Move one planned dependent by ``delta`` days and record why."""
        dependent = await self.task_service.get_by_id(dependent_id)
        if dependent is None or dependent.status != TaskStatus.PLANNED.value:
            return None
        old_start = dependent.start_date
        old_end = dependent.end_date
        if dependent.start_date:
            dependent.start_date += timedelta(days=delta)
        if dependent.end_date:
            dependent.end_date += timedelta(days=delta)
        previous_version = dependent.version
        await self.task_service.reserve_task_version(dependent, dependent.version)
        from app.services.scheduler_service import rebind_queued_assignments
        await rebind_queued_assignments(self.db, dependent.id, previous_version, dependent.version)
        await self.task_service.record_task_event(
            dependent.id,
            "dates_cascaded",
            {
                "reason": reason,
                "source_task_id": predecessor.id,
                "old_start_date": old_start,
                "old_end_date": old_end,
                "new_start_date": dependent.start_date,
                "new_end_date": dependent.end_date,
                "version": dependent.version,
            },
            actor_type="auto",
        )
        return dependent, {
            "task_id": dependent.id,
            "task_title": dependent.title,
            "old_start_date": old_start,
            "old_end_date": old_end,
            "new_start_date": dependent.start_date,
            "new_end_date": dependent.end_date,
        }

    async def get_status_history(self, task_id: int) -> list[Any]:
        """Get status change history for a task."""
        result = await self.db.execute(
            select(TaskStatusLog)
            .where(TaskStatusLog.task_id == task_id)
            .order_by(TaskStatusLog.changed_at.desc(), TaskStatusLog.id.desc())
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        history = list(result.scalars().all())
        if len(history) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "task status history",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return history

    async def get_overdue_tasks(self, iteration_id: int) -> Sequence[Task]:
        """Return open leaf delivery past its expected completion in the working zone."""
        from app.services.work_metrics import task_signals
        tasks = await self.task_service.get_all_tasks(iteration_id)
        overdue = []
        for task in tasks:
            project = task.__dict__.get("project")
            if task_signals(task, timezone=project.timezone if project else "UTC", composite=task.is_summary or bool(task.children))["is_overdue"]:
                overdue.append(task)
        overdue.sort(key=lambda task: (task.end_date, task.id))
        if len(overdue) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError("overdue task list", MAX_BOUNDED_LIST_ITEMS)
        return overdue

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
            .order_by(desc(TaskStatusLog.changed_at), TaskStatusLog.id.desc())
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
