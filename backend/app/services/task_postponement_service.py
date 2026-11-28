"""Postpone task work with a recorded reason and requirements, and reactivate it.

Postponing stops planned, active or resolved leaf work without canceling it.
Live execution is released through the same fenced path as cancellation, and
the brief, progress, evidence, artifact trail and execution provenance stay as
they were. The postponement records why, who decided and what must be true
before the work resumes. Reactivation returns resolved work to resolved and
planned or active work to planned. Only the project's PM actor, a project
manager or a workspace operator may postpone or reactivate.

Deferral (``is_deferred``) is a different thing: a scheduling policy that keeps
backlog work out of the schedule and from starting. It never stops work that has
started and records no requirements.
"""

from sqlalchemy import or_, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command
from app.models.task import Task, TaskStatus
from app.models.task_postponement import (
    POSTPONABLE_STATUSES, RESOLVED_TRIAGE_STATUSES, TaskPostponement, TaskReactivationRequirement,
)
from app.models.triage import TriageItem
from app.utils.time import utc_now

POSTPONED = TaskStatus.POSTPONED.value


def is_accepted(task):
    """Accepted work: closed and not canceled. A summary closes by roll-up once every leaf is accepted."""
    return (task.status == TaskStatus.CLOSED.value and task.canceled_at is None
            and (task.accepted_at is not None or bool(task.is_summary)))


async def open_postponement(db, task_id, *, lock=False):
    """The task's open postponement, if any."""
    statement = select(TaskPostponement).where(TaskPostponement.task_id == task_id, TaskPostponement.reactivated_at.is_(None))
    if lock:
        statement = statement.with_for_update()
    return await db.scalar(statement)


async def latest_postponement(db, task_id):
    """The open postponement, or else the most recent one."""
    return await open_postponement(db, task_id) or await db.scalar(
        select(TaskPostponement).where(TaskPostponement.task_id == task_id)
        .order_by(TaskPostponement.postponed_at.desc(), TaskPostponement.id.desc()).limit(1))


def reactivation_status(postponement):
    """Where reactivation returns the work: resolved stays resolved, all else is planned again."""
    return "resolved" if postponement is not None and postponement.from_status == "resolved" else "planned"


def decider_blockers(task, authority):
    """Why this caller cannot decide postponement for this task, as action blockers."""
    blockers = []
    if authority is not None and not authority.allows(task.project_id, "manage"):
        blockers.append({"code": "permission_denied", "message": "Project manage permission is required."})
    elif authority is not None and authority.kind == "agent" and not authority.operator and authority.actor_role != "pm":
        blockers.append({"code": "postpone_decider_required",
                         "message": "Only the project's PM, a project manager or an operator can postpone or reactivate work."})
    return blockers


def postponement_actions(task, authority):
    """Availability of the postpone and reactivate commands, in the shared action shape."""
    actions = []
    for action in ("postpone", "reactivate"):
        blockers = decider_blockers(task, authority)
        if task.is_summary:
            blockers.append({"code": "composite_task", "message": "Lifecycle is derived from leaf work."})
        if task.canceled_at:
            blockers.append({"code": "task_canceled", "message": "Reopen canceled work before continuing."})
        if action == "postpone" and task.status == POSTPONED:
            blockers.append({"code": "already_postponed", "message": "This work is already postponed."})
        elif action == "postpone" and task.status not in POSTPONABLE_STATUSES:
            blockers.append({"code": "invalid_lifecycle", "message": "Only planned, active or resolved work can be postponed."})
        if action == "reactivate" and task.status != POSTPONED:
            blockers.append({"code": "not_postponed", "message": "Only postponed work can be reactivated."})
        actions.append({"action": action, "allowed": not blockers, "blockers": blockers})
    return actions


def _require_decider(db, task):
    require_project(db, task.project_id, "manage")
    blockers = decider_blockers(task, db.info.get("authority"))
    if blockers:
        raise AuthorityError(blockers[0]["code"], blockers[0]["message"])


