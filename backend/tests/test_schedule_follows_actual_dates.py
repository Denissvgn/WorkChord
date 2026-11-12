"""Agents start work whose dependencies are done, and the plan's dates follow what happened."""

from datetime import date, datetime
import json

import httpx
import pytest
from sqlalchemy import select

from app.main import app
from app.models.agent import AgentActor, AgentTaskAssignment, TaskEvent
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.schemas.task import TaskCreate
from app.schemas.task_brief import BriefCriterion, TaskBrief
from app.services import agent_work_service, backlog_snapshot_service, work_metrics
from app.services.scheduler_service import rebind_queued_assignments
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store  # noqa: F401

TODAY = date(2026, 1, 20)  # a Tuesday inside the scenario iteration
NOW = datetime.fromisoformat("2026-01-20T12:00:00+00:00")


@pytest.fixture
def fixed_clock(monkeypatch):
    from app.utils import time

    real_utc_now = time.utc_now
    # Snapshot filenames keep a progressing clock independently of the working day.
    monkeypatch.setattr(backlog_snapshot_service, "utc_now", real_utc_now)
    monkeypatch.setattr(agent_work_service, "utc_now", lambda: NOW)
    monkeypatch.setattr(work_metrics, "utc_now", lambda: NOW)
    monkeypatch.setattr(time, "utc_now", lambda: NOW)


def _brief() -> TaskBrief:
    return TaskBrief(
        goal="Deliver result", scope="One bounded result", verification="Inspect result independently",
        acceptance_criteria=[BriefCriterion(id="result", text="Correct result")],
    )


async def _seed(factory, scenario, plan, *, assigned=True):
    """Create one agent capacity row and the planned tasks in ``plan``.

    ``plan`` maps a key to (start, end, depends_on_keys, priority, queued).
    """
    async with factory() as db:
        worker = await db.get(AgentActor, scenario.actors[0])
        # The worker preset: no task, planning, or team scope.
        worker.scopes = json.dumps(["work:execute", "assignments:read", "events:write", "runs:write"])
        row_id = None
        if assigned:
            profile = TeamMemberProfile(display_name="Build agent", profile_kind="agent", automation_enabled=True)
            row = TeamMember(name="Build agent", position="Agent", profile=profile,
                             iteration_id=scenario.iterations[0], operational_utilization=0)
            db.add_all([profile, row])
            await db.flush()
            row_id = row.id
        ids: dict[str, int] = {}
        for key, (start, end, depends_on, priority, queued) in plan.items():
            task = await TaskService(db).create(scenario.iterations[0], TaskCreate(
                title=f"Work {key}", project_id=scenario.projects[0], effort_hours=8, priority=priority,
                assignee_id=row_id, depends_on=[ids[name] for name in depends_on],
                tags=["agent", "cap:inspection"], brief=_brief(),
            ))
            task.start_date, task.end_date = start, end
            ids[key] = task.id
            if queued:
                await db.flush()
                db.add(AgentTaskAssignment(task_id=task.id, actor_id=worker.id, purpose="execution",
                                           state="queued", task_version=task.version))
        await db.commit()
        return ids


def _headers(scenario, key):
    return {"X-Agent-API-Key": scenario.actor_keys[0], "Idempotency-Key": key}


async def _begin_next(client, scenario, key):
    work = await client.get("/api/agent/me/work", headers=_headers(scenario, key))
    assert work.status_code == 200, work.text
    decision = work.json()
    assert decision["state"] == "start_assigned", decision
    body = {"assignment_id": decision["next"]["assignment"]["id"],
            "queue_revision": decision["queue_revision"], "lease_seconds": 60}
    begun = await client.post("/api/agent/me/work/begin", headers=_headers(scenario, key), json=body)
    assert begun.status_code == 200, begun.text
    return begun.json()


async def _submit(client, scenario, receipt, key):
    body = dict(
        assignment_id=receipt["assignment"]["id"], run_id=receipt["run"]["id"], claim_id=receipt["claim_id"],
        claim_generation=receipt["claim_generation"], expected_task_version=receipt["task"]["version"],
        summary="Implemented result", evidence={"inspection": "Worker observation"},
        criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed",
                                 evidence="Artifact inspected")],
    )
    submitted = await client.post("/api/agent/me/work/submit", headers=_headers(scenario, key), json=body)
    assert submitted.status_code == 200, submitted.text
    return submitted.json()


async def _dates(factory, ids):
    async with factory() as db:
        tasks = {key: await db.get(Task, task_id) for key, task_id in ids.items()}
        return {key: (task.status, task.start_date, task.end_date) for key, task in tasks.items()}


def _client():
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")


