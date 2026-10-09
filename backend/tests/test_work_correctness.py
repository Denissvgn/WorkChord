"""Atomic recovery, hierarchy, aggregate versions and cross-surface metric contracts."""

from datetime import datetime, timezone

import httpx
import pytest
from sqlalchemy import func, select

from app.authority import Authority
from app.commands import command_transaction
from app.config import get_settings
from app.main import app
from app.models.identity import Principal
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot, TaskScheduleBaseline
from app.models.task import Task, TaskDependency
from app.schemas.task import TaskUpdate
from app.services.hierarchy_repair_service import HierarchyRepairService
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.scheduler_service import SchedulerService
from app.services.snapshot_service import SnapshotService
from app.services.task_service import TaskService
from app.services.work_metrics import aggregate_metrics, leaf_metrics, working_today
from tests.test_delivery_scenarios import delivery_store


async def test_snapshot_restores_exact_allocation_membership(delivery_store):
    from app.models.team_member import TeamMember, TeamMemberProfile
    from app.schemas.team import TeamMemberCreate
    from app.services.team_service import TeamService

    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    async with factory() as db:
        saved_ids = set((await db.scalars(select(TeamMember.id).where(TeamMember.iteration_id == iteration_id))).all())
        snapshot = await SnapshotService(db).create_snapshot(iteration_id, "before_allocation")
        profile = TeamMemberProfile(display_name="Later owner", profile_kind="human")
        db.add(profile)
        await db.commit()
        profile_id = profile.id
        added = await TeamService(db).create(iteration_id, TeamMemberCreate(
            name="Later allocation", position="Engineer", profile_id=profile_id))
        added_id = added.id
        await SnapshotService(db).restore(iteration_id, snapshot)
    async with factory() as db:
        restored_ids = set((await db.scalars(select(TeamMember.id).where(TeamMember.iteration_id == iteration_id))).all())
        assert restored_ids == saved_ids
        added = await db.get(TeamMember, added_id)
        assert added is not None and added.iteration_id is None
        assert await db.get(TeamMemberProfile, profile_id) is not None


async def test_project_creation_round_trip_preserves_working_timezone(delivery_store):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/projects", json={"name": "Tokyo planning", "timezone": "Asia/Tokyo"})
        assert response.status_code == 201, response.text
        response = await client.get(f"/api/projects/{response.json()['id']}")
        assert response.status_code == 200, response.text
        assert response.json()["timezone"] == "Asia/Tokyo"


async def test_calendar_creation_round_trip_preserves_short_day_capacity(delivery_store):
    from datetime import date
    from app.models.calendar import Calendar
    from app.services.capacity_service import day_hours

    factory, _, _ = delivery_store
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/calendars", json={"name": "Reduced day", "year": 2026,
            "nominal_day_hours": 8, "short_days": ["2026-12-24"]})
        assert response.status_code == 201, response.text
        calendar_id = response.json()["id"]
        response = await client.get(f"/api/calendars/{calendar_id}")
        assert response.status_code == 200, response.text
        assert response.json()["short_days"] == ["2026-12-24"]
    async with factory() as db:
        calendar = await db.get(Calendar, calendar_id)
        assert day_hours(calendar, date(2026, 12, 24)) == 7
        assert day_hours(calendar, date(2026, 12, 23)) == 8


async def test_merge_failure_preserves_every_task_and_recovery_point(delivery_store, monkeypatch):
    factory, scenario, snapshots = delivery_store
    async with factory() as db:
        before = [(task.id, task.parent_id, task.version) for task in (await db.scalars(select(Task).order_by(Task.id))).all()]
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        service = TaskService(db)
        async def fail(*_args, **_kwargs):
            raise RuntimeError("Injected failure after parent creation")
        monkeypatch.setattr(service, "record_task_event", fail)
        with pytest.raises(RuntimeError, match="Injected failure"):
            await service.merge_tasks(scenario.iterations[0], [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]], "Combined")
    async with factory() as db:
        assert [(task.id, task.parent_id, task.version) for task in (await db.scalars(select(Task).order_by(Task.id))).all()] == before
        assert (await db.get(Iteration, scenario.iterations[0])).revision == revision
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == 0
    assert not list(snapshots.rglob("*"))


