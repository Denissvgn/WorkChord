"""Agent capability, profile, and operator-owned model catalog API."""

from typing import Annotated, Any, NoReturn, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agent import AgentActor
from app.routers.agent import (
    _admin_header_actor,
    get_agent_actor,
    get_agent_service,
)
from app.routers.agent_planning import (
    _handle_agent_error,
    get_agent_planning_command_context,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import AgentTeamRuntimeAcknowledgement
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
from app.security import ADMIN_API_KEY_HEADER, admin_api_key_is_valid
from app.services.agent_service import AgentService, actor_has_scope


router = APIRouter()


async def get_agent_model_catalog_service(
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
) -> AgentModelCatalogService:
    """Return the request-scoped model control service."""

    return AgentModelCatalogService(db)


async def get_model_catalog_principal(
    service: Annotated[AgentService, Depends(get_agent_service)],
    agent_api_key: Annotated[Optional[str], Header(alias="X-Agent-API-Key")] = None,
    admin_api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None,
) -> AgentActor:
    """Use the catalog with an agent key, or with the operator's admin key.

    An agent key is authenticated exactly as on every other agent route. Without
    one, a valid admin key acts as the operator, as it does for team setup, so
    an operator can declare models and connect the first agent before any agent
    key exists.
    """

    if not agent_api_key and admin_api_key_is_valid(admin_api_key):
        return _admin_header_actor()
    return await get_agent_actor(service, agent_api_key)


@router.post("/agent/model-catalog/execution-provenance/{run_id}/reconcile")
async def reconcile_run_provenance(
    run_id: int,
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
    apply: bool = False,
    expected_evidence_digest: Annotated[str | None, Query(pattern="^[a-f0-9]{64}$")] = None,
    archived_acknowledgement: AgentTeamRuntimeAcknowledgement | None = None,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    rationale: Annotated[str | None, Header(alias="X-Agent-Rationale")] = None,
    correlation_id: Annotated[str | None, Header(alias="X-Correlation-ID")] = None,
):
    """Preview historical evidence or atomically apply that preview as a workspace operator."""
    from app.services.execution_reconciliation import reconcile_execution_request
    try:
        return await reconcile_execution_request(db, actor, run_id, apply=apply,
            expected_evidence_digest=expected_evidence_digest, archived_acknowledgement=archived_acknowledgement,
            idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (AgentModelConflictError, LookupError) as exc:
        _handle_model_error(exc)


@router.post("/agent/tasks/{task_id}/reconcile-planning-window")
async def reconcile_task_planning_window(
    task_id: int,
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
    planning_receipt_id: Annotated[int | None, Query(gt=0)] = None,
    planning_actor_id: Annotated[int | None, Query(gt=0)] = None,
    planning_command_key: Annotated[str | None, Query(min_length=1,max_length=255)] = None,
    apply: bool = False, expected_evidence_digest: Annotated[str | None, Query(pattern="^[a-f0-9]{64}$")] = None,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    rationale: Annotated[str | None, Header(alias="X-Agent-Rationale")] = None,
    correlation_id: Annotated[str | None, Header(alias="X-Correlation-ID")] = None,
):
    """Inspect or reconcile one task after an independently proved planning cutoff extension."""
    from app.services.planning_window_reconciliation import reconcile_window
    try:
        return await reconcile_window(db, actor, task_id, planning_receipt_id, apply=apply,
            planning_actor_id=planning_actor_id,planning_command_key=planning_command_key,
            expected_evidence_digest=expected_evidence_digest, idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except (AgentModelConflictError, LookupError) as exc:
        _handle_model_error(exc)


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
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
):
    """Return code-owned advisory capability definitions."""
    _require_catalog_read(actor)
    return AgentProfileCatalogService(db).catalog()


@router.get("/agent/profile-presets", response_model=list[dict[str, Any]])
async def get_agent_profile_presets(
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
):
    """Return reusable human-reviewable agent profile presets."""
    _require_catalog_read(actor)
    return AgentProfileCatalogService(db).presets()


@router.get("/agent/routes", response_model=list[dict[str, Any]])
async def get_agent_route_index(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
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
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
    service: Annotated[
        AgentModelCatalogService,
        Depends(get_agent_model_catalog_service),
    ],
    command: Annotated[
        AgentPlanningCommandContext,
        Depends(get_agent_planning_command_context),
    ],
):
    """Create a model declaration as an admin actor or the operator."""

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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
    actor: Annotated[AgentActor, Depends(get_model_catalog_principal)],
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
