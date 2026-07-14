"""Outbound webhook target and delivery API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.outbound_webhook import (
    OutboundWebhookDeliveryResponse,
    OutboundWebhookRetryResponse,
    OutboundWebhookTargetCreate,
    OutboundWebhookTargetResponse,
    OutboundWebhookTargetUpdate,
)
from app.services.language_service import (
    backend_error_message,
    entity_deleted_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
)
from app.services.outbound_webhook_service import (
    OutboundWebhookNotFoundError,
    OutboundWebhookService,
    OutboundWebhookValidationError,
)
from app.security import require_admin_api_key

router = APIRouter(dependencies=[Depends(require_admin_api_key)])


async def get_outbound_webhook_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> OutboundWebhookService:
    """Dependency for outbound webhook API operations."""
    return OutboundWebhookService(db)


async def _bad_request(service: OutboundWebhookService, error: Exception) -> HTTPException:
    ui_language = await resolve_runtime_ui_language(service.db)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=backend_error_message(str(error), ui_language))


@router.get(
    "/outbound-webhooks/targets",
    response_model=list[OutboundWebhookTargetResponse],
)
async def list_outbound_webhook_targets(
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """List outbound webhook targets."""
    return await service.list_targets()


@router.post(
    "/outbound-webhooks/targets",
    response_model=OutboundWebhookTargetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_outbound_webhook_target(
    data: OutboundWebhookTargetCreate,
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """Create an outbound webhook target."""
    try:
        return await service.create_target(data)
    except OutboundWebhookValidationError as exc:
        raise await _bad_request(service, exc)


@router.put(
    "/outbound-webhooks/targets/{target_id}",
    response_model=OutboundWebhookTargetResponse,
)
async def update_outbound_webhook_target(
    target_id: int,
    data: OutboundWebhookTargetUpdate,
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """Update an outbound webhook target."""
    try:
        target = await service.update_target(target_id, data)
    except OutboundWebhookValidationError as exc:
        raise await _bad_request(service, exc)
    if target is None:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("outbound_webhook_target", target_id, ui_language),
        )
    return target


@router.delete("/outbound-webhooks/targets/{target_id}", response_model=MessageResponse)
async def delete_outbound_webhook_target(
    target_id: int,
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """Delete an outbound webhook target while preserving delivery history."""
    deleted = await service.delete_target(target_id)
    if not deleted:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("outbound_webhook_target", target_id, ui_language),
        )
    ui_language = await resolve_runtime_ui_language(service.db)
    return MessageResponse(message=entity_deleted_message("outbound_webhook_target", target_id, ui_language), success=True)


@router.post(
    "/outbound-webhooks/targets/{target_id}/test",
    response_model=OutboundWebhookRetryResponse,
)
async def test_outbound_webhook_target(
    target_id: int,
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """Send a test event to one webhook target."""
    result = await service.test_target(target_id)
    if result is None:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("outbound_webhook_target", target_id, ui_language),
        )
    return result


@router.get(
    "/outbound-webhooks/deliveries",
    response_model=list[OutboundWebhookDeliveryResponse],
)
async def list_outbound_webhook_deliveries(
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
    target_id: Optional[int] = Query(None, gt=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    channel: str = Query("webhook"),
    limit: int = Query(50, ge=1, le=200),
):
    """List recent outbound webhook deliveries."""
    try:
        return await service.list_deliveries(
            target_id=target_id,
            status=status_filter,
            channel=channel,
            limit=limit,
        )
    except OutboundWebhookValidationError as exc:
        raise await _bad_request(service, exc)


@router.post(
    "/outbound-webhooks/deliveries/{delivery_id}/retry",
    response_model=OutboundWebhookRetryResponse,
)
async def retry_outbound_webhook_delivery(
    delivery_id: int,
    service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)],
):
    """Retry one outbound webhook or notification delivery."""
    try:
        result = await service.retry_delivery(delivery_id)
    except OutboundWebhookValidationError as exc:
        raise await _bad_request(service, exc)
    except OutboundWebhookNotFoundError as exc:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=backend_error_message(str(exc), ui_language))
    if result is None:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("outbound_webhook_delivery", delivery_id, ui_language),
        )
    return result
