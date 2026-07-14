"""Task API router."""
import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDependencyCreate, TaskReorder, TaskMerge,
    TaskUnmerge, TaskImportTriageItemResponse, TasksImportRequest,
    TasksImportResponse, TaskStatusChange, TaskStatusChangeResponse,
    TaskStatusLogResponse, CascadeUpdateInfo, TaskBulkOperationRequest,
    TaskBulkOperationResponse, TaskMoveRequest, TaskBatchUpdateRequest,
    TaskBatchUpdateResponse, TaskBatchUpdateResponseItem,
)
from app.schemas.external_link import (
    ExternalLinkResponse,
    ExternalLinkUpdate,
    GitHubExternalLinkCreate,
    TaskExternalLinkCreate,
)
from app.schemas.agent import TaskTimelineResponse, TaskTimelineItem
from app.schemas.common import MessageResponse
from app.schemas.team import AssigneeRecommendationResponse
from app.services.agent_service import AgentService
from app.services.assignee_recommendation_service import AssigneeRecommendationService
from app.services.external_link_service import (
    ExternalLinkConflictError,
    ExternalLinkService,
    ExternalLinkValidationError,
)
from app.services.github_status_service import GitHubStatusService
from app.services.language_service import (
    backend_error_message,
    entity_not_found_message,
    invalid_status_transition_message,
    resolve_runtime_ui_language,
)
from app.services.task_bulk_operation_service import TaskBulkOperationService
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.iteration_service import IterationService
from app.services.scheduler_service import SchedulerService

router = APIRouter()
logger = logging.getLogger(__name__)


def _raise_task_version_conflict(exc: TaskVersionConflictError) -> None:
    """Raise the stable structured optimistic-concurrency response."""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=exc.detail(),
    ) from exc


async def _localized_detail(db: AsyncSession, message: str) -> str:
    ui_language = await resolve_runtime_ui_language(db)
    return backend_error_message(message, ui_language)


async def _not_found_detail(db: AsyncSession, entity: str, entity_id: int) -> str:
    ui_language = await resolve_runtime_ui_language(db)
    return entity_not_found_message(entity, entity_id, ui_language)


async def get_task_service(db: Annotated[AsyncSession, Depends(get_db)]) -> TaskService:
    """Dependency for task service."""
    return TaskService(db)


async def get_external_link_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ExternalLinkService:
    """Dependency for external link service."""
    return ExternalLinkService(db)


async def get_github_status_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> GitHubStatusService:
    """Dependency for GitHub status refresh service."""
    return await GitHubStatusService.from_runtime(db)


async def get_assignee_recommendation_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> AssigneeRecommendationService:
    """Dependency for assignee recommendation service."""
    return AssigneeRecommendationService(db)


async def get_task_bulk_operation_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> TaskBulkOperationService:
    """Dependency for selected-task bulk operation service."""
    return TaskBulkOperationService(db)


async def get_scheduler_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> SchedulerService:
    """Dependency for scheduler service."""
    return SchedulerService(db)


