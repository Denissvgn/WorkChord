"""Snapshots API router."""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.snapshot import SnapshotRestoreRequest, SnapshotRestoreResponse
from app.schemas.task import TaskCreate, TaskStatus
from app.schemas.team import TeamMemberCreate, VacationCreate
from app.security import require_admin_api_key
from app.services.iteration_service import IterationService
from app.services.snapshot_service import SnapshotPathError, SnapshotService
from app.services.task_service import TaskService
from app.services.team_service import TeamService
from app.routers.export import (
    _optional_int,
    _process_import,
    _validate_import_task_tree,
)

router = APIRouter()


async def _validate_snapshot_task_payloads(
    iteration_id: int,
    snapshot_data: dict,
    task_service: TaskService,
) -> None:
    """Validate snapshot structure and references before clearing current state."""

    if not isinstance(snapshot_data, dict):
        raise ValueError("Snapshot must contain a JSON object.")

    team_members = snapshot_data.get("team_members", [])
    tasks = snapshot_data.get("tasks", [])
    if not isinstance(team_members, list):
        raise ValueError("Snapshot team_members must be a list.")
    if not isinstance(tasks, list):
        raise ValueError("Snapshot tasks must be a list.")

    team_member_names: set[str] = set()
    try:
        for member_data in team_members:
            if not isinstance(member_data, dict):
                raise ValueError("Each snapshot team member must be a JSON object.")
            TeamMemberCreate(
                name=member_data["name"],
                position=member_data.get("position", "Developer"),
                availability_percent=member_data.get("availability_percent", 100),
                professionalism_coefficient=member_data.get("professionalism_coefficient", 1.0),
                operational_utilization=member_data.get("operational_utilization", 20),
            )
            team_member_names.add(str(member_data["name"]))
            vacations = member_data.get("vacations", [])
            if not isinstance(vacations, list):
                raise ValueError("Snapshot team member vacations must be a list.")
            for vacation_data in vacations:
                if not isinstance(vacation_data, dict):
                    raise ValueError("Each snapshot vacation must be a JSON object.")
                VacationCreate(
                    start_date=date.fromisoformat(vacation_data["start_date"]),
                    end_date=date.fromisoformat(vacation_data["end_date"]),
                )
    except (KeyError, TypeError, ValidationError) as exc:
        raise ValueError("Snapshot contains invalid team member data.") from exc

    task_ids: set[int] = set()
    external_keys: set[str] = set()
    dependency_references: list[tuple[list[int], list[str]]] = []

    def collect_task_references(data: dict) -> None:
        old_id = data.get("id")
        if old_id is not None:
            parsed_id = _optional_int(old_id, "task.id")
            if parsed_id in task_ids:
                raise ValueError(f"Snapshot contains duplicate task id {parsed_id}.")
            task_ids.add(parsed_id)

        external_key = data.get("external_key")
        if external_key:
            normalized_key = str(external_key)
            if normalized_key in external_keys:
                raise ValueError(f"Snapshot contains duplicate task external key {normalized_key}.")
            external_keys.add(normalized_key)

        dependency_ids = data.get("dependencies", [])
        dependency_keys = data.get("dependency_external_keys", [])
        if not isinstance(dependency_ids, list) or not isinstance(dependency_keys, list):
            raise ValueError("Snapshot task dependencies must be lists.")
        dependency_references.append(
            (
                [_optional_int(item, "task.dependencies") for item in dependency_ids],
                [str(item) for item in dependency_keys],
            )
        )
    task_counter = [0]
    for task_data in tasks:
        _validate_import_task_tree(task_data, depth=1, counter=task_counter)
        task_stack = [task_data]
        while task_stack:
            current_task_data = task_stack.pop()
            collect_task_references(current_task_data)
            task_stack.extend(reversed(current_task_data.get("children", []) or []))

    for dependency_ids, dependency_keys in dependency_references:
        missing_ids = [item for item in dependency_ids if item not in task_ids]
        missing_keys = [item for item in dependency_keys if item not in external_keys]
        if missing_ids or missing_keys:
            raise ValueError("Snapshot contains dependencies that do not reference snapshot tasks.")

    async def validate_task(data: dict, parent_project_id: int | None = None) -> int | None:
        requested_project_id = _optional_int(data.get("project_id"), "task.project_id")
        milestone_id = _optional_int(data.get("milestone_id"), "task.milestone_id")

        if parent_project_id is not None:
            if data.get("project_id") is None:
                requested_project_id = parent_project_id
            elif requested_project_id != parent_project_id:
                raise ValueError("Subtask project must match parent task project.")

        effective_project_id = await task_service._resolve_project_for_iteration_create(
            iteration_id,
            requested_project_id,
        )
        await task_service._require_milestone_compatible(milestone_id, effective_project_id)

        assignee_name = data.get("assignee_name")
        if assignee_name and str(assignee_name) not in team_member_names:
            raise ValueError(f"Snapshot task assignee {assignee_name} is not present in team_members.")

        try:
            status_value = data.get("status", TaskStatus.PLANNED.value)
            TaskStatus(status_value)
            TaskCreate(
                title=data["title"],
                description=data.get("description"),
                priority=data.get("priority", 5),
                effort_days=data.get("effort_days", 1),
                effort_hours=data.get("effort_hours"),
                project_id=effective_project_id,
                milestone_id=milestone_id,
                is_optional=data.get("is_optional", False),
                is_deferred=data.get("is_deferred", False),
                tags=data.get("tags", []),
                sort_order=data.get("sort_order", 0),
                min_start_date=(
                    date.fromisoformat(data["min_start_date"])
                    if data.get("min_start_date")
                    else None
                ),
                max_end_date=(
                    date.fromisoformat(data["max_end_date"])
                    if data.get("max_end_date")
                    else None
                ),
                external_key=data.get("external_key"),
                source=data.get("source"),
                source_url=data.get("source_url"),
            )
            for field_name in ("start_date", "end_date", "actual_start_date", "actual_end_date"):
                if data.get(field_name):
                    date.fromisoformat(data[field_name])
        except (KeyError, TypeError, ValidationError) as exc:
            raise ValueError("Snapshot contains invalid task data.") from exc

        return effective_project_id

    validation_stack: list[tuple[dict, int | None]] = [
        (task_data, None)
        for task_data in reversed(snapshot_data.get("tasks", []) or [])
    ]
    while validation_stack:
        task_data, parent_project_id = validation_stack.pop()
        effective_project_id = await validate_task(task_data, parent_project_id)
        for child_data in reversed(task_data.get("children", []) or []):
            validation_stack.append((child_data, effective_project_id))


