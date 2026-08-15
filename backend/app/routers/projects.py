"""Project API router."""
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user_session import UserSession
from app.schemas.common import MessageResponse
from app.schemas.iteration import IterationResponse
from app.schemas.project import (
    InitiativeCreate,
    InitiativeResponse,
    InitiativeUpdate,
    ProjectCreate,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneDeleteResponse,
    ProjectMilestoneResponse,
    ProjectMilestoneUpdate,
    ProjectPortfolioSummary,
    ProjectResponse,
    ProjectSummary,
    ProjectUpdate,
    ProjectUpdateEntryCreate,
    ProjectUpdateEntryResponse,
    RoadmapMilestonePage,
)
from app.query_limits import MAX_BOUNDED_LIST_ITEMS
from app.schemas.release import (
    ReleaseCreateRequest,
    ReleaseResponse,
    ReleaseUpdateRequest,
)
from app.schemas.task import TaskResponse
from app.services import session_service
from app.services.iteration_service import IterationService
from app.services.language_service import (
    backend_error_message,
    entity_deleted_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
    scoped_entity_not_found_message,
)
from app.services.project_service import ProjectService
from app.services.release_service import ReleaseService
from app.services.task_service import TaskService

router = APIRouter()


async def get_project_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ProjectService:
    """Dependency for project service."""
    return ProjectService(db)


async def get_release_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ReleaseService:
    """Dependency for release service."""
    return ReleaseService(db)


async def _localized_detail(service: Any, message: str) -> str:
    ui_language = await resolve_runtime_ui_language(service.db)
    return backend_error_message(message, ui_language)


async def _not_found_detail(service: Any, entity: str, entity_id: int) -> str:
    ui_language = await resolve_runtime_ui_language(service.db)
    return entity_not_found_message(entity, entity_id, ui_language)


async def _scoped_not_found_detail(
    service: Any,
    entity: str,
    entity_id: int,
    scope: str,
    scope_id: int,
) -> str:
    ui_language = await resolve_runtime_ui_language(service.db)
    return scoped_entity_not_found_message(entity, entity_id, scope, scope_id, ui_language)


@router.get("/projects", response_model=list[ProjectResponse])
async def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """List all projects."""
    return await service.list_projects()


@router.get(
    "/projects/portfolio-summaries",
    response_model=list[ProjectPortfolioSummary],
)
async def list_project_portfolio_summaries(
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """List compact project signals without one request per portfolio row."""
    return await service.list_portfolio_summaries()


@router.get("/roadmap/milestones", response_model=RoadmapMilestonePage)
async def list_roadmap_milestones(
    service: Annotated[ProjectService, Depends(get_project_service)],
    after_id: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_BOUNDED_LIST_ITEMS)] = MAX_BOUNDED_LIST_ITEMS,
):
    """List a bounded cursor page of portfolio milestone markers."""
    milestones, next_cursor = await service.list_portfolio_milestones(
        after_id=after_id,
        limit=limit,
    )
    return RoadmapMilestonePage(items=milestones, next_cursor=next_cursor)


@router.get("/initiatives", response_model=list[InitiativeResponse])
async def list_initiatives(
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """List all initiatives."""
    return await service.list_initiatives()


@router.post("/initiatives", response_model=InitiativeResponse, status_code=status.HTTP_201_CREATED)
async def create_initiative(
    data: InitiativeCreate,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Create an initiative."""
    try:
        return await service.create_initiative(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )


@router.get("/initiatives/{initiative_id}", response_model=InitiativeResponse)
async def get_initiative(
    initiative_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Get an initiative by ID."""
    initiative = await service.get_initiative_by_id(initiative_id)
    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "initiative", initiative_id),
        )
    return initiative


@router.put("/initiatives/{initiative_id}", response_model=InitiativeResponse)
async def update_initiative(
    initiative_id: int,
    data: InitiativeUpdate,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Update an initiative."""
    try:
        initiative = await service.update_initiative(initiative_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )

    if not initiative:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "initiative", initiative_id),
        )
    return initiative


@router.delete("/initiatives/{initiative_id}", response_model=MessageResponse)
async def delete_initiative(
    initiative_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Delete an initiative and leave assigned projects intact."""
    deleted = await service.delete_initiative(initiative_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "initiative", initiative_id),
        )
    ui_language = await resolve_runtime_ui_language(service.db)
    return MessageResponse(message=entity_deleted_message("initiative", initiative_id, ui_language), success=True)


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Create a project."""
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Get a project by ID."""
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Update a project."""
    try:
        project = await service.update(project_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return project


@router.post(
    "/projects/{project_id}/updates",
    response_model=ProjectUpdateEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_update(
    project_id: int,
    data: ProjectUpdateEntryCreate,
    service: Annotated[ProjectService, Depends(get_project_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Create an append-only structured update for a project."""
    update_entry = await service.create_project_update(
        project_id=project_id,
        data=data,
        created_by_session_id=current_session.id,
    )
    if update_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return update_entry