@pytest.mark.parametrize(("states", "expected"), [(("closed", "closed"), "closed"), (("resolved", "closed"), "resolved"), (("planned", "active"), "active")])
async def test_merge_truth_and_leaf_totals_are_stable(delivery_store, states, expected):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        ids = [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]]
        for task_id, state in zip(ids, states):
            (await db.get(Task, task_id)).status = state
        await db.commit()
        before = await aggregate_metrics(db, project_id=scenario.projects[0])
        parent = await TaskService(db).merge_tasks(scenario.iterations[0], ids, "Combined")
        assert parent.status == expected
        assert parent.priority == 1
        assert parent.is_summary
        after = await aggregate_metrics(db, project_id=scenario.projects[0])
        for field in ["total_tasks", "implemented_tasks", "accepted_tasks", "total_effort_days", "completion_percent"]:
            assert after[field] == before[field], field


async def test_unmerge_preserves_child_ids_and_rejects_referenced_parent(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        ids = [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]]
        parent = await service.merge_tasks(scenario.iterations[0], ids, "Combined")
        parent_id = parent.id
        db.add(TaskDependency(task_id=scenario.tasks["planned"], depends_on_id=parent.id))
        await db.commit()
        with pytest.raises(ValueError, match="referenced summary"):
            await service.unmerge_task(parent_id)
        dependency = await db.scalar(select(TaskDependency).where(TaskDependency.depends_on_id == parent_id))
        await db.delete(dependency)
        await db.commit()
        children = await service.unmerge_task(parent_id)
        assert {task.id for task in children} == set(ids)
        assert all(task.parent_id is None for task in children)
        assert await db.get(Task, parent_id) is None


