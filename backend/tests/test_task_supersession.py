"""An original superseded by work already closed or accepted: nothing reopens, and the deliverable counts once."""

from datetime import timedelta
from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy import select

from app.authority import Authority, AuthorityError
from app.commands import PlanningConflict
from app.main import app
from app.models.agent import TaskEvent
from app.models.delivery_dependency import DeliveryDependency
from app.models.delivery_observation import DeliveryObservation
from app.models.identity import Principal
from app.models.release import Release, release_tasks
from app.models.task import Task, TaskDependency
from app.models.task_postponement import TaskPostponement, TaskReactivationRequirement
from app.models.task_replacement import TaskReplacement
from app.schemas.task_replacement import TaskReplacementCreate, TaskSupersessionCreate
from app.services.delivery_dependency_service import DeliveryDependencyService
from app.services.release_service import ReleaseService
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_replacement_service import TaskReplacementService
from app.services.work_metrics import leaf_metrics
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store

__all__ = ["delivery_store"]

REASON = "The successor shipped the same importer before this task was linked to it."


def _client():
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")


def _supersede(original, successor, **overrides):
    return {"successor_task_id": successor.id, "expected_original_version": original.version,
            "expected_successor_version": successor.version, "reason": REASON, **overrides}


async def _accept(db, task):
    owner = Principal(kind="human", display_name="Release owner")
    db.add(owner)
    await db.flush()
    task.status, task.accepted_at, task.accepted_by_principal_id = "closed", utc_now(), owner.id
    task.accepted_version = task.version


async def _postponed(db, project_id, iteration_id, target_id, *, reactivated=False):
    waiting = Task(title="Waits on the importer", project_id=project_id, iteration_id=iteration_id,
                   status="planned" if reactivated else "postponed", effort_hours=8)
    db.add(waiting)
    await db.flush()
    done = {"reactivated_at": utc_now(), "reactivated_to_status": "planned", "reactivation_trigger": "command"} if reactivated else {}
    postponement = TaskPostponement(task_id=waiting.id, from_status="planned", reason="Needs the importer",
                                    task_version=waiting.version, released={}, **done)
    db.add(postponement)
    await db.flush()
    requirement = TaskReactivationRequirement(postponement_id=postponement.id, task_id=waiting.id, position=0,
                                              kind="predecessor_accepted", target_task_id=target_id)
    db.add(requirement)
    await db.flush()
    return waiting, requirement


async def _scenario(db, scenario, *, successor_state):
    """A resolved original with dependents, releases and a waiting postponement; its successor already delivered."""
    project_id, iteration_id = scenario.projects[0], scenario.iterations[0]
    original = await db.get(Task, scenario.tasks["resolved"])
    successor = await db.get(Task, scenario.tasks["closed_urgent"])
    if successor_state == "accepted":
        await _accept(db, successor)
    schedule_dependent, delivery_dependent = (Task(title=title, project_id=project_id, iteration_id=iteration_id,
                                                   status="planned", effort_hours=8)
                                              for title in ("Build on the importer", "Ship the importer"))
    db.add_all([schedule_dependent, delivery_dependent])
    await db.flush()
    db.add_all([TaskDependency(task_id=schedule_dependent.id, depends_on_id=original.id),
                DeliveryDependency(task_id=delivery_dependent.id, prerequisite_task_id=original.id)])
    waiting, requirement = await _postponed(db, project_id, iteration_id, original.id)
    _, history = await _postponed(db, project_id, iteration_id, original.id, reactivated=True)
    releases = {status: Release(name=f"Importer {status}", project_id=project_id, status=status)
                for status in ("planned", "shipped", "canceled")}
    db.add_all(releases.values())
    await db.flush()
    links = [(release.id, original.id) for release in releases.values()] + [(releases["shipped"].id, successor.id)]
    await db.execute(release_tasks.insert(), [{"release_id": r, "task_id": t, "created_at": utc_now()} for r, t in links])
    await db.commit()
    return SimpleNamespace(
        original=SimpleNamespace(id=original.id, version=original.version),
        successor=SimpleNamespace(id=successor.id, version=successor.version, accepted_at=successor.accepted_at),
        schedule_dependent=schedule_dependent.id, delivery_dependent=delivery_dependent.id,
        waiting=SimpleNamespace(id=waiting.id, version=waiting.version), requirement=requirement.id,
        history_requirement=history.id, releases={status: release.id for status, release in releases.items()})


