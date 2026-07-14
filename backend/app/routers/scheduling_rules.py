"""Scheduling rules API router."""
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.scheduling_rules import (
    SchedulingRulesSchema,
    SchedulingRulesResponse,
)
from app.schemas.common import MessageResponse
from app.security import require_admin_api_key
from app.services.scheduling_rules_service import SchedulingRulesService

router = APIRouter(dependencies=[Depends(require_admin_api_key)])
logger = logging.getLogger(__name__)


def get_rules_service() -> SchedulingRulesService:
    """Get scheduling rules service singleton."""
    return SchedulingRulesService.get_instance()


@router.get("/scheduling-rules", response_model=SchedulingRulesResponse)
async def get_scheduling_rules():
    """Get current scheduling rules configuration."""
    service = get_rules_service()

    try:
        rules_dict = service.get_rules_as_dict()
        source = "yaml" if service.has_rules else "defaults"

        return SchedulingRulesResponse(
            rules=SchedulingRulesSchema(**rules_dict),
            source=source
        )
    except Exception as e:
        logger.error("Failed to load scheduling rules", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load scheduling rules: {str(e)}"
        ) from e


@router.put("/scheduling-rules", response_model=SchedulingRulesResponse)
async def update_scheduling_rules(rules: SchedulingRulesSchema):
    """Update scheduling rules configuration."""
    service = get_rules_service()

    try:
        service.update_rules(rules.model_dump())
        return SchedulingRulesResponse(
            rules=rules,
            source="yaml"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to update scheduling rules", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update scheduling rules: {str(e)}"
        ) from e


@router.post("/scheduling-rules/reset", response_model=SchedulingRulesResponse)
async def reset_scheduling_rules():
    """Reset scheduling rules to default values."""
    service = get_rules_service()

    try:
        service.reset_to_defaults()
        rules_dict = service.get_rules_as_dict()

        return SchedulingRulesResponse(
            rules=SchedulingRulesSchema(**rules_dict),
            source="defaults"
        )
    except Exception as e:
        logger.error("Failed to reset scheduling rules", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset scheduling rules: {str(e)}"
        ) from e
