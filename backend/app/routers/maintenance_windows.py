"""Operator commands for a coordinated control-plane maintenance window."""

from typing import Annotated, Any, NoReturn

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.authority import AuthorityError
from app.database import get_db
from app.schemas.maintenance import (
    MaintenanceWindowCancel,
    MaintenanceWindowClose,
    MaintenanceWindowCreate,
    MaintenanceWindowNotice,
)
from app.services.maintenance_window_service import MaintenanceWindowConflict, MaintenanceWindowService


def require_operator(request: Request) -> None:
    authority = getattr(request.state, "authority", None)
    if authority is None or not authority.operator:
        raise AuthorityError("operator_required", "Workspace operator permission is required.")


router = APIRouter(dependencies=[Depends(require_operator)])


async def get_maintenance_window_service(
    db: Annotated[AsyncSession, Depends(get_db, scope="function")],
) -> MaintenanceWindowService:
    return MaintenanceWindowService(db)


Service = Annotated[MaintenanceWindowService, Depends(get_maintenance_window_service)]


def _refuse(exc: Exception) -> NoReturn:
    if isinstance(exc, MaintenanceWindowConflict):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail())
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"code": "maintenance_window_not_found", "message": str(exc)})
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"code": "maintenance_window_invalid", "message": str(exc)})
    raise exc


@router.get("/maintenance-windows", response_model=list[dict[str, Any]])
async def list_maintenance_windows(service: Service, limit: int = Query(20, ge=1, le=100)):
    """Return recent windows, newest first, with their recorded actual times."""
    return await service.list_windows(limit=limit)


@router.post("/maintenance-windows", response_model=dict[str, Any], status_code=status.HTTP_201_CREATED)
async def announce_maintenance_window(data: MaintenanceWindowCreate, service: Service):
    """Announce a bounded window. Admission for new work closes immediately."""
    try:
        return await service.announce(data)
    except Exception as exc:
        _refuse(exc)


@router.get("/maintenance-windows/{window_id}", response_model=dict[str, Any])
async def get_maintenance_window(window_id: int, service: Service):
    """Return the window, its receipts, and what still blocks a safe begin."""
    try:
        return await service.status(window_id)
    except Exception as exc:
        _refuse(exc)


@router.post("/maintenance-windows/{window_id}/notices", response_model=dict[str, Any])
async def record_maintenance_notice(window_id: int, data: MaintenanceWindowNotice, service: Service):
    """Record that a PM was notified through another channel. It never admits a live claim."""
    try:
        return await service.record_pm_notice(window_id, data)
    except Exception as exc:
        _refuse(exc)


@router.post("/maintenance-windows/{window_id}/begin", response_model=dict[str, Any])
async def begin_maintenance_window(window_id: int, service: Service):
    """Begin the window and record the protected claims, or list every blocker."""
    try:
        return await service.begin(window_id)
    except Exception as exc:
        _refuse(exc)


@router.post("/maintenance-windows/{window_id}/complete", response_model=dict[str, Any])
async def complete_maintenance_window(window_id: int, data: MaintenanceWindowClose, service: Service):
    """Close a begun window, record its actual end and each protected claim's resumption."""
    try:
        return await service.close(window_id, data)
    except Exception as exc:
        _refuse(exc)


@router.post("/maintenance-windows/{window_id}/cancel", response_model=dict[str, Any])
async def cancel_maintenance_window(window_id: int, data: MaintenanceWindowCancel, service: Service):
    """Withdraw an announced window before it begins and reopen admission."""
    try:
        return await service.cancel(window_id, data.note)
    except Exception as exc:
        _refuse(exc)
