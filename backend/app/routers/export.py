"""Export/Import API router."""
import json
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security import require_admin_api_key
from app.schemas.common import MessageResponse
from app.services.iteration_service import IterationService
from app.services.task_service import TaskService
from app.services.team_service import TeamService

router = APIRouter(dependencies=[Depends(require_admin_api_key)])

MAX_JSON_IMPORT_BYTES = 2 * 1024 * 1024
MAX_JSON_IMPORT_TASKS = 5000


def _optional_int(value, field_name: str) -> int | None:
    """Parse optional integer values from backward-compatible JSON imports."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an integer") from exc


async def _read_json_upload(file: UploadFile) -> dict[str, Any]:
    """Read a bounded JSON upload into an object."""
    content = await file.read(MAX_JSON_IMPORT_BYTES + 1)
    if len(content) > MAX_JSON_IMPORT_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Import file is too large",
        )
    try:
        data = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON file: {str(e)}",
        )
    if not isinstance(data, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Import file must contain a JSON object",
        )
    return data


def _validate_import_task_tree(task_data: Any, *, depth: int, counter: list[int]) -> None:
    """Validate an arbitrarily deep task tree with bounded total cardinality."""
    del depth  # Retained for compatibility with existing internal callers.
    stack = [task_data]
    while stack:
        current = stack.pop()
        if not isinstance(current, dict):
            raise ValueError("Each imported task must be a JSON object")
        counter[0] += 1
        if counter[0] > MAX_JSON_IMPORT_TASKS:
            raise ValueError("Import contains too many tasks")
        children = current.get("children", [])
        if not isinstance(children, list):
            raise ValueError("Task children must be a list")
        stack.extend(reversed(children))


@router.get("/iterations/{iteration_id}/export")
async def export_iteration(
    iteration_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Export iteration data as JSON."""
    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    task_service = TaskService(db)
    tasks = await task_service.get_by_iteration(iteration_id)

    team_service = TeamService(db)
    team_members = await team_service.get_by_iteration(iteration_id)

    # Calculate workload for each team member
    def calculate_member_workload(member, all_tasks):
        """Calculate allocated effort for a team member."""
        allocated_days = 0
        task_count = 0

        def process_task(task):
            nonlocal allocated_days, task_count
            if task.assignee and task.assignee.id == member.id and not task.is_deferred:
                if task.start_date and task.end_date:
                    # Count working days (simple approximation)
                    from datetime import timedelta
                    days = (task.end_date - task.start_date).days + 1
                    # Rough working days estimate (5/7 of calendar days)
                    working_days = int(days * 5 / 7) or 1
                    allocated_days += working_days
                    task_count += 1
            for child in task.children:
                process_task(child)

        for task in all_tasks:
            process_task(task)

        return {
            "allocated_days": allocated_days,
            "task_count": task_count,
        }

    export_data = {
        "iteration": {
            "name": iteration.name,
            "start_date": iteration.start_date.isoformat(),
            "end_date": iteration.end_date.isoformat(),
            "calendar_id": iteration.calendar_id,
            "project_id": iteration.project_id,
        },
        "team_members": [
            {
                "name": m.name,
                "position": m.position,
                "availability_percent": m.availability_percent,
                "professionalism_coefficient": m.professionalism_coefficient,
                "operational_utilization": m.operational_utilization,
                "workload": calculate_member_workload(m, tasks),
                "vacations": [
                    {
                        "start_date": v.start_date.isoformat(),
                        "end_date": v.end_date.isoformat(),
                    }
                    for v in m.vacations
                ]
            }
            for m in team_members
        ],
        "tasks": [
            _task_to_export(t) for t in tasks
        ]
    }

    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f'attachment; filename="iteration_{iteration_id}.json"'
        }
    )


def _task_to_export(task) -> dict:
    """Convert task to export format recursively with full Gantt data."""
    # Parse tags from JSON string
    tags = []
    if task.tags:
        try:
            tags = json.loads(task.tags) if isinstance(task.tags, str) else task.tags
        except (json.JSONDecodeError, TypeError):
            tags = []

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "effort_days": task.effort_days,
        "effort_hours": task.effort_hours,
        "status": task.status,
        "external_key": task.external_key,
        "source": task.source,
        "source_url": task.source_url,
        "project_id": task.project_id,
        "milestone_id": task.milestone_id,
        "assignee_name": task.assignee.name if task.assignee else None,
        # Scheduled dates from Gantt
        "start_date": task.start_date.isoformat() if task.start_date else None,
        "end_date": task.end_date.isoformat() if task.end_date else None,
        "actual_start_date": task.actual_start_date.isoformat() if task.actual_start_date else None,
        "actual_end_date": task.actual_end_date.isoformat() if task.actual_end_date else None,
        # Date constraints
        "min_start_date": task.min_start_date.isoformat() if task.min_start_date else None,
        "max_end_date": task.max_end_date.isoformat() if task.max_end_date else None,
        # Flags
        "is_optional": task.is_optional,
        "is_deferred": task.is_deferred,
        # Tags
        "tags": tags,
        # Sort order
        "sort_order": task.sort_order,
        # Dependencies (task IDs)
        "dependencies": [dep.depends_on_id for dep in task.dependencies],
        "dependency_external_keys": [
            dep.depends_on.external_key
            for dep in task.dependencies
            if getattr(dep, "depends_on", None) and dep.depends_on.external_key
        ],
        # Children (subtasks)
        "children": [_task_to_export(c) for c in task.children],
    }

