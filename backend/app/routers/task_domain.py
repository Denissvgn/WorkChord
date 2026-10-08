"""Compatible domain commands, canonical briefs and bounded task reads."""

from typing import Annotated
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.task_brief import TaskBriefRevision, TaskProgressRecord, TaskReviewRecord
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.task_brief import BriefWrite, BriefConvert, ProgressWrite, TaskReviewWrite, TaskReviewResponse, CurrentTaskReviewResponse
from app.schemas.task_domain import BacklogRestoreRequest, TaskActionRequest, TaskActionsResponse
from app.schemas.task_detail import TaskDetailResponse, TaskReferencePage, HumanWorkResponse
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.task_domain_service import TaskDomainService
from app.services.task_brief_service import TaskBriefService
from app.services.task_detail_service import TaskDetailService

router = APIRouter()
DB = Annotated[AsyncSession, Depends(get_db, scope="function")]


from app.schemas.planning_inputs import PlanningInputContext


@router.get("/tasks/planning-inputs/{kind}/{resource_id}/context", response_model=PlanningInputContext)
async def planning_input_context(kind: Literal["calendar", "project", "iteration", "profile", "member", "vacation"],
    resource_id: int, db: DB, creating_member: bool = False):
    if resource_id < 1 or creating_member and kind != "member":
        raise HTTPException(422, detail="Use a positive planning resource identity and a supported member-create context.")
    from app.services.planning_input_context import observe_planning_input
    return await domain_result(observe_planning_input(db, kind, resource_id, creating_member=creating_member))


async def domain_result(awaitable):
    try:
        result = await awaitable
    except TaskVersionConflictError as exc:
        raise HTTPException(409, detail=exc.detail()) from exc
    except LookupError as exc:
        raise HTTPException(404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, detail=[{"type": "value_error", "loc": ["body"], "msg": str(exc)}]) from exc
    if result is None:
        raise HTTPException(404, detail="Task not found or inaccessible")
    return result


from app.schemas.delivery_metrics import DeliveryMetricsResponse
from app.services.delivery_metrics_service import DeliveryMetricsService
from decimal import Decimal
from app.schemas.execution_usage import ExecutionUsageSummary
from app.services.execution_usage_service import ExecutionUsageService


@router.get("/tasks/delivery-metrics", response_model=DeliveryMetricsResponse)
async def delivery_metrics(db: DB, project_id: int | None = Query(default=None, ge=1),
    iteration_id: int | None = Query(default=None, ge=1), lookback_days: int = Query(default=30, ge=1, le=366)):
    return await domain_result(DeliveryMetricsService(db).report(project_id=project_id, iteration_id=iteration_id, lookback_days=lookback_days))


@router.get("/tasks/execution-usage", response_model=ExecutionUsageSummary)
async def execution_usage_summary(db: DB, project_id: int | None = Query(default=None, ge=1),
    iteration_id: int | None = Query(default=None, ge=1), lookback_days: int = Query(default=30, ge=1, le=366),
    budget_amount: Decimal | None = Query(default=None, ge=0, max_digits=18, decimal_places=6),
    budget_currency: str | None = Query(default=None, pattern=r"^[A-Z]{3}$")):
    return await domain_result(ExecutionUsageService(db).summary(project_id=project_id, iteration_id=iteration_id,
        lookback_days=lookback_days, budget_amount=budget_amount, budget_currency=budget_currency))


@router.get("/tasks/lookup", response_model=TaskReferencePage)
async def lookup_tasks(db: DB, project_id: int | None = None, iteration_id: int | None = None, q: str | None = Query(default=None, max_length=200), backlog_only: bool = False,
                       limit: int = Query(default=50, ge=1, le=100), after_id: int = Query(default=0, ge=0),
                       task_status: str | None = None, parent_id: int | None = Query(default=None, ge=1), roots_only: bool = False):
    return await domain_result(TaskDetailService(db).lookup(project_id=project_id, iteration_id=iteration_id, query=q, backlog_only=backlog_only, limit=limit, after_id=after_id,
        status=task_status, parent_id=parent_id, roots_only=roots_only))


@router.get("/tasks/capabilities")
async def task_capabilities(db: DB):
    from app.services.task_domain_service import domain_capabilities
    return await domain_capabilities(db)


@router.get("/tasks/my-work", response_model=HumanWorkResponse)
async def human_my_work(db: DB, limit: int = Query(default=50, ge=1, le=100), after_id: int = Query(default=0, ge=0),
                       project_id: int | None = Query(default=None, ge=1), iteration_id: int | None = Query(default=None, ge=1), backlog_only: bool = False):
    try:
        return await TaskDetailService(db).my_work(limit=limit, after_id=after_id, project_id=project_id,
            iteration_id=iteration_id, backlog_only=backlog_only)
    except ValueError as exc:
        raise HTTPException(422, detail=[{"type": "value_error", "loc": ["query"], "msg": str(exc)}]) from exc


