"""Iteration service with business logic."""
import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional, Sequence

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.iteration import Iteration
from app.models.project import Project, ProjectMilestone
from app.models.task import Task, TaskStatus as TaskStatusModel
from app.models.team_member import TeamMember
from app.query_limits import (
    CollectionLimitExceededError,
    MAX_ITERATION_LIST_ITEMS,
    MAX_ITERATION_TREE_TASKS,
)
from app.schemas.iteration import (
    IterationCreate,
    IterationProjectSummary,
    IterationResponse,
    IterationSeriesCreate,
    IterationSummary,
    IterationUpdate,
)
from app.services.calendar_service import CalendarService

MAX_SERIES_ITERATIONS = 100


@dataclass(frozen=True)
class IterationSeriesItem:
    """Computed iteration row for a series create request."""
    name: str
    start_date: date
    end_date: date


class IterationService:
    """Service for iteration operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _response_project(
        self,
        iteration: Iteration,
    ) -> Optional[IterationProjectSummary]:
        """Return compact project scope data for iteration responses."""
        if iteration.project is None:
            return None
        return IterationProjectSummary.model_validate(iteration.project)

    def to_response(self, iteration: Iteration) -> IterationResponse:
        """Build a public iteration response with computed calendar days."""
        calendar_service = CalendarService(self.db)
        working_days_info = calendar_service.calculate_working_days(
            iteration.calendar, iteration.start_date, iteration.end_date
        )
        return IterationResponse(
            id=iteration.id,
            name=iteration.name,
            calendar_id=iteration.calendar_id,
            project_id=iteration.project_id,
            project=self._response_project(iteration),
            start_date=iteration.start_date,
            end_date=iteration.end_date,
            manager_email=iteration.manager_email,
            working_days=working_days_info.working_days,
        )

    async def _project_exists(self, project_id: int) -> bool:
        """Return whether a project exists without loading the full project graph."""
        result = await self.db.execute(
            select(Project.id).where(Project.id == project_id)
        )
        return result.scalar_one_or_none() is not None

    async def _require_project_exists(self, project_id: Optional[int]) -> None:
        """Validate an optional iteration project scope."""
        if project_id is not None and not await self._project_exists(project_id):
            raise ValueError(f"Project with id {project_id} not found")

    async def _calendar_id_for_create(
        self,
        calendar_id: Optional[int],
        *,
        commit: bool = True,
    ) -> int:
        """Return an explicit or default calendar id for new iterations."""
        calendar_service = CalendarService(self.db)
        if calendar_id is None:
            default_calendar = await calendar_service.get_or_create_default(
                commit=commit
            )
            return default_calendar.id

        calendar = await calendar_service.get_by_id(calendar_id)
        if calendar is None:
            raise ValueError(f"Calendar with id {calendar_id} not found")
        return calendar.id

    def _validate_date_range(self, start_date: date, end_date: date) -> None:
        """Reject inverted iteration periods."""
        if start_date > end_date:
            raise ValueError("start_date must be before or equal to end_date")

    def _series_name(self, base_name: str, index: int) -> str:
        """Increment a trailing number, or append a sequence number."""
        cleaned = base_name.strip()
        match = re.match(r"^(.*?)(\d+)$", cleaned)
        if match:
            prefix, number = match.groups()
            width = len(number)
            return f"{prefix}{int(number) + index:0{width}d}"
        return f"{cleaned} {index + 1}"

    def _series_items(self, data: IterationSeriesCreate) -> list[IterationSeriesItem]:
        """Compute all rows for a back-to-back iteration series before writing."""
        if not data.base_name.strip():
            raise ValueError("base_name is required")

        items: list[IterationSeriesItem] = []
        current_start = data.start_date

        if data.stop.mode == "count":
            total = data.stop.count or 0
            for index in range(total):
                current_end = current_start + timedelta(days=data.duration_days - 1)
                items.append(
                    IterationSeriesItem(
                        name=self._series_name(data.base_name, index),
                        start_date=current_start,
                        end_date=current_end,
                    )
                )
                current_start = current_end + timedelta(days=1)
            return items

        until_date = data.stop.until_date
        if until_date is None:
            raise ValueError("until_date is required when mode is 'until_date'")
        if until_date < data.start_date:
            raise ValueError("until_date must be on or after start_date")

        while current_start <= until_date:
            if len(items) >= MAX_SERIES_ITERATIONS:
                raise ValueError(
                    f"Iteration series cannot create more than {MAX_SERIES_ITERATIONS} iterations"
                )
            current_end = current_start + timedelta(days=data.duration_days - 1)
            items.append(
                IterationSeriesItem(
                    name=self._series_name(data.base_name, len(items)),
                    start_date=current_start,
                    end_date=current_end,
                )
            )
            current_start = current_end + timedelta(days=1)

        return items

    async def _milestone_matches_project(
        self,
        milestone_id: Optional[int],
        project_id: int,
    ) -> bool:
        """Return whether a milestone belongs to a project."""
        if milestone_id is None:
            return True
        result = await self.db.execute(
            select(ProjectMilestone.project_id).where(ProjectMilestone.id == milestone_id)
        )
        return result.scalar_one_or_none() == project_id

    async def _reconcile_tasks_for_project_scope(
        self,
        iteration: Iteration,
        new_project_id: Optional[int],
    ) -> None:
        """Apply or validate task project links when iteration scope changes."""
        if new_project_id is None:
            return

        result = await self.db.execute(
            select(Task)
            .where(Task.iteration_id == iteration.id)
            .order_by(Task.id.asc())
            .limit(MAX_ITERATION_TREE_TASKS + 1)
        )
        tasks = list(result.scalars().all())
        if len(tasks) > MAX_ITERATION_TREE_TASKS:
            raise CollectionLimitExceededError(
                "iteration project-scope update",
                MAX_ITERATION_TREE_TASKS,
            )
        tasks_to_update: list[Task] = []
        old_project_id = iteration.project_id

        for task in tasks:
            if task.project_id == new_project_id:
                if not await self._milestone_matches_project(task.milestone_id, new_project_id):
                    raise ValueError(
                        f"Task {task.id} milestone must belong to the scoped iteration project."
                    )
                continue

            can_rewrite = task.project_id is None or (
                old_project_id is not None and task.project_id == old_project_id
            )
            if not can_rewrite:
                raise ValueError(
                    f"Cannot scope iteration to project {new_project_id}; "
                    f"task {task.id} is linked to project {task.project_id}."
                )

            if not await self._milestone_matches_project(task.milestone_id, new_project_id):
                raise ValueError(
                    f"Task {task.id} milestone must belong to the scoped iteration project."
                )
            tasks_to_update.append(task)

        if not tasks_to_update:
            return

        from app.services.snapshot_service import SnapshotService
        from app.services.task_service import TaskService

        await SnapshotService(self.db).create_snapshot(
            iteration.id,
            "before_update_iteration_project_scope",
        )
        task_service = TaskService(self.db)
        for task in tasks_to_update:
            old_project_id = task.project_id
            task.project_id = new_project_id
            task.version += 1
            await task_service.record_task_event(
                task.id,
                "task_updated",
                {
                    "changes": {
                        "project_id": {
                            "old": old_project_id,
                            "new": new_project_id,
                        }
                    },
                    "version": task.version,
                    "iteration_project_scope_update": True,
                },
            )

    async def get_all(self) -> Sequence[Iteration]:
        """Preserve the small-workspace list contract and refuse overflow."""
        result = await self.db.execute(
            select(Iteration)
            .options(
                selectinload(Iteration.calendar),
                selectinload(Iteration.project),
            )
            .order_by(Iteration.start_date.desc(), Iteration.id.desc())
            .limit(MAX_ITERATION_LIST_ITEMS + 1)
        )
        iterations = list(result.scalars().all())
        if len(iterations) > MAX_ITERATION_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "iteration list",
                MAX_ITERATION_LIST_ITEMS,
            )
        return iterations

    async def get_page(
        self,
        *,
        limit: int,
        cursor_start_date: date | None = None,
        cursor_id: int | None = None,
    ) -> Sequence[Iteration]:
        """Return one stable keyset page in newest-first order."""

        if not 1 <= limit <= MAX_ITERATION_LIST_ITEMS:
            raise ValueError(
                f"limit must be between 1 and {MAX_ITERATION_LIST_ITEMS}"
            )
        if (cursor_start_date is None) != (cursor_id is None):
            raise ValueError("cursor_start_date and cursor_id must be provided together")

        query = (
            select(Iteration)
            .options(
                selectinload(Iteration.calendar),
                selectinload(Iteration.project),
            )
            .order_by(Iteration.start_date.desc(), Iteration.id.desc())
            .limit(limit)
        )
        if cursor_start_date is not None and cursor_id is not None:
            query = query.where(
                or_(
                    Iteration.start_date < cursor_start_date,
                    (
                        (Iteration.start_date == cursor_start_date)
                        & (Iteration.id < cursor_id)
                    ),
                )
            )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, iteration_id: int) -> Iteration | None:
        """Get iteration by ID with related data."""
        result = await self.db.execute(
            select(Iteration)
            .options(
                selectinload(Iteration.calendar),
                selectinload(Iteration.project),
            )
            .where(Iteration.id == iteration_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: IterationCreate, *, commit: bool = True) -> Iteration:
        """Create an iteration, optionally leaving commit ownership to the caller."""
        self._validate_date_range(data.start_date, data.end_date)
        await self._require_project_exists(data.project_id)
        calendar_id = await self._calendar_id_for_create(
            data.calendar_id,
            commit=commit,
        )
        iteration = Iteration(
            name=data.name,
            calendar_id=calendar_id,
            project_id=data.project_id,
            start_date=data.start_date,
            end_date=data.end_date,
            manager_email=data.manager_email,
        )
        self.db.add(iteration)
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(iteration)
        created = await self.get_by_id(iteration.id)
        if created is None:
            raise RuntimeError("Created iteration could not be reloaded")
        return created

    async def create_series(self, data: IterationSeriesCreate) -> list[Iteration]:
        """Create multiple back-to-back iterations as one operation."""
        items = self._series_items(data)
        if not items:
            raise ValueError("Iteration series must create at least one iteration")

        await self._require_project_exists(data.project_id)
        calendar_id = await self._calendar_id_for_create(data.calendar_id)

        iterations = [
            Iteration(
                name=item.name,
                calendar_id=calendar_id,
                project_id=data.project_id,
                start_date=item.start_date,
                end_date=item.end_date,
                manager_email=data.manager_email,
            )
            for item in items
        ]
        self.db.add_all(iterations)
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        created: list[Iteration] = []
        for iteration in iterations:
            await self.db.refresh(iteration)
            reloaded = await self.get_by_id(iteration.id)
            if reloaded is None:
                raise RuntimeError("Created iteration could not be reloaded")
            created.append(reloaded)
        return created

    async def update(
        self,
        iteration_id: int,
        data: IterationUpdate,
        *,
        commit: bool = True,
    ) -> Iteration | None:
        """Update an iteration, optionally leaving commit ownership to the caller."""
        iteration = await self.get_by_id(iteration_id)
        if not iteration:
            return None

        update_data = data.model_dump(exclude_unset=True)
        next_start = update_data.get("start_date", iteration.start_date)
        next_end = update_data.get("end_date", iteration.end_date)
        self._validate_date_range(next_start, next_end)
        if "project_id" in update_data:
            await self._require_project_exists(update_data["project_id"])
            if update_data["project_id"] != iteration.project_id:
                await self._reconcile_tasks_for_project_scope(
                    iteration,
                    update_data["project_id"],
                )
        if "calendar_id" in update_data:
            update_data["calendar_id"] = await self._calendar_id_for_create(
                update_data["calendar_id"],
                commit=commit,
            )
        for field, value in update_data.items():
            setattr(iteration, field, value)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(iteration)
        return await self.get_by_id(iteration_id)

    async def delete(self, iteration_id: int) -> bool:
        """Delete an iteration."""
        iteration = await self.get_by_id(iteration_id)
        if not iteration:
            return False

        await self.db.delete(iteration)
        await self.db.commit()
        return True

    async def get_summary(self, iteration_id: int) -> IterationSummary | None:
        """Get iteration summary with statistics."""
        iteration = await self.get_by_id(iteration_id)
        if not iteration:
            return None

        # Calculate working days
        calendar_service = CalendarService(self.db)
        working_days_info = calendar_service.calculate_working_days(
            iteration.calendar, iteration.start_date, iteration.end_date
        )

        task_row = (
            await self.db.execute(
                select(
                    func.count(Task.id),
                    func.coalesce(
                        func.sum(
                            case(
                                (Task.status == TaskStatusModel.CLOSED.value, 1),
                                else_=0,
                            )
                        ),
                        0,
                    ),
                    func.coalesce(func.sum(Task.effort_days), 0.0),
                    func.coalesce(
                        func.sum(
                            case(
                                (
                                    Task.end_date.is_not(None)
                                    & (Task.end_date > iteration.end_date),
                                    1,
                                ),
                                else_=0,
                            )
                        ),
                        0,
                    ),
                ).where(Task.iteration_id == iteration_id)
            )
        ).one()
        total_tasks = int(task_row[0])
        completed_tasks = int(task_row[1])
        total_effort_days = float(task_row[2])

        # Calculate team capacity
        team_capacity = await self._calculate_team_capacity(iteration)

        overdue_count = int(task_row[3])

        return IterationSummary(
            id=iteration.id,
            name=iteration.name,
            project_id=iteration.project_id,
            project=self._response_project(iteration),
            start_date=iteration.start_date,
            end_date=iteration.end_date,
            working_days=working_days_info.working_days,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            total_effort_days=total_effort_days,
            team_capacity_days=team_capacity,
            overdue_tasks_count=overdue_count,
        )

    async def _calculate_team_capacity(self, iteration: Iteration) -> float:
        """Calculate total team capacity for iteration."""
        calendar_service = CalendarService(self.db)
        working_days = calendar_service.calculate_working_days(
            iteration.calendar, iteration.start_date, iteration.end_date
        ).working_days

        total_capacity = float(
            (
                await self.db.execute(
                    select(
                        func.coalesce(
                            func.sum(
                                (TeamMember.availability_percent / 100.0)
                                * (1.0 - TeamMember.operational_utilization / 100.0)
                                * TeamMember.professionalism_coefficient
                            ),
                            0.0,
                        )
                    ).where(TeamMember.iteration_id == iteration.id)
                )
            ).scalar_one()
        ) * working_days

        return round(total_capacity, 1)
