"""Postponed work keeps its last dates as history: it is never scheduled, counted, ready, dispatched or verified."""

from datetime import date

import httpx
import pytest
from sqlalchemy import select

from app.main import app
from app.models.release import Release
from app.models.task import Task, TaskDependency
from app.schemas.agent import AgentTaskAssignmentCreate
from app.services.agent_readiness import evaluate_agent_readiness
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_service import AgentService
from app.services.agent_work_service import AgentConflictError, AgentWorkService
from app.services.capacity_service import CapacityService
from app.services.iteration_service import IterationService
from app.services.release_service import ReleaseService
from app.services.review_provenance import select_reviewer
from app.services.scheduler_service import SchedulerService
from app.services.team_service import TeamService
from app.services.work_metrics import aggregate_metrics, leaf_metrics, task_signals
from tests.test_agent_routing_service import _rollout, _routing_fixture
from tests.test_delivery_scenarios import delivery_store

__all__ = ["delivery_store"]

HISTORY = (date(2026, 1, 5), date(2026, 1, 6))


@pytest.fixture
def january_today(monkeypatch):
    # Forecasts start at the working date; pin it to the first day of the seeded iteration.
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_args, **_kwargs: date(2026, 1, 5))


async def _postponed_plan(db, scenario):
    """In the second seeded iteration: postponed work holding two old days, planned work and its dependent."""
    iteration_id, member_id = scenario.iterations[1], scenario.capacity_rows[1]
    common = dict(iteration_id=iteration_id, project_id=scenario.projects[1], assignee_id=member_id,
                  effort_days=1, effort_hours=8)
    postponed = Task(title="Vendor integration", status="postponed", priority=1,
                     start_date=HISTORY[0], end_date=HISTORY[1],
                     baseline_start_date=HISTORY[0], baseline_end_date=HISTORY[1],
                     **{**common, "effort_days": 2, "effort_hours": 16})
    planned = Task(title="Settings page", status="planned", priority=1, **common)
    dependent = Task(title="Vendor dashboard", status="planned", priority=1, **common)
    db.add_all([postponed, planned, dependent])
    await db.flush()
    db.add(TaskDependency(task_id=dependent.id, depends_on_id=postponed.id))
    await db.commit()
    return iteration_id, postponed.id, planned.id, dependent.id


def _assert_schedule_skips_postponed(result, postponed_id, planned_id, dependent_id):
    unscheduled = {item["task_id"]: item for item in result["unscheduled"]}
    kept = {item["task_id"] for item in result.get("kept_dates", [])}
    # The postponed task is neither placed, kept, unscheduled nor reported missing dates.
    assert postponed_id not in unscheduled and postponed_id not in kept
    assert postponed_id not in {item["task_id"] for item in result["decisions"]}
    assert planned_id not in unscheduled and planned_id not in kept
    # Its dependent waits on it by name.
    assert unscheduled[dependent_id]["reason"] == "predecessor_postponed"
    assert unscheduled[dependent_id]["waiting_on"] == [{"task_id": postponed_id, "task_title": "Vendor integration"}]
    assert "Waiting on postponed task 'Vendor integration'" in unscheduled[dependent_id]["message"]
    assert f"(ID {postponed_id})" in unscheduled[dependent_id]["message"]


async def test_schedule_run_frees_postponed_capacity_and_waits_dependents_on_it(delivery_store, january_today):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, postponed_id, planned_id, dependent_id = await _postponed_plan(db, scenario)
        result = await SchedulerService(db).schedule_iteration(iteration_id)
        _assert_schedule_skips_postponed(result.model_dump(mode="json"), postponed_id, planned_id, dependent_id)
    async with factory() as db:
        rows = {row.id: row for row in (await db.scalars(select(Task).where(
            Task.id.in_([postponed_id, planned_id, dependent_id])))).all()}
        # The postponed task keeps its last dates as history, and the days they cover are free again.
        assert (rows[postponed_id].start_date, rows[postponed_id].end_date) == HISTORY
        assert rows[planned_id].start_date == HISTORY[0]
        assert rows[dependent_id].start_date is None and rows[dependent_id].end_date is None