async def test_failed_command_cannot_evict_old_snapshots(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    monkeypatch.setenv("SNAPSHOT_RETENTION_COUNT", "2")
    get_settings.cache_clear()
    try:
        async with factory() as db:
            service = SnapshotService(db)
            for index in range(2):
                await service.create_snapshot(scenario.iterations[0], f"saved_{index}")
            before = await service.list_snapshots(scenario.iterations[0])
            with pytest.raises(RuntimeError):
                async with command_transaction(db):
                    await service.create_snapshot(scenario.iterations[0], "rolled_back")
                    raise RuntimeError("Abort after retention")
        async with factory() as db:
            assert await SnapshotService(db).list_snapshots(scenario.iterations[0]) == before
    finally:
        get_settings.cache_clear()


async def test_preview_revision_rejects_apply_after_another_edit(delivery_store):
    _, scenario, _ = delivery_store
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        prefix = f"/api/iterations/{scenario.iterations[0]}"
        preview = await client.post(prefix + "/schedule/preview", json={"changes": []})
        assert preview.status_code == 200, preview.text
        edited = await client.put(f"/api/tasks/{scenario.tasks['planned']}", json={"title": "Concurrent edit", "expected_version": 1})
        assert edited.status_code == 200, edited.text
        applied = await client.post(prefix + "/schedule", json={"expected_revision": preview.json()["input_revision"]})
        assert applied.status_code == 409, applied.text
        assert applied.json()["detail"]["code"] == "iteration_version_conflict"


async def test_snapshot_survives_new_session_and_restores_ids_in_place(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        filename = await SnapshotService(db).create_snapshot(scenario.iterations[0], "saved")
        await TaskService(db).update(scenario.tasks["planned"], TaskUpdate(title="Changed", expected_version=1))
    async with factory() as db:
        service = SnapshotService(db)
        payload = await service.get_snapshot(scenario.iterations[0], filename)
        assert payload["snapshot_info"]["schema_version"] == 2
        restored = await service.restore(scenario.iterations[0], filename)
        assert restored["success"]
    async with factory() as db:
        task = await db.get(Task, scenario.tasks["planned"])
        assert task.title == "Planned"
        assert task.version > 1
        assert task.accepted_at is None
        assert await SnapshotService(db).get_snapshot(scenario.iterations[0], filename) is not None


async def test_project_iteration_and_portfolio_share_metric_definitions(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        project = await ProjectService(db).get_summary(scenario.projects[0])
        iteration = await IterationService(db).get_summary(scenario.iterations[0])
        portfolio = next(row for row in await ProjectService(db).list_portfolio_summaries() if row.project_id == project.id)
        for field in ["total_tasks", "completed_tasks", "implemented_tasks", "accepted_tasks", "total_effort_days", "late_start_tasks", "iteration_overflow_tasks"]:
            assert getattr(project, field) == getattr(iteration, field) == getattr(portfolio, field), field
        assert project.total_tasks == 6
        assert project.accepted_tasks == 0
        assert project.acceptance_unknown_tasks == 2
        assert project.overdue_tasks == iteration.overdue_tasks_count


async def test_late_start_does_not_overwrite_committed_baseline(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        from app.models.team_member import TeamMember
        (await db.get(TeamMember, scenario.capacity_rows[0])).operational_utilization = 0
        (await db.get(TeamMember, scenario.capacity_rows[1])).availability_percent = 0
        await db.commit()
        await SchedulerService(db).schedule_iteration(scenario.iterations[0], commit_baseline=True)
        task = await TaskService(db).get_by_id(scenario.tasks["planned"])
        baseline = task.baseline_start_date, task.baseline_end_date
        assert all(baseline)
        assert baseline[0].isoformat() >= "2026-01-07"
        version = task.version
        changed, _, _ = await TaskService(db).change_status(task.id, "active", expected_version=version)
        assert (changed.baseline_start_date, changed.baseline_end_date) == baseline
        assert changed.started_at is not None
        assert changed.actual_start_date is not None
        assert await db.scalar(select(func.count()).select_from(TaskScheduleBaseline).where(TaskScheduleBaseline.task_id == task.id)) == 1


async def test_repair_is_dry_by_default_and_does_not_invent_acceptance(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        operator = Principal(kind="system", display_name="Repair operator")
        db.add(operator)
        child = await db.get(Task, scenario.tasks["nested"])
        child.status = "closed"
        await db.commit()
        db.info["authority"] = Authority(operator.id, "system", workspace_role="operator")
        service = HierarchyRepairService(db)
        report = await service.audit(scenario.iterations[0])
        assert report["read_only"]
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == 0
        row = next(row for row in report["rows"] if row["task_id"] == scenario.tasks["parent"])
        assert row["unresolved"]
        repaired = await service.repair(scenario.iterations[0], expected_versions={row["task_id"]: row["version"]}, reason="Reconcile deterministic summary fields")
        parent = await db.get(Task, row["task_id"])
        assert parent.status == "planned"
        assert parent.priority == child.priority
        assert parent.accepted_at is None
        again = await service.repair(scenario.iterations[0], expected_versions={}, reason="Verify completed deterministic repairs")
        assert again["repaired_ids"] == []


def test_calendar_midnight_is_not_server_midnight():
    instant = datetime(2026, 1, 20, 23, 30, tzinfo=timezone.utc)
    assert str(working_today("Europe/Madrid", instant)) == "2026-01-21"
    assert str(working_today("America/New_York", instant)) == "2026-01-20"


async def test_two_http_writers_cannot_overwrite_the_same_revision(delivery_store):
    import asyncio
    _, scenario, _ = delivery_store
    path = f"/api/tasks/{scenario.tasks['planned']}"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as first, httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as second:
        responses = await asyncio.gather(first.put(path, json={"title": "First writer", "expected_version": 1}),
                                         second.put(path, json={"title": "Second writer", "expected_version": 1}))
        assert sorted(response.status_code for response in responses) == [200, 409], [response.text for response in responses]
        fresh = (await first.get(path)).json()
        assert fresh["version"] == 2
        iteration = (await first.get(f"/api/iterations/{scenario.iterations[0]}")).json()
        assert iteration["revision"] == 2
        assert fresh["iteration_revision"] == iteration["revision"]
        assert fresh["title"] in {"First writer", "Second writer"}


async def test_restore_recovers_dates_and_absences_without_inventing_acceptance(delivery_store):
    from datetime import date
    from sqlalchemy import delete
    from app.models.team_member import Vacation
    factory, scenario, _ = delivery_store
    async with factory() as db:
        from app.models.team_member import TeamMember
        # Unlinked allocations retain their local absence recovery semantics.
        (await db.get(TeamMember, scenario.capacity_rows[0])).profile_id = None
        db.add(Vacation(team_member_id=scenario.capacity_rows[0], start_date=date(2026, 1, 8), end_date=date(2026, 1, 9)))
        await db.commit()
        snapshot = await SnapshotService(db).create_snapshot(scenario.iterations[0], "saved_absences")
    async with factory() as db:
        iteration = await db.get(Iteration, scenario.iterations[0])
        iteration.end_date = date(2026, 2, 15)
        await db.execute(delete(Vacation))
        await db.commit()
    async with factory() as db:
        await SnapshotService(db).restore(scenario.iterations[0], snapshot)
    async with factory() as db:
        assert (await db.get(Iteration, scenario.iterations[0])).end_date == date(2026, 1, 30)
        absences = (await db.scalars(select(Vacation).where(Vacation.team_member_id == scenario.capacity_rows[0]))).all()
        assert [(absence.start_date, absence.end_date) for absence in absences] == [(date(2026, 1, 8), date(2026, 1, 9))]
        assert all(task.accepted_at is None for task in (await db.scalars(select(Task).where(Task.iteration_id == scenario.iterations[0]))).all())


async def test_saved_dashboard_counts_matching_leaves_across_hierarchy_changes(delivery_store):
    from app.services.saved_view_service import SavedViewService
    from app.schemas.task import TaskCreate
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await TaskService(db).create(scenario.iterations[0], TaskCreate(title="Another nested leaf", parent_id=scenario.tasks["parent"]))
        iteration = await IterationService(db).get_by_id(scenario.iterations[0])
        summary = await aggregate_metrics(db, iteration_id=iteration.id)
        count = await SavedViewService(db)._count_task_dashboard_view({}, iteration)
        assert count == summary["total_tasks"] == 7
        await TaskService(db).merge_tasks(iteration.id, [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]], "New summary")
        assert await SavedViewService(db)._count_task_dashboard_view({}, iteration) == count


async def test_rearrangement_preserves_accepted_leaves_and_inherited_facets(delivery_store):
    from app.utils.time import utc_now
    factory, scenario, _ = delivery_store
    async with factory() as db:
        reviewer = Principal(kind="human", display_name="Independent reviewer")
        db.add(reviewer)
        await db.flush()
        for key in ["closed_urgent", "closed_low"]:
            task = await db.get(Task, scenario.tasks[key])
            task.accepted_at, task.accepted_by_principal_id, task.accepted_version = utc_now(), reviewer.id, task.version
        (await db.get(Task, scenario.tasks["parent"])).is_optional = True
        await db.commit()
        service = TaskService(db)
        before = await aggregate_metrics(db, iteration_id=scenario.iterations[0])
        parent = await service.merge_tasks(scenario.iterations[0], [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]], "Accepted group")
        after = await aggregate_metrics(db, iteration_id=scenario.iterations[0])
        assert after["accepted_tasks"] == before["accepted_tasks"] == 2
        assert after["accepted_percent"] == before["accepted_percent"]
        await service.unmerge_task(parent.id)
        assert (await aggregate_metrics(db, iteration_id=scenario.iterations[0]))["accepted_tasks"] == 2
        await service.unmerge_task(scenario.tasks["parent"])
        nested = await service.get_by_id(scenario.tasks["nested"])
        assert nested.is_optional is True
        assert (await aggregate_metrics(db, iteration_id=scenario.iterations[0]))["required_tasks"] == before["required_tasks"]


async def test_agent_schedule_preview_is_transient_and_reports_input_versions(delivery_store):
    from app.models.agent import AgentActor, AgentIdempotencyRecord
    from app.schemas.agent_planning import AgentPlanningCommandContext
    from app.services.agent_planning_service import AgentPlanningService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["planning:write"]'
        actor.role = "pm"
        await db.commit()
        versions = {task.id: task.version for task in (await db.scalars(select(Task).where(Task.iteration_id == scenario.iterations[0]))).all()}
        receipt = await AgentPlanningService(db).preview_schedule(scenario.iterations[0], actor,
            command=AgentPlanningCommandContext(idempotency_key="transient-preview", rationale="Inspect the calculated plan", correlation_id="preview-check"))
        assert {row["task_id"]: row["version"] for row in receipt.result["task_states"]} == versions
        assert receipt.result["preview"] is True
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == 0
        assert await db.scalar(select(func.count()).select_from(AgentIdempotencyRecord)) == 0
        assert {task.id: task.version for task in (await db.scalars(select(Task).where(Task.iteration_id == scenario.iterations[0]))).all()} == versions


async def test_bulk_preview_default_and_input_revisions_protect_apply(delivery_store):
    factory, scenario, _ = delivery_store
    path = "/api/tasks/bulk-operations"
    payload = {"task_ids": [scenario.tasks["planned"]], "action": "set_priority", "payload": {"priority": 9}}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(path, json=payload)
        assert response.status_code == 200, response.text
        preview = response.json()
        assert preview["dry_run"] is True
        async with factory() as db:
            assert (await db.get(Task, scenario.tasks["planned"])).priority == 2
            assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == 0
        changed = await client.put(f"/api/tasks/{scenario.tasks['planned']}", json={"title": "Newer input", "expected_version": 1})
        assert changed.status_code == 200, changed.text
        response = await client.post(path, json={**payload, "dry_run": False, "expected_versions": preview["task_versions"], "expected_revisions": preview["input_revisions"]})
        assert response.status_code == 409, response.text
        assert response.json()["detail"]["code"] == "iteration_version_conflict"