@pytest.mark.parametrize("successor_state", ["accepted", "closed"])
async def test_supersession_moves_dependents_releases_and_requirements_and_counts_once(delivery_store, successor_state):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        s = await _scenario(db, scenario, successor_state=successor_state)
    async with _client() as client:
        response = await client.post(f"/api/tasks/{s.original.id}/supersession", json=_supersede(s.original, s.successor))
        assert response.status_code == 201, response.text
        view = response.json()
        again = await client.post(f"/api/tasks/{s.original.id}/supersession",
                                  json=_supersede(SimpleNamespace(id=s.original.id, version=s.original.version + 1), s.successor))
        assert again.status_code == 409, again.text
        read = await client.get(f"/api/tasks/{s.successor.id}/replacement")
        assert read.status_code == 200 and read.json()["role"] == "successor"
    assert view["disposition"] == "supersession" and view["role"] == "original"
    assert (view["original_task_id"], view["replacement_task_id"]) == (s.original.id, s.successor.id)
    assert view["decision"]["reason"] == REASON and view["decision"]["owner_decision"] is None
    assert view["replacement"]["recorded_base_commit_url"] is None
    assert view["replacement"]["accepted"] is (successor_state == "accepted")
    assert view["original"]["status_at_decision"] == "resolved" and view["original"]["independently_accepted"] is False
    assert view["acceptance"] == {"deliverable_task_id": s.successor.id, "state": "clean", "hold_reasons": [],
                                  "unattributed_carried_run_ids": []}
    assert sorted((item["task_id"], item["kind"], item["action"]) for item in view["moved_dependencies"]) == sorted([
        (s.schedule_dependent, "schedule", "moved"), (s.delivery_dependent, "delivery", "moved"),
        (s.waiting.id, "reactivation", "moved")])
    # Releases that still count work follow; a canceled release keeps only the original.
    assert view["moved_release_ids"] == sorted([s.releases["planned"], s.releases["shipped"]])

    async with factory() as db:
        original, successor = await db.get(Task, s.original.id), await db.get(Task, s.successor.id)
        # Withdrawn, not reopened: the original keeps its status; the successor is untouched.
        assert original.status == "resolved" and original.canceled_at is not None
        assert original.canceled_reason == f"Superseded by task {successor.id}: {REASON}"
        assert original.version == s.original.version + 1
        assert successor.status == "closed" and successor.version == s.successor.version
        assert (successor.accepted_at is not None) is (successor_state == "accepted")
        assert await db.scalar(select(TaskDependency.depends_on_id).where(
            TaskDependency.task_id == s.schedule_dependent)) == successor.id
        assert await db.scalar(select(DeliveryDependency.prerequisite_task_id).where(
            DeliveryDependency.task_id == s.delivery_dependent)) == successor.id
        assert (await db.get(TaskReactivationRequirement, s.requirement)).target_task_id == successor.id
        # A reactivated postponement is history and keeps naming the original.
        assert (await db.get(TaskReactivationRequirement, s.history_requirement)).target_task_id == original.id
        # The moved requirement is evaluated in the same command: an accepted successor
        # meets it and reactivates the waiting task; a closed, unaccepted one does not.
        waiting = await db.get(Task, s.waiting.id)
        requirement = await db.get(TaskReactivationRequirement, s.requirement)
        postponement = await db.get(TaskPostponement, requirement.postponement_id)
        if successor_state == "accepted":
            assert waiting.status == "planned" and requirement.met_at is not None
            assert postponement.reactivation_trigger == "requirements_met"
        else:
            assert waiting.status == "postponed" and waiting.version == s.waiting.version
            assert requirement.met_at is None and postponement.reactivated_at is None
        members = {}
        for release_id, task_id in (await db.execute(select(release_tasks.c.release_id, release_tasks.c.task_id))).all():
            members.setdefault(release_id, []).append(task_id)
        assert sorted(members[s.releases["planned"]]) == sorted([original.id, successor.id])
        assert sorted(members[s.releases["shipped"]]) == sorted([original.id, successor.id])
        assert members[s.releases["canceled"]] == [original.id]

        # The deliverable counts once, through the successor.
        accepted = int(successor_state == "accepted")
        counts = leaf_metrics([original, successor])
        assert (counts["total_tasks"], counts["implemented_tasks"], counts["accepted_tasks"]) == (1, 1, accepted)
        for status in ("planned", "shipped"):
            release = await ReleaseService(db).get_by_id(s.releases[status])
            assert (release.total_tasks, release.implemented_tasks, release.accepted_tasks) == (1, 1, accepted)
        kinds = set((await db.scalars(select(DeliveryObservation.kind).where(
            DeliveryObservation.original_task_id == original.id))).all())
        assert "replaced" in kinds and "canceled" not in kinds
        assert await DeliveryDependencyService(db).ready(s.delivery_dependent) is bool(accepted)

        events = {(row.task_id, row.event_type) for row in (await db.scalars(select(TaskEvent))).all()}
        assert {(original.id, "task_superseded"), (successor.id, "task_supersession_recorded"),
                (s.schedule_dependent, "dependency_replaced"), (s.delivery_dependent, "dependency_replaced"),
                (s.waiting.id, "dependency_replaced")} <= events

        # The original can never be reviewed or reopened into a second count.
        with pytest.raises(AuthorityError, match="superseded by task"):
            await TaskBriefService(db).require_review(original, accepting=False)
        actions = {item.action: item for item in (await TaskDomainService(db).allowed_actions(original.id)).actions}
        assert not actions["reopen"].allowed and "task_replaced" in {b.code for b in actions["reopen"].blockers}
        with pytest.raises(PlanningConflict, match="retains this work"):
            await DeliveryDependencyService(db).require_unreferenced({original.id})
        await db.rollback()


