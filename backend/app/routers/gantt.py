"""Gantt API router."""
from typing import Annotated, Optional
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.task import Task
from app.schemas.gantt import (
    GanttResponse, GanttTask, GanttAssignee, GanttMilestone, ScheduleResult,
    SchedulePreviewRequest, SchedulePreviewResponse, WorkloadIssue, SchedulingDecision
)
from app.schemas.iteration import IterationResponse
from app.services.scheduler_service import SchedulerService
from app.services.iteration_service import IterationService
from app.services.task_service import TaskService
from app.services.calendar_service import CalendarService
from sqlalchemy.orm import attributes
from datetime import date

router = APIRouter()


async def get_scheduler_service(db: Annotated[AsyncSession, Depends(get_db)]) -> SchedulerService:
    """Dependency for scheduler service."""
    return SchedulerService(db)


@router.post("/iterations/{iteration_id}/schedule", response_model=ScheduleResult)
async def schedule_iteration(
    iteration_id: int,
    service: Annotated[SchedulerService, Depends(get_scheduler_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Run automatic scheduling for an iteration."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    result = await service.schedule_iteration(iteration_id)
    return result


@router.post("/iterations/{iteration_id}/schedule/preview", response_model=SchedulePreviewResponse)
async def preview_iteration_schedule(
    iteration_id: int,
    data: SchedulePreviewRequest,
    service: Annotated[SchedulerService, Depends(get_scheduler_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Dry-run sandbox edits through the real scheduler and roll everything back.

    Applies the submitted task changes (same item shape as batch-update) and
    runs the actual scheduling pass in one transaction, serializes the
    projected Gantt state, then rolls the transaction back. The preview is
    therefore always consistent with what a subsequent batch-update apply
    (which auto-reschedules) will produce.
    """
    from app.routers.tasks import apply_batch_update_items
    from app.services.task_service import TaskVersionConflictError

    iteration_service = IterationService(db)
    task_service = TaskService(db)
    iteration = await iteration_service.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    # Neutralize nested commits from status transitions the same way
    # batch_update_tasks does; the whole preview is rolled back at the end.
    original_commit = db.commit
    async def noop_commit():
        await db.flush()
    db.commit = noop_commit

    try:
        if data.changes:
            await apply_batch_update_items(
                task_service, iteration_id, iteration.end_date, data.changes
            )

        schedule_result = await service.schedule_iteration(iteration_id, commit=False)

        tasks = await task_service.get_by_iteration(iteration_id)
        gantt_tasks: list[GanttTask] = []
        overdue_ids: list[int] = []
        for task in tasks:
            if task.is_deferred:
                continue
            gantt_task = _task_to_gantt(task, iteration.end_date)
            if gantt_task is None:
                continue
            gantt_tasks.append(gantt_task)
            if gantt_task.is_overdue:
                overdue_ids.append(gantt_task.id)
            for child in gantt_task.children:
                if child.is_overdue:
                    overdue_ids.append(child.id)

        return SchedulePreviewResponse(
            tasks=gantt_tasks,
            overdue_task_ids=overdue_ids,
            schedule_result=schedule_result,
        )
    except TaskVersionConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail(),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc
    finally:
        # Discard every preview mutation regardless of outcome.
        db.commit = original_commit
        await db.rollback()


@router.get("/iterations/{iteration_id}/gantt", response_model=GanttResponse)
async def get_gantt_data(
    iteration_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get Gantt chart data for an iteration.

    Database queries are deliberately sequential because all services share the
    request-scoped ``AsyncSession``. SQLAlchemy does not permit concurrent work
    on one async session. Vacation dates still use O(1) set lookups.
    """
    from app.services.team_service import TeamService
    from datetime import timedelta

    # Initialize services
    iteration_service = IterationService(db)
    task_service = TaskService(db)
    team_service = TeamService(db)

    # Keep request-scoped AsyncSession operations sequential. Running these
    # coroutines concurrently can corrupt session state during connection
    # provisioning and teardown.
    iteration = await iteration_service.get_by_id(iteration_id)
    tasks = await task_service.get_by_iteration(iteration_id)
    team_members = await team_service.get_by_iteration(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    # Get calendar info (sync operation, uses cached calendar from iteration)
    calendar_service = CalendarService(db)
    working_days_info = calendar_service.calculate_working_days(
        iteration.calendar, iteration.start_date, iteration.end_date
    )

    # Convert to Gantt format
    gantt_tasks = []
    overdue_ids = []

    for task in tasks:
        # Skip deferred tasks - they should not appear on Gantt
        if task.is_deferred:
            continue
        gantt_task = _task_to_gantt(task, iteration.end_date)
        if gantt_task is None:
            continue
        gantt_tasks.append(gantt_task)

        if gantt_task.is_overdue:
            overdue_ids.append(gantt_task.id)

        # Collect overdue children
        for child in gantt_task.children:
            if child.is_overdue:
                overdue_ids.append(child.id)

    # Calculate latest task end date (for overdue range)
    latest_task_end = iteration.end_date
    for task in tasks:
        if task.end_date and task.end_date > latest_task_end:
            latest_task_end = task.end_date
        for child in (task.children or []):
            if child.end_date and child.end_date > latest_task_end:
                latest_task_end = child.end_date

    # Build member_vacations dict: member_id -> list of vacation dates
    # OPTIMIZED: Use set comprehension instead of while loop
    member_vacations: dict[int, list] = {}
    for member in team_members:
        vacation_dates: set[date] = set()
        for vacation in member.vacations:
            # Generate date range using set comprehension (O(n) but no loop overhead)
            days_count = (vacation.end_date - vacation.start_date).days + 1
            vacation_dates.update(
                vacation.start_date + timedelta(days=i)
                for i in range(days_count)
                if iteration.start_date <= vacation.start_date + timedelta(days=i) <= latest_task_end
            )
        if vacation_dates:
            member_vacations[member.id] = sorted(vacation_dates)

    return GanttResponse(
        iteration=IterationResponse(
            id=iteration.id,
            name=iteration.name,
            calendar_id=iteration.calendar_id,
            start_date=iteration.start_date,
            end_date=iteration.end_date,
            working_days=working_days_info.working_days,
        ),
        tasks=gantt_tasks,
        overdue_task_ids=overdue_ids,
        holidays=working_days_info.holidays,
        weekends=working_days_info.weekends,
        member_vacations=member_vacations,
    )


def _get_calculated_effort(task: Task) -> Optional[float]:
    """Get calculated effort days from the database.

    This value is computed and stored by the scheduler during scheduling.
    If not yet scheduled, returns None.
    """
    # Use the value stored by scheduler, fall back to raw effort if not scheduled
    if task.calculated_effort_days is not None:
        return task.calculated_effort_days
    return None


def _task_to_gantt(
    task: Task,
    iteration_end_date: date,
    issues: Optional[list[WorkloadIssue]] = None,
    decisions: Optional[list[SchedulingDecision]] = None
) -> Optional[GanttTask]:
    """Convert Task to GanttTask."""
    if task.is_deferred:
        return None  # Skip deferred tasks

    # Safely check if relationships are loaded
    children_loaded = 'children' in attributes.instance_state(task).dict
    dependencies_loaded = 'dependencies' in attributes.instance_state(task).dict
    assignee_loaded = 'assignee' in attributes.instance_state(task).dict
    milestone_loaded = 'milestone' in attributes.instance_state(task).dict

    loaded_children = task.children if children_loaded else []
    loaded_dependencies = task.dependencies if dependencies_loaded else []
    loaded_assignee = task.assignee if assignee_loaded else None
    loaded_milestone = task.milestone if milestone_loaded else None

    is_composite = len(loaded_children) > 0
    is_overdue = bool(task.end_date and task.end_date > iteration_end_date)

    # Check if task violates its date constraints
    is_outside_constraints = False
    if task.start_date and task.min_start_date and task.start_date < task.min_start_date:
        is_outside_constraints = True
    if task.end_date and task.max_end_date and task.end_date > task.max_end_date:
        is_outside_constraints = True

    # Assignee for the task itself (show even if composite)
    assignee = None
    if loaded_assignee:
        assignee = GanttAssignee(id=loaded_assignee.id, name=loaded_assignee.name)

    milestone = None
    if loaded_milestone:
        milestone = GanttMilestone(
            id=loaded_milestone.id,
            project_id=loaded_milestone.project_id,
            name=loaded_milestone.name,
            status=loaded_milestone.status,
            target_date=loaded_milestone.target_date,
        )

    # Multiple assignees for composite tasks
    assignees = []
    if is_composite:
        seen_ids = set()
        for child in loaded_children:
            child_state = attributes.instance_state(child)
            child_assignee_loaded = 'assignee' in child_state.dict
            child_assignee = child.assignee if child_assignee_loaded else None
            if child_assignee and child_assignee.id not in seen_ids:
                assignees.append(GanttAssignee(
                    id=child_assignee.id, name=child_assignee.name
                ))
                seen_ids.add(child_assignee.id)

    # Parse tags
    tags = []
    if task.tags:
        try:
            tags = json.loads(task.tags)
        except json.JSONDecodeError:
            tags = []

    # Get scheduling info for this task
    task_schedule_result = None
    if task.start_date and task.end_date:
        task_issues = []
        if issues:
            # Filter issues for this task's assignee within task dates (simplified match by assignee)
            # A more precise match would check overload on specific dates,
            # here we just flag if assignee has overload issues generally during iteration
            # Ideally we'd map overload to specific task but that's complex
            pass

        task_schedule_result = {
            "scheduled_start": task.start_date.isoformat(),
            "scheduled_end": task.end_date.isoformat(),
            "issues": []  # Simplified for now
        }

    # Convert children recursively (excluding deferred)
    children = []
    for c in loaded_children:
        child_gantt = _task_to_gantt(c, iteration_end_date, issues, decisions)
        if child_gantt:  # Only add if not deferred
            children.append(child_gantt)

    # Dependencies
    dependencies = [
        dep.depends_on_id
        for dep in loaded_dependencies
    ]

    # Calculate progress (simple average for composite)
    progress = 0.0
    if is_composite and children:
        progress = sum(c.progress for c in children) / len(children)
    elif task.status == "closed":
        progress = 100.0
    elif task.status == "resolved":
        progress = 90.0
    elif task.status == "active":
        progress = 50.0
    # planned = 0.0 (default)

    # Check if task is delayed (PLANNED and start_date passed)
    today = date.today()
    is_delayed = False
    if task.status == "planned" and task.start_date and task.start_date < today:
        is_delayed = True

    return GanttTask(
        id=task.id,
        title=task.title,
        project_id=task.project_id,
        milestone_id=task.milestone_id,
        start_date=task.start_date,
        end_date=task.end_date,
        actual_start_date=task.actual_start_date,
        actual_end_date=task.actual_end_date,
        min_start_date=task.min_start_date,
        max_end_date=task.max_end_date,
        status=task.status,
        milestone=milestone,
        assignee=assignee,
        assignees=assignees,
        priority=task.priority,
        progress=progress,
        effort_days=task.effort_days,
        calculated_effort_days=_get_calculated_effort(task),
        effort_hours=task.effort_hours,
        version=task.version,
        is_overdue=is_overdue,
        is_delayed=is_delayed,
        tags=tags,
        is_composite=is_composite,
        is_optional=task.is_optional,
        is_outside_constraints=is_outside_constraints,
        children=children,
        dependencies=dependencies,
    )
