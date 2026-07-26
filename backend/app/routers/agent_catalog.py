"""Agent capability, profile, and operator-owned model catalog API."""

from typing import Annotated, Any, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agent import AgentActor
from app.routers.agent import get_agent_actor
from app.routers.agent_planning import (
    _handle_agent_error,
    get_agent_planning_command_context,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentModelBindingCreate,
    AgentModelBindingDisable,
    AgentModelBindingResponse,
    AgentModelBindingUpdate,
    AgentModelCatalogCreate,
    AgentModelCatalogDisable,
    AgentModelCatalogResponse,
    AgentModelCatalogUpdate,
    AgentModelMutationReceipt,
)
from app.schemas.team import TeamMemberProfileResponse
from app.services.agent_model_catalog_service import (
    AgentModelCatalogService,
    AgentModelConflictError,
)
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_profile_catalog_service import AgentProfileCatalogService
from app.services.agent_service import actor_has_scope


router = APIRouter()


async def get_agent_model_catalog_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AgentModelCatalogService:
    """Return the request-scoped model control service."""

    return AgentModelCatalogService(db)


def _handle_model_error(exc: Exception) -> NoReturn:
    """Map stable model-control errors without losing conflict context."""

    if isinstance(exc, AgentModelConflictError):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail(),
        )
    if isinstance(exc, LookupError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "agent_model_not_found",
                "message": str(exc),
            },
        )
    _handle_agent_error(exc)


def _require_catalog_read(actor: AgentActor) -> None:
    if not any(
        actor_has_scope(actor, scope)
        for scope in ("planning:read", "team:read", "tasks:read")
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing catalog read scope",
        )


@router.get("/agent/profile-skill-catalog", response_model=list[dict[str, Any]])
async def get_profile_skill_catalog(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Return code-owned advisory capability definitions."""
    _require_catalog_read(actor)
    return AgentProfileCatalogService(db).catalog()


@router.get("/agent/profile-presets", response_model=list[dict[str, Any]])
async def get_agent_profile_presets(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Return reusable human-reviewable agent profile presets."""
    _require_catalog_read(actor)
    return AgentProfileCatalogService(db).presets()


@router.get("/agent/routes", response_model=list[dict[str, Any]])
async def get_agent_route_index(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Return the explainable, non-authorizing agent route index."""
    _require_catalog_read(actor)
    return AgentProfileCatalogService(db).routes()


@router.post(
    "/agent/profile-presets/{preset_key}/apply",
    response_model=TeamMemberProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def apply_agent_profile_preset(
    preset_key: str,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db)],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Materialize a preset through an actor-attributed exact command receipt."""
    try:
        receipt = await AgentPlanningService(db).apply_profile_preset(
            preset_key,
            actor,
            command=command,
        )
        return TeamMemberProfileResponse.model_validate(receipt.result)
    except Exception as exc:
        _handle_agent_error(exc)


@router.get(
    "/agent/model-catalog",
    response_model=list[AgentModelCatalogResponse],
)
async def list_agent_model_catalog(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    include_disabled: Annotated[bool, Query()] = False,
):
    """Return bounded secret-free provider-neutral model declarations."""

    try:
        return await service.list_catalog(
            actor,
            include_disabled=include_disabled,
        )
    except Exception as exc:
        _handle_model_error(exc)


@router.get(
    "/agent/model-catalog/{catalog_key}",
    response_model=AgentModelCatalogResponse,
)
async def get_agent_model_catalog_entry(
    catalog_key: str,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
):
    """Return one catalog declaration by its stable WorkChord key."""

    try:
        return await service.get_catalog(actor, catalog_key.strip().lower())
    except Exception as exc:
        _handle_model_error(exc)


@router.post(
    "/agent/model-catalog",
    response_model=AgentModelMutationReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_model_catalog_entry(
    data: AgentModelCatalogCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Create a model declaration through a stored admin actor."""

    try:
        return await service.create_catalog(actor, data, command=command)
    except Exception as exc:
        _handle_model_error(exc)


@router.patch(
    "/agent/model-catalog/{catalog_id}",
    response_model=AgentModelMutationReceipt,
)
async def update_agent_model_catalog_entry(
    catalog_id: int,
    data: AgentModelCatalogUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Optimistically update a model declaration."""

    try:
        return await service.update_catalog(
            catalog_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_model_error(exc)


@router.post(
    "/agent/model-catalog/{catalog_id}/disable",
    response_model=AgentModelMutationReceipt,
)
async def disable_agent_model_catalog_entry(
    catalog_id: int,
    data: AgentModelCatalogDisable,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Soft-disable a declaration after explicit live-work reconciliation."""

    try:
        return await service.disable_catalog(
            catalog_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_model_error(exc)


@router.get(
    "/agent/model-bindings",
    response_model=list[AgentModelBindingResponse],
)
async def list_agent_model_bindings(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    actor_id: Annotated[int | None, Query(ge=1)] = None,
    include_disabled: Annotated[bool, Query()] = False,
):
    """Return actor binding evidence without credentials or runtime logs."""

    try:
        return await service.list_bindings(
            actor,
            actor_id=actor_id,
            include_disabled=include_disabled,
        )
    except Exception as exc:
        _handle_model_error(exc)


@router.get(
    "/agent/model-bindings/{binding_id}",
    response_model=AgentModelBindingResponse,
)
async def get_agent_model_binding(
    binding_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
):
    """Return one binding, including disabled historical evidence."""

    try:
        return await service.get_binding(actor, binding_id)
    except Exception as exc:
        _handle_model_error(exc)


@router.post(
    "/agent/model-bindings",
    response_model=AgentModelMutationReceipt,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_model_binding(
    data: AgentModelBindingCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Bind an existing actor to one existing catalog entry."""

    try:
        return await service.create_binding(actor, data, command=command)
    except Exception as exc:
        _handle_model_error(exc)


@router.patch(
    "/agent/model-bindings/{binding_id}",
    response_model=AgentModelMutationReceipt,
)
async def update_agent_model_binding(
    binding_id: int,
    data: AgentModelBindingUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Optimistically update one actor model binding."""

    try:
        return await service.update_binding(
            binding_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_model_error(exc)


@router.post(
    "/agent/model-bindings/{binding_id}/disable",
    response_model=AgentModelMutationReceipt,
)
async def disable_agent_model_binding(
    binding_id: int,
    data: AgentModelBindingDisable,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Soft-disable a binding without deleting assignment or run evidence."""

    try:
        return await service.disable_binding(
            binding_id,
            actor,
            data,
            command=command,
        )
    except Exception as exc:
        _handle_model_error(exc)
