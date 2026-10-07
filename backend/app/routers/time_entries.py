"""Optional human-authored time records with private correction history."""

from datetime import date
from typing import Annotated
from typing import Literal

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.routers.task_domain import domain_result
from app.schemas.time_entry import TimeEntryCreate, TimeEntryCorrection, TimeEntryVoid, TimeEntryResponse, TimeEntryPage, TimeRevisionPage, TimeEntryCapabilities
from app.services.time_entry_service import TimeEntryService
from app.services.time_report_service import TimeReportService
from app.schemas.time_report import TimeReportPage

def prevent_private_caching(response: Response):
    response.headers["Cache-Control"] = "private, no-store"


router = APIRouter(prefix="/time-entries", dependencies=[Depends(prevent_private_caching)])
DB = Annotated[AsyncSession, Depends(get_db, scope="function")]


@router.get("/capabilities", response_model=TimeEntryCapabilities)
async def capabilities(db: DB):
    authority = db.info.get("authority")
    human = bool(authority and authority.kind == "human" and authority.principal_id is not None)
    return {"schema_version": 1, "enabled": get_settings().time_entries_enabled and human,
        "human_identity_required": not human, "units": "whole_minutes", "privacy": "private_entries_manager_totals"}


@router.get("", response_model=TimeEntryPage)
async def list_entries(db: DB, project_id: int | None = Query(default=None, ge=1), task_id: int | None = Query(default=None, ge=1),
    start: date | None = None, end: date | None = None, after_id: int = Query(default=0, ge=0),
    upper_id: int | None = Query(default=None, ge=0), limit: int = Query(default=50, ge=1, le=100), include_voided: bool = False):
    return await domain_result(TimeEntryService(db).list(project_id=project_id, task_id=task_id, start=start, end=end,
        after_id=after_id, upper_id=upper_id, limit=limit, include_voided=include_voided))


@router.post("", response_model=TimeEntryResponse, status_code=201)
async def create_entry(data: TimeEntryCreate, db: DB):
    return await domain_result(TimeEntryService(db).create(data))


@router.get("/report", response_model=TimeReportPage)
async def report(db: DB, project_id: int = Query(ge=1), start: date = Query(), end: date = Query(),
    scope: Literal["mine", "project"] = "mine", after_id: int = Query(default=0, ge=0),
    upper_id: int | None = Query(default=None, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(TimeReportService(db).page(project_id, start, end, scope=scope,
        after_id=after_id, upper_id=upper_id, limit=limit))


@router.get("/export", response_class=Response, responses={200: {"description": "Scoped recorded time CSV",
    "content": {"text/csv": {"schema": {"type": "string", "format": "binary"}}}}})
async def export(db: DB, project_id: int = Query(ge=1), start: date = Query(), end: date = Query(),
    scope: Literal["mine", "project"] = "mine", kind: Literal["totals", "entries"] = "totals"):
    content = await domain_result(TimeReportService(db).export(project_id, start, end, scope=scope, kind=kind))
    return Response(content=content, media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="recorded-time.csv"',
        "Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"})


@router.get("/{entry_id}", response_model=TimeEntryResponse)
async def get_entry(entry_id: int, db: DB):
    service = TimeEntryService(db)
    return service.serialize(await domain_result(service.get(entry_id)))


@router.put("/{entry_id}", response_model=TimeEntryResponse)
async def correct_entry(entry_id: int, data: TimeEntryCorrection, db: DB):
    return await domain_result(TimeEntryService(db).correct(entry_id, data))


@router.post("/{entry_id}/void", response_model=TimeEntryResponse)
async def void_entry(entry_id: int, data: TimeEntryVoid, db: DB):
    return await domain_result(TimeEntryService(db).correct(entry_id, data, void=True))


@router.get("/{entry_id}/history", response_model=TimeRevisionPage)
async def history(entry_id: int, db: DB, after_version: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(TimeEntryService(db).history(entry_id, after_version=after_version, limit=limit))
