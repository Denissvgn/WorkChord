"""Service for saved view persistence and filter payload compatibility."""
from datetime import date
from math import isfinite
from typing import Any, Optional, Sequence

from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.iteration import Iteration
from app.models.saved_view import SavedView
from app.schemas.saved_view import (
    SavedViewCreate,
    SavedViewCreateRequest,
    SavedViewDashboardCardResponse,
    SavedViewDuplicateRequest,
    SavedViewResponse,
    SavedViewScope,
    SavedViewType,
    SavedViewUpdate,
    SavedViewUpdateRequest,
)


class SavedViewPermissionError(PermissionError):
    """Raised when a session cannot mutate a saved view."""


class SavedViewValidationError(ValueError):
    """Raised when a saved view payload is invalid."""


TASK_FILTER_DEFAULTS: dict[str, Any] = {
    "assigneeId": None,
    "projectId": None,
    "priority": None,
    "status": None,
    "hasDependency": None,
    "isOverdue": None,
    "agentReady": None,
    "planningIssue": None,
    "startDateFrom": "",
    "startDateTo": "",
    "endDateFrom": "",
    "endDateTo": "",
    "labelSlugs": [],
    "labelGroupKeys": [],
}
TASK_STATUS_VALUES = {"planned", "active", "resolved", "closed"}
TASK_PLANNING_ISSUE_VALUES = {"unassigned", "missing-effort", "any"}
TASK_SORT_VALUES = {"priority", "sort_order", "status", "title"}

PROJECT_FILTER_DEFAULTS: dict[str, Any] = {
    "search": "",
    "status": "",
    "health": "",
}
PROJECT_STATUS_VALUES = {"proposed", "planned", "active", "paused", "completed", "canceled"}
PROJECT_HEALTH_VALUES = {"unknown", "on_track", "at_risk", "off_track"}

TRIAGE_FILTER_DEFAULTS: dict[str, Any] = {
    "active": True,
    "statuses": [],
    "q": "",
    "source": "",
}
TRIAGE_STATUS_VALUES = {"new", "accepted", "declined", "duplicate", "snoozed", "converted"}

DEFAULT_SAVED_VIEW_DEFINITIONS: list[dict[str, Any]] = [
    {
        "seed_key": "triage_needs_triage",
        "name": "Needs triage",
        "description": "New intake items that need review.",
        "view_type": SavedViewType.TRIAGE.value,
        "filters_json": {"statuses": ["new"]},
    },
    {
        "seed_key": "tasks_unassigned",
        "name": "Unassigned",
        "description": "Tasks without an assigned owner.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"assigneeId": -1},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_blocked",
        "name": "Blocked",
        "description": "Tasks tagged as blocked.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"labelSlugs": ["blocked"]},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_overdue",
        "name": "Overdue",
        "description": "Tasks currently marked as overdue.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"isOverdue": True},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_high_priority",
        "name": "High priority",
        "description": "Priority 1 tasks.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"priority": 1},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_ready_for_agent",
        "name": "Ready for agent",
        "description": "Tasks that satisfy explicit agent-readiness criteria.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"agentReady": True},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_active_this_iteration",
        "name": "Active this iteration",
        "description": "Active tasks in the selected iteration.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"status": "active"},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_verification_required",
        "name": "Verification required",
        "description": "Resolved tasks waiting for independent verification.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"status": "resolved"},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "tasks_executing",
        "name": "Executing",
        "description": "Active work requiring execution supervision.",
        "view_type": SavedViewType.TASKS.value,
        "filters_json": {"status": "active"},
        "sort_json": {"sortKey": "priority"},
    },
    {
        "seed_key": "triage_agent_discovery",
        "name": "Agent discoveries",
        "description": "Out-of-scope work reported by execution agents for PM review.",
        "view_type": SavedViewType.TRIAGE.value,
        "filters_json": {"active": True, "source": "agent-discovery"},
    },
    {
        "seed_key": "projects_at_risk",
        "name": "At risk projects",
        "description": "Projects with at-risk health.",
        "view_type": SavedViewType.PROJECTS.value,
        "filters_json": {"health": "at_risk"},
    },
]

