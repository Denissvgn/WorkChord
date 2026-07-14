"""Controlled external intake API router."""
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.intake import WebIntakeRequest
from app.schemas.triage import TriageItemResponse
from app.services.session_service import get_client_ip
from app.services.web_intake_service import (
    WebIntakeConfigurationError,
    WebIntakeRateLimitError,
    WebIntakeService,
    WebIntakeUnauthorizedError,
)
from app.services.system_settings_service import RuntimeSettingsService

router = APIRouter()


async def get_web_intake_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> WebIntakeService:
    """Dependency for controlled web intake."""
    settings = await RuntimeSettingsService(db).get_web_intake_settings()
    return WebIntakeService(
        db,
        token=settings.web_intake_token,
        rate_limit_per_minute=settings.web_intake_rate_limit_per_minute,
    )


@router.post(
    "/intake/web",
    response_model=TriageItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_web_intake_item(
    request: Request,
    raw_data: Annotated[Any, Body(...)],
    service: Annotated[WebIntakeService, Depends(get_web_intake_service)],
    authorization: Annotated[Optional[str], Header(alias="Authorization")] = None,
):
    """Create a triage item from a controlled external web/form intake payload."""
    try:
        data = WebIntakeRequest.model_validate(raw_data)
        client_ip = await get_client_ip(request)
        return await service.create_triage_item(
            data,
            authorization_header=authorization,
            client_ip=client_ip,
            user_agent=request.headers.get("User-Agent"),
        )
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except WebIntakeConfigurationError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except WebIntakeUnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except WebIntakeRateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
            headers={"Retry-After": str(e.retry_after_seconds)},
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
