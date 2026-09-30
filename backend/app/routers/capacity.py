"""Authenticated person availability and bounded capacity views."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.capacity_service import CapacityService

router = APIRouter()
Database = Annotated[AsyncSession, Depends(get_db, scope="function")]


class CalendarSelection(BaseModel):
    calendar_id: int = Field(gt=0)
    expected_version: int = Field(ge=0)


class AbsenceInput(BaseModel):
    start_date: date
    end_date: date


class AbsenceUpdate(AbsenceInput):
    expected_version: int = Field(gt=0)
    deleted: bool = False


@router.get("/team-member-profiles/{profile_id}/availability")
async def get_availability(profile_id: int, db: Database):
    return await CapacityService(db).detail(profile_id)


@router.put("/team-member-profiles/{profile_id}/availability")
async def set_availability(profile_id: int, data: CalendarSelection, db: Database):
    return await CapacityService(db).set_calendar(profile_id, data.calendar_id, data.expected_version)


@router.post("/team-member-profiles/{profile_id}/absences", status_code=201)
async def create_absence(profile_id: int, data: AbsenceInput, db: Database):
    service = CapacityService(db)
    await service.save_absence(profile_id, data.start_date, data.end_date)
    return await service.detail(profile_id)


@router.put("/team-member-profiles/{profile_id}/absences/{absence_id}")
async def update_absence(profile_id: int, absence_id: int, data: AbsenceUpdate, db: Database):
    service = CapacityService(db)
    await service.save_absence(profile_id, data.start_date, data.end_date, absence_id=absence_id,
                              expected_version=data.expected_version, deleted=data.deleted)
    return await service.detail(profile_id)


@router.get("/team-member-profiles/{profile_id}/capacity")
async def get_profile_capacity(profile_id: int, start: date, end: date, db: Database):
    return await CapacityService(db).projection(profile_id, start, end)
