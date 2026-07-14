"""GitHub webhook API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.common import MessageResponse
from app.schemas.github import (
    GitHubStatusAutomationRuleCreate,
    GitHubStatusAutomationRuleResponse,
    GitHubStatusAutomationRuleUpdate,
    GitHubWebhookResponse,
)
from app.services.github_status_automation_service import GitHubStatusAutomationService
from app.services.github_webhook_service import (
    GitHubWebhookConfigurationError,
    GitHubWebhookPayloadError,
    GitHubWebhookService,
    GitHubWebhookSignatureError,
)
from app.services.language_service import (
    backend_error_message,
    entity_deleted_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
)

router = APIRouter()


async def get_github_webhook_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> GitHubWebhookService:
    """Dependency for GitHub webhook processing."""
    return await GitHubWebhookService.from_runtime(db)


async def get_github_status_automation_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> GitHubStatusAutomationService:
    """Dependency for GitHub status automation rule management."""
    return GitHubStatusAutomationService(db)


@router.get(
    "/github/status-automation-rules",
    response_model=list[GitHubStatusAutomationRuleResponse],
)
async def list_github_status_automation_rules(
    service: Annotated[
        GitHubStatusAutomationService,
        Depends(get_github_status_automation_service),
    ],
):
    """List GitHub status automation rules."""
    return await service.list_rules()


@router.post(
    "/github/status-automation-rules",
    response_model=GitHubStatusAutomationRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_github_status_automation_rule(
    raw_data: Annotated[dict, Body(...)],
    service: Annotated[
        GitHubStatusAutomationService,
        Depends(get_github_status_automation_service),
    ],
):
    """Create a GitHub status automation rule."""
    try:
        data = GitHubStatusAutomationRuleCreate.model_validate(raw_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return await service.create_rule(data)


@router.put(
    "/github/status-automation-rules/{rule_id}",
    response_model=GitHubStatusAutomationRuleResponse,
)
async def update_github_status_automation_rule(
    rule_id: int,
    raw_data: Annotated[dict, Body(...)],
    service: Annotated[
        GitHubStatusAutomationService,
        Depends(get_github_status_automation_service),
    ],
):
    """Update a GitHub status automation rule."""
    try:
        data = GitHubStatusAutomationRuleUpdate.model_validate(raw_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    rule = await service.update_rule(rule_id, data)
    if not rule:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("github_status_automation_rule", rule_id, ui_language),
        )
    return rule


@router.delete(
    "/github/status-automation-rules/{rule_id}",
    response_model=MessageResponse,
)
async def delete_github_status_automation_rule(
    rule_id: int,
    service: Annotated[
        GitHubStatusAutomationService,
        Depends(get_github_status_automation_service),
    ],
):
    """Delete a GitHub status automation rule."""
    deleted = await service.delete_rule(rule_id)
    if not deleted:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=entity_not_found_message("github_status_automation_rule", rule_id, ui_language),
        )
    ui_language = await resolve_runtime_ui_language(service.db)
    return MessageResponse(
        message=entity_deleted_message("github_status_automation_rule", rule_id, ui_language),
        success=True,
    )


@router.post("/github/webhooks", response_model=GitHubWebhookResponse)
async def receive_github_webhook(
    request: Request,
    service: Annotated[GitHubWebhookService, Depends(get_github_webhook_service)],
    github_event: Annotated[Optional[str], Header(alias="X-GitHub-Event")] = None,
    github_delivery: Annotated[Optional[str], Header(alias="X-GitHub-Delivery")] = None,
    github_signature: Annotated[Optional[str], Header(alias="X-Hub-Signature-256")] = None,
):
    """Receive and process a signed GitHub webhook delivery."""
    if not github_event:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=backend_error_message("Missing X-GitHub-Event header", ui_language),
        )

    body = await request.body()
    try:
        service.verify_signature(body, github_signature)
        payload = service.parse_payload(body)
        return await service.process(github_event, github_delivery, payload)
    except GitHubWebhookConfigurationError as exc:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=backend_error_message(str(exc), ui_language),
        ) from exc
    except GitHubWebhookSignatureError as exc:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=backend_error_message(str(exc), ui_language),
        ) from exc
    except GitHubWebhookPayloadError as exc:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=backend_error_message(str(exc), ui_language),
        ) from exc