async def require_restore_compatible(db, rows, current):
    """Refuse a snapshot restore that would move a task into or out of postponed.

    ``rows`` are the snapshot's task rows and ``current`` the tasks it replaces. A
    restore into postponed would leave the task with no recorded reason or
    requirements; a restore out of it would leave its postponement open.
    """
    by_id = {task.id: task for task in current}
    for row in rows:
        task = by_id.get(row["id"])
        if (row.get("status") == POSTPONED) != (task is not None and task.status == POSTPONED):
            raise PlanningConflict("restore_conflicts_with_task_postponement",
                                   f"Restoring would move task {row['id']} into or out of postponed. "
                                   "Reactivate or postpone it with its command, or restore a snapshot that keeps its state.")


async def require_unreferenced(db, *, task_ids=(), triage_item_ids=()):
    """Refuse deleting work that an open postponement waits for.

    Deleting the postponed task itself in the same command is allowed: its
    postponement and requirements go with it.
    """
    task_ids, triage_item_ids = list(task_ids), list(triage_item_ids)
    if not task_ids and not triage_item_ids:
        return
    requirement = TaskReactivationRequirement
    targets = []
    if task_ids:
        targets.append(requirement.target_task_id.in_(task_ids))
    if triage_item_ids:
        targets.append(requirement.target_triage_item_id.in_(triage_item_ids))
    query = (select(requirement.task_id, requirement.target_task_id, requirement.target_triage_item_id)
             .join(TaskPostponement, TaskPostponement.id == requirement.postponement_id)
             .where(TaskPostponement.reactivated_at.is_(None), or_(*targets))
             .order_by(requirement.id).limit(1))
    if task_ids:
        query = query.where(requirement.task_id.notin_(task_ids))
    # Postponed work in a scope the caller cannot read still blocks the delete.
    with internal_authority(db):
        row = (await db.execute(query)).first()
    if row is not None:
        target = f"Task {row.target_task_id}" if row.target_task_id is not None else f"Triage item {row.target_triage_item_id}"
        raise PlanningConflict("reactivation_requirement_referenced",
                               f"{target} is named by a reactivation requirement of postponed task {row.task_id}. "
                               "Reactivate that task before deleting this work.")


def _requirement_response(row):
    return {"id": row.id, "position": row.position, "kind": row.kind, "task_id": row.target_task_id,
            "triage_item_id": row.target_triage_item_id, "on_date": row.on_date, "description": row.description,
            "met": row.met_at is not None, "met_at": row.met_at}


async def postponement_record(db, postponement):
    """The postponement with each reactivation requirement and whether it is met."""
    requirements = (await db.scalars(select(TaskReactivationRequirement).where(
        TaskReactivationRequirement.postponement_id == postponement.id)
        .order_by(TaskReactivationRequirement.position, TaskReactivationRequirement.id))).all()
    released = postponement.released or {}
    return {
        "id": postponement.id, "task_id": postponement.task_id, "open": postponement.reactivated_at is None,
        "from_status": postponement.from_status, "reason": postponement.reason,
        "postponed_at": postponement.postponed_at,
        "postponed_by_principal_id": postponement.postponed_by_principal_id,
        "postponed_by_actor_id": postponement.postponed_by_actor_id,
        "task_version": postponement.task_version,
        "released": {key: released.get(key) for key in ("claim_actor_id", "claim_generation")}
        | {key: list(released.get(key) or ()) for key in ("assignment_ids", "run_ids")},
        "requirements": [_requirement_response(row) for row in requirements],
        "reactivated_at": postponement.reactivated_at,
        "reactivated_to_status": postponement.reactivated_to_status,
        "reactivation_trigger": postponement.reactivation_trigger,
        "reactivation_reason": postponement.reactivation_reason,
        "reactivated_by_principal_id": postponement.reactivated_by_principal_id,
        "reactivated_by_actor_id": postponement.reactivated_by_actor_id,
    }


