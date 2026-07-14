"""Task text import, export, and triage intake workflows."""

import json
from typing import Optional, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.triage import TriageItem, TriageItemStatus
from app.schemas.task import TaskImportDestination
from app.services.snapshot_service import SnapshotService

if TYPE_CHECKING:
    from app.services.task_service import TaskService


class TaskImportService:
    """Own task text parsing, assignee resolution, and import persistence."""

    def __init__(self, db: AsyncSession, task_service: "TaskService"):
        self.db = db
        self.task_service = task_service

    @staticmethod
    def _parsed_task_has_complete_planning_fields(parsed_task) -> bool:
        """Return whether a parsed new row has enough detail to create a task."""
        return (
            parsed_task.priority is not None
            and parsed_task.assignee_name is not None
            and parsed_task.effort_days is not None
        )

    @staticmethod
    def _normalize_import_assignee_name(value: Optional[str]) -> Optional[str]:
        """Normalize assignee tokens from task text imports."""
        text = (value or "").strip()
        if not text or text.casefold() == "unassigned":
            return None
        return text

    async def _get_team_member_lookup(
        self,
        iteration_id: int,
    ) -> tuple[dict[str, int], set[str]]:
        """Build a team member name to ID lookup for imports."""
        from app.services.team_service import TeamService

        team_members = await TeamService(self.db).get_by_iteration(iteration_id)
        by_name: dict[str, list[int]] = {}
        for member in team_members:
            key = member.name.strip().casefold()
            if key:
                by_name.setdefault(key, []).append(member.id)
        ambiguous_names = {
            key for key, member_ids in by_name.items() if len(member_ids) > 1
        }
        lookup = {
            key: member_ids[0]
            for key, member_ids in by_name.items()
            if len(member_ids) == 1
        }
        return lookup, ambiguous_names

    def _resolve_import_assignee_id(
        self,
        assignee_name: Optional[str],
        name_to_member_id: dict[str, int],
        ambiguous_names: set[str],
        *,
        line_label: str,
    ) -> Optional[int]:
        """Resolve an executable task import assignee inside the target iteration."""
        normalized = self._normalize_import_assignee_name(assignee_name)
        if normalized is None:
            return None

        key = normalized.casefold()
        if key in ambiguous_names:
            raise ValueError(
                f"{line_label}: Assignee '{normalized}' is ambiguous in this iteration"
            )
        assignee_id = name_to_member_id.get(key)
        if assignee_id is None:
            raise ValueError(
                f"{line_label}: Assignee '{normalized}' is not assigned to this iteration"
            )
        return assignee_id

    @staticmethod
    def _task_from_parsed_import(
        iteration_id: int,
        parsed_task,
        assignee_id: Optional[int],
        sort_order: int,
        project_id: Optional[int] = None,
    ) -> Task:
        """Build a task model from parsed import data."""
        priority = parsed_task.priority if parsed_task.priority is not None else 5
        effort_days = (
            parsed_task.effort_days if parsed_task.effort_days is not None else 1.0
        )
        return Task(
            iteration_id=iteration_id,
            project_id=project_id,
            parent_id=None,
            title=parsed_task.title,
            description=parsed_task.description,
            priority=priority,
            effort_days=effort_days,
            effort_hours=effort_days * 8.0,
            assignee_id=assignee_id,
            status="planned",
            is_optional=False,
            is_deferred=False,
            tags=json.dumps([]),
            sort_order=sort_order,
        )

    @staticmethod
    def _triage_item_from_parsed_import(
        iteration_id: int,
        parsed_task,
        source: str,
        labels: list[str],
    ) -> TriageItem:
        """Build a triage item model from parsed import data."""
        return TriageItem(
            title=parsed_task.title,
            description=parsed_task.description,
            source=source,
            status=TriageItemStatus.NEW.value,
            priority_hint=parsed_task.priority,
            assignee_hint=parsed_task.assignee_name,
            iteration_hint_id=iteration_id,
            labels=labels,
        )

    async def _record_triage_import_events(
        self,
        triage_items: list[TriageItem],
    ) -> None:
        """Record audit events for triage items created from task import paths."""
        for item in triage_items:
            await self.task_service.record_task_event(
                None,
                "triage_item_created",
                {
                    "triage_item_id": item.id,
                    "title": item.title,
                    "status": item.status,
                    "source": item.source,
                    "external_key": item.external_key,
                },
            )

    async def import_tasks(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
    ) -> tuple[list[Task], list[TriageItem]]:
        """Import task text into executable tasks, triage items, or both by policy."""
        from app.utils.import_parser import parse_tasks_text

        iteration_project_id = await self.task_service._iteration_project_id(
            iteration_id
        )
        await SnapshotService(self.db).create_snapshot(
            iteration_id,
            "before_import_tasks",
        )

        created_tasks: list[Task] = []
        created_triage_items: list[TriageItem] = []
        name_to_member_id, ambiguous_names = await self._get_team_member_lookup(
            iteration_id
        )
        next_sort_order = await self.task_service._get_next_root_sort_order(
            iteration_id
        )

        for parsed in parse_tasks_text(text):
            should_create_triage = destination == "triage" or (
                destination == "auto"
                and not self._parsed_task_has_complete_planning_fields(parsed)
            )
            if should_create_triage:
                triage_item = self._triage_item_from_parsed_import(
                    iteration_id,
                    parsed,
                    "task_import",
                    ["task-import"],
                )
                self.db.add(triage_item)
                created_triage_items.append(triage_item)
                continue

            assignee_id = self._resolve_import_assignee_id(
                parsed.assignee_name,
                name_to_member_id,
                ambiguous_names,
                line_label=f"Task '{parsed.title}'",
            )
            task = self._task_from_parsed_import(
                iteration_id,
                parsed,
                assignee_id,
                next_sort_order,
                project_id=iteration_project_id,
            )
            self.db.add(task)
            created_tasks.append(task)
            next_sort_order += 1

        await self.db.flush()
        await self._record_triage_import_events(created_triage_items)
        await self.db.commit()
        for task in created_tasks:
            await self.db.refresh(task)
        for triage_item in created_triage_items:
            await self.db.refresh(triage_item)
        return created_tasks, created_triage_items

    async def get_tasks_as_text(self, iteration_id: int) -> str:
        """Serialize every task in an iteration to the editable text format."""
        from app.utils.import_parser import serialize_tasks_to_text

        await self.task_service.require_iteration_exists(iteration_id)
        tasks = await self.task_service.get_all_tasks(iteration_id)
        return serialize_tasks_to_text(list(tasks))

    async def bulk_update_tasks_from_text(
        self,
        iteration_id: int,
        text: str,
        destination: TaskImportDestination = "tasks",
    ) -> tuple[list[Task], list[TriageItem]]:
        """Update ID-tagged tasks and create new tasks or triage items from text."""
        from app.utils.import_parser import parse_tasks_text

        iteration_project_id = await self.task_service._iteration_project_id(
            iteration_id
        )
        await SnapshotService(self.db).create_snapshot(
            iteration_id,
            "before_bulk_update_tasks",
        )

        processed_tasks: list[Task] = []
        created_triage_items: list[TriageItem] = []
        name_to_member_id, ambiguous_names = await self._get_team_member_lookup(
            iteration_id
        )
        next_sort_order = await self.task_service._get_next_root_sort_order(
            iteration_id
        )

        for parsed in parse_tasks_text(text):
            priority = parsed.priority if parsed.priority is not None else 5
            effort_days = (
                parsed.effort_days if parsed.effort_days is not None else 1.0
            )
            if parsed.id:
                assignee_id = self._resolve_import_assignee_id(
                    parsed.assignee_name,
                    name_to_member_id,
                    ambiguous_names,
                    line_label=f"Task '{parsed.title}'",
                )
                task = await self.task_service.get_by_id(parsed.id)
                if task and task.iteration_id == iteration_id:
                    if iteration_project_id is not None:
                        if task.project_id not in (None, iteration_project_id):
                            raise ValueError(
                                "Task project must match the scoped iteration project."
                            )
                        compatible = await self.task_service._milestone_matches_project(
                            task.milestone_id,
                            iteration_project_id,
                        )
                        if task.milestone_id is not None and not compatible:
                            raise ValueError(
                                "Task milestone must belong to the scoped iteration project."
                            )
                        task.project_id = iteration_project_id
                    task.title = parsed.title
                    if parsed.description is not None:
                        task.description = parsed.description
                    task.priority = priority
                    task.effort_days = effort_days
                    task.effort_hours = effort_days * 8.0
                    task.assignee_id = assignee_id
                    processed_tasks.append(task)
                continue

            should_create_triage = destination == "triage" or (
                destination == "auto"
                and not self._parsed_task_has_complete_planning_fields(parsed)
            )
            if should_create_triage:
                triage_item = self._triage_item_from_parsed_import(
                    iteration_id,
                    parsed,
                    "task_text_editor",
                    ["task-text-editor"],
                )
                self.db.add(triage_item)
                created_triage_items.append(triage_item)
                continue

            assignee_id = self._resolve_import_assignee_id(
                parsed.assignee_name,
                name_to_member_id,
                ambiguous_names,
                line_label=f"Task '{parsed.title}'",
            )
            task = self._task_from_parsed_import(
                iteration_id,
                parsed,
                assignee_id,
                next_sort_order,
                project_id=iteration_project_id,
            )
            self.db.add(task)
            processed_tasks.append(task)
            next_sort_order += 1

        await self.db.flush()
        await self._record_triage_import_events(created_triage_items)
        await self.db.commit()
        for task in processed_tasks:
            await self.db.refresh(task)
        for triage_item in created_triage_items:
            await self.db.refresh(triage_item)
        return processed_tasks, created_triage_items
