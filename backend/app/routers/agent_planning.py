"""Agent-authenticated PM setup and schedule-control commands."""

from typing import Annotated, NoReturn

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import mcp_agent_tools
from app.database import get_db
from app.models.agent import AgentActor
from app.routers.agent import get_agent_actor
from app.schemas.agent import AgentTaskCreate, AgentTaskPatch
from app.schemas.agent_planning import (
    AgentPlanningCommandContext,
    AgentPlanningReceipt,
    AgentScheduleCommand,
)
from app.schemas.iteration import IterationCreate, IterationUpdate
from app.schemas.project import (
    ProjectCreate,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneUpdate,
    ProjectUpdate,
)
from app.schemas.team import (
    TeamMemberCreate,
    TeamMemberProfileCreate,
    TeamMemberProfileUpdate,
    TeamMemberUpdate,
    VacationCreate,
    VacationUpdate,
)
from app.schemas.triage import (
    TriageActionRequest,
    TriageClassificationSuggestionResponse,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageItemCreate,
    TriageItemResponse,
    TriageItemUpdate,
    TriageSnoozeRequest,
)
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    require_scope,
)
from app.services.task_service import TaskVersionConflictError
from app.services.triage_service import TriageConflictError


router = APIRouter()


async def get_agent_planning_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AgentPlanningService:
    """Return the request-scoped PM setup command adapter."""
    return AgentPlanningService(db)


