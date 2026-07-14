"""Saved view API router."""
from typing import Annotated, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user_session import UserSession
from app.schemas.common import MessageResponse
from app.schemas.saved_view import (
    SavedViewCreateRequest,
    SavedViewDashboardCardResponse,
    SavedViewDuplicateRequest,
    SavedViewResponse,
    SavedViewType,
    SavedViewUpdateRequest,
)
from app.services import session_service
from app.services.language_service import (
    backend_error_message,
    entity_deleted_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
)
from app.services.saved_view_service import (
    SavedViewPermissionError,
    SavedViewService,
    SavedViewValidationError,
)

router = APIRouter()


async def get_saved_view_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> SavedViewService:
    """Dependency for saved view service."""
    return SavedViewService(db)


async def raise_saved_view_http_error(service: SavedViewService, exc: Exception) -> NoReturn:
    """Map service/schema errors to saved-view API responses."""
    ui_language = await resolve_runtime_ui_language(service.db)
    detail = backend_error_message(str(exc), ui_language)
    if isinstance(exc, SavedViewPermissionError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail) from exc
    if isinstance(exc, (SavedViewValidationError, ValueError, ValidationError)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc
    raise exc


@router.get("/saved-views", response_model=list[SavedViewResponse])
async def list_saved_views(
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
    view_type: Annotated[SavedViewType, Query()],
):
    """List saved views visible to the current session."""
    return await service.list_visible(view_type, current_session.id)


@router.post(
    "/saved-views",
    response_model=SavedViewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_saved_view(
    data: SavedViewCreateRequest,
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Create a user-owned saved view."""
    try:
        return await service.create_for_session(data, current_session.id)
    except Exception as exc:
        await raise_saved_view_http_error(service, exc)


@router.get("/saved-views/dashboard-cards", response_model=list[SavedViewDashboardCardResponse])
async def list_saved_view_dashboard_cards(
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
    iteration_id: Annotated[int, Query(ge=1)],
):
    """List saved-view-backed dashboard cards for the selected iteration."""
    cards = await service.list_dashboard_cards(iteration_id, current_session.id)
    if cards is None:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("iteration", iteration_id, ui_language),
        )
    return cards


@router.get("/saved-views/{view_id}", response_model=SavedViewResponse)
async def get_saved_view(
    view_id: int,
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Get a saved view visible to the current session."""
    view = await service.get_visible_by_id(view_id, current_session.id)
    if not view:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("saved_view", view_id, ui_language),
        )
    return view


@router.put("/saved-views/{view_id}", response_model=SavedViewResponse)
async def update_saved_view(
    view_id: int,
    data: SavedViewUpdateRequest,
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Update a saved view owned by the current session."""
    try:
        view = await service.update_for_session(view_id, data, current_session.id)
    except Exception as exc:
        await raise_saved_view_http_error(service, exc)

    if not view:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("saved_view", view_id, ui_language),
        )
    return view


@router.delete("/saved-views/{view_id}", response_model=MessageResponse)
async def delete_saved_view(
    view_id: int,
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Delete a saved view owned by the current session."""
    try:
        deleted = await service.delete_for_session(view_id, current_session.id)
    except Exception as exc:
        await raise_saved_view_http_error(service, exc)

    if not deleted:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("saved_view", view_id, ui_language),
        )
    ui_language = await resolve_runtime_ui_language(service.db)
    return MessageResponse(message=entity_deleted_message("saved_view", view_id, ui_language), success=True)


@router.post(
    "/saved-views/{view_id}/duplicate",
    response_model=SavedViewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def duplicate_saved_view(
    view_id: int,
    data: SavedViewDuplicateRequest,
    service: Annotated[SavedViewService, Depends(get_saved_view_service)],
    current_session: Annotated[UserSession, Depends(session_service.get_current_session)],
):
    """Duplicate any valid visible saved view into a user-owned copy."""
    try:
        view = await service.duplicate_for_session(view_id, data, current_session.id)
    except Exception as exc:
        await raise_saved_view_http_error(service, exc)

    if not view:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("saved_view", view_id, ui_language),
        )
    return view
