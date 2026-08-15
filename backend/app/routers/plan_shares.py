"""Read-only iteration plan sharing API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user_session import UserSession
from app.schemas.common import MessageResponse
from app.schemas.plan_share import PlanShareResponse
from app.services import session_service
from app.services.plan_share_service import PlanShareService

router = APIRouter()


@router.get(
    "/iterations/{iteration_id}/plan-share",
    response_model=PlanShareResponse | None,
)
async def get_current_plan_share(
    iteration_id: int,
    response: Response,
    current_session: Annotated[
        UserSession,
        Depends(session_service.get_current_session),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PlanShareResponse | None:
    """Return the current session's active share for one iteration."""
    response.headers["Cache-Control"] = "no-store"
    service = PlanShareService(db)
    share = await service.get_owned_current(iteration_id, current_session.id)
    return service.to_response(share) if share else None


@router.post(
    "/iterations/{iteration_id}/plan-share",
    response_model=PlanShareResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_plan_share(
    iteration_id: int,
    response: Response,
    current_session: Annotated[
        UserSession,
        Depends(session_service.get_current_session),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PlanShareResponse:
    """Create a new immutable snapshot and revoke this owner's prior link."""
    response.headers["Cache-Control"] = "no-store"
    service = PlanShareService(db)
    share = await service.create(iteration_id, current_session)
    if share is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found",
        )
    return service.to_response(share)


@router.get(
    "/plan-shares/{public_id}",
    response_model=PlanShareResponse,
)
async def get_plan_share(
    public_id: str,
    response: Response,
    _current_session: Annotated[
        UserSession,
        Depends(session_service.get_current_session),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PlanShareResponse:
    """Resolve a token-scoped immutable snapshot for read-only viewing."""
    response.headers["Cache-Control"] = "no-store"
    service = PlanShareService(db)
    share = await service.get_active_by_public_id(public_id)
    if share is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan share not found or no longer available",
        )
    return service.to_response(share)


@router.delete(
    "/plan-shares/{share_id}",
    response_model=MessageResponse,
)
async def revoke_plan_share(
    share_id: int,
    response: Response,
    current_session: Annotated[
        UserSession,
        Depends(session_service.get_current_session),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MessageResponse:
    """Revoke a share only when the current browser session owns it."""
    response.headers["Cache-Control"] = "no-store"
    revoked = await PlanShareService(db).revoke(share_id, current_session.id)
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan share not found or not owned by this session",
        )
    return MessageResponse(message="Plan share revoked", success=True)
