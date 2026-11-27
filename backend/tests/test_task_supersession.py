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
        assert read.status_code == 200 and read.json()["role"] == "replacement"
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
        assert (await db.get(Task, s.waiting.id)).version == s.waiting.version
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