@router.get("/iterations/{iteration_id}/tasks", response_model=list[TaskResponse])
async def get_tasks(
    iteration_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get all tasks for an iteration (tree structure)."""
    # Get iteration to check end_date for overdue detection
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(db, "iteration", iteration_id)
        )

    tasks = await service.get_by_iteration(iteration_id)
    return [service.task_to_response(t, iteration.end_date) for t in tasks]


@router.post(
    "/iterations/{iteration_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    iteration_id: int,
    data: TaskCreate,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a new task in an iteration."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    try:
        task = await service.create(iteration_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(db, str(e))
        )
    return service.task_to_response(task, iteration.end_date)


async def apply_batch_update_items(
    service: TaskService,
    iteration_id: int,
    iteration_end_date,
    items,
) -> tuple[list[TaskResponse], list[TaskBatchUpdateResponseItem]]:
    """Apply a list of TaskBatchUpdateItem changes without committing.

    Shared by the batch-update endpoint (which commits afterwards) and the
    schedule preview endpoint (which rolls everything back). Raises ValueError
    or TaskVersionConflictError; transaction control stays with the caller.
    """
    updated_tasks_list: list[TaskResponse] = []
    results: list[TaskBatchUpdateResponseItem] = []
    for item in items:
        task = await service.get_by_id(item.task_id)
        if not task:
            raise ValueError(f"Task with id {item.task_id} not found")
        if task.iteration_id != iteration_id:
            raise ValueError(f"Task with id {item.task_id} does not belong to iteration {iteration_id}")

        res_task = None
        current_status_val = task.status.value if hasattr(task.status, 'value') else task.status
        new_status_val = item.update.status.value if hasattr(item.update.status, 'value') else item.update.status

        expected_version = (
            item.expected_version
            if item.expected_version is not None
            else item.update.expected_version
        )
        if item.update.status is not None and new_status_val != current_status_val:
            # Run status transition
            updated_task, _, _ = await service.change_status(
                task_id=item.task_id,
                new_status=item.update.status,
                reason=item.status_reason,
                expected_version=expected_version,
            )
            if not updated_task:
                raise ValueError(f"Invalid status transition for task {item.task_id}")

            # Remove status from TaskUpdate fields set so update() won't reject it
            update_values = item.update.model_dump(exclude_unset=True)
            update_values.pop("status", None)
            update_values["expected_version"] = updated_task.version
            fields_to_update = TaskUpdate(**update_values)

            res_task = await service.update(item.task_id, fields_to_update)
        else:
            # Remove status or update normally if it's the same or None
            update_values = item.update.model_dump(exclude_unset=True)
            update_values.pop("status", None)
            if item.expected_version is not None:
                update_values["expected_version"] = item.expected_version
            fields_to_update = TaskUpdate(**update_values)
            res_task = await service.update(item.task_id, fields_to_update)

        if not res_task:
            raise ValueError(f"Failed to update task {item.task_id}")

        # Note: task_to_response fetches dependencies or metadata, we should do it after flush.
        updated_tasks_list.append(service.task_to_response(res_task, iteration_end_date))
        results.append(TaskBatchUpdateResponseItem(task_id=item.task_id, success=True))

    return updated_tasks_list, results


@router.post("/iterations/{iteration_id}/tasks/batch-update", response_model=TaskBatchUpdateResponse)
async def batch_update_tasks(
    iteration_id: int,
    data: TaskBatchUpdateRequest,
    service: Annotated[TaskService, Depends(get_task_service)],
    scheduler_service: Annotated[SchedulerService, Depends(get_scheduler_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Batch update multiple tasks in a single iteration under transaction block."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    original_commit = db.commit
    async def noop_commit():
        await db.flush()

    db.commit = noop_commit
    try:
        updated_tasks_list, results = await apply_batch_update_items(
            service, iteration_id, iteration.end_date, data.tasks
        )

        # Restore commit and final commit
        db.commit = original_commit
        await db.commit()
    except Exception as e:
        db.commit = original_commit
        await db.rollback()
        if isinstance(e, TaskVersionConflictError):
            _raise_task_version_conflict(e)
        if isinstance(e, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        raise

    # Automatically reschedule after successful batch commit
    schedule_res = None
    try:
        schedule_res = await scheduler_service.schedule_iteration(iteration_id)
    except Exception:
        # Scheduling is a secondary operation after the batch transaction commits.
        logger.warning(
            "Automatic reschedule after task batch update failed",
            exc_info=True,
            extra={"iteration_id": iteration_id},
        )

    return TaskBatchUpdateResponse(
        results=results,
        updated_tasks=updated_tasks_list,
        schedule_result=schedule_res
    )


@router.post("/tasks/bulk-operations", response_model=TaskBulkOperationResponse)
async def run_task_bulk_operation(
    data: TaskBulkOperationRequest,
    service: Annotated[TaskBulkOperationService, Depends(get_task_bulk_operation_service)],
):
    """Preview or apply one operation to a selected set of tasks."""
    return await service.run(data)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get task by ID."""
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)

    return service.task_to_response(task, iteration.end_date if iteration else None)


