"""LLM API router."""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security import require_admin_api_key
from app.models import Project, ProjectMilestone, Task, WorkTemplate
from app.schemas.llm import (
    FormalizeDraftRequest, FormalizeRequest, FormalizeResponse,
    ImproveDescriptionRequest, ImproveDescriptionResponse,
    ExplainScheduleRequest, ExplainScheduleResponse,
    GroundedAISuggestionResponse, TaskAISuggestRequest,
)
from app.services.llm_service import LLMService
from app.services.task_service import TaskService
from app.services.scheduler_service import SchedulerService

router = APIRouter(dependencies=[Depends(require_admin_api_key)])


async def get_llm_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LLMService:
    """Dependency for LLM service."""
    return await LLMService.from_runtime(db)


async def _task_ai_context_pack(
    db: AsyncSession,
    data: TaskAISuggestRequest,
    task: Task | None = None,
) -> dict:
    """Build a compact source-labelled context pack for grounded task AI."""
    form = data.model_dump()
    context: dict = {
        "form": form,
        "user_context": data.user_context,
        "persisted_task_id": task.id if task else None,
    }

    if task:
        context.update(
            {
                "task_title": task.title,
                "task_description": task.description,
                "task_status": task.status,
                "task_priority": task.priority,
                "task_tags": task.tags or [],
                "task_source": task.source,
                "task_source_url": task.source_url,
                "task_external_key": task.external_key,
            }
        )

    project_id = data.project_id or (task.project_id if task else None)
    if project_id:
        project = await db.get(Project, project_id)
        if project:
            context["project"] = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "health": project.health,
                "target_date": project.target_date,
            }

    milestone_id = data.milestone_id or (task.milestone_id if task else None)
    if milestone_id:
        milestone = await db.get(ProjectMilestone, milestone_id)
        if milestone:
            context["milestone"] = {
                "id": milestone.id,
                "project_id": milestone.project_id,
                "name": milestone.name,
                "description": milestone.description,
                "status": milestone.status,
                "target_date": milestone.target_date,
            }

    if data.template_id:
        template = await db.get(WorkTemplate, data.template_id)
        if template:
            context["template"] = {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "default_title": template.default_title,
                "default_description": template.default_description,
                "default_priority": template.default_priority,
                "default_effort_days": template.default_effort_days,
                "default_labels": template.default_labels or [],
                "default_checklist": template.default_checklist or [],
            }

    dependency_ids = data.depends_on
    if dependency_ids:
        result = await db.execute(select(Task).where(Task.id.in_(dependency_ids)))
        dependencies = result.scalars().all()
        context["dependencies"] = [
            {
                "id": dependency.id,
                "title": dependency.title,
                "status": dependency.status,
                "start_date": dependency.start_date,
                "end_date": dependency.end_date,
            }
            for dependency in dependencies
        ]

    return context


@router.post("/tasks/draft/formalize", response_model=FormalizeResponse)
async def formalize_task_draft(
    data: FormalizeDraftRequest,
    llm_service: Annotated[LLMService, Depends(get_llm_service)]
):
    """Formalize unsaved task form data using LLM/fallback behavior."""
    title = data.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title is required",
        )

    return await llm_service.formalize_task(
        title=title,
        description=data.description,
        context=data.context,
    )


@router.post("/tasks/draft/improve-description", response_model=ImproveDescriptionResponse)
async def improve_task_description_draft(
    data: ImproveDescriptionRequest,
    llm_service: Annotated[LLMService, Depends(get_llm_service)]
):
    """Improve an unsaved task description using LLM/fallback behavior."""
    return await llm_service.improve_description(
        current_description=data.current_description,
        context=data.context,
    )


@router.post("/tasks/ai/suggest", response_model=GroundedAISuggestionResponse)
async def suggest_task_draft(
    data: TaskAISuggestRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
):
    """Generate grounded advisory suggestions for unsaved task form data."""
    if not data.title.strip() and not (data.description or "").strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title or description is required",
        )
    context_pack = await _task_ai_context_pack(db, data)
    return await llm_service.suggest_task(context_pack)


@router.post("/tasks/{task_id}/formalize", response_model=FormalizeResponse)
async def formalize_task(
    task_id: int,
    data: FormalizeRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)]
):
    """Formalize a task using LLM."""
    task_service = TaskService(db)
    task = await task_service.get_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return await llm_service.formalize_task(
        title=task.title,
        description=task.description,
        context=data.context
    )


@router.post("/tasks/{task_id}/improve-description", response_model=ImproveDescriptionResponse)
async def improve_task_description(
    task_id: int,
    data: ImproveDescriptionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)]
):
    """Improve task description using LLM."""
    task_service = TaskService(db)
    task = await task_service.get_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return await llm_service.improve_description(
        current_description=data.current_description or task.description or "",
        context=data.context
    )


@router.post("/tasks/{task_id}/ai/suggest", response_model=GroundedAISuggestionResponse)
async def suggest_existing_task(
    task_id: int,
    data: TaskAISuggestRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
):
    """Generate grounded advisory suggestions for an existing task."""
    task_service = TaskService(db)
    task = await task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    context_pack = await _task_ai_context_pack(db, data, task=task)
    return await llm_service.suggest_task(context_pack)


@router.post("/iterations/{iteration_id}/explain-schedule", response_model=ExplainScheduleResponse)
async def explain_schedule(
    iteration_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
    data: Annotated[ExplainScheduleRequest | None, Body()] = None,
):
    """Generate human-readable explanation for iteration schedule."""
    # First, run scheduling to get decisions
    scheduler_service = SchedulerService(db)
    schedule_result = await scheduler_service.schedule_iteration(iteration_id)

    if not schedule_result.success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not schedule iteration {iteration_id}"
        )

    request = data or ExplainScheduleRequest()
    return await llm_service.explain_schedule(
        decisions=schedule_result.decisions,
        workload_issues=schedule_result.workload_issues,
        detail_level=request.detail_level
    )
