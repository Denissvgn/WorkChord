"""Return postponed work to its lifecycle once every recorded requirement holds.

A postponement records requirements of four kinds: named work accepted, a day in
the task's working time zone, an owner decision, and linked work or a triage item
resolved. Nothing here is a person's command except the owner decision. The other
kinds are evaluated against current facts whenever those facts can have changed:
when a task is resolved or accepted, when a triage item is resolved, when the
owner records a decision, and on the daily date check, which also sweeps any
postponement an earlier evaluation could not finish.

Every evaluation first takes the shared planning lock, as every planning command
does, and then the postponement's own row. Two triggers arriving together are
therefore serialized: the second sees what the first committed, and a postponement
whose last requirement the second completes is reactivated exactly once.

A requirement stays met once it has been met; ``met_at`` records when. The task
returns to planned, or to resolved when it was postponed after resolution, and its
timeline names the requirement that completed it.
"""

import copy
import dataclasses
import logging
from datetime import datetime

from sqlalchemy import or_, select

from app.authority import AuthorityError, internal_authority
from app.commands import PlanningConflict, atomic_command, current_command, lock_planning
from app.config import get_settings
from app.models.task import Task, TaskStatus
from app.models.task_postponement import RESOLVED_TRIAGE_STATUSES, TaskPostponement, TaskReactivationRequirement
from app.models.triage import TriageItem
from app.services.task_postponement_service import POSTPONED, TaskPostponementService, is_accepted, open_postponement
from app.utils.time import utc_now

logger = logging.getLogger(__name__)

AUTOMATIC_TRIGGER = "requirements_met"
# Reactivation can resolve work that other postponed work waits for; bound the chain.
MAX_CASCADE_ROUNDS = 10

_CHECKS = "reactivation_checks"


def request_reactivation_check(db, *, task_id=None, triage_item_id=None):
    """Note that work postponed tasks may wait for has changed.

    The command that owns the transaction evaluates the notes once its own change is
    complete, inside the same transaction, so the evaluation sees it and rolls back
    with it.
    """
    checks = db.info.setdefault(_CHECKS, {"tasks": set(), "triage": set()})
    if task_id is not None:
        checks["tasks"].add(task_id)
    if triage_item_id is not None:
        checks["triage"].add(triage_item_id)


async def process_reactivation_checks(db):
    """Evaluate the postponements that wait for the noted work; called by the command boundary."""
    service = ReactivationService(db)
    for _ in range(MAX_CASCADE_ROUNDS):
        checks = db.info.pop(_CHECKS, None)
        if not checks or not (checks["tasks"] or checks["triage"]):
            return
        await service.evaluate_waiting(sorted(checks["tasks"]), sorted(checks["triage"]))
    db.info.pop(_CHECKS, None)
    logger.warning("Reactivation checks did not settle within %s rounds", MAX_CASCADE_ROUNDS)


def require_owner_decision(db):
    """Only the workspace owner, or the trusted local owner, can record an owner decision."""
    authority = db.info.get("authority")
    if authority is None:
        if get_settings().workchord_auth_mode == "trusted_local":
            return None
        raise AuthorityError("authentication_required", "Sign in to continue.", 401)
    if (authority.read_only or authority.kind in {"agent", "system"}
            or not (authority.workspace_role == "owner" or authority.local)):
        raise AuthorityError("owner_decision_required", "Only the workspace owner can record an owner decision.")
    return authority


def _describe(requirement):
    if requirement.kind == "predecessor_accepted":
        return f"task {requirement.target_task_id} was accepted"
    if requirement.kind == "date":
        return f"the date {requirement.on_date.isoformat()} was reached"
    if requirement.kind == "owner_decision":
        return f"the owner decided: {requirement.description}"
    if requirement.target_task_id is not None:
        return f"linked task {requirement.target_task_id} was resolved"
    return f"linked triage item {requirement.target_triage_item_id} was resolved"


def _summary(requirement):
    return {"requirement_id": requirement.id, "kind": requirement.kind, "task_id": requirement.target_task_id,
            "triage_item_id": requirement.target_triage_item_id,
            "on_date": requirement.on_date.isoformat() if requirement.on_date else None,
            "description": requirement.description}


