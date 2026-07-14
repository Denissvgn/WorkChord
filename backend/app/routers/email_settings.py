"""Email settings API router."""
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.email_settings import (
    EmailSettingsUpdate,
    EmailSettingsResponse,
    TestEmailRequest,
    TestEmailResponse,
)
from app.security import require_admin_api_key
from app.services.email_settings_service import EmailSettingsService
from app.services.system_settings_service import RuntimeSettingsError

router = APIRouter(dependencies=[Depends(require_admin_api_key)])
logger = logging.getLogger(__name__)


def _response(settings) -> EmailSettingsResponse:
    return EmailSettingsResponse(
        enabled=settings.enabled,
        smtp_host=settings.smtp_host,
        smtp_port=settings.smtp_port,
        smtp_user=settings.smtp_user,
        smtp_from_email=settings.smtp_from_email,
        smtp_use_tls=settings.smtp_use_tls,
        has_password=settings.has_password,
        field_sources=settings.field_sources,
    )


async def get_settings_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> EmailSettingsService:
    """Get email settings service singleton."""
    return EmailSettingsService(db)


@router.get("/email-settings", response_model=EmailSettingsResponse)
async def get_email_settings(
    service: Annotated[EmailSettingsService, Depends(get_settings_service)],
):
    """Get current email settings (password masked)."""
    try:
        settings = await service.get_settings()
    except RuntimeSettingsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return _response(settings)


@router.put("/email-settings", response_model=EmailSettingsResponse)
async def update_email_settings(
    data: EmailSettingsUpdate,
    service: Annotated[EmailSettingsService, Depends(get_settings_service)],
):
    """Update email settings."""
    try:
        settings = await service.update_settings(
            enabled=data.enabled,
            smtp_host=data.smtp_host,
            smtp_port=data.smtp_port,
            smtp_user=data.smtp_user,
            smtp_password=data.smtp_password,
            smtp_from_email=data.smtp_from_email,
            smtp_use_tls=data.smtp_use_tls,
            clear_smtp_password=data.clear_smtp_password,
        )

        return _response(settings)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Unexpected persistence/encryption failures stay server errors with the
        # existing response contract and a full internal diagnostic.
        logger.error("Failed to save email settings", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save email settings: {str(e)}"
        ) from e


@router.post("/email-settings/test", response_model=TestEmailResponse)
async def test_email_settings(
    data: TestEmailRequest,
    service: Annotated[EmailSettingsService, Depends(get_settings_service)],
):
    """Send a test email to verify settings."""
    success, message = await service.test_connection(data.recipient)

    return TestEmailResponse(
        success=success,
        message=message,
    )