@router.get(
    "/projects/{project_id}/updates",
    response_model=list[ProjectUpdateEntryResponse],
)
async def list_project_updates(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """List append-only structured updates for a project."""
    updates = await service.list_project_updates(project_id)
    if updates is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return updates


@router.get(
    "/projects/{project_id}/milestones",
    response_model=list[ProjectMilestoneResponse],
)
async def list_project_milestones(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """List milestones for a project in roadmap order."""
    milestones = await service.list_milestones(project_id)
    if milestones is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return milestones


@router.post(
    "/projects/{project_id}/milestones",
    response_model=ProjectMilestoneResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_milestone(
    project_id: int,
    data: ProjectMilestoneCreateRequest,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Create a project-scoped milestone."""
    milestone = await service.create_milestone(project_id, data)
    if milestone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return milestone


@router.patch(
    "/projects/{project_id}/milestones/{milestone_id}",
    response_model=ProjectMilestoneResponse,
)
async def update_project_milestone(
    project_id: int,
    milestone_id: int,
    data: ProjectMilestoneUpdate,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Update a milestone that belongs to the project path."""
    milestone = await service.update_milestone(project_id, milestone_id, data)
    if milestone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _scoped_not_found_detail(service, "milestone", milestone_id, "project", project_id),
        )
    return milestone


@router.delete(
    "/projects/{project_id}/milestones/{milestone_id}",
    response_model=ProjectMilestoneDeleteResponse,
)
async def delete_project_milestone(
    project_id: int,
    milestone_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """Delete a project milestone while keeping linked tasks."""
    detached_task_count = await service.delete_milestone(project_id, milestone_id)
    if detached_task_count is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _scoped_not_found_detail(service, "milestone", milestone_id, "project", project_id),
        )
    ui_language = await resolve_runtime_ui_language(service.db)
    return ProjectMilestoneDeleteResponse(
        success=True,
        message=entity_deleted_message("project_milestone", milestone_id, ui_language),
        detached_task_count=detached_task_count,
    )


@router.get(
    "/projects/{project_id}/iterations",
    response_model=list[IterationResponse],
)
async def list_project_iterations(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
):
    """List iterations explicitly scoped to a project."""
    iterations = await service.list_iterations(project_id)
    if iterations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )

    iteration_service = IterationService(service.db)
    return [iteration_service.to_response(iteration) for iteration in iterations]


@router.get(
    "/projects/{project_id}/releases",
    response_model=list[ReleaseResponse],
)
async def list_project_releases(
    project_id: int,
    service: Annotated[ReleaseService, Depends(get_release_service)],
):
    """List releases for a project."""
    releases = await service.list_for_project(project_id)
    if releases is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return releases


@router.post(
    "/projects/{project_id}/releases",
    response_model=ReleaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_release(
    project_id: int,
    data: ReleaseCreateRequest,
    service: Annotated[ReleaseService, Depends(get_release_service)],
):
    """Create a release for a project."""
    try:
        release = await service.create_for_project(project_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )

    if release is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return release


@router.get("/releases/{release_id}", response_model=ReleaseResponse)
async def get_release(
    release_id: int,
    service: Annotated[ReleaseService, Depends(get_release_service)],
):
    """Get a release by ID."""
    release = await service.get_by_id(release_id)
    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "release", release_id),
        )
    return release


@router.put("/releases/{release_id}", response_model=ReleaseResponse)
async def update_release(
    release_id: int,
    data: ReleaseUpdateRequest,
    service: Annotated[ReleaseService, Depends(get_release_service)],
):
    """Update release metadata and task links."""
    try:
        release = await service.update(release_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(service, str(e)),
        )

    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "release", release_id),
        )
    return release


@router.delete("/projects/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
    detach_tasks: bool = Query(False),
):
    """Delete a project, optionally detaching linked tasks first."""
    result = await service.delete(project_id, detach_tasks=detach_tasks)
    if result == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    if result == "has_tasks":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=await _localized_detail(service, "Project has linked tasks. Use detach_tasks=true to delete and detach tasks."),
        )

    ui_language = await resolve_runtime_ui_language(service.db)
    return MessageResponse(message=entity_deleted_message("project", project_id, ui_language), success=True)


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
async def get_project_tasks(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Get linked project task tree roots."""
    tasks = await service.get_tasks(project_id)
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )

    task_service = TaskService(service.db)
    return [task_service.task_to_response(task) for task in tasks]


@router.get("/projects/{project_id}/summary", response_model=ProjectSummary)
async def get_project_summary(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    """Get project summary metrics."""
    summary = await service.get_summary(project_id)
    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, "project", project_id),
        )
    return summary
