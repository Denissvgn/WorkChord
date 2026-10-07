"""Durable ownership, normalized effort and explicit task-domain commands."""

from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import or_, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import atomic_command, lock_iterations
from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMemberProfile
from app.schemas.task_domain import TaskActionsResponse, TaskActionRequest
from app.services.task_brief_service import clear_acceptance
from app.utils.time import utc_now


def normalize_effort(values: dict, day_hours: float, *, current_hours=None) -> dict:
    """Hours are authoritative; round once to six decimals, preserving zero and unknown."""
    days = values.get("effort_days")
    hours = values.get("effort_hours")
    if "effort_hours" not in values or hours is None and days is not None:
        hours = days * day_hours if days is not None else (None if "effort_days" in values else current_hours)
    if hours is not None and days is not None and abs(hours - days * day_hours) > 0.000001:
        raise ValueError("effort_hours and effort_days disagree for the nominal workday")
    if hours is not None:
        decimal = Decimal(str(hours))
        if not decimal.is_finite() or decimal < 0:
            raise ValueError("Effort must be finite and nonnegative")
        hours = float(decimal.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
    provenance = values.get("estimate_provenance") or ("estimated" if hours is not None else "unknown")
    if (provenance == "unknown") != (hours is None):
        raise ValueError("Unknown effort must be null; known effort requires assumed or estimated provenance")
    return {"effort_hours": hours, "effort_days": hours / day_hours if hours is not None else None, "estimate_provenance": provenance}


async def nominal_day_hours(db, iteration_id) -> float:
    from app.models.calendar import Calendar
    value = await db.scalar(select(Calendar.nominal_day_hours).join(Iteration, Iteration.calendar_id == Calendar.id).where(Iteration.id == iteration_id)) if iteration_id else None
    return value or 8.0


async def refresh_nominal_day_hours(db, iteration_ids, day_hours):
    """Refresh display units under the caller's planning-input reservations."""
    tasks = await db.scalars(select(Task).where(Task.iteration_id.in_(iteration_ids)).order_by(Task.id))
    for task in tasks:
        task.nominal_day_hours = day_hours
        task._legacy_effort_days = task.effort_days


async def domain_capabilities(db):
    """Advertise adoption only after the installed schema's backfill is complete."""
    if db is None:
        return {"schema_version": 1, "ready": False, "features": [], "reason": "database_unavailable"}
    with internal_authority(db):
        pending = await db.scalar(select(Task.id).where(Task.domain_backfill_version < 1).limit(1))
    ready = pending is None
    return {"schema_version": 1, "ready": ready, "reason": None if ready else "domain_backfill_pending",
        "features": ["task-actions-v1", "paged-worksets-v1", "project-backlog-v1", "human-ownership-v1", "nullable-effort-v1", "structured-brief-v1", "criterion-evidence-v1", "bounded-task-detail-v1", "profile-availability-v1", "delivery-dependencies-v1", "human-my-work-v1", "human-my-work-filters-v1", "task-discussion-v1", "delivery-metrics-v1"] if ready else [],
        "legacy_iteration_routes": True, "legacy_task_versions_required": get_settings().strict_mutation_versions,
        "aggregate_revisions_required": get_settings().strict_mutation_versions,
        "aggregate_revision_header": "X-Expected-Revisions",
        "missing_revision_code": "mutation_revision_required",
        "current_review_projection": ready}


async def require_owner(db, profile_id, project_id):
    """Validate human ownership independently of capacity IDs and agent assignment."""
    if profile_id is None:
        return
    require_project(db, project_id, "edit")
    from app.models.identity import Principal, PrincipalProfileLink, ProjectMembership, WorkspaceMembership
    # Membership lookup reveals only an eligibility result, never another identity's credentials.
    with internal_authority(db):
        profile = await db.get(TeamMemberProfile, profile_id)
        principal = await db.scalar(select(Principal).join(PrincipalProfileLink, PrincipalProfileLink.principal_id == Principal.id)
            .where(PrincipalProfileLink.profile_id == profile_id))
        role = await db.scalar(select(ProjectMembership.role).where(ProjectMembership.principal_id == principal.id, ProjectMembership.project_id == project_id)) if principal else None
        workspace_role = await db.scalar(select(WorkspaceMembership.role).where(WorkspaceMembership.principal_id == principal.id)) if principal else None
    if profile is None or profile.profile_kind != "human":
        raise ValueError("Owner must be an existing human profile")
    authority = db.info.get("authority")
    from app.config import get_settings
    if authority is not None and authority.local or authority is None and get_settings().workchord_auth_mode == "trusted_local":
        return
    if principal is None or not principal.enabled or principal.kind != "human" or not (
        workspace_role in {"owner", "operator"} or role in {"editor", "executor", "manager"}
        or project_id is None and workspace_role == "member"
    ):
        raise ValueError("Owner needs an enabled human identity with execution membership in this project")


def action_projection(task, authority, *, dependencies_complete=True, live_assignment=False):
    """Transport-independent availability; execution commands recheck under row locks."""
    human = authority is None or authority.kind in {"human", "local"}
    claimed = task.claimed_by is not None or live_assignment
    output = []
    permissions = {"start_manual": "execute", "resolve_manual": "execute", "block": "edit", "unblock": "edit",
                   "cancel": "manage", "reopen": "manage", "commit": "edit", "uncommit": "edit", "review": "review"}
    for action, permission in permissions.items():
        blockers = []
        def block(code, message):
            blockers.append({"code": code, "message": message})
        if authority is not None and not authority.allows(task.project_id, permission):
            block("permission_denied", f"Project {permission} permission is required.")
        if task.is_summary and action not in {"commit", "uncommit"}:
            block("composite_task", "Lifecycle is derived from leaf work.")
        if task.canceled_at and action != "reopen":
            block("task_canceled", "Reopen canceled work before continuing.")
        if action in {"start_manual", "resolve_manual"}:
            if not human:
                block("human_execution_required", "Agents must use assigned work with its current fence.")
            if claimed:
                block("agent_ownership_active", "Recover or cancel agent ownership before manual execution.")
            if task.blocked_reason:
                block("task_blocked", task.blocked_reason)
            if task.is_deferred:
                block("task_deferred", "Remove deferral before executing work.")
            if action == "start_manual":
                if task.status != "planned":
                    block("invalid_lifecycle", "Manual start requires planned work.")
                if not dependencies_complete:
                    block("dependencies_incomplete", "Complete the prerequisites before starting.")
            elif task.status != "active" or task.execution_mode != "manual":
                block("invalid_lifecycle", "Manual resolution requires active manual work.")
        if action == "reopen" and not task.canceled_at and task.status != "closed":
            block("invalid_lifecycle", "Only closed or canceled work can be reopened.")
        if action == "unblock" and not task.blocked_reason:
            block("not_blocked", "This task has no explicit block.")
        if action == "block" and task.status == "closed":
            block("invalid_lifecycle", "Reopen accepted work before blocking it.")
        if action in {"commit", "uncommit"}:
            if claimed:
                block("agent_ownership_active", "Recover agent ownership before changing schedule commitment.")
            if task.status != "planned":
                block("invalid_lifecycle", "Schedule commitment changes require planned work.")
            if action == "commit" and task.iteration_id is not None:
                block("already_committed", "Use the iteration move command for committed work.")
            if action == "uncommit" and task.iteration_id is None:
                block("not_committed", "This task is already in the project backlog.")
            if task.project_id is None:
                block("project_required", "Choose a project before changing schedule commitment.")
        if action == "review":
            if task.status != "resolved":
                block("invalid_lifecycle", "Only resolved work can be reviewed.")
            if authority is not None and authority.principal_id is not None and task.executed_by_principal_id == authority.principal_id and not (authority.operator and authority.review_override and authority.reason):
                block("independent_review_required", "Another reviewer must review this work.")
            if not human:
                block("agent_protocol_required", "Use the assigned verification command.")
        output.append({"action": action, "allowed": not blockers, "blockers": blockers})
    return output


class TaskDomainService:
    def __init__(self, db):
        self.db = db

    @property
    def tasks(self):
        from app.services.task_service import TaskService
        return TaskService(self.db)

    async def ownership(self, task_id, *, lock=False):
        assignments = select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == task_id, AgentTaskAssignment.state.in_(["queued", "accepted"])).order_by(AgentTaskAssignment.id)
        runs = select(AgentRun).where(AgentRun.task_id == task_id, AgentRun.status == "running").order_by(AgentRun.id)
        if lock:
            assignments, runs = assignments.with_for_update(), runs.with_for_update()
        return list((await self.db.scalars(assignments)).all()), list((await self.db.scalars(runs)).all())

    async def allowed_actions(self, task_id):
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise ValueError("Task not found or inaccessible")
        assignments, runs = await self.ownership(task.id)
        from app.models.task import TaskDependency
        edge, target = TaskDependency.__table__, Task.__table__.alias("action_dependency")
        unavailable = select(edge.c.id).outerjoin(target, target.c.id == edge.c.depends_on_id).where(edge.c.task_id == task.id,
            or_(target.c.id.is_(None), target.c.status.notin_(["resolved", "closed"]), target.c.canceled_at.is_not(None))).exists()
        from app.services.delivery_dependency_service import DeliveryDependencyService
        dependencies_complete = not bool(await self.db.scalar(select(unavailable))) and await DeliveryDependencyService(self.db).ready(task.id)
        actions = action_projection(task, self.db.info.get("authority"), dependencies_complete=dependencies_complete, live_assignment=bool(assignments or runs))
        authority = self.db.info.get("authority")
        review_action = next(item for item in actions if item["action"] == "review")
        import copy
        accept_action = copy.deepcopy(review_action)
        accept_action["action"] = "accept_review"
        for availability, accepting in ((review_action, False), (accept_action, True)):
            if availability["allowed"]:
                from app.services.task_brief_service import TaskBriefService
                try:
                    await TaskBriefService(self.db).require_review(task, accepting=accepting)
                except (AuthorityError, ValueError) as exc:
                    availability["allowed"] = False
                    availability["blockers"] = [{"code": getattr(exc, "code", "current_evidence_required"), "message": str(exc)}]
        actions.append(accept_action)
        progress_blockers = []
        if authority is not None and not authority.allows(task.project_id, "execute"):
            progress_blockers.append({"code": "permission_denied", "message": "Execution permission is required to record evidence."})
        if authority is not None and authority.kind == "agent":
            progress_blockers.append({"code": "agent_protocol_required", "message": "Submit evidence through assigned work with its current fence."})
        if task.canceled_at or task.status == "closed" or task.is_summary:
            progress_blockers.append({"code": "open_leaf_required", "message": "Evidence requires open leaf work."})
        actions.append({"action": "record_progress", "allowed": not progress_blockers, "blockers": progress_blockers})
        if authority is not None and authority.kind == "agent":
            from app.services.agent_work_service import AgentWorkService
            from app.utils.time import as_utc
            full_task = await self.tasks.get_by_id(task_id)
            assignment = next((item for item in assignments if item.actor_id == authority.actor_id and item.purpose == "execution"), None)
            start_codes = await AgentWorkService(self.db)._start_blockers(full_task, assignment, utc_now()) if assignment is not None else ["exact_assignment_required"]
            if not authority.allows(task.project_id, "execute"):
                start_codes.append("permission_denied")
            if task.canceled_at or task.blocked_reason:
                start_codes.append("task_unavailable")
            live = assignment is not None and assignment.state == "accepted" and assignment.task_version == task.version and task.status == "active" and task.claimed_by == authority.actor_id and task.claim_expires_at is not None and as_utc(task.claim_expires_at) > as_utc(utc_now()) and any(run.actor_id == authority.actor_id and run.assignment_id == assignment.id and run.claim_generation == task.claim_generation for run in runs)
            review_assignment = next((item for item in assignments if item.actor_id == authority.actor_id and item.purpose == "verification" and item.task_version == task.version), None)
            review_codes = [] if review_assignment is not None else ["exact_verification_assignment_required"]
            if not review_codes:
                from app.services.task_brief_service import TaskBriefService
                try:
                    await TaskBriefService(self.db).require_review(task, accepting=True)
                except (AuthorityError, ValueError) as exc:
                    review_codes.append(getattr(exc, "code", "current_evidence_required"))
            for action_name, codes in (("begin_assigned_work", start_codes), ("submit_assigned_work", [] if live and authority.allows(task.project_id, "execute") and not task.canceled_at and not task.blocked_reason else ["live_execution_fence_required"]), ("review_assigned_work", review_codes)):
                actions.append({"action": action_name, "allowed": not codes, "blockers": [{"code": code, "message": code.replace("_", " ")} for code in sorted(set(codes))]})
        return TaskActionsResponse(task_id=task.id, version=task.version,
            actions=actions,
            claim_generation=task.claim_generation, running_run_ids=[run.id for run in runs], live_assignment_ids=[item.id for item in assignments])

    @atomic_command
    async def command(self, task_id: int, data: TaskActionRequest):
        await self.tasks._lock_task_scope(task_id, target_iteration_id=data.iteration_id, expected_revisions=data.expected_revisions,
            require_revisions=data.action in {"commit", "uncommit"})
        task = await self.tasks.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found or inaccessible")
        self.tasks.ensure_expected_version(task, data.expected_version)
        available = await self.allowed_actions(task.id)
        selected = next(item for item in available.actions if item.action == data.action)
        if not selected.allowed:
            first = selected.blockers[0]
            raise AuthorityError(first.code, first.message, 409 if first.code != "permission_denied" else 403)
        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(task.iteration_id, "before_task_command")
        if data.action in {"commit", "uncommit"}:
            return await self._commitment(task, data)
        if data.action == "start_manual":
            task.execution_mode = "manual"
            task, _, _ = await self.tasks.change_status(task.id, "active", reason=data.reason, expected_version=task.version, manual_execution=True, commit=False)
        elif data.action == "resolve_manual":
            task, _, _ = await self.tasks.change_status(task.id, "resolved", reason=data.reason, expected_version=task.version, manual_execution=True, commit=False)
        else:
            await self.tasks.reserve_task_version(task, data.expected_version)
            if data.action == "block":
                task.blocked_reason = data.reason
            elif data.action == "unblock":
                task.blocked_reason = None
            elif data.action == "cancel":
                await self._cancel_execution(task, data)
                task.canceled_at, task.canceled_reason = utc_now(), data.reason
                task.canceled_by_principal_id = getattr(self.db.info.get("authority"), "principal_id", None)
                clear_acceptance(task)
            elif data.action == "reopen":
                await self.tasks._require_unclaimed_structure([task.id])
                old_status = task.status
                task.canceled_at = task.canceled_reason = task.canceled_by_principal_id = None
                task.status = "active" if old_status in {"active", "resolved", "closed"} else "planned"
                task.execution_mode = "manual" if getattr(self.db.info.get("authority"), "kind", "local") in {"human", "local"} else "scheduled"
                clear_acceptance(task)
                task.progress = None
                task.resolved_at = task.actual_end_date = None
                from app.models.task_status_log import TaskStatusLog
                if task.status != old_status:
                    self.db.add(TaskStatusLog(task_id=task.id, from_status=old_status, to_status=task.status, reason=data.reason, triggered_by="user"))
                if task.parent_id:
                    await self.tasks.status_service.reconcile_parent_chain(task.parent_id, commit=False)
        await self.tasks.record_task_event(task.id, f"task_{data.action}", {"reason": data.reason, "version": task.version})
        await self.db.flush()
        return await self.tasks.get_by_id(task.id)

    async def _cancel_execution(self, task, data):
        hints, run_hints = await self.ownership(task.id)
        actor_ids = {item.actor_id for item in hints} | {run.actor_id for run in run_hints}
        if task.claimed_by:
            actor_ids.add(task.claimed_by)
        actors = list((await self.db.scalars(select(AgentActor).where(AgentActor.id.in_(actor_ids)).order_by(AgentActor.id).with_for_update())).all())
        assignments, runs = await self.ownership(task.id, lock=True)
        if assignments or runs or task.claimed_by is not None:
            if (data.expected_claim_generation != task.claim_generation or sorted(data.expected_live_assignment_ids) != [item.id for item in assignments]
                    or sorted(data.expected_running_run_ids) != [run.id for run in runs]):
                raise AuthorityError("execution_ownership_changed", "Reload current claims, runs and assignments before canceling active execution.", 409)
        for actor in actors:
            self.db.info.setdefault("domain_queue_actors", set()).add(actor.id)
            actor.queue_revision += 1
        for assignment in assignments:
            assignment.state, assignment.reason = "cancelled", data.reason
        for run in runs:
            run.status, run.ended_at, run.error = "cancelled", utc_now(), data.reason
        task.claimed_by = task.claim_id = task.claim_expires_at = None
        task.claim_generation += 1
        await self.tasks.record_task_event(task.id, "execution_canceled", {"reason": data.reason, "run_ids": [run.id for run in runs], "assignment_ids": [item.id for item in assignments], "claim_generation": task.claim_generation})

    async def _commitment(self, task, data):
        if data.action == "commit":
            return await self.tasks.move_task(task.id, data.iteration_id, expected_version=data.expected_version, expected_revisions=data.expected_revisions)
        ids = await self.tasks._task_subtree_ids(task.id)
        await self.tasks._require_no_cross_subtree_dependencies(ids)
        await self.tasks._require_unclaimed_structure(ids)
        rows = list((await self.db.scalars(select(Task).where(Task.id.in_(ids)).order_by(Task.id))).all())
        if any(item.status != "planned" for item in rows):
            raise ValueError("All leaf work must be planned before removing schedule commitment")
        old_parent = task.parent_id
        for item in rows:
            await self.tasks.reserve_task_version(item, item.version)
            previous = item.iteration_id
            item.iteration_id = item.assignee_id = item.start_date = item.end_date = item.calculated_effort_days = None
            if item.id == task.id:
                item.parent_id = None
            await self.tasks.record_task_event(item.id, "schedule_uncommitted", {"iteration_id": previous, "reason": data.reason, "version": item.version})
        await self.db.flush()
        if old_parent:
            await self.tasks.status_service.reconcile_parent_chain(old_parent, commit=False)
        return await self.tasks.get_by_id(task.id)