@router.get(
    "/tasks/{task_id}/assignee-recommendations",
    response_model=list[AssigneeRecommendationResponse],
)
async def get_task_assignee_recommendations(
    task_id: int,
    service: Annotated[AssigneeRecommendationService, Depends(get_assignee_recommendation_service)],
):
    """Return explainable assignee recommendations for a task."""
    recommendations = await service.recommend_for_task(task_id)
    if recommendations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return recommendations


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Update a task."""
    try:
        task = await service.update(task_id, data)
    except TaskVersionConflictError as exc:
        _raise_task_version_conflict(exc)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)

    return service.task_to_response(task, iteration.end_date if iteration else None)


@router.post("/tasks/{task_id}/move", response_model=TaskResponse)
async def move_task(
    task_id: int,
    data: TaskMoveRequest,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Move a task subtree to a target iteration."""
    try:
        task = await service.move_task(
            task_id,
            target_iteration_id=data.iteration_id,
            parent_id=data.parent_id,
            expected_version=data.expected_version,
        )
    except TaskVersionConflictError as exc:
        _raise_task_version_conflict(exc)
    except ValueError as e:
        detail = str(e)
        if detail == f"Iteration with id {data.iteration_id} not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)
    return service.task_to_response(task, iteration.end_date if iteration else None)


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)]
):
    """Delete a task and its subtasks."""
    deleted = await service.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return MessageResponse(message=f"Task {task_id} deleted", success=True)