async def test_an_already_canceled_original_keeps_its_cancel_reason(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original = await db.get(Task, scenario.tasks["active"])
        canceled_at = utc_now() - timedelta(days=2)
        original.canceled_at, original.canceled_reason = canceled_at, "Duplicate of the importer task"
        await db.commit()
        successor = await db.get(Task, scenario.tasks["closed_low"])
        ids = SimpleNamespace(id=original.id, version=original.version), SimpleNamespace(id=successor.id, version=successor.version)
    result = await _with_service(factory, lambda service: service.supersede(
        ids[0].id, TaskSupersessionCreate(**_supersede(*ids))))
    assert result["original"]["canceled"] and result["original"]["status"] == "active"
    async with factory() as db:
        kept = await db.get(Task, ids[0].id)
        assert kept.canceled_reason == "Duplicate of the importer task" and kept.status == "active"
        relation = await db.scalar(select(TaskReplacement).where(TaskReplacement.original_task_id == kept.id))
        assert relation.original_snapshot["canceled_before_decision"] is True


async def _with_service(factory, call):
    async with factory() as db:
        return await call(TaskReplacementService(db))


async def test_supersession_refuses_ineligible_pairs(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        planned, active, resolved, closed, accepted_original = [
            await db.get(Task, scenario.tasks[key]) for key in ("planned", "active", "resolved", "closed_urgent", "closed_low")]
        await _accept(db, accepted_original)
        foreign = await db.get(Task, scenario.tasks["other_project"])
        foreign.status = "closed"
        canceled_successor = Task(title="Canceled delivery", project_id=scenario.projects[0],
                                  iteration_id=scenario.iterations[0], status="closed", canceled_at=utc_now())
        db.add(canceled_successor)
        await db.commit()
        frozen = {key: SimpleNamespace(id=task.id, version=task.version) for key, task in (
            ("planned", planned), ("active", active), ("resolved", resolved), ("closed", closed),
            ("accepted_original", accepted_original), ("foreign", foreign), ("canceled", canceled_successor))}

    async def supersede(original, successor):
        return await _with_service(factory, lambda service: service.supersede(
            frozen[original].id, TaskSupersessionCreate(**_supersede(frozen[original], frozen[successor]))))

    for successor in ("planned", "resolved", "canceled"):
        with pytest.raises(PlanningConflict) as refused:
            await supersede("active", successor)
        assert refused.value.code == "supersession_successor_not_delivered"
    with pytest.raises(PlanningConflict, match="same project"):
        await supersede("active", "foreign")
    with pytest.raises(PlanningConflict) as refused:
        await supersede("accepted_original", "closed")
    assert refused.value.code == "replacement_original_accepted"
    with pytest.raises(ValueError, match="cannot supersede itself"):
        await supersede("closed", "closed")
    await supersede("active", "closed")
    # One disposition per task: the successor cannot also supersede or replace another original.
    with pytest.raises(PlanningConflict) as refused:
        await supersede("resolved", "closed")
    assert refused.value.code == "task_replacement_exists"


async def test_the_fresh_replacement_still_refuses_a_closed_replacement(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, closed = await db.get(Task, scenario.tasks["resolved"]), await db.get(Task, scenario.tasks["closed_urgent"])
        ids = SimpleNamespace(id=original.id, version=original.version), SimpleNamespace(id=closed.id, version=closed.version)
    data = TaskReplacementCreate(replacement_task_id=ids[1].id, expected_original_version=ids[0].version,
                                 expected_replacement_version=ids[1].version, reason="Unknown publisher",
                                 owner_decision="Owner approved", carried_run_ids=[],
                                 base_commit_url="https://github.com/example/project/commit/" + "0" * 40)
    with pytest.raises(PlanningConflict) as refused:
        await _with_service(factory, lambda service: service.record(ids[0].id, data))
    assert refused.value.code == "replacement_not_fresh"


@pytest.mark.parametrize(("kind", "role", "project_role", "allowed"), [
    ("human", None, "editor", False),
    ("human", None, "manager", True),
    ("agent", "worker", "manager", False),
    ("agent", "pm", "manager", True),
])
async def test_only_a_project_manager_or_pm_actor_supersedes(delivery_store, kind, role, project_role, allowed):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, successor = await db.get(Task, scenario.tasks["resolved"]), await db.get(Task, scenario.tasks["closed_urgent"])
        data = TaskSupersessionCreate(**_supersede(original, successor))
        db.info["authority"] = Authority(None, kind, projects={scenario.projects[0]: project_role}, actor_role=role,
                                         scopes=frozenset(("planning:read", "planning:write")) if kind == "agent" else frozenset())
        service = TaskReplacementService(db)
        if allowed:
            view = await service.supersede(original.id, data)
            assert view["disposition"] == "supersession"
        else:
            with pytest.raises(AuthorityError):
                await service.supersede(original.id, data)


def _frozen(*tasks):
    return [SimpleNamespace(id=task.id, version=task.version) for task in tasks]


async def _refused(factory, original, successor, *, expected=PlanningConflict, **overrides):
    with pytest.raises(expected) as refused:
        await _with_service(factory, lambda service: service.supersede(
            original.id, TaskSupersessionCreate(**_supersede(original, successor, **overrides))))
    async with factory() as db:
        # A refused command changes nothing: no disposition, and the original is not withdrawn.
        assert await db.scalar(select(TaskReplacement.id).where(TaskReplacement.original_task_id == original.id)) is None
        kept = await db.get(Task, original.id)
        assert kept.version == original.version and kept.canceled_at is None
    return refused.value


@pytest.mark.parametrize("successor_state", ["accepted", "closed"])
async def test_a_milestone_whose_only_leaf_was_superseded_counts_the_successor(delivery_store, successor_state):
    from app.models.project import ProjectMilestone
    factory, scenario, _ = delivery_store
    async with factory() as db:
        milestone = ProjectMilestone(project_id=scenario.projects[0], name="Importer milestone", status="completed")
        db.add(milestone)
        await db.flush()
        original = Task(title="Only leaf of the milestone", project_id=scenario.projects[0],
                        iteration_id=scenario.iterations[0], milestone_id=milestone.id, status="resolved")
        dependent = Task(title="Waits on the milestone", project_id=scenario.projects[0],
                         iteration_id=scenario.iterations[0], status="planned")
        db.add_all([original, dependent])
        await db.flush()
        # The successor lives in no milestone at all.
        successor = await db.get(Task, scenario.tasks["closed_urgent"])
        if successor_state == "accepted":
            await _accept(db, successor)
        db.add(DeliveryDependency(task_id=dependent.id, prerequisite_milestone_id=milestone.id))
        await db.commit()
        dependent_id = dependent.id
        original, successor = _frozen(original, successor)
        assert not await DeliveryDependencyService(db).ready(dependent_id)
    await _with_service(factory, lambda service: service.supersede(
        original.id, TaskSupersessionCreate(**_supersede(original, successor))))
    async with factory() as db:
        assert await DeliveryDependencyService(db).ready(dependent_id) is (successor_state == "accepted")


async def test_a_schedule_dependent_follows_a_successor_in_another_iteration_as_a_delivery_prerequisite(delivery_store):
    from app.models.iteration import Iteration
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first = await db.get(Iteration, scenario.iterations[0])
        later = Iteration(name="February delivery", start_date=first.end_date + timedelta(days=3),
                          end_date=first.end_date + timedelta(days=30), calendar_id=first.calendar_id,
                          project_id=scenario.projects[0])
        db.add(later)
        await db.flush()
        original = await db.get(Task, scenario.tasks["resolved"])
        successor = Task(title="Importer, delivered next iteration", project_id=scenario.projects[0],
                         iteration_id=later.id, status="closed")
        db.add(successor)
        await db.flush()
        await _accept(db, successor)
        converted, merged = (Task(title=title, project_id=scenario.projects[0], iteration_id=first.id, status="planned")
                             for title in ("Follows the importer", "Already waits on the successor"))
        db.add_all([converted, merged])
        await db.flush()
        db.add_all([TaskDependency(task_id=converted.id, depends_on_id=original.id),
                    TaskDependency(task_id=merged.id, depends_on_id=original.id),
                    DeliveryDependency(task_id=merged.id, prerequisite_task_id=successor.id)])
        await db.commit()
        ids = SimpleNamespace(converted=converted.id, merged=merged.id)
        original, successor = _frozen(original, successor)
    view = await _with_service(factory, lambda service: service.supersede(
        original.id, TaskSupersessionCreate(**_supersede(original, successor))))
    assert sorted((item["task_id"], item["kind"], item["action"]) for item in view["moved_dependencies"]) == sorted([
        (ids.converted, "schedule", "converted"), (ids.merged, "schedule", "merged")])
    async with factory() as db:
        assert (await db.scalars(select(TaskDependency).where(TaskDependency.depends_on_id == original.id))).all() == []
        for task_id in (ids.converted, ids.merged):
            edges = (await db.scalars(select(DeliveryDependency.prerequisite_task_id).where(
                DeliveryDependency.task_id == task_id))).all()
            assert edges == [successor.id]
            assert await DeliveryDependencyService(db).ready(task_id)
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == ids.converted,
                                                           TaskEvent.event_type == "dependency_replaced"))).all()
        assert len(events) == 1 and '"converted"' in events[0].payload