class TaskPostponementService:
    def __init__(self, db):
        self.db = db

    @property
    def tasks(self):
        from app.services.task_service import TaskService
        return TaskService(self.db)

    async def get(self, task_id):
        """The task with its open postponement, or its most recent one."""
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise LookupError("Task not found or inaccessible")
        require_project(self.db, task.project_id, "read")
        postponement = await latest_postponement(self.db, task_id)
        if postponement is None:
            raise LookupError("This task has never been postponed")
        return await self.projection(task_id, postponement)

    async def projection(self, task_id, postponement):
        tasks = self.tasks
        task = await tasks.get_by_id(task_id)
        if postponement is None:
            return {"task": tasks.task_to_response(task), "postponement": None}
        return {"task": tasks.task_to_response(task), "postponement": await postponement_record(self.db, postponement)}

    async def _locked_task(self, task_id, expected_version):
        from app.services.task_hierarchy_service import TaskTreeIntegrityError
        hint = await self.db.scalar(select(Task).where(Task.id == task_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        _require_decider(self.db, hint)
        try:
            await self.tasks._lock_task_scope(task_id)
            task = await self.tasks.get_by_id(task_id)
        except TaskTreeIntegrityError as exc:
            raise PlanningConflict("task_ancestry_invalid", "Reload or repair this task's ancestry before changing its lifecycle.") from exc
        if task is None:
            raise LookupError("Task not found or inaccessible")
        self.tasks.ensure_expected_version(task, expected_version)
        if task.is_summary or task.children:
            raise PlanningConflict("postponement_leaf_required", "Postpone or reactivate leaf work; a summary's status is derived from it.")
        if task.canceled_at:
            raise PlanningConflict("task_canceled", "Reopen canceled work before postponing or reactivating it.")
        return task

    @atomic_command
    async def postpone(self, task_id, data, *, commit=True):
        """Stop planned, active or resolved leaf work until its requirements are met."""
        task = await self._locked_task(task_id, data.expected_version)
        if task.status == POSTPONED:
            raise PlanningConflict("already_postponed", "This work is already postponed.")
        if task.status not in POSTPONABLE_STATUSES:
            raise PlanningConflict("postpone_invalid_lifecycle",
                                   f"Only planned, active or resolved work can be postponed; this task is {task.status}.")
        if await open_postponement(self.db, task.id) is not None:
            raise PlanningConflict("postponement_open", "This task already has an open postponement; reactivate it first.")
        requirements = await self._requirements(task, data.requirements)
        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(task.iteration_id, "before_task_postpone")
        from app.services.task_domain_service import release_execution
        released = await release_execution(
            self.db, task, f"Postponed: {data.reason}", expected_claim_generation=data.expected_claim_generation,
            expected_live_assignment_ids=data.expected_live_assignment_ids,
            expected_running_run_ids=data.expected_running_run_ids, event_type="execution_released",
            purpose="postponing", only_when_live=True, extra={"cause": "postponed"})
        from_status = task.status
        task = await self.tasks.status_service.apply_postponement_transition(
            task, POSTPONED, reason=data.reason, expected_version=data.expected_version)
        from app.services.identity_service import acting_principal_id
        authority = self.db.info.get("authority")
        postponement = TaskPostponement(
            task_id=task.id, from_status=from_status, reason=data.reason, postponed_at=utc_now(),
            postponed_by_principal_id=await acting_principal_id(self.db),
            postponed_by_actor_id=getattr(authority, "actor_id", None), task_version=task.version,
            released=released or {})
        self.db.add(postponement)
        await self.db.flush()
        for position, requirement in enumerate(requirements):
            self.db.add(TaskReactivationRequirement(postponement_id=postponement.id, task_id=task.id, position=position,
                                                    **requirement))
        await self.tasks.record_task_event(task.id, "task_postponed", {
            "postponement_id": postponement.id, "from_status": from_status, "reason": data.reason,
            "requirements": [{key: value.isoformat() if hasattr(value, "isoformat") else value
                              for key, value in requirement.items() if value is not None}
                             for requirement in requirements],
            "released": released, "version": task.version})
        await self.db.flush()
        return await self.projection(task.id, postponement)

    @atomic_command
    async def reactivate(self, task_id, data, *, trigger="command", commit=True):
        """Return postponed work to planned, or to resolved if it was postponed after resolution."""
        task = await self._locked_task(task_id, data.expected_version)
        if task.status != POSTPONED:
            raise PlanningConflict("task_not_postponed", "Only postponed work can be reactivated.")
        postponement = await open_postponement(self.db, task.id, lock=True)
        task = await self.resume(task, postponement, reason=data.reason, trigger=trigger, expected_version=data.expected_version)
        await self.db.flush()
        return await self.projection(task.id, postponement)

    async def resume(self, task, postponement, *, reason, trigger, expected_version, automatic=False, event_extra=None):
        """Move locked postponed work back to planned or resolved and close its postponement.

        An automatic resume is the server's own decision once the recorded
        requirements hold: it names no person and its audit rows are written as
        the system. Work postponed without a record (an imported file, for
        example) returns to planned.
        """
        target = reactivation_status(postponement)
        task = await self.tasks.status_service.apply_postponement_transition(
            task, target, reason=reason, expected_version=expected_version, automatic=automatic)
        if postponement is not None:
            postponement.reactivated_at = utc_now()
            postponement.reactivated_to_status = target
            postponement.reactivation_trigger = trigger
            postponement.reactivation_reason = reason
            if not automatic:
                from app.services.identity_service import acting_principal_id
                authority = self.db.info.get("authority")
                postponement.reactivated_by_principal_id = await acting_principal_id(self.db)
                postponement.reactivated_by_actor_id = getattr(authority, "actor_id", None)
        await self.tasks.record_task_event(task.id, "task_reactivated", {
            "postponement_id": postponement.id if postponement is not None else None, "to_status": target,
            "reason": reason, "trigger": trigger, "version": task.version, **(event_extra or {})},
            **({"actor_type": "auto"} if automatic else {}))
        if target == "resolved":
            # Resolved work again may be what other postponed work waits for.
            from app.services.task_reactivation_service import request_reactivation_check
            request_reactivation_check(self.db, task_id=task.id)
        return task

    async def _requirements(self, task, items):
        """Validate each requirement against current facts; refuse one that can never or already holds."""
        from app.services.work_metrics import working_today
        seen, rows = set(), []
        for item in items:
            key = (item.kind, item.task_id, item.triage_item_id, item.on_date, item.description)
            if key in seen:
                raise ValueError("Each reactivation requirement may be listed once")
            seen.add(key)
            row = {"kind": item.kind, "target_task_id": item.task_id, "target_triage_item_id": item.triage_item_id,
                   "on_date": item.on_date, "description": item.description}
            if item.task_id is not None:
                if item.task_id == task.id:
                    raise ValueError("A postponed task cannot wait for itself")
                target = await self.db.scalar(select(Task).where(Task.id == item.task_id))
                if target is None:
                    raise ValueError(f"Task {item.task_id} is not found or inaccessible")
                if target.canceled_at is not None:
                    raise ValueError(f"Task {item.task_id} is canceled and can never complete this requirement")
                if item.kind == "predecessor_accepted" and is_accepted(target):
                    raise ValueError(f"Task {item.task_id} is already accepted")
                if item.kind == "linked_resolved" and target.status in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}:
                    raise ValueError(f"Task {item.task_id} is already resolved")
            if item.triage_item_id is not None:
                triage_status = await self.db.scalar(select(TriageItem.status).where(TriageItem.id == item.triage_item_id))
                if triage_status is None:
                    raise ValueError(f"Triage item {item.triage_item_id} is not found or inaccessible")
                if triage_status in RESOLVED_TRIAGE_STATUSES:
                    raise ValueError(f"Triage item {item.triage_item_id} is already resolved")
            if item.on_date is not None and item.on_date <= working_today(await self._timezone(task)):
                raise ValueError("A date requirement must be a day after today in the task's working time zone")
            rows.append(row)
        return rows

    async def _timezone(self, task):
        from app.models.calendar import Calendar
        from app.models.iteration import Iteration
        from app.models.project import Project
        with internal_authority(self.db):
            if task.project_id is not None:
                return await self.db.scalar(select(Project.timezone).where(Project.id == task.project_id))
            return await self.db.scalar(select(Calendar.timezone).join(Iteration, Iteration.calendar_id == Calendar.id)
                                        .where(Iteration.id == task.iteration_id))
