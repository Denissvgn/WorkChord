"""Record and read an audited disposition that names the task delivering another task's work.

A clean replacement: an original task whose runs lack attribution can never pass
independent review. Its work is done again as a separate task from a clean base.
The disposition keeps the original with its attempts, artifacts and unknown
attribution, names who decided and why, moves the original's dependents and
release membership to the replacement, and withdraws the original from delivery
counts. Only the replacement can be accepted, and a replacement that carries
commits from an unattributed run stays held.

A supersession: the original's deliverable was already closed or accepted as
another task before anyone recorded a replacement. The successor is not
re-executed or reopened, and the original is not reopened: it is withdrawn from
delivery counts with its history kept, and its dependents, delivery
prerequisites, release membership and the reactivation requirements that name it
move to the successor, so the deliverable counts once.
"""

import logging

from sqlalchemy import insert, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command, lock_backlog_project
from app.models.agent import AgentRun, AgentTaskAssignment
from app.models.delivery_dependency import DeliveryDependency
from app.models.project import Project
from app.models.release import Release, release_tasks
from app.models.task import Task, TaskDependency
from app.models.task_postponement import TaskPostponement, TaskReactivationRequirement
from app.models.task_replacement import TaskReplacement
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.utils.github_links import GitHubLinkError, parse_github_url
from app.utils.time import utc_now

logger = logging.getLogger(__name__)

HOLD_UNATTRIBUTED = "carried_contribution_unattributed"
REPLACEMENT, SUPERSESSION = "replacement", "supersession"
# A supersession moves membership of every release that still counts work; a
# canceled release counts nothing, so it keeps listing only the original.
SUPERSESSION_RELEASE_STATUSES = ("planned", "building", "shipped")


def attributed(row):
    """A contribution counts as attributed only with a known profile and publisher and no gap."""
    return bool(row.get("profile_id") and row.get("publisher_key") and not row.get("missing"))


async def replaced_by(db, task_id):
    """The disposition that replaced this task, if any."""
    with internal_authority(db):
        return await db.scalar(select(TaskReplacement).where(TaskReplacement.original_task_id == task_id))


async def replacing(db, task_id):
    """The disposition this task delivers as a replacement, if any."""
    with internal_authority(db):
        return await db.scalar(select(TaskReplacement).where(TaskReplacement.replacement_task_id == task_id))


MAX_SUPERSESSION_CHAIN = 32


async def delivering_leaves(db, leaves):
    """The leaves whose acceptance decides a scope's delivery, each deliverable counted once.

    A replaced original is dropped: its fresh replacement delivers the same
    milestone and is a leaf of the scope itself. A superseded original is
    represented by its successor, which may live in another milestone or
    iteration, followed through any later disposition of that successor. A chain
    longer than the bound fails closed: the scope reads as not delivered.
    """
    chosen, visited, frontier = {}, set(), [leaf for leaf in leaves]
    for _ in range(MAX_SUPERSESSION_CHAIN):
        frontier = [task for task in frontier if task.id not in visited]
        if not frontier:
            return list(chosen.values())
        visited.update(task.id for task in frontier)
        with internal_authority(db):
            relations = {row.original_task_id: row for row in (await db.scalars(select(TaskReplacement).where(
                TaskReplacement.original_task_id.in_([task.id for task in frontier])))).all()}
        successors = []
        for task in frontier:
            relation = relations.get(task.id)
            if relation is None:
                chosen.setdefault(task.id, task)
            elif relation.disposition == SUPERSESSION:
                successors.append(relation.replacement_task_id)
        if not successors:
            return list(chosen.values())
        with internal_authority(db):
            frontier = list((await db.scalars(select(Task).where(Task.id.in_(successors)))).all())
    logger.warning("Supersession chain from tasks %s exceeds %s links; the scope reads as not delivered",
                   sorted(leaf.id for leaf in leaves), MAX_SUPERSESSION_CHAIN)
    return []


