"""Iteration API router."""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.iteration import (
    IterationCreate,
    IterationSeriesCreate,
    IterationSeriesResponse,
    IterationUpdate,
    IterationResponse,
    IterationSummary,
)
from app.schemas.common import MessageResponse
from app.query_limits import MAX_ITERATION_LIST_ITEMS
from app.services.iteration_service import IterationService

router = APIRouter()


async def get_iteration_service(db: Annotated[AsyncSession, Depends(get_db)]) -> IterationService:
    """Dependency for iteration service."""
    return IterationService(db)


@router.get("/iterations", response_model=list[IterationResponse])
async def get_iterations(
    service: Annotated[IterationService, Depends(get_iteration_service)],
    limit: Annotated[
        int | None,
        Query(ge=1, le=MAX_ITERATION_LIST_ITEMS),
    ] = None,
    cursor_start_date: date | None = None,
    cursor_id: int | None = None,
):
    """Get the compatible small list or one explicit stable keyset page."""
    try:
        if limit is None:
            if cursor_start_date is not None or cursor_id is not None:
                raise ValueError("an iteration cursor requires an explicit limit")
            iterations = await service.get_all()
        else:
            iterations = await service.get_page(
                limit=limit,
                cursor_start_date=cursor_start_date,
                cursor_id=cursor_id,
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return [service.to_response(iteration) for iteration in iterations]


@router.post(
    "/iterations",
    response_model=IterationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_iteration(
    data: IterationCreate,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Create a new iteration."""
    try:
        iteration = await service.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return service.to_response(iteration)


@router.post(
    "/iterations/series",
    response_model=IterationSeriesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_iteration_series(
    data: IterationSeriesCreate,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Create a back-to-back series of iterations."""
    try:
        iterations = await service.create_series(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return IterationSeriesResponse(
        iterations=[service.to_response(iteration) for iteration in iterations]
    )


@router.get("/iterations/{iteration_id}", response_model=IterationResponse)
async def get_iteration(
    iteration_id: int,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Get iteration by ID."""
    iteration = await service.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )
    return service.to_response(iteration)


@router.put("/iterations/{iteration_id}", response_model=IterationResponse)
async def update_iteration(
    iteration_id: int,
    data: IterationUpdate,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Update an iteration."""
    try:
        iteration = await service.update(iteration_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )
    return service.to_response(iteration)


@router.delete("/iterations/{iteration_id}", response_model=MessageResponse)
async def delete_iteration(
    iteration_id: int,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Delete an iteration."""
    deleted = await service.delete(iteration_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )
    return MessageResponse(message=f"Iteration {iteration_id} deleted", success=True)


@router.get("/iterations/{iteration_id}/summary", response_model=IterationSummary)
async def get_iteration_summary(
    iteration_id: int,
    service: Annotated[IterationService, Depends(get_iteration_service)]
):
    """Get iteration summary with statistics."""
    summary = await service.get_summary(iteration_id)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )
    return summary