@router.get("/tasks/owner-options")
async def task_owner_options(db: DB, project_id: int | None = None, after_id: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=100)):
    from sqlalchemy import or_
    from app.authority import internal_authority, require_project
    from app.models.identity import Principal, PrincipalProfileLink, ProjectMembership, WorkspaceMembership
    from app.models.team_member import TeamMemberProfile
    require_project(db, project_id)
    query = select(TeamMemberProfile.id, TeamMemberProfile.display_name.label("name")).where(TeamMemberProfile.profile_kind == "human", TeamMemberProfile.id > after_id)
    authority = db.info.get("authority")
    if authority is not None and not authority.local:
        project_member = select(ProjectMembership.principal_id).where(ProjectMembership.project_id == project_id, ProjectMembership.role.in_(["editor", "executor", "manager"]))
        workspace_member = select(WorkspaceMembership.principal_id).where(WorkspaceMembership.role.in_(["owner", "operator", *(["member"] if project_id is None else [])]))
        query = query.join(PrincipalProfileLink, PrincipalProfileLink.profile_id == TeamMemberProfile.id).join(Principal, Principal.id == PrincipalProfileLink.principal_id).where(
            Principal.enabled.is_(True), Principal.kind == "human", or_(Principal.id.in_(project_member), Principal.id.in_(workspace_member)))
    with internal_authority(db):
        rows = (await db.execute(query.order_by(TeamMemberProfile.id).limit(limit + 1))).mappings().all()
    return {"items": [dict(row) for row in rows[:limit]], "has_more": len(rows) > limit, "next_after_id": rows[limit - 1]["id"] if len(rows) > limit else None}