@router.get("/tasks/{task_id}/external-links", response_model=list[ExternalLinkResponse])
async def list_task_external_links(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """List persisted and legacy external links for a task."""
    task = await task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    links = await link_service.list_task_links(task_id)
    return link_service.task_links_to_response(task, links or [])


@router.post(
    "/tasks/{task_id}/external-links",
    response_model=ExternalLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_external_link(
    task_id: int,
    raw_data: Annotated[dict, Body(...)],
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """Create a persisted external link for a task."""
    try:
        data = TaskExternalLinkCreate.model_validate(raw_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    link = await link_service.create_task_link(task_id, data)
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return link_service.link_to_response(link)


@router.post(
    "/tasks/{task_id}/external-links/github",
    response_model=ExternalLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_github_external_link(
    task_id: int,
    raw_data: Annotated[dict, Body(...)],
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """Parse and create a manual GitHub link for a task."""
    try:
        data = GitHubExternalLinkCreate.model_validate(raw_data)
        link = await link_service.create_task_github_link(task_id, data.url)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ExternalLinkValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ExternalLinkConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return link_service.link_to_response(link)


@router.post(
    "/external-links/{link_id}/refresh-github",
    response_model=ExternalLinkResponse,
)
async def refresh_github_external_link(
    link_id: int,
    github_service: Annotated[GitHubStatusService, Depends(get_github_status_service)],
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """Refresh cached GitHub PR status metadata for one external link."""
    try:
        link = await github_service.refresh_pull_request_status(link_id)
    except ExternalLinkValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"External link with id {link_id} not found",
        )
    return link_service.link_to_response(link)


@router.put("/external-links/{link_id}", response_model=ExternalLinkResponse)
async def update_external_link(
    link_id: int,
    raw_data: Annotated[dict, Body(...)],
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """Update a persisted external link."""
    try:
        data = ExternalLinkUpdate.model_validate(raw_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    link = await link_service.update(link_id, data)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"External link with id {link_id} not found",
        )
    return link_service.link_to_response(link)


@router.delete("/external-links/{link_id}", response_model=MessageResponse)
async def delete_external_link(
    link_id: int,
    link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)],
):
    """Delete a persisted external link."""
    deleted = await link_service.delete_link(link_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"External link with id {link_id} not found",
        )
    return MessageResponse(message=f"External link {link_id} deleted", success=True)


@router.post(
    "/tasks/{task_id}/subtasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_subtask(
    task_id: int,
    data: TaskCreate,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a subtask under a parent task."""
    try:
        task = await service.create_subtask(task_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent task with id {task_id} not found"
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)

    return service.task_to_response(task, iteration.end_date if iteration else None)


@router.get("/tasks/{task_id}/subtasks", response_model=list[TaskResponse])
async def get_subtasks(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get subtasks of a task."""
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)
    end_date = iteration.end_date if iteration else None

    return [service.task_to_response(child, end_date) for child in task.children]


@router.post("/tasks/{task_id}/dependencies", response_model=MessageResponse)
async def add_dependency(
    task_id: int,
    data: TaskDependencyCreate,
    service: Annotated[TaskService, Depends(get_task_service)]
):
    """Add a dependency to a task."""
    try:
        success = await service.add_dependency(task_id, data.depends_on_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add dependency. Check that both tasks exist and are different."
        )
    return MessageResponse(
        message=f"Dependency added: Task {task_id} now depends on Task {data.depends_on_id}",
        success=True
    )


@router.delete(
    "/tasks/{task_id}/dependencies/{depends_on_id}",
    response_model=MessageResponse
)
async def remove_dependency(
    task_id: int,
    depends_on_id: int,
    service: Annotated[TaskService, Depends(get_task_service)]
):
    """Remove a dependency from a task."""
    success = await service.remove_dependency(task_id, depends_on_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dependency not found: Task {task_id} -> Task {depends_on_id}"
        )
    return MessageResponse(
        message=f"Dependency removed: Task {task_id} no longer depends on Task {depends_on_id}",
        success=True
    )


@router.post("/tasks/reorder", response_model=MessageResponse)
async def reorder_tasks(
    data: TaskReorder,
    service: Annotated[TaskService, Depends(get_task_service)]
):
    """Reorder a list of tasks by updating their sort_order."""
    try:
        await service.reorder_tasks(
            data.task_ids,
            iteration_id=data.iteration_id,
            parent_id=data.parent_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return MessageResponse(message="Tasks reordered", success=True)


@router.post(
    "/iterations/{iteration_id}/tasks/merge",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def merge_tasks(
    iteration_id: int,
    data: TaskMerge,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Merge multiple leaf tasks under a new parent task."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    try:
        parent_task = await service.merge_tasks(
            iteration_id=iteration_id,
            task_ids=data.task_ids,
            parent_title=data.parent_title,
            parent_description=data.parent_description,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not parent_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not merge tasks. Ensure all tasks exist, belong to this iteration, and have no children."
        )

    return service.task_to_response(parent_task, iteration.end_date)


@router.post(
    "/tasks/{task_id}/unmerge",
    response_model=list[TaskResponse],
    status_code=status.HTTP_200_OK
)
async def unmerge_task(
    task_id: int,
    data: TaskUnmerge,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Promote all child tasks to top level and optionally delete the parent."""
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    if not task.children or len(task.children) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task has no children to unmerge"
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)

    promoted_tasks = await service.unmerge_task(task_id, data.delete_parent)

    return [service.task_to_response(t, iteration.end_date if iteration else None) for t in promoted_tasks]

@router.post(
    "/iterations/{iteration_id}/tasks/import",
    response_model=TasksImportResponse,
    status_code=status.HTTP_201_CREATED
)
async def import_tasks(
    iteration_id: int,
    data: TasksImportRequest,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Import tasks from text format."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    try:
        tasks, triage_items = await service.import_tasks(
            iteration_id,
            data.text,
            data.destination,
        )
        return TasksImportResponse(
            imported_count=len(tasks) + len(triage_items),
            task_count=len(tasks),
            triage_count=len(triage_items),
            tasks=[service.task_to_response(t, iteration.end_date) for t in tasks],
            triage_items=[
                TaskImportTriageItemResponse.model_validate(item)
                for item in triage_items
            ],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/iterations/{iteration_id}/tasks/text",
    response_model=str,
)
async def get_tasks_text(
    iteration_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get all tasks in text format for editing."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(db, "iteration", iteration_id),
        )

    try:
        return await service.get_tasks_as_text(iteration_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(db, str(e)),
        )


@router.post(
    "/iterations/{iteration_id}/tasks/bulk-update",
    response_model=TasksImportResponse,
    status_code=status.HTTP_200_OK
)
async def bulk_update_tasks(
    iteration_id: int,
    data: TasksImportRequest,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Bulk update tasks from text format.
    Supports update via [ID: 123] and creation.
    """
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=await _not_found_detail(db, "iteration", iteration_id)
        )

    try:
        tasks, triage_items = await service.bulk_update_tasks_from_text(
            iteration_id,
            data.text,
            data.destination,
        )
        return TasksImportResponse(
            imported_count=len(tasks) + len(triage_items),
            task_count=len(tasks),
            triage_count=len(triage_items),
            tasks=[service.task_to_response(t, iteration.end_date) for t in tasks],
            triage_items=[
                TaskImportTriageItemResponse.model_validate(item)
                for item in triage_items
            ],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(db, str(e))
        )


@router.put("/tasks/{task_id}/status", response_model=TaskStatusChangeResponse)
async def change_task_status(
    task_id: int,
    data: TaskStatusChange,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Change task status with validation and side effects.

    Valid transitions:
    - planned -> active: Sets actual_start_date, recalculates end_date if late
    - active -> resolved: Work completed, pending validation
    - resolved -> active: Return for rework
    - resolved -> closed: Full completion, sets actual_end_date

    Cascade updates: When dates shift, dependent tasks are automatically updated.
    """
    try:
        task, cascade_updates, notification_sent = await service.change_status(
            task_id=task_id,
            new_status=data.status,
            reason=data.reason,
            expected_version=data.expected_version,
        )
    except TaskVersionConflictError as exc:
        _raise_task_version_conflict(exc)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=await _localized_detail(db, str(e))
        )

    if not task:
        # Check if task exists at all
        existing = await service.get_by_id(task_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=await _not_found_detail(db, "task", task_id)
            )
        ui_language = await resolve_runtime_ui_language(db)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=invalid_status_transition_message(existing.status, data.status.value, ui_language)
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(task.iteration_id)

    return TaskStatusChangeResponse(
        task=service.task_to_response(task, iteration.end_date if iteration else None),
        cascade_updates=[
            CascadeUpdateInfo(
                task_id=u["task_id"],
                task_title=u["task_title"],
                old_start_date=u["old_start_date"],
                new_start_date=u["new_start_date"],
                old_end_date=u["old_end_date"],
                new_end_date=u["new_end_date"]
            )
            for u in cascade_updates
        ],
        notifications_sent=notification_sent
    )


@router.get("/tasks/{task_id}/status-history", response_model=list[TaskStatusLogResponse])
async def get_task_status_history(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)]
):
    """Get status change history for a task."""
    import json

    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    logs = await service.get_status_history(task_id)

    return [
        TaskStatusLogResponse(
            id=log.id,
            task_id=log.task_id,
            from_status=log.from_status,
            to_status=log.to_status,
            changed_at=log.changed_at,
            reason=log.reason,
            triggered_by=log.triggered_by,
            affected_task_ids=json.loads(log.affected_task_ids) if log.affected_task_ids else []
        )
        for log in logs
    ]


@router.get("/tasks/{task_id}/timeline", response_model=TaskTimelineResponse)
async def get_task_timeline(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get merged task timeline with events, status logs, and agent runs."""
    agent_service = AgentService(db)
    task = await agent_service.task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    items = await agent_service.get_task_timeline(task_id)
    return TaskTimelineResponse(
        task_id=task_id,
        items=[TaskTimelineItem(**item) for item in items]
    )


@router.get("/iterations/{iteration_id}/history", response_model=list[TaskStatusLogResponse])
async def get_iteration_status_history(
    iteration_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get recent status history for all tasks in an iteration."""
    import json
    from app.services.iteration_service import IterationService

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)
    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    logs = await service.get_iteration_status_history(iteration_id)

    return [
        TaskStatusLogResponse(
            id=log.id,
            task_id=log.task_id,
            task_title=log.task_title,
            from_status=log.from_status,
            to_status=log.to_status,
            changed_at=log.changed_at,
            reason=log.reason,
            triggered_by=log.triggered_by,
            affected_task_ids=json.loads(log.affected_task_ids) if log.affected_task_ids else []
        )
        for log in logs
    ]



@router.get("/iterations/{iteration_id}/overdue", response_model=list[TaskResponse])
async def get_overdue_tasks(
    iteration_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Get all overdue tasks for an iteration.

    Overdue tasks are those with status='planned' and start_date < today.
    These tasks should have been started but haven't transitioned to 'active'.
    """
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    tasks = await service.get_overdue_tasks(iteration_id)
    return [service.task_to_response(t, iteration.end_date) for t in tasks]
