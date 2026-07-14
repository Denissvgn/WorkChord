"""Label taxonomy API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.label import (
    LabelCreate,
    LabelGroupCreate,
    LabelGroupResponse,
    LabelGroupUpdate,
    LabelResponse,
    LabelUpdate,
)
from app.services.language_service import entity_not_found_message, resolve_runtime_ui_language
from app.services.label_service import LabelConflictError, LabelService

router = APIRouter()


async def get_label_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LabelService:
    """Dependency for label service."""
    return LabelService(db)


@router.get("/label-groups", response_model=list[LabelGroupResponse])
async def list_label_groups(
    service: Annotated[LabelService, Depends(get_label_service)],
    include_inactive: bool = Query(False),
):
    """List governed label groups."""
    return await service.list_groups(include_inactive=include_inactive)


@router.post(
    "/label-groups",
    response_model=LabelGroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_label_group(
    data: LabelGroupCreate,
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Create a governed label group."""
    try:
        return await service.create_group(data)
    except LabelConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.put("/label-groups/{group_id}", response_model=LabelGroupResponse)
async def update_label_group(
    group_id: int,
    data: LabelGroupUpdate,
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Update a governed label group."""
    try:
        group = await service.update_group(group_id, data)
    except LabelConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if not group:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("label_group", group_id, ui_language),
        )
    return group


@router.get("/labels", response_model=list[LabelResponse])
async def list_labels(
    service: Annotated[LabelService, Depends(get_label_service)],
    group_key: Annotated[Optional[str], Query()] = None,
    include_inactive: bool = Query(False),
    q: Annotated[Optional[str], Query()] = None,
):
    """List governed labels."""
    return await service.list_labels(
        group_key=group_key,
        include_inactive=include_inactive,
        q=q,
    )


@router.post(
    "/labels",
    response_model=LabelResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_label(
    data: LabelCreate,
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Create a governed label."""
    try:
        return await service.create_label(data)
    except LabelConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/labels/{label_id}", response_model=LabelResponse)
async def update_label(
    label_id: int,
    data: LabelUpdate,
    service: Annotated[LabelService, Depends(get_label_service)],
):
    """Update a governed label."""
    try:
        label = await service.update_label(label_id, data)
    except LabelConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not label:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("label", label_id, ui_language),
        )
    return label