@router.post("/iterations/import")
async def import_new_iteration(
    file: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Import a new iteration from JSON export file."""
    data = await _read_json_upload(file)

    # Create iteration first
    if "iteration" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing iteration data in export file"
        )

    iter_data = data["iteration"]
    from app.schemas.iteration import IterationCreate
    from datetime import date

    # Try to calculate work days if simple Create is used, but IterationCreate requires start/end
    # Assuming the export format matches what IterationCreate expects (except dates as strings)

    iter_create = IterationCreate(
        name=f"Imported: {iter_data['name']}",
        start_date=date.fromisoformat(iter_data["start_date"]),
        end_date=date.fromisoformat(iter_data["end_date"]),
        calendar_id=iter_data.get("calendar_id"),
        project_id=_optional_int(iter_data.get("project_id"), "iteration.project_id"),
    )

    iteration_service = IterationService(db)
    try:
        new_iteration = await iteration_service.create(iter_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    try:
        return await _process_import(new_iteration.id, data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


async def _process_import(
    iteration_id: int,
    data: dict,
    db: AsyncSession,
    *,
    create_snapshots: bool = True,
):
    """Import team members and tasks while preserving task metadata and dependencies."""
    imported_count = 0

    # Build name -> id mapping for team members
    name_to_member_id: dict[str, int] = {}

    # Import team members
    team_service = TeamService(db)
    if "team_members" in data:
        from app.schemas.team import TeamMemberCreate, VacationCreate

        for member_data in data["team_members"]:
            member_create = TeamMemberCreate(
                name=member_data["name"],
                position=member_data.get("position", "Developer"),
                availability_percent=member_data.get("availability_percent", 100),
                professionalism_coefficient=member_data.get("professionalism_coefficient", 1.0),
                operational_utilization=member_data.get("operational_utilization", 20),
            )
            member = await team_service.create(iteration_id, member_create)

            # Store mapping for assignee lookup
            name_to_member_id[member_data["name"]] = member.id

            # Import vacations
            for vac_data in member_data.get("vacations", []):
                from datetime import date
                vac_create = VacationCreate(
                    start_date=date.fromisoformat(vac_data["start_date"]),
                    end_date=date.fromisoformat(vac_data["end_date"]),
                )
                await team_service.add_vacation(member.id, vac_create)

            imported_count += 1

    # Import tasks
    if "tasks" in data:
        if not isinstance(data["tasks"], list):
            raise ValueError("tasks must be a list")
        task_counter = [0]
        for task_data in data["tasks"]:
            _validate_import_task_tree(task_data, depth=1, counter=task_counter)

        task_service = TaskService(db)
        id_to_new_id: dict[int, int] = {}
        external_key_to_new_id: dict[str, int] = {}
        pending_dependencies: list[tuple[int, list[int], list[str]]] = []

        for task_data in data["tasks"]:
            await _import_task(
                task_service,
                iteration_id,
                task_data,
                None,
                name_to_member_id,
                id_to_new_id,
                external_key_to_new_id,
                pending_dependencies,
                create_snapshots=create_snapshots,
            )
            imported_count += 1

        from app.models.task import TaskDependency

        for new_task_id, dependency_ids, dependency_external_keys in pending_dependencies:
            resolved_ids: set[int] = set()
            for old_dep_id in dependency_ids:
                if old_dep_id in id_to_new_id:
                    resolved_ids.add(id_to_new_id[old_dep_id])
            for dep_external_key in dependency_external_keys:
                if dep_external_key in external_key_to_new_id:
                    resolved_ids.add(external_key_to_new_id[dep_external_key])
            for resolved_id in resolved_ids:
                if resolved_id != new_task_id:
                    db.add(TaskDependency(task_id=new_task_id, depends_on_id=resolved_id))
        await db.commit()

    return MessageResponse(
        message=f"Imported iteration '{iteration_id}' with {imported_count} items successfully",
        success=True
    )

@router.post("/iterations/{iteration_id}/import")
async def import_iteration(
    iteration_id: int,
    file: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Import tasks and team members into an iteration from JSON file."""
    data = await _read_json_upload(file)

    iteration_service = IterationService(db)
    iteration = await iteration_service.get_by_id(iteration_id)

    if not iteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Iteration with id {iteration_id} not found"
        )

    try:
        return await _process_import(iteration_id, data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


async def _import_task_record(
    task_service: TaskService,
    iteration_id: int,
    task_data: dict,
    parent_id: Optional[int],
    name_to_member_id: dict[str, int],
    id_to_new_id: dict[int, int],
    external_key_to_new_id: dict[str, int],
    pending_dependencies: list[tuple[int, list[int], list[str]]],
    *,
    create_snapshots: bool = True,
):
    """Import one task record after its parent has been persisted."""
    from app.schemas.task import TaskCreate
    from datetime import date

    # Look up assignee_id from assignee_name
    assignee_id = None
    assignee_name = task_data.get("assignee_name")
    if assignee_name and assignee_name in name_to_member_id:
        assignee_id = name_to_member_id[assignee_name]

    # Parse date constraints
    min_start_date = None
    if task_data.get("min_start_date"):
        min_start_date = date.fromisoformat(task_data["min_start_date"])

    max_end_date = None
    if task_data.get("max_end_date"):
        max_end_date = date.fromisoformat(task_data["max_end_date"])

    task_create = TaskCreate(
        title=task_data["title"],
        description=task_data.get("description"),
        parent_id=parent_id,
        priority=task_data.get("priority", 5),
        effort_days=task_data.get("effort_days", 1),
        effort_hours=task_data.get("effort_hours"),
        assignee_id=assignee_id,
        project_id=_optional_int(task_data.get("project_id"), "task.project_id"),
        milestone_id=_optional_int(task_data.get("milestone_id"), "task.milestone_id"),
        is_optional=task_data.get("is_optional", False),
        is_deferred=task_data.get("is_deferred", False),
        tags=task_data.get("tags", []),
        sort_order=task_data.get("sort_order", 0),
        min_start_date=min_start_date,
        max_end_date=max_end_date,
        external_key=task_data.get("external_key"),
        source=task_data.get("source"),
        source_url=task_data.get("source_url"),
    )

    task = await task_service.create(
        iteration_id,
        task_create,
        create_snapshot=create_snapshots,
    )
    if task_data.get("id") is not None:
        id_to_new_id[int(task_data["id"])] = task.id
    if task.external_key:
        external_key_to_new_id[task.external_key] = task.id

    # Restore status and dates directly for import fidelity.
    if task_data.get("status"):
        task.status = task_data["status"]
    if task_data.get("start_date"):
        task.start_date = date.fromisoformat(task_data["start_date"])
    if task_data.get("end_date"):
        task.end_date = date.fromisoformat(task_data["end_date"])
    if task_data.get("actual_start_date"):
        task.actual_start_date = date.fromisoformat(task_data["actual_start_date"])
    if task_data.get("actual_end_date"):
        task.actual_end_date = date.fromisoformat(task_data["actual_end_date"])
    if (
        task_data.get("status")
        or task_data.get("start_date")
        or task_data.get("end_date")
        or task_data.get("actual_start_date")
        or task_data.get("actual_end_date")
    ):
        await task_service.db.commit()

    pending_dependencies.append(
        (
            task.id,
            [int(dep_id) for dep_id in task_data.get("dependencies", [])],
            [str(key) for key in task_data.get("dependency_external_keys", [])],
        )
    )

    return task


async def _import_task(
    task_service: TaskService,
    iteration_id: int,
    task_data: dict,
    parent_id: Optional[int],
    name_to_member_id: dict[str, int],
    id_to_new_id: dict[int, int],
    external_key_to_new_id: dict[str, int],
    pending_dependencies: list[tuple[int, list[int], list[str]]],
    *,
    create_snapshots: bool = True,
) -> None:
    """Import a complete task tree iteratively so product depth stays unbounded."""
    stack: list[tuple[dict, Optional[int]]] = [(task_data, parent_id)]
    while stack:
        current_data, current_parent_id = stack.pop()
        task = await _import_task_record(
            task_service,
            iteration_id,
            current_data,
            current_parent_id,
            name_to_member_id,
            id_to_new_id,
            external_key_to_new_id,
            pending_dependencies,
            create_snapshots=create_snapshots,
        )
        children = current_data.get("children", [])
        for child_data in reversed(children):
            stack.append((child_data, task.id))
