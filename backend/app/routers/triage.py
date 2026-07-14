"""Triage API router."""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.team import AssigneeRecommendationResponse
from app.schemas.triage import (
    TriageActionRequest,
    TriageClassificationSuggestionResponse,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageDuplicateSuggestionsResponse,
    TriageItemCreate,
    TriageItemResponse,
    TriageItemStatus,
    TriageItemUpdate,
    TriageSnoozeRequest,
    TriageTaskDraftRequest,
    TriageTaskDraftResponse,
)
from app.services.assignee_recommendation_service import AssigneeRecommendationService
from app.services.language_service import (
    backend_error_message,
    entity_not_found_message,
    resolve_runtime_ui_language,
)
from app.services.llm_service import LLMService
from app.services.triage_service import (
    TriageConflictError,
    TriageDraftNotFoundError,
    TriageService,
)

router = APIRouter()


async def get_triage_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TriageService:
    """Dependency for triage service."""
    return TriageService(db)


async def get_llm_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LLMService:
    """Dependency for LLM-powered triage classification."""
    return await LLMService.from_runtime(db)


async def get_assignee_recommendation_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> AssigneeRecommendationService:
    """Dependency for assignee recommendation service."""
    return AssigneeRecommendationService(db)


async def _bad_request(service, error: ValueError) -> HTTPException:
    ui_language = await resolve_runtime_ui_language(service.db)
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=backend_error_message(str(error), ui_language),
    )


async def _not_found_detail(service, triage_item_id: int) -> str:
    ui_language = await resolve_runtime_ui_language(service.db)
    return entity_not_found_message("triage_item", triage_item_id, ui_language)


@router.get("/triage", response_model=list[TriageItemResponse])
async def list_triage_items(
    service: Annotated[TriageService, Depends(get_triage_service)],
    active: Annotated[Optional[bool], Query()] = True,
    statuses: Annotated[Optional[list[TriageItemStatus]], Query(alias="status")] = None,
    q: Optional[str] = Query(None, min_length=1),
    source: Optional[str] = Query(None, min_length=1, max_length=100),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """List triage items."""
    return await service.list_items(
        active=active,
        statuses=statuses,
        q=q,
        source=source,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/triage",
    response_model=TriageItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_triage_item(
    data: TriageItemCreate,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Create a triage item."""
    try:
        return await service.create(data)
    except ValueError as e:
        raise await _bad_request(service, e)


@router.get("/triage/{triage_item_id}", response_model=TriageItemResponse)
async def get_triage_item(
    triage_item_id: int,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Get a triage item by ID."""
    item = await service.get_by_id(triage_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.get(
    "/triage/{triage_item_id}/duplicate-suggestions",
    response_model=TriageDuplicateSuggestionsResponse,
)
async def get_triage_duplicate_suggestions(
    triage_item_id: int,
    service: Annotated[TriageService, Depends(get_triage_service)],
    limit_per_type: int = Query(5, ge=1, le=20),
    min_score: float = Query(0.1, ge=0),
):
    """Get advisory duplicate suggestions for a triage item."""
    suggestions = await service.get_duplicate_suggestions(
        triage_item_id,
        limit_per_type=limit_per_type,
        min_score=min_score,
    )
    if not suggestions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return suggestions


@router.post(
    "/triage/{triage_item_id}/classify",
    response_model=TriageClassificationSuggestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def classify_triage_item(
    triage_item_id: int,
    service: Annotated[TriageService, Depends(get_triage_service)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
):
    """Create an advisory classification suggestion for a triage item."""
    suggestion = await service.classify_item(triage_item_id, llm_service=llm_service)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return suggestion


@router.get(
    "/triage/{triage_item_id}/assignee-recommendations",
    response_model=list[AssigneeRecommendationResponse],
)
async def get_triage_assignee_recommendations(
    triage_item_id: int,
    service: Annotated[AssigneeRecommendationService, Depends(get_assignee_recommendation_service)],
    iteration_id: Optional[int] = Query(None),
):
    """Return explainable assignee recommendations for a triage item."""
    try:
        recommendations = await service.recommend_for_triage(
            triage_item_id,
            iteration_id=iteration_id,
        )
    except ValueError as e:
        raise await _bad_request(service, e)
    if recommendations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return recommendations


@router.get(
    "/triage/{triage_item_id}/classification-suggestions",
    response_model=list[TriageClassificationSuggestionResponse],
)
async def list_triage_classification_suggestions(
    triage_item_id: int,
    service: Annotated[TriageService, Depends(get_triage_service)],
    limit: int = Query(20, ge=1, le=100),
):
    """List stored advisory classification suggestions for a triage item."""
    suggestions = await service.list_classification_suggestions(
        triage_item_id,
        limit=limit,
    )
    if suggestions is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return suggestions


@router.post(
    "/triage/{triage_item_id}/draft-task",
    response_model=TriageTaskDraftResponse,
)
async def draft_triage_task(
    triage_item_id: int,
    data: TriageTaskDraftRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
):
    """Generate transient task draft details for triage conversion."""
    try:
        draft = await service.draft_task(
            triage_item_id,
            data,
            llm_service=llm_service,
        )
    except TriageDraftNotFoundError as e:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=backend_error_message(str(e), ui_language),
        )
    except ValueError as e:
        raise await _bad_request(service, e)

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return draft


@router.put("/triage/{triage_item_id}", response_model=TriageItemResponse)
async def update_triage_item(
    triage_item_id: int,
    data: TriageItemUpdate,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Update editable triage item metadata."""
    try:
        item = await service.update(triage_item_id, data)
    except ValueError as e:
        raise await _bad_request(service, e)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.post("/triage/{triage_item_id}/accept", response_model=TriageItemResponse)
async def accept_triage_item(
    triage_item_id: int,
    data: TriageActionRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Accept a triage item."""
    item = await service.accept(triage_item_id, data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.post("/triage/{triage_item_id}/decline", response_model=TriageItemResponse)
async def decline_triage_item(
    triage_item_id: int,
    data: TriageActionRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Decline a triage item."""
    item = await service.decline(triage_item_id, data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.post("/triage/{triage_item_id}/snooze", response_model=TriageItemResponse)
async def snooze_triage_item(
    triage_item_id: int,
    data: TriageSnoozeRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Snooze a triage item."""
    try:
        item = await service.snooze(triage_item_id, data)
    except ValueError as e:
        raise await _bad_request(service, e)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.post("/triage/{triage_item_id}/mark-duplicate", response_model=TriageItemResponse)
async def mark_triage_item_duplicate(
    triage_item_id: int,
    data: TriageDuplicateRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Mark a triage item as duplicate."""
    try:
        item = await service.mark_duplicate(triage_item_id, data)
    except ValueError as e:
        raise await _bad_request(service, e)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )
    return item


@router.post(
    "/triage/{triage_item_id}/convert-to-task",
    response_model=TriageConvertToTaskResponse,
)
async def convert_triage_item_to_task(
    triage_item_id: int,
    data: TriageConvertToTaskRequest,
    service: Annotated[TriageService, Depends(get_triage_service)],
):
    """Convert a triage item to a planned task."""
    try:
        result = await service.convert_to_task(triage_item_id, data)
    except TriageConflictError as e:
        ui_language = await resolve_runtime_ui_language(service.db)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=backend_error_message(str(e), ui_language),
        )
    except ValueError as e:
        raise await _bad_request(service, e)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(service, triage_item_id),
        )

    item, task = result
    return TriageConvertToTaskResponse(
        triage_item=TriageItemResponse.model_validate(item),
        task=service.task_service.task_to_response(task),
    )