@router.get("/iterations/{iteration_id}/snapshots")
async def list_snapshots(
    iteration_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """List available snapshots for an iteration."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    snapshot_service = SnapshotService(db)
    try:
        return snapshot_service.list_snapshots(iteration_id)
    except SnapshotPathError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post(
    "/iterations/{iteration_id}/snapshots/{filename}/restore",
    response_model=SnapshotRestoreResponse,
)
async def restore_snapshot(
    iteration_id: int,
    filename: str,
    data: SnapshotRestoreRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[None, Depends(require_admin_api_key)],
):
    """Restore iteration state from a snapshot."""
    if not data.confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Snapshot restore requires confirm=true.",
        )

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    snapshot_service = SnapshotService(db)
    try:
        snapshot_data = snapshot_service.get_snapshot(iteration_id, filename)
    except SnapshotPathError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not snapshot_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Snapshot {filename} not found"
        )

    task_service = TaskService(db)
    try:
        await _validate_snapshot_task_payloads(iteration_id, snapshot_data, task_service)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    recovery_snapshot = await snapshot_service.create_snapshot(
        iteration_id,
        "before_restore",
    )
    if recovery_snapshot is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create a pre-restore recovery snapshot.",
        )

    restored_count = len(snapshot_data.get("team_members", []) or []) + len(
        snapshot_data.get("tasks", []) or []
    )

    original_commit = db.commit

    async def flush_instead_of_commit() -> None:
        await db.flush()

    db.commit = flush_instead_of_commit
    try:
        # Clear current state only after validation and recovery snapshot creation.
        tasks = await task_service.get_all_tasks(iteration_id)
        for task in tasks:
            await db.delete(task)

        team_service = TeamService(db)
        members = await team_service.get_by_iteration(iteration_id)
        for member in members:
            await db.delete(member)
        await db.flush()

        await _process_import(
            iteration_id,
            snapshot_data,
            db,
            create_snapshots=False,
        )

        audit_event = await task_service.record_task_event(
            None,
            "snapshot_restored",
            {
                "iteration_id": iteration_id,
                "source_snapshot": filename,
                "pre_restore_snapshot": recovery_snapshot,
                "restored_count": restored_count,
            },
            actor_type="admin",
        )
        db.commit = original_commit
        await db.commit()
        await db.refresh(audit_event)
    except Exception as exc:
        db.commit = original_commit
        await db.rollback()
        if not isinstance(exc, ValueError):
            raise
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    finally:
        db.commit = original_commit

    return SnapshotRestoreResponse(
        message=f"Restored {restored_count} items from snapshot {filename}",
        success=True,
        source_snapshot=filename,
        pre_restore_snapshot=recovery_snapshot,
        restored_count=restored_count,
        audit_event_id=audit_event.id,
    )