DASHBOARD_CARD_SEED_ORDER = [
    "tasks_unassigned",
    "tasks_blocked",
    "tasks_overdue",
    "tasks_high_priority",
    "tasks_ready_for_agent",
    "tasks_active_this_iteration",
    "triage_needs_triage",
    "projects_at_risk",
]
DASHBOARD_CARD_SEED_INDEX = {
    seed_key: index for index, seed_key in enumerate(DASHBOARD_CARD_SEED_ORDER)
}


class SavedViewService:
    """Service for saved view CRUD and compatibility-safe read models."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _query(self) -> Select:
        """Build the base saved view query."""
        return select(SavedView)

    def _require_personal_creator(self, scope: SavedViewScope | str, session_id: Optional[int]) -> None:
        if self._enum_value(scope) == SavedViewScope.PERSONAL.value and session_id is None:
            raise SavedViewValidationError("Personal saved views require created_by_session_id")

    def _require_object(self, value: Any, field_name: str) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise SavedViewValidationError(f"{field_name} must be a JSON object")
        return value

    def _normalize_nullable_int(
        self,
        value: Any,
        field_name: str,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
    ) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{field_name} must be an integer or null")
        if minimum is not None and value < minimum:
            raise ValueError(f"{field_name} must be at least {minimum}")
        if maximum is not None and value > maximum:
            raise ValueError(f"{field_name} must be at most {maximum}")
        return value

    def _normalize_nullable_bool(self, value: Any, field_name: str) -> Optional[bool]:
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean or null")
        return value

    def _normalize_bool(self, value: Any, field_name: str) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"{field_name} must be a boolean")
        return value

    def _normalize_string(self, value: Any, field_name: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        return value

    def _normalize_enum_string_or_empty(
        self,
        value: Any,
        field_name: str,
        allowed_values: set[str],
    ) -> str:
        if value is None or value == "":
            return ""
        if not isinstance(value, str) or value not in allowed_values:
            allowed = ", ".join(sorted(allowed_values))
            raise ValueError(f"{field_name} must be one of {allowed}, or empty")
        return value

    def _normalize_date_string(self, value: Any, field_name: str) -> str:
        if value == "":
            return ""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a YYYY-MM-DD string or empty")
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(f"{field_name} must be a YYYY-MM-DD string or empty") from exc
        return value

    def _normalize_string_list(self, value: Any, field_name: str) -> list[str]:
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise ValueError(f"{field_name} must be a list of strings")
        return value

    def _normalize_task_filters(self, filters: dict[str, Any]) -> tuple[dict[str, Any], bool, Optional[str]]:
        normalized = dict(TASK_FILTER_DEFAULTS)
        try:
            if "assigneeId" in filters:
                normalized["assigneeId"] = self._normalize_nullable_int(filters["assigneeId"], "assigneeId")
            if "projectId" in filters:
                normalized["projectId"] = self._normalize_nullable_int(filters["projectId"], "projectId")
            if "priority" in filters:
                normalized["priority"] = self._normalize_nullable_int(filters["priority"], "priority", 1, 10)
            if "status" in filters:
                status = filters["status"]
                if status is None:
                    normalized["status"] = None
                elif isinstance(status, str) and status in TASK_STATUS_VALUES:
                    normalized["status"] = status
                else:
                    raise ValueError("status must be one of planned, active, resolved, closed, or null")
            if "hasDependency" in filters:
                normalized["hasDependency"] = self._normalize_nullable_bool(filters["hasDependency"], "hasDependency")
            if "isOverdue" in filters:
                normalized["isOverdue"] = self._normalize_nullable_bool(filters["isOverdue"], "isOverdue")
            if "agentReady" in filters:
                normalized["agentReady"] = self._normalize_nullable_bool(filters["agentReady"], "agentReady")
            if "planningIssue" in filters:
                planning_issue = filters["planningIssue"]
                if planning_issue is None:
                    normalized["planningIssue"] = None
                elif (
                    isinstance(planning_issue, str)
                    and planning_issue in TASK_PLANNING_ISSUE_VALUES
                ):
                    normalized["planningIssue"] = planning_issue
                else:
                    allowed = ", ".join(sorted(TASK_PLANNING_ISSUE_VALUES))
                    raise ValueError(
                        f"planningIssue must be one of {allowed}, or null"
                    )

            for field_name in ("startDateFrom", "startDateTo", "endDateFrom", "endDateTo"):
                if field_name in filters:
                    normalized[field_name] = self._normalize_date_string(filters[field_name], field_name)

            for field_name in ("labelSlugs", "labelGroupKeys"):
                if field_name in filters:
                    normalized[field_name] = self._normalize_string_list(filters[field_name], field_name)
        except ValueError as exc:
            return {}, False, str(exc)

        return normalized, True, None

    def _normalize_project_filters(self, filters: dict[str, Any]) -> tuple[dict[str, Any], bool, Optional[str]]:
        normalized = dict(PROJECT_FILTER_DEFAULTS)
        try:
            if "search" in filters:
                normalized["search"] = self._normalize_string(filters["search"], "search")
            if "status" in filters:
                normalized["status"] = self._normalize_enum_string_or_empty(
                    filters["status"],
                    "status",
                    PROJECT_STATUS_VALUES,
                )
            if "health" in filters:
                normalized["health"] = self._normalize_enum_string_or_empty(
                    filters["health"],
                    "health",
                    PROJECT_HEALTH_VALUES,
                )
        except ValueError as exc:
            return {}, False, str(exc)

        return normalized, True, None

    def _normalize_triage_filters(self, filters: dict[str, Any]) -> tuple[dict[str, Any], bool, Optional[str]]:
        normalized = dict(TRIAGE_FILTER_DEFAULTS)
        try:
            if "active" in filters:
                normalized["active"] = self._normalize_bool(filters["active"], "active")
            if "statuses" in filters:
                statuses = self._normalize_string_list(filters["statuses"], "statuses")
                invalid_statuses = [status for status in statuses if status not in TRIAGE_STATUS_VALUES]
                if invalid_statuses:
                    allowed = ", ".join(sorted(TRIAGE_STATUS_VALUES))
                    raise ValueError(f"statuses must contain only {allowed}")
                normalized["statuses"] = statuses
            if "q" in filters:
                normalized["q"] = self._normalize_string(filters["q"], "q")
            if "source" in filters:
                normalized["source"] = self._normalize_string(filters["source"], "source")
        except ValueError as exc:
            return {}, False, str(exc)

        return normalized, True, None

    def normalize_filters(
        self,
        view_type: SavedViewType | str,
        filters: Any,
    ) -> tuple[dict[str, Any], bool, Optional[str]]:
        """Normalize known filter fields and ignore unknown future keys."""
        if not isinstance(filters, dict):
            return {}, False, "filters_json must be a JSON object"

        view_type_value = self._enum_value(view_type)
        if view_type_value == SavedViewType.TASKS.value:
            return self._normalize_task_filters(filters)
        if view_type_value == SavedViewType.PROJECTS.value:
            return self._normalize_project_filters(filters)
        if view_type_value == SavedViewType.TRIAGE.value:
            return self._normalize_triage_filters(filters)

        return {}, False, "view_type must be one of tasks, projects, or triage"

    def normalize_sort(
        self,
        view_type: SavedViewType | str,
        sort_json: Any,
    ) -> tuple[dict[str, Any], bool, Optional[str]]:
        """Normalize sort settings for known view surfaces."""
        if not isinstance(sort_json, dict):
            return {}, False, "sort_json must be a JSON object"

        if self._enum_value(view_type) != SavedViewType.TASKS.value:
            return dict(sort_json), True, None

        if "sortKey" not in sort_json:
            return {}, True, None

        sort_key = sort_json["sortKey"]
        if not isinstance(sort_key, str) or sort_key not in TASK_SORT_VALUES:
            allowed = ", ".join(sorted(TASK_SORT_VALUES))
            return {}, False, f"sortKey must be one of {allowed}"

        return {"sortKey": sort_key}, True, None

    def _valid_object_or_empty(self, value: Any, field_name: str) -> tuple[dict[str, Any], Optional[str]]:
        if isinstance(value, dict):
            return dict(value), None
        return {}, f"{field_name} must be a JSON object"

    def _response_for_view(self, view: SavedView) -> SavedViewResponse:
        filters, filters_valid, filters_reason = self.normalize_filters(
            view.view_type,
            view.filters_json,
        )
        sort_json, sort_valid, sort_reason = self.normalize_sort(view.view_type, view.sort_json)
        columns_json, columns_reason = self._valid_object_or_empty(view.columns_json, "columns_json")
        invalid_reasons = [
            reason
            for reason in (
                filters_reason if not filters_valid else None,
                sort_reason if not sort_valid else None,
                columns_reason,
            )
            if reason
        ]

        return SavedViewResponse(
            id=view.id,
            name=view.name,
            description=view.description,
            seed_key=view.seed_key,
            view_type=view.view_type,
            scope=view.scope,
            filters_json=filters if filters_valid else {},
            sort_json=sort_json,
            columns_json=columns_json,
            created_by_session_id=view.created_by_session_id,
            schema_version=view.schema_version,
            is_valid=not invalid_reasons,
            invalid_reason="; ".join(invalid_reasons) if invalid_reasons else None,
            created_at=view.created_at,
            updated_at=view.updated_at,
        )

    async def get_by_id(self, view_id: int) -> Optional[SavedView]:
        """Get a saved view by ID."""
        result = await self.db.execute(self._query().where(SavedView.id == view_id))
        return result.scalar_one_or_none()

    def _normalized_system_definition(self, definition: dict[str, Any]) -> dict[str, Any]:
        """Build a validated saved view row from a built-in definition."""
        view_type = definition["view_type"]
        filters_json, filters_valid, filters_reason = self.normalize_filters(
            view_type,
            definition.get("filters_json", {}),
        )
        if not filters_valid:
            raise SavedViewValidationError(filters_reason)

        sort_json, sort_valid, sort_reason = self.normalize_sort(
            view_type,
            definition.get("sort_json", {}),
        )
        if not sort_valid:
            raise SavedViewValidationError(sort_reason)

        columns_json = self._require_object(
            definition.get("columns_json", {}),
            "columns_json",
        )

        return {
            "seed_key": definition["seed_key"],
            "name": definition["name"],
            "description": definition.get("description"),
            "view_type": view_type,
            "scope": SavedViewScope.SYSTEM.value,
            "filters_json": filters_json,
            "sort_json": sort_json,
            "columns_json": columns_json,
            "created_by_session_id": None,
            "schema_version": definition.get("schema_version", 1),
        }

    async def seed_default_views(self) -> list[SavedView]:
        """Insert or refresh built-in system saved views."""
        result = await self.db.execute(
            select(SavedView).where(SavedView.seed_key.is_not(None))
        )
        views_by_seed = {
            view.seed_key: view
            for view in result.scalars().all()
            if view.seed_key
        }
        touched: list[SavedView] = []

        for definition in DEFAULT_SAVED_VIEW_DEFINITIONS:
            row_data = self._normalized_system_definition(definition)
            view = views_by_seed.get(row_data["seed_key"])
            if view is None:
                view = SavedView(**row_data)
                self.db.add(view)
                views_by_seed[row_data["seed_key"]] = view
                touched.append(view)
                continue

            changed = False
            for field, value in row_data.items():
                if getattr(view, field) != value:
                    setattr(view, field, value)
                    changed = True
            if changed:
                touched.append(view)

        if not touched:
            return []

        await self.db.commit()
        for view in touched:
            await self.db.refresh(view)
        return touched

    def _target_path_for_view(self, view: SavedViewResponse) -> str:
        """Return the frontend route that opens a saved view."""
        if view.view_type == SavedViewType.TASKS.value:
            return f"/tasks?view={view.id}"
        if view.view_type == SavedViewType.TRIAGE.value:
            return f"/triage?view={view.id}"
        return f"/projects?view={view.id}"

    async def _active_label_group_slugs(self) -> dict[str, set[str]]:
        """Map active label group keys to their active label slugs."""
        from app.services.label_service import LabelService

        groups = await LabelService(self.db).list_groups(include_inactive=False)
        return {
            group.key: {label.slug for label in group.labels}
            for group in groups
        }

    def _task_child_filters_for_assignee(self, filters: dict[str, Any]) -> dict[str, Any]:
        child_filters = dict(filters)
        child_filters.update({
            "priority": None,
            "status": None,
            "hasDependency": None,
            "isOverdue": None,
            "agentReady": None,
            "startDateFrom": "",
            "startDateTo": "",
            "endDateFrom": "",
            "endDateTo": "",
        })
        return child_filters

    def _task_child_filters_for_project(self, filters: dict[str, Any]) -> dict[str, Any]:
        child_filters = self._task_child_filters_for_assignee(filters)
        child_filters["assigneeId"] = None
        return child_filters

    def _task_has_any_tag(self, task: Any, selected_tags: set[str]) -> bool:
        if not selected_tags:
            return True
        return any(tag in selected_tags for tag in (task.tags or []))

    def _task_date_value(self, value: Any) -> str:
        return value.isoformat() if hasattr(value, "isoformat") else str(value)

    def _task_matches_planning_issue(
        self,
        task: Any,
        planning_issue: Optional[str],
    ) -> bool:
        if planning_issue is None:
            return True
        if task.is_deferred or task.is_composite or task.children:
            return False

        effort_days = task.effort_days
        missing_effort = (
            isinstance(effort_days, bool)
            or not isinstance(effort_days, (int, float))
            or not isfinite(effort_days)
            or effort_days <= 0
        )
        unassigned = task.assignee is None

        if planning_issue == "unassigned":
            return unassigned
        if planning_issue == "missing-effort":
            return missing_effort
        return unassigned or missing_effort

    def _task_matches_filters(
        self,
        task: Any,
        filters: dict[str, Any],
        label_group_slugs: dict[str, set[str]],
    ) -> bool:
        if not self._task_matches_planning_issue(
            task,
            filters.get("planningIssue"),
        ):
            return False

        assignee_id = filters.get("assigneeId")
        if assignee_id is not None:
            is_unassigned_filter = assignee_id == -1
            matches_self = (
                task.assignee is None
                if is_unassigned_filter
                else task.assignee is not None and task.assignee.id == assignee_id
            )
            child_filters = self._task_child_filters_for_assignee(filters)
            has_matching_assignee = matches_self or any(
                self._task_matches_filters(child, child_filters, label_group_slugs)
                for child in task.children
            )
            if not has_matching_assignee:
                return False

        project_id = filters.get("projectId")
        if project_id is not None:
            matches_self = task.project_id == project_id
            child_filters = self._task_child_filters_for_project(filters)
            has_matching_project = matches_self or any(
                self._task_matches_filters(child, child_filters, label_group_slugs)
                for child in task.children
            )
            if not has_matching_project:
                return False

        if filters.get("priority") is not None and task.priority != filters["priority"]:
            return False

        if filters.get("status") is not None and task.status != filters["status"]:
            return False

        if filters.get("hasDependency") is not None:
            has_dependencies = len(task.dependencies) > 0
            if filters["hasDependency"] != has_dependencies:
                return False

        if filters.get("isOverdue") is not None and task.is_overdue != filters["isOverdue"]:
            return False

        if filters.get("agentReady") is not None and task.agent_readiness.is_ready != filters["agentReady"]:
            return False

        if filters.get("startDateFrom") and task.start_date is not None:
            if self._task_date_value(task.start_date) < filters["startDateFrom"]:
                return False
        if filters.get("startDateTo") and task.start_date is not None:
            if self._task_date_value(task.start_date) > filters["startDateTo"]:
                return False
        if filters.get("endDateFrom") and task.end_date is not None:
            if self._task_date_value(task.end_date) < filters["endDateFrom"]:
                return False
        if filters.get("endDateTo") and task.end_date is not None:
            if self._task_date_value(task.end_date) > filters["endDateTo"]:
                return False

        label_slugs = set(filters.get("labelSlugs", []))
        if label_slugs and not self._task_has_any_tag(task, label_slugs):
            return False

        label_group_keys = filters.get("labelGroupKeys", [])
        if label_group_keys:
            selected_group_slugs = set().union(
                *(label_group_slugs.get(group_key, set()) for group_key in label_group_keys)
            )
            if not selected_group_slugs:
                return False
            if not self._task_has_any_tag(task, selected_group_slugs):
                return False

        return True

    def _task_filter_includes_row(
        self,
        task: Any,
        filters: dict[str, Any],
        label_group_slugs: dict[str, set[str]],
    ) -> bool:
        if self._task_matches_filters(task, filters, label_group_slugs):
            return True
        return any(
            self._task_filter_includes_row(child, filters, label_group_slugs)
            for child in task.children
        )

    async def _count_task_dashboard_view(
        self,
        filters: dict[str, Any],
        iteration: Iteration,
    ) -> int:
        from app.services.task_service import TaskService

        task_service = TaskService(self.db)
        root_tasks = await task_service.get_by_iteration(iteration.id)
        label_group_slugs = await self._active_label_group_slugs()
        task_service.agent_capability_slugs = label_group_slugs.get("capability")
        task_responses = [
            task_service.task_to_response(task, iteration.end_date)
            for task in root_tasks
        ]
        return sum(
            1
            for task in task_responses
            if self._task_filter_includes_row(task, filters, label_group_slugs)
        )

    async def _count_project_dashboard_view(self, filters: dict[str, Any]) -> int:
        from app.services.project_service import ProjectService

        projects = await ProjectService(self.db).list_projects()
        search = filters.get("search", "").strip().lower()
        status_filter = filters.get("status", "")
        health_filter = filters.get("health", "")

        return sum(
            1
            for project in projects
            if (
                (not search or search in project.name.lower())
                and (not status_filter or project.status == status_filter)
                and (not health_filter or project.health == health_filter)
            )
        )

    async def _count_triage_dashboard_view(self, filters: dict[str, Any]) -> int:
        from app.services.triage_service import TriageService

        return await TriageService(self.db).count_items(
            active=filters.get("active", True),
            statuses=filters.get("statuses") or None,
            q=filters.get("q") or None,
            source=filters.get("source") or None,
        )

    async def _dashboard_count(
        self,
        view: SavedViewResponse,
        iteration: Iteration,
    ) -> int:
        if view.view_type == SavedViewType.TASKS.value:
            return await self._count_task_dashboard_view(view.filters_json, iteration)
        if view.view_type == SavedViewType.PROJECTS.value:
            return await self._count_project_dashboard_view(view.filters_json)
        if view.view_type == SavedViewType.TRIAGE.value:
            return await self._count_triage_dashboard_view(view.filters_json)
        return 0

    async def list_dashboard_cards(
        self,
        iteration_id: int,
        session_id: Optional[int],
    ) -> Optional[list[SavedViewDashboardCardResponse]]:
        """Build system saved-view dashboard cards visible to a session."""
        iteration_result = await self.db.execute(
            select(Iteration).where(Iteration.id == iteration_id)
        )
        iteration = iteration_result.scalar_one_or_none()
        if iteration is None:
            return None

        result = await self.db.execute(
            self._query().where(
                SavedView.scope == SavedViewScope.SYSTEM.value,
                SavedView.seed_key.in_(DASHBOARD_CARD_SEED_ORDER),
            )
        )
        views = [
            view
            for view in result.scalars().all()
            if self._is_visible_to_session(view, session_id)
        ]
        views.sort(key=lambda view: DASHBOARD_CARD_SEED_INDEX.get(view.seed_key or "", 999))

        cards: list[SavedViewDashboardCardResponse] = []
        for view_model in views:
            view = self._response_for_view(view_model)
            count = await self._dashboard_count(view, iteration) if view.is_valid else 0
            cards.append(
                SavedViewDashboardCardResponse(
                    saved_view_id=view.id,
                    seed_key=view.seed_key or "",
                    name=view.name,
                    description=view.description,
                    view_type=view.view_type,
                    scope=view.scope,
                    count=count,
                    target_path=self._target_path_for_view(view),
                    is_valid=view.is_valid,
                    invalid_reason=view.invalid_reason,
                )
            )

        return cards

    async def create(self, data: SavedViewCreate) -> SavedView:
        """Create a saved view after scope and filter validation."""
        self._require_personal_creator(data.scope, data.created_by_session_id)
        self._require_object(data.filters_json, "filters_json")
        self._require_object(data.sort_json, "sort_json")
        self._require_object(data.columns_json, "columns_json")
        filters_json, is_valid, invalid_reason = self.normalize_filters(
            data.view_type,
            data.filters_json,
        )
        if not is_valid:
            raise SavedViewValidationError(invalid_reason)
        sort_json, sort_valid, sort_reason = self.normalize_sort(
            data.view_type,
            data.sort_json,
        )
        if not sort_valid:
            raise SavedViewValidationError(sort_reason)

        saved_view_data = data.model_dump()
        saved_view_data["view_type"] = self._enum_value(saved_view_data["view_type"])
        saved_view_data["scope"] = self._enum_value(saved_view_data["scope"])
        saved_view_data["filters_json"] = filters_json
        saved_view_data["sort_json"] = sort_json
        view = SavedView(**saved_view_data)
        self.db.add(view)
        await self.db.commit()
        await self.db.refresh(view)
        return view

    async def update(self, view_id: int, data: SavedViewUpdate) -> Optional[SavedView]:
        """Apply a saved view update after scope and filter validation."""
        view = await self.get_by_id(view_id)
        if not view:
            return None

        update_data = data.model_dump(exclude_unset=True)
        next_scope = update_data.get("scope", view.scope)
        next_session_id = update_data.get("created_by_session_id", view.created_by_session_id)
        next_view_type = update_data.get("view_type", view.view_type)
        self._require_personal_creator(next_scope, next_session_id)

        if "filters_json" in update_data or "view_type" in update_data:
            filters_input = update_data.get("filters_json", view.filters_json)
            filters_json, is_valid, invalid_reason = self.normalize_filters(
                next_view_type,
                filters_input,
            )
            if not is_valid:
                raise SavedViewValidationError(invalid_reason)
            update_data["filters_json"] = filters_json

        if "sort_json" in update_data or "view_type" in update_data:
            sort_input = update_data.get("sort_json", view.sort_json)
            sort_json, sort_valid, sort_reason = self.normalize_sort(
                next_view_type,
                sort_input,
            )
            if not sort_valid:
                raise SavedViewValidationError(sort_reason)
            update_data["sort_json"] = sort_json

        if "columns_json" in update_data:
            update_data["columns_json"] = self._require_object(update_data["columns_json"], "columns_json")

        for field, value in update_data.items():
            setattr(view, field, self._enum_value(value))

        await self.db.commit()
        await self.db.refresh(view)
        return view

    async def list_visible(
        self,
        view_type: SavedViewType | str,
        session_id: Optional[int],
    ) -> Sequence[SavedViewResponse]:
        """List views visible to a session for a given surface."""
        view_type_value = self._enum_value(view_type)
        visibility_filter = SavedView.scope.in_([
            SavedViewScope.SHARED.value,
            SavedViewScope.SYSTEM.value,
        ])
        if session_id is not None:
            visibility_filter = or_(
                visibility_filter,
                (SavedView.scope == SavedViewScope.PERSONAL.value)
                & (SavedView.created_by_session_id == session_id),
            )

        result = await self.db.execute(
            self._query()
            .where(SavedView.view_type == view_type_value, visibility_filter)
            .order_by(SavedView.scope, SavedView.name, SavedView.id)
        )
        return [self._response_for_view(view) for view in result.scalars().all()]

    def _is_visible_to_session(self, view: SavedView, session_id: Optional[int]) -> bool:
        if view.scope in (SavedViewScope.SHARED.value, SavedViewScope.SYSTEM.value):
            return True
        return session_id is not None and view.created_by_session_id == session_id

    def _can_write(self, view: SavedView, session_id: Optional[int]) -> bool:
        return (
            view.scope != SavedViewScope.SYSTEM.value
            and session_id is not None
            and view.created_by_session_id == session_id
        )

    async def get_visible_model(
        self,
        view_id: int,
        session_id: Optional[int],
    ) -> Optional[SavedView]:
        """Get a saved view model only when it is visible to the session."""
        view = await self.get_by_id(view_id)
        if not view or not self._is_visible_to_session(view, session_id):
            return None
        return view

    async def get_visible_by_id(
        self,
        view_id: int,
        session_id: Optional[int],
    ) -> Optional[SavedViewResponse]:
        """Get a saved view response only when it is visible to the session."""
        view = await self.get_visible_model(view_id, session_id)
        return self._response_for_view(view) if view else None

    def _reject_system_scope(self, scope: SavedViewScope | str) -> None:
        if self._enum_value(scope) == SavedViewScope.SYSTEM.value:
            raise SavedViewPermissionError("System saved views are read-only")

    async def create_for_session(
        self,
        data: SavedViewCreateRequest,
        session_id: int,
    ) -> SavedViewResponse:
        """Create a user-owned saved view from a public API payload."""
        self._reject_system_scope(data.scope)
        view = await self.create(
            SavedViewCreate(
                **data.model_dump(),
                created_by_session_id=session_id,
            )
        )
        return self._response_for_view(view)

    async def update_for_session(
        self,
        view_id: int,
        data: SavedViewUpdateRequest,
        session_id: int,
    ) -> Optional[SavedViewResponse]:
        """Update a saved view when the caller owns it."""
        view = await self.get_visible_model(view_id, session_id)
        if not view:
            return None
        if not self._can_write(view, session_id):
            raise SavedViewPermissionError("Only the creating session can update this saved view")
        if data.scope is not None:
            self._reject_system_scope(data.scope)

        update_data = data.model_dump(exclude_unset=True)
        if self._enum_value(update_data.get("scope")) == SavedViewScope.PERSONAL.value:
            update_data["created_by_session_id"] = view.created_by_session_id

        updated = await self.update(view_id, SavedViewUpdate(**update_data))
        return self._response_for_view(updated) if updated else None

    async def delete_for_session(
        self,
        view_id: int,
        session_id: int,
    ) -> bool:
        """Delete a saved view when the caller owns it."""
        view = await self.get_visible_model(view_id, session_id)
        if not view:
            return False
        if not self._can_write(view, session_id):
            raise SavedViewPermissionError("Only the creating session can delete this saved view")

        await self.db.delete(view)
        await self.db.commit()
        return True

    async def duplicate_for_session(
        self,
        view_id: int,
        data: SavedViewDuplicateRequest,
        session_id: int,
    ) -> Optional[SavedViewResponse]:
        """Create a user-owned copy of any valid visible saved view."""
        source = await self.get_visible_model(view_id, session_id)
        if not source:
            return None
        self._reject_system_scope(data.scope)

        source_response = self._response_for_view(source)
        if not source_response.is_valid:
            raise SavedViewValidationError("Cannot duplicate an invalid saved view")

        name = data.name or f"Copy of {source.name}"
        description = (
            data.description
            if "description" in data.model_fields_set
            else source.description
        )
        view = await self.create(
            SavedViewCreate(
                name=name[:255],
                description=description,
                view_type=SavedViewType(source.view_type),
                scope=data.scope,
                filters_json=source_response.filters_json,
                sort_json=source_response.sort_json,
                columns_json=source_response.columns_json,
                created_by_session_id=session_id,
                schema_version=source.schema_version,
            )
        )
        return self._response_for_view(view)
