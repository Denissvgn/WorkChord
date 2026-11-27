"""Canceled and superseded work is shown and counted as terminal, never under the status it kept."""

from datetime import date, timedelta
from types import SimpleNamespace

import httpx
import pytest

from app import mcp_agent_tools
from app.main import app
from app.models.release import Release, release_tasks
from app.models.task import Task
from app.models.task_replacement import TaskReplacement
from app.services.agent_service import AgentService
from app.services.delivery_metrics_service import DeliveryMetricsService, summarize_observations
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.release_service import ReleaseService
from app.services.work_metrics import aggregate_metrics, leaf_metrics
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_supersession import _client, _scenario, _supersede

__all__ = ["delivery_store"]

STORED = ("planned", "active", "resolved", "closed", "postponed")


async def _cancel(client, task):
    response = await client.post(f"/api/tasks/{task.id}/commands", json={
        "action": "cancel", "expected_version": task.version, "reason": "No longer needed"})
    assert response.status_code == 200, response.text
    return response.json()


async def _withdrawn_scenario(factory, scenario):
    """A resolved original superseded by closed work, an active task canceled, and a replaced planned task."""
    async with factory() as db:
        s = await _scenario(db, scenario, successor_state="closed")
        active = await db.get(Task, scenario.tasks["active"])
        replaced = Task(title="Replaced original", project_id=scenario.projects[0], iteration_id=scenario.iterations[0],
                        status="planned", effort_hours=8)
        db.add(replaced)
        await db.flush()
        active_ref = SimpleNamespace(id=active.id, version=active.version)
        await db.commit()
    async with factory() as db:
        before = {"iteration": await aggregate_metrics(db, iteration_id=scenario.iterations[0]),
                  "project": await aggregate_metrics(db, project_id=scenario.projects[0])}
    async with _client() as client:
        assert (await client.post(f"/api/tasks/{s.original.id}/supersession",
                                  json=_supersede(s.original, s.successor))).status_code == 201
        canceled = await _cancel(client, active_ref)
    async with factory() as db:
        # A clean replacement is recorded with its own row: the original is withdrawn as superseded too.
        replaced = await db.get(Task, replaced.id)
        replaced.canceled_at = utc_now()
        db.add(TaskReplacement(project_id=scenario.projects[0], original_task_id=replaced.id,
                               replacement_task_id=scenario.tasks["planned"], disposition="replacement", reason="Unknown publisher",
                               owner_decision="Owner approved", base_commit_url="https://github.com/example/project/commit/" + "0" * 40,
                               carried_run_ids=[], moved_dependencies=[], moved_release_ids=[],
                               original_snapshot={}, review_policy={}, decided_at=utc_now()))
        await db.commit()
        return s, active_ref.id, replaced.id, canceled, before


