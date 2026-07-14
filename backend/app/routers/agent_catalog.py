"""Agent capability catalog, profile preset, and route-index API."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agent import AgentActor
from app.routers.agent import get_agent_actor
from app.routers.agent_planning import (
    _handle_agent_error,
    get_agent_planning_command_context,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.team import TeamMemberProfileResponse
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_profile_catalog_service import AgentProfileCatalogService
from app.services.agent_service import actor_has_scope


router = APIRouter()


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
