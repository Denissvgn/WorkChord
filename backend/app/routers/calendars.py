"""Calendar API router."""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.calendar import (
    CalendarCreate, CalendarUpdate, CalendarResponse,
    CalendarImportRequest, CalendarImportResponse,
    WorkingDaysRequest, WorkingDaysResponse
)
from app.schemas.common import MessageResponse
from app.services.calendar_service import CalendarService

router = APIRouter()


async def get_calendar_service(db: Annotated[AsyncSession, Depends(get_db)]) -> CalendarService:
    """Dependency for calendar service."""
    return CalendarService(db)


@router.get("/calendars", response_model=list[CalendarResponse])
async def get_calendars(
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Get all calendars."""
    return await service.get_all()


@router.post(
    "/calendars",
    response_model=CalendarResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_calendar(
    data: CalendarCreate,
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Create a new calendar."""
    return await service.create(data)


@router.get("/calendars/{calendar_id}", response_model=CalendarResponse)
async def get_calendar(
    calendar_id: int,
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Get calendar by ID."""
    calendar = await service.get_by_id(calendar_id)
    if not calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calendar with id {calendar_id} not found"
        )
    return calendar


@router.put("/calendars/{calendar_id}", response_model=CalendarResponse)
async def update_calendar(
    calendar_id: int,
    data: CalendarUpdate,
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Update a calendar."""
    calendar = await service.update(calendar_id, data)
    if not calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calendar with id {calendar_id} not found"
        )
    return calendar


@router.delete("/calendars/{calendar_id}", response_model=MessageResponse)
async def delete_calendar(
    calendar_id: int,
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Delete a calendar."""
    try:
        deleted = await service.delete(calendar_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calendar with id {calendar_id} not found"
        )
    return MessageResponse(message=f"Calendar {calendar_id} deleted", success=True)


@router.post("/calendars/{calendar_id}/import-holidays", response_model=CalendarImportResponse)
async def import_calendar_holidays(
    calendar_id: int,
    data: CalendarImportRequest,
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Import holidays into a calendar from public data or CSV rows."""
    try:
        result = await service.import_holidays(calendar_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calendar with id {calendar_id} not found"
        )
    return result


@router.get("/calendars/{calendar_id}/working-days", response_model=WorkingDaysResponse)
async def get_working_days(
    calendar_id: int,
    start_date: Annotated[date, Query(description="Start date (ISO format)")],
    end_date: Annotated[date, Query(description="End date (ISO format)")],
    service: Annotated[CalendarService, Depends(get_calendar_service)]
):
    """Calculate working days for a period."""
    calendar = await service.get_by_id(calendar_id)
    if not calendar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calendar with id {calendar_id} not found"
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date"
        )

    return service.calculate_working_days(calendar, start_date, end_date)