async def test_edges_to_the_successor_merge_and_its_own_edges_to_the_original_are_removed(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, successor = await db.get(Task, scenario.tasks["resolved"]), await db.get(Task, scenario.tasks["closed_urgent"])
        dependent = Task(title="Waits on both", project_id=scenario.projects[0], iteration_id=scenario.iterations[0],
                         status="planned")
        db.add(dependent)
        await db.flush()
        db.add_all([TaskDependency(task_id=dependent.id, depends_on_id=original.id),
                    TaskDependency(task_id=dependent.id, depends_on_id=successor.id),
                    DeliveryDependency(task_id=dependent.id, prerequisite_task_id=original.id),
                    DeliveryDependency(task_id=dependent.id, prerequisite_task_id=successor.id),
                    TaskDependency(task_id=successor.id, depends_on_id=original.id),
                    DeliveryDependency(task_id=successor.id, prerequisite_task_id=original.id)])
        waiting, requirement = await _postponed(db, scenario.projects[0], scenario.iterations[0], original.id)
        twin = TaskReactivationRequirement(postponement_id=requirement.postponement_id, task_id=waiting.id, position=1,
                                           kind="predecessor_accepted", target_task_id=successor.id)
        db.add(twin)
        await db.commit()
        ids = SimpleNamespace(dependent=dependent.id, waiting=waiting.id, requirement=requirement.id, twin=twin.id)
        original, successor = _frozen(original, successor)
    view = await _with_service(factory, lambda service: service.supersede(
        original.id, TaskSupersessionCreate(**_supersede(original, successor))))
    assert sorted((item["task_id"], item["kind"], item["action"]) for item in view["moved_dependencies"]) == sorted([
        (ids.dependent, "schedule", "merged"), (ids.dependent, "delivery", "merged"),
        (successor.id, "schedule", "removed"), (successor.id, "delivery", "removed"),
        (ids.waiting, "reactivation", "merged")])
    async with factory() as db:
        assert (await db.scalars(select(TaskDependency.depends_on_id).where(
            TaskDependency.task_id == ids.dependent))).all() == [successor.id]
        assert (await db.scalars(select(DeliveryDependency.prerequisite_task_id).where(
            DeliveryDependency.task_id == ids.dependent))).all() == [successor.id]
        assert (await db.scalars(select(TaskDependency).where(TaskDependency.task_id == successor.id))).all() == []
        assert (await db.scalars(select(DeliveryDependency).where(DeliveryDependency.task_id == successor.id))).all() == []
        assert await db.get(TaskReactivationRequirement, ids.requirement) is None
        assert (await db.get(TaskReactivationRequirement, ids.twin)).target_task_id == successor.id


async def test_a_dependency_cycle_is_refused_and_rolls_back(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, successor = await db.get(Task, scenario.tasks["resolved"]), await db.get(Task, scenario.tasks["closed_urgent"])
        dependent = Task(title="Depends on the original", project_id=scenario.projects[0],
                         iteration_id=scenario.iterations[0], status="planned")
        db.add(dependent)
        await db.flush()
        # The successor already depends on the original's dependent, so moving the edge would close a loop.
        db.add_all([DeliveryDependency(task_id=dependent.id, prerequisite_task_id=original.id),
                    DeliveryDependency(task_id=successor.id, prerequisite_task_id=dependent.id)])
        await db.commit()
        dependent_id = dependent.id
        original, successor = _frozen(original, successor)
    assert (await _refused(factory, original, successor)).code == "replacement_dependency_cycle"
    async with factory() as db:
        assert await db.scalar(select(DeliveryDependency.prerequisite_task_id).where(
            DeliveryDependency.task_id == dependent_id)) == original.id


async def test_supersession_refuses_stale_live_summary_and_unauthorized_moves(delivery_store):
    from app.models.agent import AgentTaskAssignment
    from app.services.task_service import TaskVersionConflictError
    factory, scenario, _ = delivery_store
    async with factory() as db:
        resolved, active, closed, parent = [await db.get(Task, scenario.tasks[key])
                                            for key in ("resolved", "active", "closed_urgent", "parent")]
        db.add(AgentTaskAssignment(task_id=active.id, actor_id=scenario.actors[0], purpose="execution",
                                   queue_class="normal", state="queued", task_version=active.version,
                                   routing_snapshot="{}"))
        # A dependent in another project, which a manager of the first project cannot edit.
        db.add(DeliveryDependency(task_id=scenario.tasks["other_project"], prerequisite_task_id=resolved.id))
        await db.commit()
        resolved, active, closed, parent = _frozen(resolved, active, closed, parent)
    await _refused(factory, resolved, closed, expected=TaskVersionConflictError,
                   expected_successor_version=closed.version + 1)
    assert (await _refused(factory, active, closed)).code == "replacement_original_execution_live"
    assert (await _refused(factory, parent, closed)).code == "replacement_leaf_required"
    assert (await _refused(factory, resolved, parent)).code == "replacement_leaf_required"

    async def as_manager(service):
        service.db.info["authority"] = Authority(None, "human", projects={scenario.projects[0]: "manager"})
        return await service.supersede(resolved.id, TaskSupersessionCreate(**_supersede(resolved, closed)))

    await _refused_with(factory, as_manager, resolved, AuthorityError)
    async with factory() as db:
        assert await db.scalar(select(DeliveryDependency.prerequisite_task_id).where(
            DeliveryDependency.task_id == scenario.tasks["other_project"])) == resolved.id


async def _refused_with(factory, call, original, expected):
    with pytest.raises(expected):
        await _with_service(factory, call)
    async with factory() as db:
        assert await db.scalar(select(TaskReplacement.id).where(TaskReplacement.original_task_id == original.id)) is None
        assert (await db.get(Task, original.id)).version == original.version


async def test_a_worker_agent_cannot_supersede_over_rest(delivery_store, monkeypatch):
    from app.config import get_settings
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, successor = _frozen(await db.get(Task, scenario.tasks["resolved"]),
                                      await db.get(Task, scenario.tasks["closed_urgent"]))
    try:
        async with _client() as client:
            refused = await client.post(f"/api/tasks/{original.id}/supersession", json=_supersede(original, successor),
                                        headers={"X-Agent-API-Key": scenario.actor_keys[0]})
        assert refused.status_code == 403, refused.text
    finally:
        get_settings.cache_clear()
    async with factory() as db:
        assert await db.scalar(select(TaskReplacement.id)) is None


async def test_a_postponed_original_has_its_postponement_closed(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original = await db.get(Task, scenario.tasks["resolved"])
        original.status = "postponed"
        postponement = TaskPostponement(task_id=original.id, from_status="resolved", reason="Waiting on a vendor",
                                        task_version=original.version, released={})
        db.add(postponement)
        await db.commit()
        postponement_id = postponement.id
        original, successor = _frozen(original, await db.get(Task, scenario.tasks["closed_urgent"]))
    view = await _with_service(factory, lambda service: service.supersede(
        original.id, TaskSupersessionCreate(**_supersede(original, successor))))
    assert view["original"]["status_at_decision"] == "postponed"
    async with factory() as db:
        kept = await db.get(Task, original.id)
        assert kept.status == "resolved" and kept.canceled_at is not None
        closed = await db.get(TaskPostponement, postponement_id)
        assert closed.reactivated_at is not None and closed.reactivated_to_status == "resolved"
        assert closed.reactivation_trigger == "supersession" and f"task {successor.id}" in closed.reactivation_reason
        events = {row.event_type for row in (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == kept.id))).all()}
        assert {"postponement_closed", "task_superseded"} <= events


async def test_the_successor_of_a_supersession_cannot_be_canceled_but_a_fresh_replacement_can(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original, successor, fresh_original, fresh = _frozen(*[await db.get(Task, scenario.tasks[key]) for key in (
            "resolved", "closed_urgent", "active", "planned")])
    await _with_service(factory, lambda service: service.supersede(
        original.id, TaskSupersessionCreate(**_supersede(original, successor))))
    data = TaskReplacementCreate(replacement_task_id=fresh.id, expected_original_version=fresh_original.version,
                                 expected_replacement_version=fresh.version, reason="Unknown publisher",
                                 owner_decision="Owner approved", carried_run_ids=[],
                                 base_commit_url="https://github.com/example/project/commit/" + "0" * 40)
    await _with_service(factory, lambda service: service.record(fresh_original.id, data))
    async with factory() as db:
        actions = {item.action: item for item in (await TaskDomainService(db).allowed_actions(successor.id)).actions}
        assert not actions["cancel"].allowed
        assert "task_delivers_supersession" in {blocker.code for blocker in actions["cancel"].blockers}
        actions = {item.action: item for item in (await TaskDomainService(db).allowed_actions(fresh.id)).actions}
        assert "task_delivers_supersession" not in {blocker.code for blocker in actions["cancel"].blockers}
    async with _client() as client:
        refused = await client.post(f"/api/tasks/{successor.id}/commands", json={
            "action": "cancel", "expected_version": successor.version, "reason": "No longer needed"})
        assert refused.status_code == 409 and "task_delivers_supersession" in refused.text, refused.text


async def test_a_supersession_chain_beyond_the_bound_reads_as_not_delivered_and_warns(delivery_store, monkeypatch, caplog):
    import logging
    from app.services import task_replacement_service
    from app.services.task_replacement_service import delivering_leaves
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second, third = [await db.get(Task, scenario.tasks[key]) for key in ("resolved", "closed_urgent", "closed_low")]
        await _accept(db, third)
        for original, successor in ((first, second), (second, third)):
            db.add(TaskReplacement(project_id=scenario.projects[0], original_task_id=original.id,
                                   replacement_task_id=successor.id, disposition="supersession", reason=REASON,
                                   carried_run_ids=[], moved_dependencies=[], moved_release_ids=[],
                                   original_snapshot={}, review_policy={}, decided_at=utc_now()))
        await db.commit()
        assert [task.id for task in await delivering_leaves(db, [first])] == [third.id]
        monkeypatch.setattr(task_replacement_service, "MAX_SUPERSESSION_CHAIN", 1)
        with caplog.at_level(logging.WARNING, logger="app.services.task_replacement_service"):
            assert await delivering_leaves(db, [first]) == []
        assert any("exceeds 1 links" in record.getMessage() for record in caplog.records)