async def test_schedule_preview_skips_postponed_work(delivery_store, january_today):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, postponed_id, planned_id, dependent_id = await _postponed_plan(db, scenario)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        preview = await client.post(f"/api/iterations/{iteration_id}/schedule/preview", json={"changes": []})
    assert preview.status_code == 200, preview.text
    body = preview.json()
    _assert_schedule_skips_postponed(body["schedule_result"], postponed_id, planned_id, dependent_id)
    planned = next(task for task in body["tasks"] if task["id"] == planned_id)
    assert planned["start_date"] == HISTORY[0].isoformat()


async def test_postponed_work_commits_no_capacity(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        _, postponed_id, *_ = await _postponed_plan(db, scenario)
        member_id = scenario.capacity_rows[1]
        projection = await CapacityService(db).projection(scenario.profile, *HISTORY)
        # Only the seeded first-iteration work holds these days; the postponed baseline adds nothing.
        committed = {row["date"]: row["committed_effort_hours"] for row in projection["days"]}
        postponed = await db.get(Task, postponed_id)
        postponed.status = "planned"
        await db.commit()
        with_planned = await CapacityService(db).projection(scenario.profile, *HISTORY)
        assert sum(row["committed_effort_hours"] for row in with_planned["days"]) == pytest.approx(
            sum(committed.values()) + 16)
        planned_workload = await TeamService(db).get_workload(member_id)
        postponed.status = "postponed"
        await db.commit()
        workload = await TeamService(db).get_workload(member_id)
        assert planned_workload.allocated_days - workload.allocated_days == pytest.approx(2)


def _readiness(task, dependencies=()):
    return evaluate_agent_readiness(task, tags=["agent", "cap:backend-python"], children=[], dependencies=list(dependencies))


def test_readiness_names_postponed_as_the_blocker_and_waits_dependents_on_it_by_name():
    stopped = Task(id=41, title="Vendor integration", status="postponed", iteration_id=1, assignee_id=1,
                   start_date=HISTORY[0], end_date=HISTORY[1], priority=5, effort_days=1, effort_hours=8)
    readiness = _readiness(stopped)
    status = next(item for item in readiness.criteria if item.key == "status")
    assert readiness.is_ready is False and status.passed is False
    assert "Task is postponed" in status.reason and status.reason in readiness.blockers

    dependent = Task(id=42, title="Vendor dashboard", status="planned", iteration_id=1, assignee_id=1,
                     start_date=HISTORY[0], end_date=HISTORY[1], priority=5, effort_days=1, effort_hours=8)
    edge = TaskDependency(task_id=42, depends_on_id=41, depends_on=stopped)
    readiness = _readiness(dependent, [edge])
    dependencies = next(item for item in readiness.criteria if item.key == "dependencies")
    assert dependencies.passed is False and "dependencies" in readiness.blocker_codes
    assert dependencies.reason == "Waiting on postponed task 'Vendor integration' (ID 41) until it is reactivated."


async def test_dispatch_never_offers_or_assigns_postponed_work(db_session, profile_factory, actor_factory,
                                                               team_member_factory, task_factory):
    pm, worker, task, _, _ = await _routing_fixture(db_session, profile_factory, actor_factory, team_member_factory, task_factory)
    task.status = "postponed"
    await db_session.commit()
    task_id, version, worker_id = task.id, task.version, worker.id
    pipeline = await AgentService(db_session).get_pipeline()
    assert task_id not in {item.id for column in pipeline.values() for item in column}
    service = AgentWorkService(db_session, rollout_service=_rollout("shadow"))
    for purpose in ("execution", "verification"):
        await db_session.refresh(pm)
        with pytest.raises(AgentConflictError, match="postponed"):
            await service.create_assignment(pm, AgentTaskAssignmentCreate(
                task_id=task_id, actor_id=worker_id, purpose=purpose, expected_task_version=version),
                idempotency_key=f"postponed-{purpose}", rationale="Assign stopped work", correlation_id=f"postponed-{purpose}")
        await db_session.rollback()


async def test_no_verifier_can_be_selected_for_postponed_work():
    task = Task(id=7, title="Stopped review", status="postponed", project_id=None)
    with pytest.raises(AgentRoutingConflictError) as refused:
        await select_reviewer(None, task, [], None)
    assert refused.value.code == "task_postponed"


def test_postponed_task_raises_no_schedule_signal():
    task = Task(id=9, title="Stopped", status="postponed", start_date=date(2026, 1, 5), end_date=date(2026, 1, 6))
    signals = task_signals(task, iteration_end=date(2026, 1, 5), project_target=date(2026, 1, 5),
                           now=None, effective_flags={"effective_is_deferred": False, "effective_is_optional": False})
    assert not any(signals[key] for key in ("is_late_start", "is_overdue", "is_iteration_overflow", "is_project_target_overflow"))


def test_leaf_metrics_count_postponed_apart_from_other_statuses():
    tasks = [Task(id=index, title=status, status=status, effort_days=1, effort_hours=8)
             for index, status in enumerate(("planned", "active", "resolved", "closed", "postponed"), start=1)]
    metrics = leaf_metrics(tasks)
    assert metrics["tasks_by_status"] == {"planned": 1, "active": 1, "resolved": 1, "closed": 1, "postponed": 1}
    assert metrics["postponed_tasks"] == 1 and metrics["total_tasks"] == 5
    # Postponed effort is neither planned, remaining nor done: 4 planned days, 2 remaining, 2 done.
    assert metrics["total_effort_days"] == 4 and metrics["required_effort_days"] == 4
    assert metrics["remaining_effort_days"] == 2
    assert metrics["total_effort_days"] - metrics["remaining_effort_days"] == 2


async def test_iteration_and_release_progress_count_postponed_separately(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, postponed_id, planned_id, dependent_id = await _postponed_plan(db, scenario)
        metrics = await aggregate_metrics(db, iteration_id=iteration_id)
        assert metrics["status_counts"] == {"planned": 3, "active": 0, "resolved": 0, "closed": 0, "postponed": 1}
        assert metrics["postponed_tasks"] == 1 and metrics["total_tasks"] == 4
        # Its old dates are in the past, but postponed work is not overdue and does not set the finish.
        assert metrics["overdue_tasks"] == 0 and metrics["task_end_date"] is None
        # Its two days of effort are neither planned nor done; nothing has started, so nothing is done.
        assert metrics["total_effort_days"] == pytest.approx(3) and metrics["remaining_effort_days"] == pytest.approx(3)
        # Only the dependent counts as blocked; the postponed task is not also blocked or unestimated.
        assert metrics["blocked_tasks"] == 1 and metrics["unknown_estimate_tasks"] == 0
        listed = await aggregate_metrics(db, iteration_id=iteration_id, matching="postponed")
        assert [item["id"] for item in listed["items"]] == [postponed_id]

        summary = await IterationService(db).get_summary(iteration_id)
        assert summary.postponed_tasks == 1 and summary.status_counts["postponed"] == 1

        release = Release(project_id=scenario.projects[1], name="Vendor release", target_date=date(2026, 1, 2))
        release.tasks = list((await db.scalars(select(Task).where(Task.id.in_([postponed_id, planned_id])))).all())
        db.add(release)
        await db.commit()
        loaded = await ReleaseService(db).get_by_id(release.id)
        assert loaded.postponed_tasks == 1 and loaded.status_counts == {
            "planned": 1, "active": 0, "resolved": 0, "closed": 0, "postponed": 1}
        assert loaded.target_overflow_tasks == 0


async def test_dependent_with_saved_dates_and_its_own_cause_keeps_dates_and_waits_on_postponed_work(
        delivery_store, january_today):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, postponed_id, _, dependent_id = await _postponed_plan(db, scenario)
        dependent = await db.get(Task, dependent_id)
        dependent.start_date, dependent.end_date = date(2026, 1, 12), date(2026, 1, 13)
        dependent.effort_hours = dependent.effort_days = None
        blocked = Task(title="Blocked vendor report", status="planned", priority=1, iteration_id=iteration_id,
                       project_id=scenario.projects[1], assignee_id=scenario.capacity_rows[1], effort_days=1,
                       effort_hours=8, blocked_reason="Waiting for access")
        db.add(blocked)
        await db.flush()
        blocked_id = blocked.id
        db.add(TaskDependency(task_id=blocked_id, depends_on_id=postponed_id))
        await db.commit()
        result = (await SchedulerService(db).schedule_iteration(iteration_id)).model_dump(mode="json")
    kept = {item["task_id"]: item for item in result["kept_dates"]}
    # The postponed wait is the primary reason; the missing estimate is reported beside it.
    assert kept[dependent_id]["reason"] == "predecessor_postponed"
    assert kept[dependent_id]["also"] == ["no_estimate"]
    assert kept[dependent_id]["waiting_on"] == [{"task_id": postponed_id, "task_title": "Vendor integration"}]
    assert (kept[dependent_id]["start_date"], kept[dependent_id]["end_date"]) == ("2026-01-12", "2026-01-13")
    assert "Waiting on postponed task 'Vendor integration'" in kept[dependent_id]["message"]
    assert "positive effort estimate" in kept[dependent_id]["message"]
    unscheduled = {item["task_id"]: item for item in result["unscheduled"]}
    assert unscheduled[blocked_id]["reason"] == "predecessor_postponed"
    assert unscheduled[blocked_id]["also"] == ["blocked"]


async def test_dependency_on_a_summary_waits_on_its_postponed_child(delivery_store, january_today):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, member_id = scenario.iterations[1], scenario.capacity_rows[1]
        common = dict(iteration_id=iteration_id, project_id=scenario.projects[1], priority=1)
        summary = Task(title="Vendor rollout", status="planned", **common)
        db.add(summary)
        await db.flush()
        leaf = dict(common, assignee_id=member_id, effort_days=1, effort_hours=8, parent_id=summary.id)
        running = Task(title="Vendor contract", status="planned", **leaf)
        stopped = Task(title="Vendor sandbox", status="postponed", start_date=HISTORY[0], end_date=HISTORY[1], **leaf)
        dependent = Task(title="Vendor launch", status="planned", assignee_id=member_id, effort_days=1,
                         effort_hours=8, **common)
        db.add_all([running, stopped, dependent])
        await db.flush()
        db.add(TaskDependency(task_id=dependent.id, depends_on_id=summary.id))
        await db.commit()
        ids = (running.id, stopped.id, dependent.id)
        result = (await SchedulerService(db).schedule_iteration(iteration_id)).model_dump(mode="json")
    running_id, stopped_id, dependent_id = ids
    unscheduled = {item["task_id"]: item for item in result["unscheduled"]}
    # The summary's planned child is scheduled, but the dependent does not start after it alone.
    assert unscheduled[dependent_id]["reason"] == "predecessor_postponed"
    assert unscheduled[dependent_id]["waiting_on"] == [{"task_id": stopped_id, "task_title": "Vendor sandbox"}]
    assert running_id not in unscheduled
    async with factory() as db:
        rows = {row.id: row for row in (await db.scalars(select(Task).where(Task.id.in_(ids)))).all()}
        assert rows[running_id].start_date is not None and rows[dependent_id].start_date is None


def test_readiness_names_postponed_work_below_a_summary_prerequisite():
    stopped = Task(id=51, title="Vendor sandbox", status="postponed", is_deferred=False)
    running = Task(id=52, title="Vendor contract", status="planned", is_deferred=False)
    summary = Task(id=50, title="Vendor rollout", status="planned", is_deferred=False)
    summary.children = [running, stopped]
    dependent = Task(id=53, title="Vendor launch", status="planned", iteration_id=1, assignee_id=1,
                     start_date=HISTORY[0], end_date=HISTORY[1], priority=5, effort_days=1, effort_hours=8)
    readiness = _readiness(dependent, [TaskDependency(task_id=53, depends_on_id=50, depends_on=summary)])
    dependencies = next(item for item in readiness.criteria if item.key == "dependencies")
    assert dependencies.passed is False
    assert dependencies.reason == "Waiting on postponed task 'Vendor sandbox' (ID 51) until it is reactivated."
