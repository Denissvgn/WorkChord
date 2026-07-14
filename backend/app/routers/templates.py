"""Template API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.template import (
    TemplateType,
    WorkTemplateCreate,
    WorkTemplateResponse,
    WorkTemplateUpdate,
)
from app.services.language_service import entity_not_found_message, resolve_runtime_ui_language
from app.services.template_service import TemplateService

router = APIRouter()


async def get_template_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TemplateService:
    """Dependency for template service."""
    return TemplateService(db)


@router.get("/templates", response_model=list[WorkTemplateResponse])
async def list_templates(
    service: Annotated[TemplateService, Depends(get_template_service)],
    template_type: Annotated[Optional[TemplateType], Query()] = None,
    include_inactive: bool = Query(False),
):
    """List reusable templates."""
    return await service.list_templates(
        template_type=template_type,
        include_inactive=include_inactive,
    )


@router.post(
    "/templates",
    response_model=WorkTemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    data: WorkTemplateCreate,
    service: Annotated[TemplateService, Depends(get_template_service)],
):
    """Create a reusable template."""
    return await service.create(data)


@router.get("/templates/{template_id}", response_model=WorkTemplateResponse)
async def get_template(
    template_id: int,
    service: Annotated[TemplateService, Depends(get_template_service)],
):
    """Get a template by ID."""
    template = await service.get_by_id(template_id)
    if not template:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("template", template_id, ui_language),
        )
    return template


@router.put("/templates/{template_id}", response_model=WorkTemplateResponse)
async def update_template(
    template_id: int,
    data: WorkTemplateUpdate,
    service: Annotated[TemplateService, Depends(get_template_service)],
):
    """Update a reusable template."""
    template = await service.update(template_id, data)
    if not template:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("template", template_id, ui_language),
        )
    return template
