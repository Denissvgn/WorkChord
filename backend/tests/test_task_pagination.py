"""Keyset coverage, mutation semantics and permission-bounded history reads."""
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import delete

from app.models.agent import TaskEvent
from app.models.task import Task
from app.services.agent_service import AgentService
from app.services.task_detail_service import TaskDetailService
from app.services.task_timeline_service import TaskTimelineService
from app.query_limits import CollectionLimitExceededError
from tests.test_delivery_scenarios import delivery_store


@pytest.mark.parametrize("size", [501, 2501])
async def test_large_reference_pages_are_complete_and_filtered(delivery_store, size):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        tasks = [Task(title=f"Paged {i}", project_id=scenario.projects[0], status="planned") for i in range(size)]
        db.add_all(tasks)
        await db.commit()
        expected = {t.id for t in tasks}
        seen = []
        after = 0
        service = TaskDetailService(db)
        while True:
            page = await service.lookup(project_id=scenario.projects[0], query="Paged ", status="planned", limit=100, after_id=after)
            assert len(page.items) <= 100 and page.consistency == "live"
            seen.extend(item.id for item in page.items)
            if not page.has_more:
                break
            assert page.next_after_id > after
            after = page.next_after_id
        assert len(seen) == len(set(seen)) == size and set(seen) == expected


async def test_live_page_mutations_keep_ids_monotonic_and_scope_isolated(delivery_store):
    from app.authority import Authority
    factory, scenario, _ = delivery_store
    async with factory() as db:
        tasks = [Task(title=f"Cursor {i}", project_id=scenario.projects[0], status="planned") for i in range(5)]
        foreign = Task(title="Cursor foreign", project_id=scenario.projects[1], status="planned")
        db.add_all([*tasks, foreign]);await db.commit()
        db.info["authority"] = Authority(1, "human", projects={scenario.projects[0]: "viewer"})
        service = TaskDetailService(db)
        first = await service.lookup(query="Cursor", limit=2)
        assert [item.id for item in first.items] == [tasks[0].id, tasks[1].id]
        # Filter changes behind the cursor are visible after an explicit refresh.
        db.info.pop("authority")
        tasks[0].status = "active"
        await db.delete(tasks[2])
        inserted = Task(title="Cursor new", project_id=scenario.projects[0]);db.add(inserted)
        await db.commit()
        db.info["authority"] = Authority(1, "human", projects={scenario.projects[0]: "viewer"})
        next_page = await service.lookup(query="Cursor", limit=100, after_id=first.next_after_id)
        assert [item.id for item in next_page.items] == [tasks[3].id, tasks[4].id, inserted.id]
        assert foreign.id not in [item.id for item in next_page.items]
        assert (await service.lookup(query="Cursor", status="active")).items[0].id == tasks[0].id


async def test_history_pages_ties_and_legacy_bound(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task_id = scenario.tasks["planned"]
        at = datetime(2026, 1, 1, tzinfo=UTC)
        events = [TaskEvent(task_id=task_id, event_type="observed", created_at=at, payload="{}") for _ in range(501)]
        db.add_all(events);await db.commit()
        service = TaskTimelineService(db)
        seen = []
        cursor = None
        while True:
            page = await service.page(task_id, limit=50, cursor=cursor)
            seen.extend(item["event_key"] for item in page["items"])
            if not page["has_more"]:break
            cursor = page["next_cursor"]
        assert len(seen) == len(set(seen)) and {f"0:{e.id}" for e in events} <= set(seen)
        with pytest.raises(CollectionLimitExceededError):await AgentService(db).get_task_timeline(task_id)
        with pytest.raises(ValueError, match="cursor"):
            await service.page(scenario.tasks["active"], cursor=cursor)
        with pytest.raises(ValueError, match="cursor"):
            await service.page(task_id, cursor="bad")


async def test_scope_pages_hold_an_insert_boundary_and_summary_counts_are_complete(delivery_store):
    from app.models.project import Project
    from app.services.project_service import ProjectService
    from app.services.iteration_service import IterationService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        projects = [Project(name=f"Scope {i}") for i in range(501)]
        db.add_all(projects);await db.commit()
        service = ProjectService(db)
        first = await service.project_page(limit=100)
        inserted = Project(name="Later scope");db.add(inserted);await db.commit()
        seen = [item.id for item in first["items"]]
        page = first
        while page["has_more"]:
            page = await service.project_page(limit=100, after_id=page["next_after_id"], upper_id=first["upper_id"])
            seen.extend(item.id for item in page["items"])
        assert len(seen) == len(set(seen)) and inserted.id not in seen
        assert {item.id for item in projects} <= set(seen)
        summaries = await service.portfolio_page(limit=100, upper_id=first["upper_id"])
        assert len(summaries["items"]) == 100 and summaries["has_more"]
        iterations = await IterationService(db).id_page(limit=1)
        assert len(iterations["items"]) == 1 and iterations["has_more"]
        # Summary totals are SQL aggregates, not sums of a loaded display page.
        task_rows = [Task(title="Large summary", project_id=scenario.projects[0]) for _ in range(2501)]
        db.add_all(task_rows);await db.commit()
        summary = await service.get_summary(scenario.projects[0])
        assert summary.total_tasks >= 2501


async def test_mixed_timeline_sources_have_stable_ties_and_actor_provenance(delivery_store):
    from app.models.agent import AgentRun, AgentRunEvent
    from app.models.task_status_log import TaskStatusLog
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task_id = scenario.tasks["planned"]
        at = datetime(2026, 1, 1, tzinfo=UTC)
        run = AgentRun(task_id=task_id, actor_id=scenario.actors[0], status="succeeded", started_at=at)
        db.add(run);await db.flush()
        db.add_all([TaskEvent(task_id=task_id, event_type="observed", created_at=at),
            TaskStatusLog(task_id=task_id, from_status="planned", to_status="active", changed_at=at),
            AgentRunEvent(run_id=run.id, event_type="checkpoint", created_at=at)])
        await db.commit()
        items = []
        cursor = None
        while True:
            page = await TaskTimelineService(db).page(task_id, limit=2, cursor=cursor)
            items.extend(page["items"])
            if not page["has_more"]:break
            cursor=page["next_cursor"]
        tied = [item for item in items if item["timestamp"] == at]
        assert [item["item_type"] for item in tied] == ["agent_run_event", "agent_run", "status_log", "task_event"]
        assert tied[0]["actor_id"] == tied[1]["actor_id"] == scenario.actors[0]
        assert len({item["event_key"] for item in items}) == len(items)


async def test_oversized_reads_reject_before_relationship_or_history_hydration(delivery_store, monkeypatch):
    from app.services.task_hierarchy_service import TaskHierarchyService
    from app.services.task_service import TaskService
    from app.services.delivery_metrics_service import DeliveryMetricsService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        db.add_all([Task(title="Oversized read", project_id=scenario.projects[0], iteration_id=scenario.iterations[0]) for _ in range(2501)])
        await db.commit()
        def forbidden(*_args, **_kwargs):raise AssertionError("Hydration preceded the bound check")
        monkeypatch.setattr(TaskHierarchyService, "_task_graph_query", forbidden)
        with pytest.raises(CollectionLimitExceededError):await TaskService(db).get_by_iteration(scenario.iterations[0])
        monkeypatch.setattr(DeliveryMetricsService, "_window_observations", forbidden)
        with pytest.raises(CollectionLimitExceededError):await DeliveryMetricsService(db).report(project_id=scenario.projects[0])