@router.get("/tasks/migration-diagnostics")
async def task_migration_diagnostics(db: DB, after_id: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    from app.authority import require_operator
    require_operator(db)
    rows = (await db.execute(select(Task.id, Task.ownership_provenance, Task.estimate_provenance, Task.legacy_estimate,
        Task.domain_backfill_version, Task.domain_migration_notes).where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).mappings().all()
    return {"items": [dict(row) for row in rows[:limit]], "has_more": len(rows) > limit,
        "next_after_id": rows[limit - 1]["id"] if len(rows) > limit else None}


@router.get("/tasks/review-queue", response_model=TaskReferencePage)
async def task_review_queue(db: DB, limit: int = Query(default=50, ge=1, le=100), after_id: int = Query(default=0, ge=0),
                          project_id: int | None = Query(default=None, ge=1), iteration_id: int | None = Query(default=None, ge=1), backlog_only: bool = False):
    from sqlalchemy import or_
    authority = db.info.get("authority")
    service = TaskDetailService(db)
    query = service.references().where(Task.status == "resolved", Task.canceled_at.is_(None), Task.is_summary.is_(False))
    if backlog_only and iteration_id is not None:
        raise HTTPException(422, detail="Select backlog or an iteration, not both")
    if project_id is not None:
        from app.authority import require_project
        require_project(db, project_id)
        query = query.where(Task.project_id == project_id)
    if iteration_id is not None:
        query = query.where(Task.iteration_id == iteration_id)
    if backlog_only:
        query = query.where(Task.iteration_id.is_(None))
    if authority is not None:
        if not authority.local and not authority.operator:
            query = query.where(Task.project_id.in_([project_id for project_id in authority.projects if authority.allows(project_id, "review")]))
        if authority.principal_id is not None:
            query = query.where(or_(Task.executed_by_principal_id.is_(None), Task.executed_by_principal_id != authority.principal_id))
            own_progress = select(TaskProgressRecord.id).where(TaskProgressRecord.original_task_id == Task.id,
                TaskProgressRecord.artifact_revision == Task.artifact_revision, TaskProgressRecord.principal_id == authority.principal_id).exists()
            query = query.where(~own_progress)
    return await service.page(query, limit=limit, after_id=after_id)


@router.get("/tasks/{task_id}/detail", response_model=TaskDetailResponse)
async def task_detail(task_id: int, db: DB, limit: int = Query(default=50, ge=1, le=100),
                      children_after_id: int = Query(default=0, ge=0), dependencies_after_id: int = Query(default=0, ge=0)):
    return await domain_result(TaskDetailService(db).detail(task_id, limit=limit, children_after_id=children_after_id, dependencies_after_id=dependencies_after_id))


@router.post("/projects/{project_id}/backlog", response_model=TaskResponse, status_code=201)
async def create_backlog_task(project_id: int, data: TaskCreate, db: DB):
    if data.project_id is not None and data.project_id != project_id:
        raise HTTPException(422, detail=[{"type": "value_error", "loc": ["body", "project_id"], "msg": "Task project must match the destination project"}])
    task = await domain_result(TaskService(db).create(None, data.model_copy(update={"project_id": project_id})))
    return TaskService(db).task_to_response(task)


@router.get("/tasks/{task_id}/actions", response_model=TaskActionsResponse)
async def task_actions(task_id: int, db: DB):
    return await domain_result(TaskDomainService(db).allowed_actions(task_id))


@router.post("/tasks/{task_id}/commands", response_model=TaskResponse)
async def task_command(task_id: int, data: TaskActionRequest, db: DB):
    task = await domain_result(TaskDomainService(db).command(task_id, data))
    return TaskService(db).task_to_response(task)


@router.put("/tasks/{task_id}/brief", response_model=TaskResponse)
async def write_task_brief(task_id: int, data: BriefWrite, db: DB):
    task = await domain_result(TaskBriefService(db).write(task_id, data))
    return TaskService(db).task_to_response(task)


@router.post("/tasks/{task_id}/brief/convert")
async def convert_task_brief(task_id: int, data: BriefConvert, db: DB):
    return await domain_result(TaskBriefService(db).conversion(task_id, data))


@router.post("/tasks/{task_id}/progress", response_model=TaskResponse)
async def record_task_progress(task_id: int, data: ProgressWrite, db: DB):
    task = await domain_result(TaskBriefService(db).write_progress(task_id, data))
    return TaskService(db).task_to_response(task)


@router.post("/tasks/{task_id}/review", response_model=TaskResponse)
async def review_task(task_id: int, data: TaskReviewWrite, db: DB):
    task = await domain_result(TaskBriefService(db).review(task_id, data))
    return TaskService(db).task_to_response(task)


@router.get("/tasks/{task_id}/reviews", response_model=list[TaskReviewResponse])
async def task_reviews(task_id: int, db: DB, limit: int = Query(default=50, ge=1, le=100), after_id: int = Query(default=0, ge=0)):
    await domain_result(TaskDetailService(db).detail(task_id, limit=1))
    return list((await db.scalars(select(TaskReviewRecord).where(TaskReviewRecord.original_task_id == task_id, TaskReviewRecord.id > after_id).order_by(TaskReviewRecord.id).limit(limit))).all())


@router.get("/tasks/{task_id}/reviews/current", response_model=CurrentTaskReviewResponse)
async def current_task_review(task_id: int, db: DB):
    detail = await domain_result(TaskDetailService(db).detail(task_id, limit=1))
    task = detail.task
    review = await db.scalar(select(TaskReviewRecord).where(TaskReviewRecord.original_task_id == task_id,
        TaskReviewRecord.task_version == task.version, TaskReviewRecord.brief_revision == task.brief_revision,
        TaskReviewRecord.artifact_revision == task.artifact_revision).order_by(TaskReviewRecord.id.desc()).limit(1))
    return {"task_version": task.version, "review": review}


async def brief_history_page(db, task_id, model, after_id, limit):
    if await db.scalar(select(Task.id).where(Task.id == task_id)) is None:
        raise HTTPException(404, detail="Task not found or inaccessible")
    rows = list((await db.scalars(select(model).where(model.original_task_id == task_id, model.id > after_id).order_by(model.id).limit(limit + 1))).all())
    return {"items": [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in rows[:limit]],
        "has_more": len(rows) > limit, "next_after_id": rows[limit - 1].id if len(rows) > limit else None}


@router.get("/tasks/{task_id}/brief/history")
async def task_brief_history(task_id: int, db: DB, limit: int = Query(default=10, ge=1, le=20), after_id: int = Query(default=0, ge=0)):
    return await brief_history_page(db, task_id, TaskBriefRevision, after_id, limit)


@router.get("/tasks/{task_id}/progress/history")
async def task_progress_history(task_id: int, db: DB, limit: int = Query(default=10, ge=1, le=20), after_id: int = Query(default=0, ge=0)):
    return await brief_history_page(db, task_id, TaskProgressRecord, after_id, limit)


@router.get("/projects/{project_id}/backlog/snapshots")
async def backlog_snapshots(project_id: int, db: DB):
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    return await BacklogSnapshotService(db).list(project_id)


@router.post("/projects/{project_id}/backlog/snapshots/{snapshot_id}/restore", response_model=list[TaskResponse])
async def restore_backlog(project_id: int, snapshot_id: int, data: BacklogRestoreRequest, db: DB):
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    return await domain_result(BacklogSnapshotService(db).restore(project_id, snapshot_id, data.expected_versions, reason=data.reason))
