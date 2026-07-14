"""Request source linking API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.request_source import (
    RequestSourceLinkCreateRequest,
    RequestSourceLinkWithSourceResponse,
    RequestSourceResponse,
)
from app.services.request_source_service import (
    RequestSourceConflictError,
    RequestSourceNotFoundError,
    RequestSourceService,
    RequestSourceTargetNotFoundError,
    RequestSourceValidationError,
)

router = APIRouter()


async def get_request_source_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> RequestSourceService:
    """Dependency for request-source service."""
    return RequestSourceService(db)


def _bad_request(error: Exception) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


def _not_found(error: Exception) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("/request-sources", response_model=list[RequestSourceResponse])
async def search_request_sources(
    service: Annotated[RequestSourceService, Depends(get_request_source_service)],
    q: Optional[str] = Query(None, min_length=1),
    source_type: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
):
    """Search request sources for linking."""
    try:
        return await service.search_sources(q=q, source_type=source_type, limit=limit)
    except RequestSourceValidationError as e:
        raise _bad_request(e)


@router.get(
    "/request-source-links",
    response_model=list[RequestSourceLinkWithSourceResponse],
)
async def list_request_source_links(
    service: Annotated[RequestSourceService, Depends(get_request_source_service)],
    target_type: str = Query(...),
    target_id: int = Query(..., gt=0),
):
    """List request-source links for one target."""
    try:
        return await service.list_links_for_target(target_type, target_id)
    except RequestSourceValidationError as e:
        raise _bad_request(e)
    except RequestSourceTargetNotFoundError as e:
        raise _not_found(e)


@router.post(
    "/request-source-links",
    response_model=RequestSourceLinkWithSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_request_source_link(
    raw_data: Annotated[dict, Body(...)],
    service: Annotated[RequestSourceService, Depends(get_request_source_service)],
):
    """Create a request source and link, or link an existing source."""
    try:
        data = RequestSourceLinkCreateRequest.model_validate(raw_data)
        return await service.create_link(data)
    except ValidationError as e:
        raise _bad_request(e)
    except RequestSourceValidationError as e:
        raise _bad_request(e)
    except RequestSourceTargetNotFoundError as e:
        raise _not_found(e)
    except RequestSourceNotFoundError as e:
        raise _not_found(e)
    except RequestSourceConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/request-source-links/{link_id}", response_model=MessageResponse)
async def delete_request_source_link(
    link_id: int,
    service: Annotated[RequestSourceService, Depends(get_request_source_service)],
):
    """Unlink a request source from a target."""
    deleted = await service.unlink(link_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request source link with id {link_id} not found",
        )
    return MessageResponse(message=f"Request source link {link_id} deleted", success=True)
