"""Browser identity lifecycle API."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user_session import UserSession
from app.schemas.common import MessageResponse
from app.schemas.session import UserSession as UserSessionSchema
from app.services import session_service


router = APIRouter()


@router.get("/session/whoami", response_model=UserSessionSchema)
async def whoami(
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
) -> UserSession:
    """Return privacy-safe attribution for the current opaque browser session."""
    return current_session


@router.post("/session/rotate", response_model=UserSessionSchema)
async def rotate_session(
    response: Response,
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserSession:
    """Rotate the browser token without changing saved-view ownership."""
    return await session_service.rotate_session(db, current_session, response)


@router.delete("/session", response_model=MessageResponse)
async def revoke_session(
    response: Response,
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MessageResponse:
    """Revoke the current browser identity."""
    await session_service.revoke_session(db, current_session, response)
    return MessageResponse(message="Browser session revoked")