async def test_task_response_carries_the_displayed_state_and_successor(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, replaced_id, canceled, _ = await _withdrawn_scenario(factory, scenario)
    assert canceled["displayed_state"] == "canceled" and canceled["status"] == "active"
    assert canceled["successor_task_id"] is None and canceled["successor_kind"] is None
    async with _client() as client:
        superseded = (await client.get(f"/api/tasks/{s.original.id}")).json()
        stored_canceled = (await client.get(f"/api/tasks/{canceled_id}")).json()
        replaced = (await client.get(f"/api/tasks/{replaced_id}")).json()
        live = (await client.get(f"/api/tasks/{s.successor.id}")).json()
        tree = (await client.get(f"/api/iterations/{scenario.iterations[0]}/tasks")).json()
    # The stored status is untouched; the displayed state is derived.
    assert (superseded["status"], superseded["displayed_state"]) == ("resolved", "superseded")
    assert (superseded["successor_task_id"], superseded["successor_kind"]) == (s.successor.id, "supersession")
    assert (stored_canceled["status"], stored_canceled["displayed_state"]) == ("active", "canceled")
    # A replaced original is labelled superseded, with the replacement as its successor.
    assert (replaced["displayed_state"], replaced["successor_task_id"], replaced["successor_kind"]) == (
        "superseded", scenario.tasks["planned"], "replacement")
    assert (live["displayed_state"], live["successor_task_id"]) == ("closed", None)
    by_id = {item["id"]: item for item in tree}
    assert by_id[canceled_id]["displayed_state"] == "canceled" and by_id[s.original.id]["displayed_state"] == "superseded"
    async with factory() as db:
        assert (await db.get(Task, s.original.id)).status == "resolved"


async def test_iteration_project_and_milestone_counts_report_terminal_work_apart(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, replaced_id, _, before = await _withdrawn_scenario(factory, scenario)
    async with factory() as db:
        for name, summary in (("iteration", await IterationService(db).get_summary(scenario.iterations[0])),
                              ("project", await ProjectService(db).get_summary(scenario.projects[0]))):
            counts, earlier = summary.status_counts, before[name]["status_counts"]
            assert (summary.canceled_tasks, summary.superseded_tasks) == (1, 2)
            assert (counts["canceled"], counts["superseded"]) == (1, 2)
            # The original was resolved, the canceled task active and the replaced one planned: each count falls by one.
            assert counts["resolved"] == earlier["resolved"] - 1 and counts["active"] == earlier["active"] - 1
            assert counts["planned"] == earlier["planned"] - 1 and counts["closed"] == earlier["closed"]
            assert summary.total_tasks == before[name]["total_tasks"] - 3
            assert sum(counts[state] for state in STORED) == summary.total_tasks
        groups = (await ProjectService(db).get_summary(scenario.projects[0])).milestone_groups
        assert sum(group.canceled_tasks + group.superseded_tasks for group in groups) == 3
        # Other projects see none of it.
        other = await aggregate_metrics(db, project_id=scenario.projects[1])
        assert (other["canceled_tasks"], other["superseded_tasks"]) == (0, 0)
        portfolio = {item.project_id: item for item in await ProjectService(db)._portfolio_summaries(
            [await ProjectService(db).get_by_id(scenario.projects[0])])}
        assert (portfolio[scenario.projects[0]].canceled_tasks, portfolio[scenario.projects[0]].superseded_tasks) == (1, 2)


async def test_metric_matches_open_the_terminal_counts(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, replaced_id, _, _ = await _withdrawn_scenario(factory, scenario)
    async with _client() as client:
        for metric, expected in (("canceled", {canceled_id}), ("superseded", {s.original.id, replaced_id})):
            page = (await client.get("/api/tasks/metric-matches", params={"metric": metric, "iteration_id": scenario.iterations[0]})).json()
            assert {item["id"] for item in page["items"]} == expected
            assert {item["displayed_state"] for item in page["items"]} == {metric}
        resolved = (await client.get("/api/tasks/metric-matches", params={"metric": "resolved", "iteration_id": scenario.iterations[0]})).json()
        assert s.original.id not in {item["id"] for item in resolved["items"]}


async def test_status_filters_keep_working_and_terminal_states_can_be_selected(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, replaced_id, _, _ = await _withdrawn_scenario(factory, scenario)
    project = scenario.projects[0]
    async with _client() as client:
        async def ids(state, **extra):
            response = await client.get("/api/tasks/lookup", params={"project_id": project, "task_status": state, "limit": 100, **extra})
            assert response.status_code == 200, response.text
            return {item["id"]: item for item in response.json()["items"]}
        assert set(await ids("canceled")) == {canceled_id}
        superseded = await ids("superseded")
        assert set(superseded) == {s.original.id, replaced_id}
        assert superseded[s.original.id]["status"] == "resolved" and superseded[s.original.id]["displayed_state"] == "superseded"
        # A status filter no longer returns withdrawn work under the status it kept.
        assert s.original.id not in await ids("resolved") and canceled_id not in await ids("active")
        assert scenario.tasks["closed_urgent"] in await ids("closed")
        assert s.waiting.id in await ids("postponed")
        assert (await client.get("/api/tasks/lookup", params={"project_id": project, "task_status": "cancelled"})).status_code == 422
        # The project task list takes the same filter, flat and at any depth.
        listed = await client.get(f"/api/projects/{project}/tasks", params={"status": "superseded"})
        assert {item["id"] for item in listed.json()} == {s.original.id, replaced_id}
        assert {item["displayed_state"] for item in listed.json()} == {"superseded"}
        assert {item["id"] for item in (await client.get(f"/api/projects/{project}/tasks", params={"status": "canceled"})).json()} == {canceled_id}
        assert (await client.get(f"/api/projects/{project}/tasks", params={"status": "bogus"})).status_code == 422
        roots = (await client.get(f"/api/projects/{project}/tasks")).json()
        assert {item["id"] for item in roots} >= {s.original.id, canceled_id}
    async with factory() as db:
        for state, expected in (("canceled", {canceled_id}), ("superseded", {s.original.id, replaced_id})):
            listed = await mcp_agent_tools.list_project_tasks(db, project, state)
            assert {item["id"] for item in listed} == expected
            assert {item["displayed_state"] for item in listed} == {state}
        with pytest.raises(ValueError):
            await mcp_agent_tools.list_project_tasks(db, project, "cancelled")
        assert {item["id"] for item in await mcp_agent_tools.list_project_tasks(db, project)} >= {s.original.id}


async def test_release_progress_counts_withdrawn_work_in_its_own_buckets(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, _, _, _ = await _withdrawn_scenario(factory, scenario)
    async with factory() as db:
        # A canceled release keeps listing the superseded original (membership moves only for live releases).
        release = await ReleaseService(db).get_by_id(s.releases["canceled"])
        assert release.superseded_tasks == 1 and release.canceled_tasks == 0
        assert release.status_counts["resolved"] == 0 and release.total_tasks == 0
        assert [(task.id, task.status, task.displayed_state) for task in release.tasks] == [(s.original.id, "resolved", "superseded")]
        await db.execute(release_tasks.insert().values(release_id=release.id, task_id=canceled_id, created_at=utc_now()))
        await db.commit()
    async with factory() as db:
        release = await ReleaseService(db).get_by_id(s.releases["canceled"])
        assert (release.canceled_tasks, release.superseded_tasks) == (1, 1)
        assert release.status_counts["active"] == 0 and release.completed_tasks == 0
        assert release.target_overflow_tasks == 0
    async with _client() as client:
        body = (await client.get(f"/api/projects/{scenario.projects[0]}/releases")).json()
        canceled_release = next(item for item in body if item["id"] == s.releases["canceled"])
        assert (canceled_release["canceled_tasks"], canceled_release["superseded_tasks"]) == (1, 1)
        assert {task["displayed_state"] for task in canceled_release["tasks"]} == {"canceled", "superseded"}


async def test_release_target_overflow_ignores_canceled_work(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        release = Release(name="Dated", project_id=scenario.projects[0], status="planned", target_date=date(2026, 1, 10))
        db.add(release)
        await db.flush()
        task = await db.get(Task, scenario.tasks["planned"])
        task.end_date = date(2026, 1, 20)
        await db.execute(release_tasks.insert().values(release_id=release.id, task_id=task.id, created_at=utc_now()))
        await db.commit()
        assert (await ReleaseService(db).get_by_id(release.id)).target_overflow_tasks == 1
        task.canceled_at = utc_now()
        await db.commit()
        assert (await ReleaseService(db).get_by_id(release.id)).target_overflow_tasks == 0


async def test_agent_pipeline_and_ready_tasks_skip_withdrawn_work(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        resolved = await db.get(Task, scenario.tasks["resolved"])
        planned = await db.get(Task, scenario.tasks["planned"])
        before = await AgentService(db).get_pipeline()
        assert resolved.id in {task.id for task in before["verification_required"]}
        resolved.canceled_at = planned.canceled_at = utc_now()
        await db.commit()
        pipeline = await AgentService(db).get_pipeline()
        listed = {task.id for stage in pipeline.values() for task in stage}
        assert resolved.id not in listed and planned.id not in listed
        # Everything else is still offered.
        assert {task.id for stage in before.values() for task in stage} - listed == {resolved.id, planned.id}


async def test_delivery_analytics_counts_superseded_work_apart_from_canceled(delivery_store):
    factory, scenario, _ = delivery_store
    s, canceled_id, replaced_id, _, _ = await _withdrawn_scenario(factory, scenario)
    async with factory() as db:
        report = await DeliveryMetricsService(db).report(project_id=scenario.projects[0], lookback_days=30,
                                                         now=utc_now() + timedelta(minutes=5))
        assert report.canceled_leaf_tasks == 1 and report.superseded_leaf_tasks == 1
        assert report.coverage["current_canceled_leaf_tasks"] == 1 and report.coverage["current_superseded_leaf_tasks"] == 2
        assert s.original.id not in {item.task_id for item in report.review_queue}


def test_summarize_observations_never_counts_one_task_as_both_canceled_and_superseded():
    start = utc_now()
    rows = [SimpleNamespace(id=index, original_task_id=7, kind=kind, observed_at=start + timedelta(seconds=index))
            for index, kind in enumerate(("canceled", "replaced"), start=1)]
    rows.append(SimpleNamespace(id=3, original_task_id=8, kind="canceled", observed_at=start + timedelta(seconds=3)))
    result = summarize_observations(rows, start - timedelta(days=1), start + timedelta(days=1))
    assert (result["canceled_leaf_tasks"], result["superseded_leaf_tasks"]) == (1, 1)


def test_leaf_metrics_counts_terminal_leaves_apart_from_every_status():
    def task(index, status, *, canceled, successor=None):
        item = Task(id=index, title=status, status=status, effort_days=1, effort_hours=8,
                    canceled_at=utc_now() if canceled else None)
        item.__dict__["successor_task_id"] = successor
        return item
    metrics = leaf_metrics([task(1, "planned", canceled=False), task(2, "resolved", canceled=True),
                            task(3, "active", canceled=True, successor=1), task(4, "closed", canceled=True)])
    assert metrics["total_tasks"] == 1 and metrics["tasks_by_status"]["planned"] == 1
    assert (metrics["canceled_tasks"], metrics["superseded_tasks"]) == (2, 1)
    assert (metrics["tasks_by_status"]["canceled"], metrics["tasks_by_status"]["superseded"]) == (2, 1)
    assert metrics["tasks_by_status"]["resolved"] == metrics["tasks_by_status"]["active"] == 0
    assert metrics["implemented_tasks"] == 0 and metrics["total_effort_days"] == 1


def test_canceled_planned_work_is_no_planning_gap():
    from app.services.planning_issues import missing_effort, needs_assignee
    planned = SimpleNamespace(status="planned", canceled_at=None, is_deferred=False, is_composite=False, children=[],
                              assignee=None, agent_working=False, effort_days=None)
    assert needs_assignee(planned) and missing_effort(planned)
    planned.canceled_at = utc_now()
    assert not needs_assignee(planned) and not missing_effort(planned)


async def test_queries_joining_the_replacement_table_still_compile_and_run(delivery_store):
    from sqlalchemy import select
    from app.services.task_display_state import task_state_clause
    factory, scenario, _ = delivery_store
    s, _, replaced_id, _, _ = await _withdrawn_scenario(factory, scenario)
    async with factory() as db:
        joined = select(Task).join(TaskReplacement, TaskReplacement.original_task_id == Task.id)
        str(joined.compile())
        rows = list((await db.scalars(joined.where(task_state_clause("superseded")).order_by(Task.id))).all())
        assert {task.id for task in rows} == {s.original.id, replaced_id}
        assert {task.successor_kind for task in rows} == {"supersession", "replacement"}
        # A live task has no successor to probe for.
        live = await db.get(Task, scenario.tasks["closed_low"])
        assert live.successor_task_id is None and live.displayed_state == "closed"