async def test_early_start_and_early_finish_pull_the_row_and_dependents_forward(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {
        "first": (date(2026, 1, 26), date(2026, 1, 26), (), 1, True),
        "second": (date(2026, 1, 27), date(2026, 1, 27), ("first",), 1, True),
        "third": (date(2026, 1, 28), date(2026, 1, 28), (), 5, False),
    })
    async with _client() as client:
        receipt = await _begin_next(client, scenario, "begin-first")
        assert receipt["task"]["id"] == ids["first"]
        assert await _dates(factory, ids) == {
            "first": ("active", TODAY, TODAY),
            "second": ("planned", date(2026, 1, 21), date(2026, 1, 21)),
            "third": ("planned", date(2026, 1, 22), date(2026, 1, 22)),
        }
        async with factory() as db:
            second = await db.get(Task, ids["second"])
            queued = (await db.scalars(select(AgentTaskAssignment).where(
                AgentTaskAssignment.task_id == second.id))).one()
            # A change of dates alone keeps the queued dispatch valid.
            assert queued.task_version == second.version
            moved = (await db.scalars(select(TaskEvent).where(
                TaskEvent.task_id == second.id, TaskEvent.event_type == "task_schedule_applied"))).all()
            assert [json.loads(event.payload)["source_task_id"] for event in moved] == [ids["first"]]
        waiting = (await client.get("/api/agent/me/work", headers=_headers(scenario, "poll"))).json()
        assert waiting["state"] == "resume"

        await _submit(client, scenario, receipt, "submit-first")
        assert await _dates(factory, ids) == {
            "first": ("resolved", TODAY, TODAY),
            "second": ("planned", TODAY, TODAY),
            "third": ("planned", date(2026, 1, 21), date(2026, 1, 21)),
        }
        receipt = await _begin_next(client, scenario, "begin-second")
        assert receipt["task"]["id"] == ids["second"]
        assert (await _dates(factory, ids))["second"] == ("active", TODAY, TODAY)


async def test_late_start_moves_dependents_later_and_keeps_their_dispatch(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {
        "first": (date(2026, 1, 12), date(2026, 1, 12), (), 1, True),
        "second": (date(2026, 1, 13), date(2026, 1, 13), ("first",), 1, True),
    })
    async with _client() as client:
        await _begin_next(client, scenario, "begin-late")
        assert await _dates(factory, ids) == {
            "first": ("active", TODAY, TODAY),
            "second": ("planned", date(2026, 1, 21), date(2026, 1, 21)),
        }
        decision = (await client.get("/api/agent/me/work", headers=_headers(scenario, "poll"))).json()
        async with factory() as db:
            second = await db.get(Task, ids["second"])
            queued = (await db.scalars(select(AgentTaskAssignment).where(
                AgentTaskAssignment.task_id == second.id))).one()
            assert queued.task_version == second.version
        assert decision["state"] == "resume"


async def test_unfinished_dependency_still_holds_work_back(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {
        "first": (TODAY, TODAY, (), 1, False),
        "second": (date(2026, 1, 21), date(2026, 1, 21), ("first",), 1, True),
    })
    async with _client() as client:
        decision = (await client.get("/api/agent/me/work", headers=_headers(scenario, "poll"))).json()
    assert decision["state"] == "wait", decision
    assert decision["blocked_assigned"][0]["blocker_codes"] == [f"dependency_{ids['first']}_unresolved"]


async def test_a_planning_period_that_has_not_begun_holds_work_back(delivery_store, fixed_clock):
    factory, scenario, _ = delivery_store
    await _seed(factory, scenario, {"first": (date(2026, 1, 26), date(2026, 1, 26), (), 1, True)})
    async with factory() as db:
        iteration = await db.get(Iteration, scenario.iterations[0])
        iteration.start_date = date(2026, 1, 21)
        await db.commit()
    async with _client() as client:
        decision = (await client.get("/api/agent/me/work", headers=_headers(scenario, "poll"))).json()
    assert decision["state"] == "wait", decision
    assert decision["blocked_assigned"][0]["blocker_codes"] == ["iteration_not_started"]


async def test_following_actual_dates_never_removes_a_date(delivery_store, fixed_clock):
    """A plan loaded without assignees keeps its dates when one of its tasks starts."""
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {
        "first": (date(2026, 1, 26), date(2026, 1, 27), (), 1, True),
        "other": (date(2026, 1, 27), date(2026, 1, 28), (), 1, False),
    }, assigned=False)
    async with factory() as db:
        other_version = (await db.get(Task, ids["other"])).version
    async with _client() as client:
        await _begin_next(client, scenario, "begin-unassigned")
    assert await _dates(factory, ids) == {
        # Without a capacity row the forecast keeps its length from the actual start.
        "first": ("active", TODAY, date(2026, 1, 21)),
        "other": ("planned", date(2026, 1, 27), date(2026, 1, 28)),
    }
    async with factory() as db:
        assert (await db.get(Task, ids["other"])).version == other_version


async def test_only_plain_queued_assignments_follow_a_change_of_dates(delivery_store):
    factory, scenario, _ = delivery_store
    ids = await _seed(factory, scenario, {
        "plain": (TODAY, TODAY, (), 1, True),
        "routed": (TODAY, TODAY, (), 1, True),
        "running": (TODAY, TODAY, (), 1, True),
    })
    async with factory() as db:
        rows = {key: (await db.scalars(select(AgentTaskAssignment).where(
            AgentTaskAssignment.task_id == task_id))).one() for key, task_id in ids.items()}
        rows["routed"].routing_snapshot = json.dumps({"schema_version": "routing-decision-snapshot-v1"})
        rows["running"].state = "accepted"
        versions = {key: row.task_version for key, row in rows.items()}
        for key, task_id in ids.items():
            await rebind_queued_assignments(db, task_id, versions[key], versions[key] + 1)
        assert rows["plain"].task_version == versions["plain"] + 1
        # Routing evidence is bound to the exact task version, and running work to its fence.
        assert rows["routed"].task_version == versions["routed"]
        assert rows["running"].task_version == versions["running"]
