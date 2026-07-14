"""Selected-task bulk operation orchestration."""
import json
from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.iteration import Iteration
from app.models.task import Task, TaskStatus
from app.schemas.task import (
    TaskBulkOperationRequest,
    TaskBulkOperationResponse,
    TaskBulkOperationResult,
    TaskResponse,
    TaskUpdate,
)
from app.schemas.team import AssigneeRecommendationResponse
from app.services.assignee_recommendation_service import AssigneeRecommendationService
from app.services.language_service import (
    backend_error_message,
    incomplete_dependency_message,
    invalid_status_transition_message,
    localized,
    resolve_runtime_ui_language,
    task_requires_schedule_message,
)
from app.services.task_service import TaskService


class TaskBulkOperationService:
    """Validate, preview, and apply selected-task bulk operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_service = TaskService(db)
        self.recommendation_service = AssigneeRecommendationService(db)

    async def run(self, data: TaskBulkOperationRequest) -> TaskBulkOperationResponse:
        """Run or preview one bulk operation for selected tasks."""
        ui_language = await resolve_runtime_ui_language(self.db)
        task_ids = self._unique_task_ids(data.task_ids)
        if len(task_ids) != len(data.task_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=localized(ui_language, "task_ids must not contain duplicates", "task_ids не должен содержать дубликаты"),
            )

        found_tasks = await self._load_found_tasks(task_ids)
        found_iteration_ids = {task.iteration_id for task in found_tasks.values()}
        if len(found_iteration_ids) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=localized(
                    ui_language,
                    "Bulk task operations require all found tasks to be in one iteration",
                    "Массовые операции с задачами требуют, чтобы все найденные задачи были в одной итерации",
                ),
            )

        iteration_end_date: Optional[Any] = None
        if found_iteration_ids:
            iteration_result = await self.db.execute(
                select(Iteration).where(Iteration.id == next(iter(found_iteration_ids)))
            )
            iteration = iteration_result.scalar_one_or_none()
            iteration_end_date = iteration.end_date if iteration else None

        results: list[TaskBulkOperationResult] = []
        for task_id in task_ids:
            task = found_tasks.get(task_id)
            if not task:
                results.append(
                    TaskBulkOperationResult(
                        task_id=task_id,
                        outcome="failed",
                        error=localized(ui_language, f"Task with id {task_id} not found", f"Задача с id {task_id} не найдена"),
                    )
                )
                continue

            fresh_task = await self.task_service.get_by_id(task_id)
            if not fresh_task:
                results.append(
                    TaskBulkOperationResult(
                        task_id=task_id,
                        outcome="failed",
                        error=localized(ui_language, f"Task with id {task_id} not found", f"Задача с id {task_id} не найдена"),
                    )
                )
                continue

            try:
                result = await self._run_for_task(fresh_task, data, iteration_end_date, ui_language)
            except ValueError as exc:
                await self.db.rollback()
                result = TaskBulkOperationResult(
                    task_id=task_id,
                    outcome="failed",
                    error=backend_error_message(str(exc), ui_language),
                )
            results.append(result)

        failed_count = sum(1 for result in results if result.outcome == "failed")
        return TaskBulkOperationResponse(
            requested_count=len(task_ids),
            succeeded_count=len(results) - failed_count,
            failed_count=failed_count,
            dry_run=data.dry_run,
            results=results,
        )

    async def _run_for_task(
        self,
        task: Task,
        data: TaskBulkOperationRequest,
        iteration_end_date: Optional[Any],
        ui_language,
    ) -> TaskBulkOperationResult:
        if data.action == "delete":
            return await self._delete_task(task, data.dry_run, ui_language)

        update, changes, recommendation, warnings = await self._build_update(task, data, ui_language)
        if not changes:
            return TaskBulkOperationResult(
                task_id=task.id,
                outcome="skipped",
                warnings=warnings or [localized(ui_language, "No changes needed", "Изменения не требуются")],
                assignee_recommendation=recommendation,
            )

        if data.dry_run:
            return TaskBulkOperationResult(
                task_id=task.id,
                outcome="would_update",
                changes=changes,
                warnings=warnings,
                assignee_recommendation=recommendation,
            )

        if data.action == "change_status":
            new_status = update.status
            if new_status is None:
                raise ValueError(localized(ui_language, "status is required", "status обязателен"))
            updated_task, _, _ = await self.task_service.change_status(
                task.id,
                new_status,
                reason=self._optional_text(data.payload.get("reason")),
            )
            if not updated_task:
                raise ValueError(invalid_status_transition_message(task.status, new_status.value, ui_language))
        else:
            updated_task = await self.task_service.update(task.id, update)
            if not updated_task:
                raise ValueError(localized(ui_language, f"Task with id {task.id} not found", f"Задача с id {task.id} не найдена"))

        return TaskBulkOperationResult(
            task_id=task.id,
            outcome="updated",
            changes=changes,
            warnings=warnings,
            task=self.task_service.task_to_response(updated_task, iteration_end_date),
            assignee_recommendation=recommendation,
        )

    async def _delete_task(self, task: Task, dry_run: bool, ui_language) -> TaskBulkOperationResult:
        changes = {"deleted": {"old": False, "new": True}}
        if dry_run:
            return TaskBulkOperationResult(
                task_id=task.id,
                outcome="would_delete",
                changes=changes,
            )

        deleted = await self.task_service.delete(task.id)
        if not deleted:
            return TaskBulkOperationResult(
                task_id=task.id,
                outcome="failed",
                error=localized(ui_language, f"Task with id {task.id} not found", f"Задача с id {task.id} не найдена"),
            )
        return TaskBulkOperationResult(
            task_id=task.id,
            outcome="deleted",
            changes=changes,
        )

    async def _build_update(
        self,
        task: Task,
        data: TaskBulkOperationRequest,
        ui_language,
    ) -> tuple[TaskUpdate, dict[str, Any], Optional[AssigneeRecommendationResponse], list[str]]:
        payload = data.payload or {}
        warnings: list[str] = []
        recommendation: Optional[AssigneeRecommendationResponse] = None
        update_data: dict[str, Any] = {}

        if data.action == "set_assignee":
            assignee_id = self._required_int(payload, "assignee_id")
            await self.task_service.require_iteration_assignee(assignee_id, task.iteration_id)
            update_data["assignee_id"] = assignee_id
        elif data.action == "clear_assignee":
            update_data["assignee_id"] = None
        elif data.action == "auto_assign":
            assignee_id, recommendation, auto_warnings = await self._auto_assignee_for_task(task, payload)
            warnings.extend(auto_warnings)
            if assignee_id is None:
                return TaskUpdate(), {}, recommendation, warnings
            update_data["assignee_id"] = assignee_id
        elif data.action == "set_project":
            update_data["project_id"] = self._required_int(payload, "project_id")
            if "milestone_id" in payload:
                update_data["milestone_id"] = payload["milestone_id"]
        elif data.action == "clear_project":
            update_data["project_id"] = None
            update_data["milestone_id"] = None
        elif data.action == "set_milestone":
            update_data["milestone_id"] = self._required_int(payload, "milestone_id")
        elif data.action == "clear_milestone":
            update_data["milestone_id"] = None
        elif data.action == "set_priority":
            priority = self._required_int(payload, "priority")
            if priority < 1 or priority > 10:
                raise ValueError("priority must be between 1 and 10")
            update_data["priority"] = priority
        elif data.action == "add_labels":
            update_data["tags"] = self._apply_label_delta(
                self._task_tags(task),
                self._required_labels(payload),
                add=True,
            )
        elif data.action == "remove_labels":
            update_data["tags"] = self._apply_label_delta(
                self._task_tags(task),
                self._required_labels(payload),
                add=False,
            )
        elif data.action == "set_flags":
            if "is_optional" not in payload and "is_deferred" not in payload:
                raise ValueError("set_flags requires is_optional or is_deferred")
            if "is_optional" in payload:
                update_data["is_optional"] = bool(payload["is_optional"])
            if "is_deferred" in payload:
                update_data["is_deferred"] = bool(payload["is_deferred"])
        elif data.action == "change_status":
            status_value = self._required_text(payload, "status")
            new_status = TaskStatus(status_value)
            error = self._status_transition_error(task, new_status, ui_language)
            if error:
                raise ValueError(error)
            update_data["status"] = new_status
        else:
            raise ValueError(f"Unsupported bulk action: {data.action}")

        update = TaskUpdate(**update_data)
        await self._validate_update(task, update)
        changes = self._changes_for_update(task, update)
        return update, changes, recommendation, warnings

    async def _validate_update(self, task: Task, update: TaskUpdate) -> None:
        update_data = update.model_dump(exclude_unset=True)
        project_id_was_set = "project_id" in update.model_fields_set
        milestone_id_was_set = "milestone_id" in update.model_fields_set
        assignee_id_was_set = "assignee_id" in update.model_fields_set
        project_id = update_data.get("project_id") if project_id_was_set else task.project_id

        if project_id_was_set:
            await self.task_service.require_task_project_scope_for_update(
                task,
                project_id,
                project_id_was_set,
            )
            if task.parent_id is not None:
                parent = await self.task_service.get_by_id(task.parent_id)
                if parent and project_id != parent.project_id:
                    raise ValueError("Subtask project must match parent task project.")
        else:
            project_id = await self.task_service.require_task_project_scope_for_update(
                task,
                project_id,
                project_id_was_set,
            )

        if milestone_id_was_set:
            await self.task_service._require_milestone_compatible(
                update_data.get("milestone_id"),
                project_id,
            )

        if assignee_id_was_set:
            await self.task_service.require_iteration_assignee(
                update_data.get("assignee_id"),
                task.iteration_id,
            )

    def _changes_for_update(self, task: Task, update: TaskUpdate) -> dict[str, Any]:
        changes: dict[str, Any] = {}
        update_data = update.model_dump(exclude_unset=True)
        for field, new_value in update_data.items():
            if field == "status":
                old_value = task.status
                new_value = new_value.value if hasattr(new_value, "value") else new_value
            elif field == "tags":
                old_value = self._task_tags(task)
            else:
                old_value = getattr(task, field)
            if old_value != new_value:
                changes[field] = {"old": old_value, "new": new_value}
        return changes

    async def _auto_assignee_for_task(
        self,
        task: Task,
        payload: dict[str, Any],
    ) -> tuple[Optional[int], Optional[AssigneeRecommendationResponse], list[str]]:
        warnings: list[str] = []
        if task.children:
            warnings.append("Composite tasks are skipped for auto-assignment")
            return None, None, warnings
        if task.status in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}:
            warnings.append("Resolved or closed tasks are skipped for auto-assignment")
            return None, None, warnings
        if not task.start_date or not task.end_date:
            warnings.append("Unscheduled tasks are skipped for auto-assignment")
            return None, None, warnings

        recommendations = await self.recommendation_service.recommend_for_task(task.id)
        if not recommendations:
            warnings.append("No assignee recommendations are available")
            return None, None, warnings

        top = recommendations[0]
        min_confidence = self._optional_float(payload.get("min_confidence"), 0.5)
        if top.confidence < min_confidence:
            warnings.append(
                f"Top recommendation confidence {top.confidence:.2f} is below {min_confidence:.2f}"
            )
            return None, top, warnings
        if task.assignee_id == top.team_member_id:
            warnings.append("Task already has the recommended assignee")
            return None, top, warnings
        return top.team_member_id, top, warnings

    def _status_transition_error(self, task: Task, new_status: TaskStatus, ui_language) -> Optional[str]:
        new_value = new_status.value if hasattr(new_status, "value") else str(new_status)
        if task.status == new_value:
            return None
        valid_next = self.task_service.VALID_TRANSITIONS.get(task.status, [])
        if new_value not in valid_next:
            return invalid_status_transition_message(task.status, new_value, ui_language)
        if task.status == TaskStatus.PLANNED.value:
            if not task.start_date or not task.end_date:
                return task_requires_schedule_message(ui_language)
            for dependency in task.dependencies or []:
                dep_task = dependency.depends_on
                if dep_task and dep_task.status not in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}:
                    return incomplete_dependency_message(dep_task.title, dep_task.status, ui_language)
        return None

    async def _load_found_tasks(self, task_ids: list[int]) -> dict[int, Task]:
        result = await self.db.execute(select(Task).where(Task.id.in_(task_ids)))
        return {task.id: task for task in result.scalars().all()}

    def _unique_task_ids(self, task_ids: list[int]) -> list[int]:
        seen: set[int] = set()
        unique: list[int] = []
        for task_id in task_ids:
            if task_id not in seen:
                unique.append(task_id)
                seen.add(task_id)
        return unique

    def _task_tags(self, task: Task) -> list[str]:
        try:
            value = json.loads(task.tags) if task.tags else []
        except (TypeError, json.JSONDecodeError):
            return []
        if not isinstance(value, list):
            return []
        return [str(item).strip() for item in value if str(item).strip()]

    def _apply_label_delta(self, current: list[str], labels: list[str], add: bool) -> list[str]:
        if add:
            result = list(current)
            for label in labels:
                if label not in result:
                    result.append(label)
            return result
        to_remove = set(labels)
        return [label for label in current if label not in to_remove]

    def _required_labels(self, payload: dict[str, Any]) -> list[str]:
        raw_labels = payload.get("labels")
        if not isinstance(raw_labels, list):
            raise ValueError("labels must be a list")
        labels: list[str] = []
        for raw in raw_labels:
            label = str(raw).strip()
            if label and label not in labels:
                labels.append(label)
        if not labels:
            raise ValueError("labels must contain at least one non-empty label")
        return labels

    def _required_int(self, payload: dict[str, Any], key: str) -> int:
        value = payload.get(key)
        if value is None:
            raise ValueError(f"{key} is required")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{key} must be an integer") from exc

    def _required_text(self, payload: dict[str, Any], key: str) -> str:
        value = str(payload.get(key) or "").strip()
        if not value:
            raise ValueError(f"{key} is required")
        return value

    def _optional_text(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _optional_float(self, value: Any, default: float) -> float:
        if value is None:
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