async def relation_for(db, task_id):
    """The disposition to show for this task; a replacement that was itself replaced shows as replaced."""
    return await replaced_by(db, task_id) or await replacing(db, task_id)


async def _assignments(db, task_id):
    rows = (await db.scalars(select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == task_id)
                             .order_by(AgentTaskAssignment.id).limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
    if len(rows) > MAX_BOUNDED_LIST_ITEMS:
        raise CollectionLimitExceededError("task assignments", MAX_BOUNDED_LIST_ITEMS)
    return list(rows)


async def attempt_history(db, task):
    """Every recorded attempt on this task alone, with its server-held attribution."""
    from app.services.review_provenance import review_history
    with internal_authority(db):
        return await review_history(db, task, await _assignments(db, task.id), strict=True, include_carried=False)


def _carried_bound_row(original_task_id, reason):
    """A contributor row that holds the replacement: the carried chain is too long or cyclic to read."""
    return {"run_id": None, "actor_id": None, "profile_id": None, "publisher_key": None,
            "missing": [reason], "carried_from_task_id": original_task_id, "truncated": reason}


async def carried_contributors(db, task):
    """Contributor rows for the original runs this replacement carries, read from current records.

    The walk through earlier replacements is bounded like carried_profile_history: depth, visited
    task ids and carried run count. A bound that is hit ends the walk with a held row.
    """
    from app.services.review_provenance import MAX_CARRIED_HISTORY_RUNS, MAX_CARRIED_REPLACEMENT_DEPTH
    rows, visited, loaded, current = [], {task.id}, 0, task
    while True:
        relation = await replacing(db, current.id)
        if relation is None or not relation.carried_run_ids:
            return rows
        if len(visited) > MAX_CARRIED_REPLACEMENT_DEPTH:
            return rows + [_carried_bound_row(relation.original_task_id, "carried_history_depth")]
        if relation.original_task_id in visited:
            return rows + [_carried_bound_row(relation.original_task_id, "carried_history_cycle")]
        loaded += len(relation.carried_run_ids)
        if loaded > MAX_CARRIED_HISTORY_RUNS:
            return rows + [_carried_bound_row(relation.original_task_id, "carried_history_runs")]
        with internal_authority(db):
            original = await db.get(Task, relation.original_task_id)
        history = await attempt_history(db, original)
        carried = set(relation.carried_run_ids)
        level = [{**row, "carried_from_task_id": original.id} for row in history.contributors if row.get("run_id") in carried]
        for run_id in sorted(carried - {row["run_id"] for row in level}):
            # A carried run without a contributor record cannot show who wrote its commits.
            level.append({"run_id": run_id, "actor_id": None, "profile_id": None, "publisher_key": None,
                          "missing": ["contributor_record"], "carried_from_task_id": original.id})
        rows.extend(level)
        visited.add(original.id)
        # Runs carried from a replacement may build on what that replacement carried in turn,
        # so the earlier original's carried runs count here too and can hold this replacement.
        current = original


async def require_acceptable(db, task, *, accepting):
    """A replaced original is never reviewed; a replacement carrying unattributed work stays held."""
    relation = await replaced_by(db, task.id)
    if relation is not None:
        verb = "superseded" if relation.disposition == SUPERSESSION else "replaced"
        raise AuthorityError("task_replaced", f"Task {task.id} was {verb} by task {relation.replacement_task_id}. "
                             "Its work is retained for audit and is never accepted independently.", 409)
    if accepting and any(not attributed(row) for row in await carried_contributors(db, task)):
        raise AuthorityError("replacement_contribution_unattributed",
                             "This replacement carries commits from an unattributed run and stays held.", 409)


async def require_restore_compatible(db, rows, current):
    """Refuse a snapshot restore that would undo or bypass a replacement disposition.

    ``rows`` are the snapshot's task rows and ``current`` the tasks it replaces.
    A restore may not change a disposition task's canceled state or status, nor
    any dependency that touches one: the original would come back unaccepted
    forever, its dependents would wait on it, and the deliverable would count twice.
    """
    ids = {row["id"] for row in rows} | {task.id for task in current}
    with internal_authority(db):
        pairs = (await db.execute(select(TaskReplacement.original_task_id, TaskReplacement.replacement_task_id).where(
            TaskReplacement.original_task_id.in_(ids) | TaskReplacement.replacement_task_id.in_(ids)))).all()
        linked = {task_id for pair in pairs for task_id in pair}
        if not linked:
            return
        present = {}
        for source, target in (await db.execute(select(TaskDependency.task_id, TaskDependency.depends_on_id)
                                                 .where(TaskDependency.task_id.in_(ids)))).all():
            present.setdefault(source, set()).add(target)
    by_id = {task.id: task for task in current}
    for row in rows:
        task = by_id.get(row["id"])
        changed = set(row.get("dependencies") or ()) ^ present.get(row["id"], set())
        state_changed = row["id"] in linked and (
            task is None or bool(row.get("canceled_at")) != (task.canceled_at is not None) or row.get("status") != task.status)
        if state_changed or (changed and (row["id"] in linked or changed & linked)):
            raise PlanningConflict("restore_conflicts_with_task_replacement",
                                   f"Restoring would change task {row['id']}, which a replacement disposition records. "
                                   "Restore a snapshot taken after the replacement, or adjust the work directly.")


def _contributor(row):
    return {"run_id": row.get("run_id"), "actor_id": row.get("actor_id"), "profile_id": row.get("profile_id"),
            "publisher_key": row.get("publisher_key"), "commit_urls": list(row.get("commit_urls") or ()),
            "missing": list(row.get("missing") or ([] if attributed(row) else
                                                    [key for key in ("profile_id", "publisher_key") if not row.get(key)])),
            "attributed": attributed(row), "carried_from_task_id": row.get("carried_from_task_id")}


def _require_decider(db, project_id):
    require_project(db, project_id, "manage")
    authority = db.info.get("authority")
    if authority is not None and authority.kind == "agent" and not authority.operator and authority.actor_role != "pm":
        raise AuthorityError("replacement_decider_required",
                             "Only the project's PM or an operator can replace or supersede a task.")


def _base_commit(url):
    try:
        link = parse_github_url(url)
    except (GitHubLinkError, ValueError) as exc:
        raise ValueError("The replacement base must be an immutable GitHub commit URL") from exc
    if link.github_type != "commit":
        raise ValueError("The replacement base must be an immutable GitHub commit URL")
    return link.url


class TaskReplacementService:
    def __init__(self, db):
        self.db = db

    @property
    def tasks(self):
        from app.services.task_service import TaskService
        return TaskService(self.db)

    async def get(self, task_id):
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise LookupError("Task not found or inaccessible")
        require_project(self.db, task.project_id, "read")
        relation = await relation_for(self.db, task_id)
        if relation is None:
            raise LookupError("This task has no replacement disposition")
        return await self.projection(relation, task_id)

    async def projection(self, relation, task_id):
        with internal_authority(self.db):
            original = await self.db.get(Task, relation.original_task_id)
            replacement = await self.db.get(Task, relation.replacement_task_id)
            policy = bool(await self.db.scalar(select(Project.require_different_review_publisher)
                                               .where(Project.id == relation.project_id)))
        original_history = await attempt_history(self.db, original)
        replacement_history = await attempt_history(self.db, replacement)
        carried = [_contributor(row) for row in await carried_contributors(self.db, replacement)]
        unattributed_carried = sorted({row["run_id"] for row in carried if not row["attributed"] and row["run_id"]})
        attempts = [_contributor(row) for row in original_history.contributors]
        candidate = replacement_history.candidate
        accepted = (replacement.status == "closed" and replacement.accepted_at is not None
                    and replacement.accepted_version == replacement.version)
        snapshot = relation.original_snapshot or {}
        return {
            "id": relation.id, "project_id": relation.project_id, "disposition": relation.disposition,
            "role": "original" if task_id == original.id else
                    "successor" if relation.disposition == SUPERSESSION else "replacement",
            "original_task_id": original.id, "replacement_task_id": replacement.id,
            "decision": {"reason": relation.reason, "owner_decision": relation.owner_decision,
                         "decided_at": relation.decided_at, "decided_by_principal_id": relation.decided_by_principal_id,
                         "decided_by_actor_id": relation.decided_by_actor_id},
            "review_policy": {"require_different_review_publisher_at_decision":
                              bool((relation.review_policy or {}).get("require_different_review_publisher")),
                              "require_different_review_publisher": policy},
            "original": {"task_id": original.id, "status": original.status, "canceled": original.canceled_at is not None,
                         "independently_accepted": False, "status_at_decision": snapshot.get("status", original.status),
                         "version_at_decision": snapshot.get("version", original.version), "attempts": attempts,
                         "unattributed_run_ids": sorted({row["run_id"] for row in attempts
                                                         if not row["attributed"] and row["run_id"]})},
            "replacement": {"task_id": replacement.id, "status": replacement.status, "accepted": accepted,
                            "recorded_base_commit_url": relation.base_commit_url,
                            "candidate": {key: candidate.get(key) for key in ("base_commit_url", "commit_url", "pr_url", "digest")}
                            if candidate else None,
                            "contributors": [_contributor(row) for row in replacement_history.contributors]},
            "carried_contributions": carried,
            "moved_dependencies": list(relation.moved_dependencies or ()),
            "moved_release_ids": list(relation.moved_release_ids or ()),
            "acceptance": {"deliverable_task_id": replacement.id, "state": "held" if unattributed_carried else "clean",
                           "hold_reasons": [HOLD_UNATTRIBUTED] if unattributed_carried else [],
                           "unattributed_carried_run_ids": unattributed_carried},
        }

    @atomic_command
    async def record(self, original_id, data, *, commit=True):
        """Link a fresh replacement to an unaccepted original under one audited decision."""
        hint = await self.db.scalar(select(Task).where(Task.id == original_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        _require_decider(self.db, hint.project_id)
        if data.replacement_task_id == original_id:
            raise ValueError("A task cannot replace itself")
        target = await self.db.scalar(select(Task.iteration_id).where(Task.id == data.replacement_task_id))
        await self.tasks._lock_task_scope(original_id, target_iteration_id=target)
        original = await self.tasks.get_by_id(original_id)
        replacement = await self.tasks.get_by_id(data.replacement_task_id)
        if original is None or replacement is None:
            raise LookupError("Task not found or inaccessible")
        if replacement.iteration_id is None and replacement.project_id is not None:
            await lock_backlog_project(self.db, replacement.project_id)
        if original.project_id is None or replacement.project_id != original.project_id:
            raise PlanningConflict("replacement_scope_mismatch", "The original and its replacement must belong to the same project.")
        self.tasks.ensure_expected_version(original, data.expected_original_version)
        self.tasks.ensure_expected_version(replacement, data.expected_replacement_version)
        await self._require_eligible(original, replacement)
        base = _base_commit(data.base_commit_url)
        history = await attempt_history(self.db, original)
        recorded_runs = {row.get("run_id") for row in history.contributors}
        stray = sorted(set(data.carried_run_ids) - recorded_runs)
        if stray:
            raise PlanningConflict("replacement_carried_run_unknown",
                                   f"Carried runs {stray} are not recorded contributions of task {original.id}.")
        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(original.iteration_id, "before_task_replacement")
        moved = await self._move_dependents(original, replacement)
        releases = await self._move_releases(original, replacement)
        from app.services.identity_service import acting_principal_id
        authority = self.db.info.get("authority")
        principal_id = await acting_principal_id(self.db)
        actor_id = getattr(authority, "actor_id", None)
        policy = bool(await self.db.scalar(select(Project.require_different_review_publisher)
                                           .where(Project.id == original.project_id)))
        snapshot = {"status": original.status, "version": original.version,
                    "canceled_before_decision": original.canceled_at is not None,
                    "unattributed_run_ids": sorted({row["run_id"] for row in history.contributors
                                                    if row.get("run_id") and not attributed(row)})}
        relation = TaskReplacement(
            project_id=original.project_id, original_task_id=original.id, replacement_task_id=replacement.id,
            disposition=REPLACEMENT, reason=data.reason, owner_decision=data.owner_decision, base_commit_url=base,
            carried_run_ids=list(data.carried_run_ids), moved_dependencies=moved, moved_release_ids=releases,
            original_snapshot=snapshot, review_policy={"require_different_review_publisher": policy},
            decided_by_principal_id=principal_id, decided_by_actor_id=actor_id, decided_at=utc_now())
        self.db.add(relation)
        await self.tasks.reserve_task_version(original, data.expected_original_version)
        if original.canceled_at is None:
            from app.services.task_brief_service import clear_acceptance
            original.canceled_at = utc_now()
            original.canceled_reason = f"Replaced by task {replacement.id}: {data.reason}"
            original.canceled_by_principal_id = principal_id
            clear_acceptance(original)
        event = {"original_task_id": original.id, "replacement_task_id": replacement.id, "reason": data.reason,
                 "owner_decision": data.owner_decision, "base_commit_url": base,
                 "carried_run_ids": list(data.carried_run_ids)}
        await self.tasks.record_task_event(original.id, "task_replaced", {**event, "version": original.version})
        await self.tasks.record_task_event(replacement.id, "task_replacement_recorded", {**event, "version": replacement.version})
        for item in moved:
            await self.tasks.record_task_event(item["task_id"], "dependency_replaced", {
                "original_task_id": original.id, "replacement_task_id": replacement.id, **item})
        await self.db.flush()
        return await self.projection(relation, original.id)

    @atomic_command
    async def supersede(self, original_id, data, *, commit=True):
        """Record that a closed or accepted successor already delivered this original's work.

        Neither task is reopened or re-executed. The original keeps its status,
        progress, attempts and history; unless it was already canceled it is
        withdrawn as superseded work, so the deliverable counts once, through the
        successor. Its dependents, delivery prerequisites, release membership and
        open reactivation requirements move to the successor.
        """
        hint = await self.db.scalar(select(Task).where(Task.id == original_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        _require_decider(self.db, hint.project_id)
        if data.successor_task_id == original_id:
            raise ValueError("A task cannot supersede itself")
        target = await self.db.scalar(select(Task.iteration_id).where(Task.id == data.successor_task_id))
        await self.tasks._lock_task_scope(original_id, target_iteration_id=target)
        original = await self.tasks.get_by_id(original_id)
        successor = await self.tasks.get_by_id(data.successor_task_id)
        if original is None or successor is None:
            raise LookupError("Task not found or inaccessible")
        if successor.iteration_id is None and successor.project_id is not None:
            await lock_backlog_project(self.db, successor.project_id)
        if original.project_id is None or successor.project_id != original.project_id:
            raise PlanningConflict("replacement_scope_mismatch", "The original and its successor must belong to the same project.")
        self.tasks.ensure_expected_version(original, data.expected_original_version)
        self.tasks.ensure_expected_version(successor, data.expected_successor_version)
        await self._require_supersedable(original, successor)
        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(original.iteration_id, "before_task_supersession")
        moved = await self._move_dependents(original, successor, delivered=True)
        moved += await self._move_requirements(original, successor)
        if any(item["kind"] == "reactivation" for item in moved):
            # A moved requirement may now name work that is already accepted or resolved;
            # evaluate the waiting postponements at the end of this command.
            from app.services.task_reactivation_service import request_reactivation_check
            request_reactivation_check(self.db, task_id=successor.id)
        releases = await self._move_releases(original, successor, statuses=SUPERSESSION_RELEASE_STATUSES)
        from app.services.identity_service import acting_principal_id
        authority = self.db.info.get("authority")
        principal_id = await acting_principal_id(self.db)
        policy = bool(await self.db.scalar(select(Project.require_different_review_publisher)
                                           .where(Project.id == original.project_id)))
        snapshot = {"status": original.status, "version": original.version,
                    "canceled_before_decision": original.canceled_at is not None,
                    "canceled_reason_before_decision": original.canceled_reason,
                    "successor_status": successor.status, "successor_version": successor.version,
                    "successor_accepted": successor.accepted_at is not None
                    and successor.accepted_version == successor.version}
        relation = TaskReplacement(
            project_id=original.project_id, original_task_id=original.id, replacement_task_id=successor.id,
            disposition=SUPERSESSION, reason=data.reason, owner_decision=None, base_commit_url=None,
            carried_run_ids=[], moved_dependencies=moved, moved_release_ids=releases, original_snapshot=snapshot,
            review_policy={"require_different_review_publisher": policy},
            decided_by_principal_id=principal_id, decided_by_actor_id=getattr(authority, "actor_id", None),
            decided_at=utc_now())
        self.db.add(relation)
        closed = await self._close_postponement(original, successor, data)
        if closed is None:
            await self.tasks.reserve_task_version(original, data.expected_original_version)
        if original.canceled_at is None:
            # Withdrawn, not reopened: progress and execution history stay as they were.
            original.canceled_at = utc_now()
            original.canceled_reason = f"Superseded by task {successor.id}: {data.reason}"
            original.canceled_by_principal_id = principal_id
        event = {"original_task_id": original.id, "successor_task_id": successor.id, "reason": data.reason,
                 "successor_status": successor.status, "moved_release_ids": releases}
        await self.tasks.record_task_event(original.id, "task_superseded", {**event, "version": original.version})
        await self.tasks.record_task_event(successor.id, "task_supersession_recorded",
                                           {**event, "version": successor.version})
        for item in moved:
            await self.tasks.record_task_event(item["task_id"], "dependency_replaced", {
                "original_task_id": original.id, "replacement_task_id": successor.id, **item})
        await self.db.flush()
        return await self.projection(relation, original.id)

    async def _close_postponement(self, original, successor, data):
        """End a postponed original's open postponement: its work is delivered, so nothing is left to wait for.

        The postponement closes the way reactivation would, returning the original
        to planned (or resolved, if it was postponed after resolution) under the
        trigger ``supersession``; the original is then withdrawn as superseded, so
        it never returns to work. Returns the closed postponement, or None when
        the original was not postponed.
        """
        from app.services.task_postponement_service import POSTPONED, open_postponement, reactivation_status
        if original.status != POSTPONED:
            return None
        postponement = await open_postponement(self.db, original.id, lock=True)
        target = reactivation_status(postponement)
        reason = f"Superseded by task {successor.id}: {data.reason}"
        await self.tasks.status_service.apply_postponement_transition(
            original, target, reason=reason, expected_version=data.expected_original_version)
        if postponement is not None:
            from app.services.identity_service import acting_principal_id
            postponement.reactivated_at = utc_now()
            postponement.reactivated_to_status = target
            postponement.reactivation_trigger = SUPERSESSION
            postponement.reactivation_reason = reason
            postponement.reactivated_by_principal_id = await acting_principal_id(self.db)
            postponement.reactivated_by_actor_id = getattr(self.db.info.get("authority"), "actor_id", None)
        await self.tasks.record_task_event(original.id, "postponement_closed", {
            "postponement_id": postponement.id if postponement is not None else None, "to_status": target,
            "trigger": SUPERSESSION, "successor_task_id": successor.id, "reason": reason, "version": original.version})
        return postponement or target

    async def _require_unused(self, original, replacement):
        # A replacement whose own work later proves unattributable can itself be replaced.
        if await replaced_by(self.db, original.id) is not None:
            raise PlanningConflict("task_replacement_exists", "This task has already been replaced.")
        if await relation_for(self.db, replacement.id) is not None:
            raise PlanningConflict("task_replacement_exists", "The replacement already takes part in a replacement disposition.")
        if original.is_summary or original.children or replacement.is_summary or replacement.children:
            raise PlanningConflict("replacement_leaf_required", "Replace one leaf task with another leaf task.")

    async def _require_no_live_execution(self, original):
        live = await self.db.scalar(select(AgentTaskAssignment.id).where(
            AgentTaskAssignment.task_id == original.id, AgentTaskAssignment.state.in_(("queued", "accepted"))).limit(1))
        running = await self.db.scalar(select(AgentRun.id).where(AgentRun.task_id == original.id,
                                                                 AgentRun.status == "running").limit(1))
        if live is not None or running is not None or original.claimed_by is not None:
            raise PlanningConflict("replacement_original_execution_live",
                                   "Recover or cancel the original's live execution before replacing it.")

    async def _require_supersedable(self, original, successor):
        await self._require_unused(original, successor)
        if original.accepted_at is not None:
            # Its acceptance would stay counted beside the successor's.
            raise PlanningConflict("replacement_original_accepted",
                                   "Accepted work cannot be superseded; cancel it or reopen it through review first.")
        await self._require_no_live_execution(original)
        if successor.status != "closed" or successor.canceled_at is not None:
            raise PlanningConflict("supersession_successor_not_delivered",
                                   "The successor must be closed or accepted work that is not canceled.")

    async def _require_eligible(self, original, replacement):
        await self._require_unused(original, replacement)
        if original.status == "closed" or original.accepted_at is not None:
            raise PlanningConflict("replacement_original_accepted", "Accepted work cannot be replaced; reopen it through review first.")
        if original.milestone_id != replacement.milestone_id:
            raise PlanningConflict("replacement_scope_mismatch", "The replacement must deliver the original's milestone.")
        await self._require_no_live_execution(original)
        attempted = await self.db.scalar(select(AgentRun.id).where(AgentRun.task_id == replacement.id).limit(1))
        assigned = await self.db.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == replacement.id).limit(1))
        if (replacement.status != "planned" or replacement.canceled_at is not None or replacement.accepted_at is not None
                or replacement.executed_by_principal_id is not None or replacement.claimed_by is not None
                or attempted is not None or assigned is not None):
            raise PlanningConflict("replacement_not_fresh",
                                   "The replacement must be planned work with no attempts, assignments or acceptance.")

    async def _move_dependents(self, original, replacement, *, delivered=False):
        """Point each dependent at the replacement; prerequisite identity, not dependent work, changes.

        A dependent keeps its version, so work already issued for it stays valid,
        and its downstream evidence is not invalidated by this re-pointing. With
        ``delivered`` (a supersession), a schedule dependent of an original whose
        successor is in another iteration gets a delivery prerequisite on the
        successor instead of a schedule edge (action ``converted``).
        """
        moved = []
        self.db.info["delivery_reconciling"] = True
        try:
            for model, column, kind in ((TaskDependency, TaskDependency.depends_on_id, "schedule"),
                                        (DeliveryDependency, DeliveryDependency.prerequisite_task_id, "delivery")):
                # Every dependent must follow, including one in another project; the
                # decider needs edit access to each, so none is silently left behind.
                with internal_authority(self.db):
                    edges = (await self.db.scalars(select(model).where(column == original.id).order_by(model.id))).all()
                    scopes = dict((await self.db.execute(select(Task.id, Task.project_id).where(
                        Task.id.in_([edge.task_id for edge in edges])))).all())
                for edge in edges:
                    require_project(self.db, scopes.get(edge.task_id), "edit")
                    duplicate = await self.db.scalar(select(model.id).where(model.task_id == edge.task_id,
                                                                            column == replacement.id).limit(1))
                    if edge.task_id == replacement.id or duplicate is not None:
                        await self.db.delete(edge)
                        action = "removed" if edge.task_id == replacement.id else "merged"
                    elif kind == "schedule" and replacement.iteration_id != original.iteration_id and delivered:
                        # A schedule edge cannot cross iterations. The successor is already
                        # closed, so its ordering is met; what the dependent still needs is
                        # the successor's acceptance, which a delivery prerequisite states.
                        await self.db.delete(edge)
                        existing = await self.db.scalar(select(DeliveryDependency.id).where(
                            DeliveryDependency.task_id == edge.task_id,
                            DeliveryDependency.prerequisite_task_id == replacement.id).limit(1))
                        if existing is None:
                            self.db.add(DeliveryDependency(task_id=edge.task_id, prerequisite_task_id=replacement.id))
                        await self.db.flush()
                        action = "converted" if existing is None else "merged"
                    else:
                        if kind == "schedule" and replacement.iteration_id != original.iteration_id:
                            raise PlanningConflict("replacement_scope_mismatch",
                                                   "Schedule dependents can follow only a replacement in the original's iteration.")
                        if kind == "schedule":
                            edge.depends_on = replacement
                        else:
                            edge.prerequisite_task_id = replacement.id
                        action = "moved"
                    moved.append({"task_id": edge.task_id, "kind": kind, "action": action})
            await self.db.flush()
        finally:
            self.db.info.pop("delivery_reconciling", None)
        if moved:
            from app.services.delivery_dependency_service import DeliveryDependencyService
            try:
                await DeliveryDependencyService(self.db).validate_cycles()
            except PlanningConflict as exc:
                raise PlanningConflict("replacement_dependency_cycle",
                                       "A dependent of the original is a prerequisite of the replacement.") from exc
        return moved

    async def _move_requirements(self, original, successor):
        """Reactivation requirements of open postponements that name the original name the successor.

        A requirement on a reactivated postponement is history and keeps its target.
        The postponed task keeps its version; whether a moved requirement now holds
        is evaluated against the successor like any other requirement.
        """
        moved = []
        requirement = TaskReactivationRequirement
        with internal_authority(self.db):
            rows = (await self.db.scalars(
                select(requirement).join(TaskPostponement, TaskPostponement.id == requirement.postponement_id)
                .where(requirement.target_task_id == original.id, TaskPostponement.reactivated_at.is_(None))
                .order_by(requirement.id))).all()
            scopes = dict((await self.db.execute(select(Task.id, Task.project_id).where(
                Task.id.in_([row.task_id for row in rows])))).all())
        for row in rows:
            # A postponed task in another project must follow too. Changing what a
            # postponement waits for is a postponement decision, so it needs the same
            # manage permission as postponing that task.
            require_project(self.db, scopes.get(row.task_id), "manage")
            with internal_authority(self.db):
                duplicate = await self.db.scalar(select(requirement.id).where(
                    requirement.postponement_id == row.postponement_id, requirement.kind == row.kind,
                    requirement.target_task_id == successor.id).limit(1))
            # The successor is closed, so it has no open postponement of its own.
            if duplicate is not None:
                await self.db.delete(row)
                action = "merged"
            else:
                row.target_task_id = successor.id
                action = "moved"
            moved.append({"task_id": row.task_id, "kind": "reactivation", "action": action})
        if rows:
            await self.db.flush()
        return moved

    async def _move_releases(self, original, replacement, *, statuses=("planned", "building")):
        """Releases that planned the original's deliverable count the replacement instead.

        A replacement follows only open releases; a supersession, whose successor is
        already delivered, also follows shipped ones.
        """
        releases = (await self.db.execute(select(Release.id).join(release_tasks, release_tasks.c.release_id == Release.id)
                                          .where(release_tasks.c.task_id == original.id,
                                                 Release.status.in_(statuses)).order_by(Release.id))).scalars().all()
        present = set((await self.db.scalars(select(release_tasks.c.release_id).where(
            release_tasks.c.task_id == replacement.id))).all())
        added = [release_id for release_id in releases if release_id not in present]
        if added:
            # The original stays listed for audit; as withdrawn work it no longer counts.
            await self.db.execute(insert(release_tasks), [{"release_id": release_id, "task_id": replacement.id,
                                                           "created_at": utc_now()} for release_id in added])
        return list(releases)