async def get_agent_planning_command_context(
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
) -> AgentPlanningCommandContext:
    """Validate required durable-audit headers for one PM command."""
    try:
        return AgentPlanningCommandContext(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


def _handle_agent_error(exc: Exception) -> NoReturn:
    """Map safe command-domain errors to stable HTTP status codes."""
    if isinstance(exc, AgentPermissionError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    if isinstance(exc, TaskVersionConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail())
    if isinstance(exc, AgentConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(exc, TriageConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    raise exc


@router.post(
    "/agent/planning/projects",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create a project through the planning domain service."""
    try:
        return await service.create_project(
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/projects/{project_id}",
    response_model=AgentPlanningReceipt,
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Partially update a project through the planning domain service."""
    try:
        return await service.update_project(
            project_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/projects/{project_id}/milestones",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_milestone(
    project_id: int,
    data: ProjectMilestoneCreateRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create one project-scoped milestone through the planning service."""
    try:
        return await service.create_milestone(
            project_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/projects/{project_id}/milestones/{milestone_id}",
    response_model=AgentPlanningReceipt,
)
async def update_project_milestone(
    project_id: int,
    milestone_id: int,
    data: ProjectMilestoneUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Update one milestone inside its project scope."""
    try:
        return await service.update_milestone(
            project_id,
            milestone_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.delete(
    "/agent/planning/projects/{project_id}/milestones/{milestone_id}",
    response_model=AgentPlanningReceipt,
)
async def delete_project_milestone(
    project_id: int,
    milestone_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Delete one milestone while retaining an exact detachment receipt."""
    try:
        return await service.delete_milestone(
            project_id,
            milestone_id,
            actor,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/iterations/{iteration_id}/tasks",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_planning_task(
    iteration_id: int,
    data: AgentTaskCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create one decomposed task with complete PM command metadata."""
    try:
        return await service.create_task(
            iteration_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/tasks/{task_id}",
    response_model=AgentPlanningReceipt,
)
async def patch_planning_task(
    task_id: int,
    data: AgentTaskPatch,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Patch decomposition fields with optimistic version and exact replay."""
    try:
        return await service.patch_task(
            task_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/iterations",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_iteration(
    data: IterationCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create an iteration through the iteration domain service."""
    try:
        return await service.create_iteration(
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/iterations/{iteration_id}",
    response_model=AgentPlanningReceipt,
)
async def update_iteration(
    iteration_id: int,
    data: IterationUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Partially update an iteration through the iteration domain service."""
    try:
        return await service.update_iteration(
            iteration_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/team-member-profiles",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    data: TeamMemberProfileCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create a reusable team profile through the team domain service."""
    try:
        return await service.create_profile(
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/team-member-profiles/{profile_id}",
    response_model=AgentPlanningReceipt,
)
async def update_profile(
    profile_id: int,
    data: TeamMemberProfileUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Partially update a reusable team profile."""
    try:
        return await service.update_profile(
            profile_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/iterations/{iteration_id}/team-members",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_team_member(
    iteration_id: int,
    data: TeamMemberCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Add one capacity owner to an iteration."""
    try:
        return await service.create_team_member(
            iteration_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/team-members/{member_id}",
    response_model=AgentPlanningReceipt,
)
async def update_team_member(
    member_id: int,
    data: TeamMemberUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Partially update one iteration capacity owner."""
    try:
        return await service.update_team_member(
            member_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/team-members/{member_id}/vacations",
    response_model=AgentPlanningReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_vacation(
    member_id: int,
    data: VacationCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create one validated vacation period."""
    try:
        return await service.create_vacation(
            member_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/vacations/{vacation_id}",
    response_model=AgentPlanningReceipt,
)
async def update_vacation(
    vacation_id: int,
    data: VacationUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Partially update one validated vacation period."""
    try:
        return await service.update_vacation(
            vacation_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/iterations/{iteration_id}/schedule/preview",
    response_model=AgentPlanningReceipt,
)
async def preview_schedule(
    iteration_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Preview scheduling in a rolled-back savepoint and persist only its receipt."""
    try:
        return await service.preview_schedule(
            iteration_id,
            actor,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/iterations/{iteration_id}/schedule/apply",
    response_model=AgentPlanningReceipt,
)
async def apply_schedule(
    iteration_id: int,
    data: AgentScheduleCommand,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Apply a preview token set with task-level optimistic concurrency."""
    try:
        return await service.apply_schedule(
            iteration_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


def _require_triage_result(result, triage_item_id: int):
    """Map a shared triage adapter's missing result into the REST domain contract."""
    if result is None:
        raise LookupError(f"Triage item with id {triage_item_id} not found")
    return result


@router.post(
    "/agent/planning/triage",
    response_model=TriageItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_planning_triage_item(
    data: TriageItemCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Create one actor-attributed triage item through the shared command adapter."""
    try:
        require_scope(actor, "planning:write")
        return await mcp_agent_tools.create_triage_item(
            db,
            actor,
            data.model_dump(mode="json"),
            idempotency_key=command.idempotency_key,
            rationale=command.rationale,
            correlation_id=command.correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/triage/{triage_item_id}/classify",
    response_model=TriageClassificationSuggestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def classify_planning_triage_item(
    triage_item_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Persist one exact advisory classification through the shared adapter."""
    try:
        require_scope(actor, "planning:write")
        result = await mcp_agent_tools.classify_triage_item(
            db,
            actor,
            triage_item_id,
            idempotency_key=command.idempotency_key,
            rationale=command.rationale,
            correlation_id=command.correlation_id,
        )
        return _require_triage_result(result, triage_item_id)
    except Exception as exc:
        _handle_agent_error(exc)


@router.patch(
    "/agent/planning/triage/{triage_item_id}",
    response_model=TriageItemResponse,
)
async def update_planning_triage_item(
    triage_item_id: int,
    data: TriageItemUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Update editable triage metadata through the shared durable adapter."""
    try:
        require_scope(actor, "planning:write")
        result = await mcp_agent_tools.update_triage_item(
            db,
            actor,
            triage_item_id,
            data.model_dump(mode="json", exclude_unset=True),
            idempotency_key=command.idempotency_key,
            rationale=command.rationale,
            correlation_id=command.correlation_id,
        )
        return _require_triage_result(result, triage_item_id)
    except Exception as exc:
        _handle_agent_error(exc)


async def _run_triage_action(
    adapter,
    *,
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    data,
    command: AgentPlanningCommandContext,
):
    """Invoke one shared durable triage action with the REST command context."""
    require_scope(actor, "planning:write")
    result = await adapter(
        db,
        actor,
        triage_item_id,
        data.model_dump(mode="json", exclude_unset=True),
        idempotency_key=command.idempotency_key,
        rationale=command.rationale,
        correlation_id=command.correlation_id,
    )
    return _require_triage_result(result, triage_item_id)


@router.post(
    "/agent/planning/triage/{triage_item_id}/accept",
    response_model=TriageItemResponse,
)
async def accept_planning_triage_item(
    triage_item_id: int,
    data: TriageActionRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Accept one triage item with an exact actor-attributed receipt."""
    try:
        return await _run_triage_action(
            mcp_agent_tools.accept_triage_item,
            db=db,
            actor=actor,
            triage_item_id=triage_item_id,
            data=data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/triage/{triage_item_id}/decline",
    response_model=TriageItemResponse,
)
async def decline_planning_triage_item(
    triage_item_id: int,
    data: TriageActionRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Decline one triage item with an exact actor-attributed receipt."""
    try:
        return await _run_triage_action(
            mcp_agent_tools.decline_triage_item,
            db=db,
            actor=actor,
            triage_item_id=triage_item_id,
            data=data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/triage/{triage_item_id}/snooze",
    response_model=TriageItemResponse,
)
async def snooze_planning_triage_item(
    triage_item_id: int,
    data: TriageSnoozeRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Snooze one triage item with an exact actor-attributed receipt."""
    try:
        return await _run_triage_action(
            mcp_agent_tools.snooze_triage_item,
            db=db,
            actor=actor,
            triage_item_id=triage_item_id,
            data=data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/triage/{triage_item_id}/mark-duplicate",
    response_model=TriageItemResponse,
)
async def mark_planning_triage_item_duplicate(
    triage_item_id: int,
    data: TriageDuplicateRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Record one duplicate disposition through the shared durable adapter."""
    try:
        return await _run_triage_action(
            mcp_agent_tools.mark_triage_item_duplicate,
            db=db,
            actor=actor,
            triage_item_id=triage_item_id,
            data=data,
            command=command,
        )
    except Exception as exc:
        _handle_agent_error(exc)


@router.post(
    "/agent/planning/triage/{triage_item_id}/convert-to-task",
    response_model=TriageConvertToTaskResponse,
)
async def convert_planning_triage_item_to_task(
    triage_item_id: int,
    data: TriageConvertToTaskRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)],
):
    """Convert one triage item through the same locked exact-replay adapter as MCP."""
    try:
        require_scope(actor, "planning:write")
        result = await mcp_agent_tools.convert_triage_to_task(
            db,
            actor,
            triage_item_id,
            data.model_dump(mode="json"),
            idempotency_key=command.idempotency_key,
            rationale=command.rationale,
            correlation_id=command.correlation_id,
        )
        return _require_triage_result(result, triage_item_id)
    except Exception as exc:
        _handle_agent_error(exc)
