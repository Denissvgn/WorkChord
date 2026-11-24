"""Record and read an audited clean replacement of task work that cannot be attributed.

An original task whose runs lack attribution can never pass independent review.
Its work is done again as a separate task from a clean base. The disposition
keeps the original with its attempts, artifacts and unknown attribution, names
who decided and why, moves the original's dependents and release membership to
the replacement, and withdraws the original from delivery counts. Only the
replacement can be accepted, and a replacement that carries commits from an
unattributed run stays held.
"""

from sqlalchemy import insert, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command, lock_backlog_project
from app.models.agent import AgentRun, AgentTaskAssignment
from app.models.delivery_dependency import DeliveryDependency
from app.models.project import Project
from app.models.release import Release, release_tasks
from app.models.task import Task, TaskDependency
from app.models.task_replacement import TaskReplacement
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.utils.github_links import GitHubLinkError, parse_github_url
from app.utils.time import utc_now

HOLD_UNATTRIBUTED = "carried_contribution_unattributed"


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


async def carried_contributors(db, task):
    """Contributor rows for the original runs this replacement carries, read from current records."""
    relation = await replacing(db, task.id)
    if relation is None or not relation.carried_run_ids:
        return []
    with internal_authority(db):
        original = await db.get(Task, relation.original_task_id)
    history = await attempt_history(db, original)
    carried = set(relation.carried_run_ids)
    rows = [{**row, "carried_from_task_id": original.id} for row in history.contributors if row.get("run_id") in carried]
    for run_id in sorted(carried - {row["run_id"] for row in rows}):
        # A carried run without a contributor record cannot show who wrote its commits.
        rows.append({"run_id": run_id, "actor_id": None, "profile_id": None, "publisher_key": None,
                     "missing": ["contributor_record"], "carried_from_task_id": original.id})
    return rows


async def require_acceptable(db, task, *, accepting):
    """A replaced original is never reviewed; a replacement carrying unattributed work stays held."""
    relation = await replaced_by(db, task.id)
    if relation is not None:
        raise AuthorityError("task_replaced", f"Task {task.id} was replaced by task {relation.replacement_task_id}. "
                             "Its work is retained for audit and is never accepted independently.", 409)
    if accepting and any(not attributed(row) for row in await carried_contributors(db, task)):
        raise AuthorityError("replacement_contribution_unattributed",
                             "This replacement carries commits from an unattributed run and stays held.", 409)


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
        raise AuthorityError("replacement_decider_required", "Only the project's PM or an operator can replace a task.")


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
            "id": relation.id, "project_id": relation.project_id,
            "role": "original" if task_id == original.id else "replacement",
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
            reason=data.reason, owner_decision=data.owner_decision, base_commit_url=base,
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

    async def _require_eligible(self, original, replacement):
        # A replacement whose own work later proves unattributable can itself be replaced.
        if await replaced_by(self.db, original.id) is not None:
            raise PlanningConflict("task_replacement_exists", "This task has already been replaced.")
        if await relation_for(self.db, replacement.id) is not None:
            raise PlanningConflict("task_replacement_exists", "The replacement already takes part in a replacement disposition.")
        if original.is_summary or original.children or replacement.is_summary or replacement.children:
            raise PlanningConflict("replacement_leaf_required", "Replace one leaf task with another leaf task.")
        if original.status == "closed" or original.accepted_at is not None:
            raise PlanningConflict("replacement_original_accepted", "Accepted work cannot be replaced; reopen it through review first.")
        if original.milestone_id != replacement.milestone_id:
            raise PlanningConflict("replacement_scope_mismatch", "The replacement must deliver the original's milestone.")
        live = await self.db.scalar(select(AgentTaskAssignment.id).where(
            AgentTaskAssignment.task_id == original.id, AgentTaskAssignment.state.in_(("queued", "accepted"))).limit(1))
        running = await self.db.scalar(select(AgentRun.id).where(AgentRun.task_id == original.id,
                                                                 AgentRun.status == "running").limit(1))
        if live is not None or running is not None or original.claimed_by is not None:
            raise PlanningConflict("replacement_original_execution_live",
                                   "Recover or cancel the original's live execution before replacing it.")
        attempted = await self.db.scalar(select(AgentRun.id).where(AgentRun.task_id == replacement.id).limit(1))
        assigned = await self.db.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == replacement.id).limit(1))
        if (replacement.status != "planned" or replacement.canceled_at is not None or replacement.accepted_at is not None
                or replacement.executed_by_principal_id is not None or replacement.claimed_by is not None
                or attempted is not None or assigned is not None):
            raise PlanningConflict("replacement_not_fresh",
                                   "The replacement must be planned work with no attempts, assignments or acceptance.")

    async def _move_dependents(self, original, replacement):
        """Point each dependent at the replacement; prerequisite identity, not dependent work, changes.

        A dependent keeps its version, so work already issued for it stays valid,
        and its downstream evidence is not invalidated by this re-pointing.
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

    async def _move_releases(self, original, replacement):
        """Open releases that planned the original's deliverable count the replacement instead."""
        releases = (await self.db.execute(select(Release.id).join(release_tasks, release_tasks.c.release_id == Release.id)
                                          .where(release_tasks.c.task_id == original.id,
                                                 Release.status.in_(("planned", "building"))).order_by(Release.id))).scalars().all()
        present = set((await self.db.scalars(select(release_tasks.c.release_id).where(
            release_tasks.c.task_id == replacement.id))).all())
        added = [release_id for release_id in releases if release_id not in present]
        if added:
            # The original stays listed for audit; as withdrawn work it no longer counts.
            await self.db.execute(insert(release_tasks), [{"release_id": release_id, "task_id": replacement.id,
                                                           "created_at": utc_now()} for release_id in added])
        return list(releases)