class ReactivationService:
    def __init__(self, db):
        self.db = db
        self.postponements = TaskPostponementService(db)

    async def evaluate_waiting(self, task_ids, triage_item_ids):
        """Evaluate each open postponement with an unmet requirement on this work."""
        waiting = []
        if task_ids:
            waiting.append(TaskReactivationRequirement.target_task_id.in_(task_ids))
        if triage_item_ids:
            waiting.append(TaskReactivationRequirement.target_triage_item_id.in_(triage_item_ids))
        if not waiting:
            return []
        with internal_authority(self.db):
            ids = (await self.db.scalars(
                select(TaskPostponement.id).join(TaskReactivationRequirement,
                                                 TaskReactivationRequirement.postponement_id == TaskPostponement.id)
                .where(TaskPostponement.reactivated_at.is_(None), TaskReactivationRequirement.met_at.is_(None), or_(*waiting))
                .distinct().order_by(TaskPostponement.id))).all()
        return [task_id for postponement_id in ids if (task_id := await self._evaluate_isolated(postponement_id)) is not None]

    async def run_date_check(self, *, now=None):
        """The periodic check: reactivate postponed work whose requirements now hold, notably its date.

        Facts are read without any lock first; the planning lock, which every locked command
        advances, is taken only for a postponement where a requirement newly holds, so a check
        that finds nothing changes nothing. Each postponement is its own transaction, and one
        that cannot be evaluated is logged and left for the next check. Returns the IDs of the
        tasks it reactivated.
        """
        now = now or utc_now()
        with internal_authority(self.db):
            ids = (await self.db.scalars(select(TaskPostponement.id).where(TaskPostponement.reactivated_at.is_(None))
                                         .order_by(TaskPostponement.id))).all()
        reactivated = []
        for postponement_id in ids:
            try:
                if not await self._due(postponement_id, now):
                    await self.db.rollback()
                    continue
                task_id = await self.evaluate_one(postponement_id, now=now)
            except Exception:
                logger.warning("Reactivation check of postponement %s failed", postponement_id, exc_info=True)
                await self.db.rollback()
                continue
            if task_id is not None:
                reactivated.append(task_id)
        await self.db.rollback()
        return reactivated

    @atomic_command
    async def evaluate_one(self, postponement_id, *, now=None, commit=True):
        """Evaluate one open postponement as its own command; the task ID if it was reactivated."""
        return await self._evaluate(postponement_id, now=now)

    @atomic_command
    async def record_owner_decision(self, task_id, requirement_id, data, *, commit=True):
        """The owner's command: record that the decision an owner_decision requirement waits for was made."""
        authority = require_owner_decision(self.db)
        hint = await self.db.scalar(select(Task).where(Task.id == task_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        from app.authority import require_project
        require_project(self.db, hint.project_id, "read")
        await lock_planning(self.db)
        with internal_authority(self.db):
            postponement = await open_postponement(self.db, task_id, lock=True)
            task = await self.db.scalar(select(Task).where(Task.id == task_id).execution_options(populate_existing=True))
            if task is None:
                raise LookupError("Task not found or inaccessible")
            self.postponements.tasks.ensure_expected_version(task, data.expected_version)
            requirement = await self.db.scalar(select(TaskReactivationRequirement).where(
                TaskReactivationRequirement.id == requirement_id, TaskReactivationRequirement.task_id == task_id,
                TaskReactivationRequirement.kind == "owner_decision").execution_options(populate_existing=True))
            if requirement is None:
                raise LookupError("Owner decision requirement not found for this task")
            if postponement is None or requirement.postponement_id != postponement.id:
                raise PlanningConflict("postponement_closed", "This task is no longer postponed for that decision.")
            if requirement.met_at is None:
                now = utc_now()
                requirement.met_at = now
                await self.postponements.tasks.record_task_event(task.id, "owner_decision_recorded", {
                    **_summary(requirement), "decision": data.decision, "postponement_id": postponement.id,
                    "principal_id": getattr(authority, "principal_id", None)}, actor_type="user")
                await self.db.flush()
                # The same evaluation as any trigger: a date that came due since the last check counts too.
                await self._apply(postponement, task, await self._requirements(postponement), now, [requirement])
            return await self.postponements.projection(task_id, await self._latest(task_id))

    async def _latest(self, task_id):
        from app.services.task_postponement_service import latest_postponement
        return await latest_postponement(self.db, task_id)

    async def _requirements(self, postponement):
        return (await self.db.scalars(select(TaskReactivationRequirement).where(
            TaskReactivationRequirement.postponement_id == postponement.id)
            .order_by(TaskReactivationRequirement.position, TaskReactivationRequirement.id)
            .execution_options(populate_existing=True))).all()

    def _save_state(self):
        """Copy the command's reservations so a failed evaluation can give back what it took."""
        state = current_command(self.db)
        saved = {field.name: copy.copy(getattr(state, field.name)) for field in dataclasses.fields(state)}
        return saved, copy.copy(self.db.info.get("discussion_events"))

    def _restore_state(self, saved):
        values, discussion = saved
        state = current_command(self.db)
        for name, value in values.items():
            setattr(state, name, value)
        if discussion is None:
            self.db.info.pop("discussion_events", None)
        else:
            self.db.info["discussion_events"] = discussion

    async def _evaluate_isolated(self, postponement_id, *, now=None):
        """Evaluate one postponement in a savepoint: a failure never blocks the command that triggered it.

        Without a requirement that newly holds nothing is locked or changed. The shared planning
        lock is taken before the savepoint so that rolling the savepoint back never un-reserves
        it, and the command's other reservations are restored after a failure.
        """
        if not await self._due(postponement_id, now):
            return None
        await lock_planning(self.db)
        saved = self._save_state()
        try:
            async with self.db.begin_nested():
                return await self._evaluate(postponement_id, now=now)
        except Exception:
            self._restore_state(saved)
            logger.warning("Reactivation of the task postponed by postponement %s failed", postponement_id, exc_info=True)
            return None

    async def _due(self, postponement_id, now=None):
        """Read-only: whether a requirement of this open postponement newly holds, or all are already met."""
        with internal_authority(self.db):
            postponement = await self.db.scalar(select(TaskPostponement).where(
                TaskPostponement.id == postponement_id, TaskPostponement.reactivated_at.is_(None)))
            if postponement is None:
                return False
            task = await self.db.scalar(select(Task).where(Task.id == postponement.task_id))
            if task is None or task.status != POSTPONED:
                return False
            # Exactly what _complete_if_met refuses: such a task never reactivates, so never lock for it.
            if task.canceled_at is not None or task.is_summary or await self.db.scalar(
                    select(Task.id).where(Task.parent_id == task.id).limit(1)) is not None:
                return False
            requirements = await self._requirements(postponement)
            return all(requirement.met_at is not None for requirement in requirements) or bool(
                await self._holding(requirements, task, now or utc_now()))

    async def _evaluate(self, postponement_id, *, now=None):
        """Mark each requirement that now holds as met and reactivate once every one is met."""
        now = now or utc_now()
        # Shared planning first, then the postponement row, as every planning command orders its locks.
        await lock_planning(self.db)
        with internal_authority(self.db):
            postponement = await self.db.scalar(select(TaskPostponement).where(
                TaskPostponement.id == postponement_id, TaskPostponement.reactivated_at.is_(None))
                .with_for_update().execution_options(populate_existing=True))
            if postponement is None:
                # Another trigger reactivated it first.
                return None
            task = await self.db.scalar(select(Task).where(Task.id == postponement.task_id).execution_options(populate_existing=True))
            if task is None or task.status != POSTPONED:
                return None
            return await self._apply(postponement, task, await self._requirements(postponement), now, [])

    async def _apply(self, postponement, task, requirements, now, newly_met):
        """Record every requirement that holds now, then reactivate if all are met."""
        for requirement in await self._holding(requirements, task, now):
            requirement.met_at = now
            newly_met.append(requirement)
        await self.db.flush()
        return await self._complete_if_met(postponement, task, newly_met, requirements)

    async def _holding(self, requirements, task, now):
        """The unmet requirements whose fact is true now. An owner decision is never inferred."""
        today = None
        holding = []
        for requirement in requirements:
            if requirement.met_at is not None or requirement.kind == "owner_decision":
                continue
            if requirement.kind == "date" and today is None:
                from app.services.work_metrics import working_today
                today = working_today(await self.postponements._timezone(task), now)
            if await self._holds(requirement, today):
                holding.append(requirement)
        return holding

    async def _holds(self, requirement, today):
        if requirement.kind == "date":
            return requirement.on_date <= today
        if requirement.target_triage_item_id is not None:
            status = await self.db.scalar(select(TriageItem.status).where(TriageItem.id == requirement.target_triage_item_id)
                                          .execution_options(populate_existing=True))
            return status in RESOLVED_TRIAGE_STATUSES
        if requirement.target_task_id is None:
            return False
        target = await self.db.scalar(select(Task).where(Task.id == requirement.target_task_id).execution_options(populate_existing=True))
        if target is None or target.canceled_at is not None:
            return False
        if requirement.kind == "predecessor_accepted":
            return is_accepted(target)
        return target.status in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}

    async def _complete_if_met(self, postponement, task, newly_met, requirements):
        """Reactivate the task once, if every requirement is met; return its ID, or None."""
        if any(requirement.met_at is None for requirement in requirements):
            return None
        # All met with none newly met: an earlier attempt could not finish, so this sweep retries it.
        newly_met = newly_met or [max(requirements, key=lambda requirement: requirement.met_at)]
        from app.services.task_hierarchy_service import TaskTreeIntegrityError
        try:
            await self.postponements.tasks._lock_task_scope(task.id)
        except TaskTreeIntegrityError as exc:
            raise PlanningConflict("task_ancestry_invalid", "Reload or repair this task's ancestry before changing its lifecycle.") from exc
        task = await self.postponements.tasks.get_by_id(task.id)
        if task is None or task.status != POSTPONED or task.canceled_at is not None or task.is_summary or task.children:
            return None
        completed_by = "; ".join(_describe(requirement) for requirement in newly_met)
        reason = f"Reactivation requirements met: {completed_by}"
        task = await self.postponements.resume(
            task, postponement, reason=reason, trigger=AUTOMATIC_TRIGGER, expected_version=task.version, automatic=True,
            event_extra={"completed_by": [_summary(requirement) for requirement in newly_met],
                         "requirements": [_summary(requirement) | {"met_at": requirement.met_at.isoformat()}
                                          for requirement in requirements]})
        await self._notify_pm(task, postponement, newly_met, reason)
        await self.db.flush()
        return task.id

    async def _notify_pm(self, task, postponement, newly_met, reason):
        """Tell the project's planning side the work is back: a durable event for webhooks and agents.

        The status change that returns the task already queues the manager email with
        the reason, which names the completing requirement; this event adds the
        structured record for webhook subscribers.
        """
        from app.services.outbound_webhook_service import emit_outbound_webhook_event
        await emit_outbound_webhook_event(
            self.db, commit=False, event_type="task.reactivated", entity_type="task", entity_id=task.id,
            data={"task_id": task.id, "title": task.title, "project_id": task.project_id, "iteration_id": task.iteration_id,
                  "postponement_id": postponement.id, "to_status": task.status, "reason": reason,
                  "postponed_by_principal_id": postponement.postponed_by_principal_id,
                  "postponed_by_actor_id": postponement.postponed_by_actor_id,
                  "completed_by": [_summary(requirement) for requirement in newly_met]})


async def run_due_postponement_checks(*, now: datetime | None = None) -> list[int]:
    """Entry point for the worker: run the daily check in its own session."""
    from app.database import async_session_maker
    from app.maintenance import require_background_writes_enabled

    require_background_writes_enabled("postponement reactivation check")
    async with async_session_maker() as db:
        with internal_authority(db):
            return await ReactivationService(db).run_date_check(now=now)


async def postponement_check_loop(stop_event, *, interval_seconds=900.0):
    """Run the check at a steady interval until shutdown; each run is idempotent."""
    import asyncio
    while not stop_event.is_set():
        try:
            reactivated = await run_due_postponement_checks()
            if reactivated:
                logger.info("Reactivated postponed tasks %s", reactivated)
        except Exception:
            logger.error("Postponement reactivation check failed", exc_info=True)
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval_seconds)
        except TimeoutError:
            continue
