"""Runtime system settings API router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.system_settings import (
    AppRuntimeSettingsResponse,
    AppRuntimeSettingsUpdate,
    GitHubRuntimeSettingsResponse,
    GitHubRuntimeSettingsUpdate,
    LLMRuntimeSettingsResponse,
    LLMRuntimeSettingsUpdate,
    SystemSettingsResponse,
    WebIntakeRuntimeSettingsResponse,
    WebIntakeRuntimeSettingsUpdate,
)
from app.services.system_settings_service import RuntimeSettingsError, RuntimeSettingsService
from app.security import require_admin_api_key

router = APIRouter(dependencies=[Depends(require_admin_api_key)])


async def get_runtime_settings_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> RuntimeSettingsService:
    """Dependency for runtime system settings."""
    return RuntimeSettingsService(db)


def _bad_request(error: ValueError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/system-settings", response_model=SystemSettingsResponse)
async def get_system_settings(
    service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)],
):
    """Return resolved runtime settings and restart-required env settings."""
    return await service.system_response()


@router.put("/system-settings/llm", response_model=LLMRuntimeSettingsResponse)
async def update_llm_settings(
    data: LLMRuntimeSettingsUpdate,
    service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)],
):
    """Update runtime LLM settings."""
    try:
        return await service.update_llm(data)
    except RuntimeSettingsError as exc:
        raise _bad_request(exc) from exc


@router.put("/system-settings/app", response_model=AppRuntimeSettingsResponse)
async def update_app_settings(
    data: AppRuntimeSettingsUpdate,
    service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)],
):
    """Update runtime app language settings."""
    try:
        return await service.update_app(data)
    except RuntimeSettingsError as exc:
        raise _bad_request(exc) from exc


@router.put("/system-settings/github", response_model=GitHubRuntimeSettingsResponse)
async def update_github_settings(
    data: GitHubRuntimeSettingsUpdate,
    service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)],
):
    """Update runtime GitHub settings."""
    try:
        return await service.update_github(data)
    except RuntimeSettingsError as exc:
        raise _bad_request(exc) from exc


@router.put("/system-settings/web-intake", response_model=WebIntakeRuntimeSettingsResponse)
async def update_web_intake_settings(
    data: WebIntakeRuntimeSettingsUpdate,
    service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)],
):
    """Update runtime controlled web-intake settings."""
    try:
        return await service.update_web_intake(data)
    except RuntimeSettingsError as exc:
        raise _bad_request(exc) from exc
