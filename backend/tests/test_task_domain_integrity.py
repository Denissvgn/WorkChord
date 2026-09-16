"""Task context, recovery and project projections stay consistent across commands."""

from dataclasses import replace

import pytest
from sqlalchemy import delete, func, select

from app.authority import Authority, AuthorityError
from app.commands import command_transaction
from app.models.calendar import Calendar
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task, TaskDependency
from app.models.task_brief import TaskProgressRecord
from app.schemas.iteration import IterationUpdate
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_brief import BriefCriterion, CriterionProgress, ProgressWrite, TaskBrief, TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.services.backlog_snapshot_service import BacklogSnapshotService
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.snapshot_service import SnapshotService
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.work_metrics import aggregate_metrics
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context


async def test_nested_backlog_participates_in_project_and_milestone_metrics(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        project_id = scenario.projects[1]
        before = await aggregate_metrics(db, project_id=project_id)
        parent = await service.create(None, TaskCreate(title="Backlog group", project_id=project_id))
        child = await service.create(None, TaskCreate(title="Nested group", project_id=project_id, parent_id=parent.id))
        await service.create(None, TaskCreate(title="Nested deliverable", project_id=project_id, parent_id=child.id, effort_hours=2))
        after = await aggregate_metrics(db, project_id=project_id)
        assert after["total_tasks"] == before["total_tasks"] + 1
        assert after["structural_tasks"] == before["structural_tasks"] + 2
        assert (await ProjectService(db).get_summary(project_id)).total_tasks == after["total_tasks"]
        assert sum(row["total_tasks"] for row in await aggregate_metrics(db, project_id=project_id, group_by="milestone")) == after["total_tasks"]
        assert sum(row["total_tasks"] for row in await aggregate_metrics(db, project_ids=[project_id], group_by="project")) == after["total_tasks"]


async def test_blocked_metrics_include_explicit_and_canceled_dependencies(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        project_id = scenario.projects[1]
        blocked = await service.create(None, TaskCreate(title="Waiting for supplier", project_id=project_id))
        await TaskDomainService(db).command(blocked.id, TaskActionRequest(action="block", expected_version=blocked.version, reason="Supplier unavailable"))
        prerequisite = await service.create(None, TaskCreate(title="Canceled prerequisite", project_id=project_id))
        prerequisite.status = "resolved"
        await db.commit()
        await TaskDomainService(db).command(prerequisite.id, TaskActionRequest(action="cancel", expected_version=prerequisite.version, reason="Result withdrawn"))
        await service.create(None, TaskCreate(title="Waiting on withdrawn result", project_id=project_id, depends_on=[prerequisite.id]))
        metrics = await aggregate_metrics(db, project_id=project_id)
        assert metrics["blocked_tasks"] == 2


async def test_blocked_metrics_do_not_hide_inaccessible_prerequisites(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = await TaskService(db).create(None, TaskCreate(title="Scoped deliverable", project_id=scenario.projects[1]))
        db.add(TaskDependency(task_id=task.id, depends_on_id=scenario.tasks["closed_urgent"]))
        await db.commit()
        db.info["authority"] = Authority(None, "human", projects={scenario.projects[1]: "viewer"})
        metrics = await aggregate_metrics(db, project_id=scenario.projects[1])
        assert metrics["blocked_tasks"] == 1
        assert metrics["total_tasks"] == 2


@pytest.mark.parametrize("operation", ["add", "remove", "update_add", "update_remove"])
async def test_dependency_mutations_invalidate_evidence_without_erasing_history(delivery_store, operation):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, reviewer_id = await human_context(db, scenario.projects[0])
        db.info["authority"] = worker
        service, commands, briefs = TaskService(db), TaskDomainService(db), TaskBriefService(db)
        prerequisite = await service.create(None, TaskCreate(title="Prerequisite", project_id=scenario.projects[0]))
        prerequisite.status = "resolved"
        await db.commit()
        task = await service.create(None, TaskCreate(title="Result", project_id=scenario.projects[0],
            depends_on=[prerequisite.id] if operation.endswith("remove") else [],
            brief=TaskBrief(acceptance_criteria=[BriefCriterion(id="result", text="Result meets scope")])) )
        task_id, dependency_id = task.id, prerequisite.id
        task = await commands.command(task_id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Begin"))
        task = await briefs.write_progress(task_id, ProgressWrite(expected_version=task.version,
            criteria=[CriterionProgress(criterion_id="result", criterion_revision=1, state="completed", evidence="Evidence for original context")]))
        task = await commands.command(task_id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Ready"))
        original_version = task.version
        if operation == "add":
            await service.add_dependency(task_id, dependency_id)
        elif operation == "remove":
            await service.remove_dependency(task_id, dependency_id)
        else:
            await service.update(task_id, TaskUpdate(expected_version=task.version, depends_on=[dependency_id] if operation == "update_add" else []))
        task = await service.get_by_id(task_id)
        assert task.version == original_version + 1
        assert task.progress is None
        assert task.accepted_at is None and task.accepted_version is None
        assert await db.scalar(select(func.count()).select_from(TaskProgressRecord).where(TaskProgressRecord.original_task_id == task_id)) == 1
        current_version = task.version
        if operation.endswith("add"):
            await service.add_dependency(task_id, dependency_id)
        else:
            await service.remove_dependency(task_id, dependency_id)
        task = await service.get_by_id(task_id)
        assert task.version == current_version
        db.info["authority"] = Authority(reviewer_id, "human", projects={scenario.projects[0]: "reviewer"})
        with pytest.raises(ValueError, match="Current brief evidence"):
            await briefs.review(task_id, TaskReviewWrite(expected_version=task.version, brief_revision=task.brief_revision,
                artifact_revision=task.artifact_revision, verdict="accept", reason="Inspect changed context"))


@pytest.mark.parametrize("moving_prerequisite", [False, True])
async def test_backlog_project_move_rejects_crossing_edges_atomically(delivery_store, moving_prerequisite):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        prerequisite = await service.create(None, TaskCreate(title="Prerequisite", project_id=scenario.projects[0]))
        dependent = await service.create(None, TaskCreate(title="Dependent", project_id=scenario.projects[0], depends_on=[prerequisite.id]))
        task = prerequisite if moving_prerequisite else dependent
        task_id, version = task.id, task.version
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        with pytest.raises(ValueError, match="dependenc"):
            await service.update(task_id, TaskUpdate(expected_version=version, project_id=scenario.projects[1]))
        task = await service.get_by_id(task_id)
        assert (task.project_id, task.version) == (scenario.projects[0], version)
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_backlog_subtree_move_preserves_internal_edges_and_captures_both_scopes(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        parent = await service.create(None, TaskCreate(title="Delivery group", project_id=scenario.projects[0]))
        first = await service.create(None, TaskCreate(title="First", project_id=scenario.projects[0], parent_id=parent.id))
        second = await service.create(None, TaskCreate(title="Second", project_id=scenario.projects[0], parent_id=parent.id, depends_on=[first.id]))
        parent_id, first_id, second_id = parent.id, first.id, second.id
        versions = {task_id: (await service.get_by_id(task_id)).version for task_id in [parent_id, first_id, second_id]}
        before = set((await db.scalars(select(ApplicationSnapshot.id))).all())
        parent = await service.get_by_id(parent_id)
        await service.update(parent_id, TaskUpdate(expected_version=parent.version, project_id=scenario.projects[1]))
        snapshots = list((await db.scalars(select(ApplicationSnapshot).where(ApplicationSnapshot.id.notin_(before)))).all())
        assert {row.project_id for row in snapshots} == set(scenario.projects)
        for task_id in [parent_id, first_id, second_id]:
            moved = await service.get_by_id(task_id)
            assert moved.project_id == scenario.projects[1]
            assert moved.version == versions[task_id] + 1
        assert (await service.get_by_id(second_id)).dependencies[0].depends_on_id == first_id
        current = await BacklogSnapshotService(db).capture(scenario.projects[1])
        _, tasks = await service._load_iteration_tree(None, project_id=scenario.projects[1])
        restored = await BacklogSnapshotService(db).restore(scenario.projects[1], current, {item.id: item.version for item in tasks.values()}, reason="Round trip")
        assert restored[0].id == parent_id


async def test_backlog_move_requires_permission_in_both_projects(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        db.info["authority"] = replace(worker, projects={scenario.projects[0]: "manager", scenario.projects[1]: "viewer"})
        task = await TaskService(db).create(None, TaskCreate(title="Owned scope", project_id=scenario.projects[0]))
        task_id, version = task.id, task.version
        with pytest.raises(AuthorityError):
            await TaskService(db).update(task_id, TaskUpdate(expected_version=version, project_id=scenario.projects[1]))
        task = await TaskService(db).get_by_id(task_id)
        assert (task.project_id, task.version) == (scenario.projects[0], version)


@pytest.mark.parametrize("backlog", [False, True])
async def test_restore_advances_above_deleted_version_and_rejects_stale_writes(delivery_store, backlog):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        iteration_id = None if backlog else scenario.iterations[1]
        task = await service.create(iteration_id, TaskCreate(title="Original", project_id=scenario.projects[1], brief=TaskBrief(goal="Preserved goal")))
        task_id, stale_version = task.id, task.version
        snapshot_service = BacklogSnapshotService(db) if backlog else SnapshotService(db)
        snapshot = await snapshot_service.capture(scenario.projects[1]) if backlog else await snapshot_service.create_snapshot(iteration_id, "original")
        for number in range(5):
            task = await service.update(task_id, TaskUpdate(expected_version=task.version, title=f"Later edit {number}"))
        deleted_version = task.version
        await service.delete(task_id, expected_version=deleted_version)
        if backlog:
            await snapshot_service.restore(scenario.projects[1], snapshot, {}, reason="Recover older image")
        else:
            await snapshot_service.restore(iteration_id, snapshot)
        task = await service.get_by_id(task_id)
        assert task.version > deleted_version
        assert task.title == "Original" and task.brief["goal"] == "Preserved goal"
        assert task.progress is None and task.accepted_at is None
        with pytest.raises(TaskVersionConflictError):
            await service.update(task_id, TaskUpdate(expected_version=stale_version, title="Stale editor"))
        task = await service.get_by_id(task_id)
        restored_version = task.version
        if backlog:
            await snapshot_service.restore(scenario.projects[1], snapshot, {task_id: task.version}, reason="Repeat recovery")
        else:
            await snapshot_service.restore(iteration_id, snapshot)
        assert (await service.get_by_id(task_id)).version > restored_version


@pytest.mark.parametrize("backlog", [False, True])
async def test_restore_rejects_missing_historical_deletion_fence(delivery_store, backlog):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        iteration_id = None if backlog else scenario.iterations[1]
        task = await service.create(iteration_id, TaskCreate(title="Historic deletion", project_id=scenario.projects[1]))
        task_id = task.id
        snapshot_service = BacklogSnapshotService(db) if backlog else SnapshotService(db)
        snapshot = await snapshot_service.capture(scenario.projects[1]) if backlog else await snapshot_service.create_snapshot(iteration_id, "original")
        # A raw database deletion represents a record removed before deletion fences existed.
        await db.execute(delete(Task.__table__).where(Task.id == task_id))
        await db.commit()
        db.expunge_all()
        before = list((await db.execute(select(Task.id, Task.version).order_by(Task.id))).all())
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        with pytest.raises(AuthorityError) as failure:
            if backlog:
                await snapshot_service.restore(scenario.projects[1], snapshot, {}, reason="Recover old work")
            else:
                await snapshot_service.restore(iteration_id, snapshot)
        assert failure.value.code == "snapshot_version_history_unknown"
        assert await db.get(Task, task_id) is None
        assert list((await db.execute(select(Task.id, Task.version).order_by(Task.id))).all()) == before
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


@pytest.mark.parametrize("hours", [None, 0, 1.5, 8])
async def test_calendar_switch_preserves_hours_and_refreshes_day_units(delivery_store, hours):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        calendar = Calendar(name="Six-hour workday", year=2026, nominal_day_hours=6)
        db.add(calendar)
        await db.commit()
        task = await TaskService(db).create(scenario.iterations[1], TaskCreate(title="Estimate", project_id=scenario.projects[1], effort_hours=hours))
        task_id, version = task.id, task.version
        provenance = task.estimate_provenance
        await IterationService(db).update(scenario.iterations[1], IterationUpdate(calendar_id=calendar.id))
        task = await TaskService(db).get_by_id(task_id)
        assert task.effort_hours == hours
        assert task.nominal_day_hours == 6
        assert task.effort_days == (hours / 6 if hours is not None else None)
        assert task.estimate_provenance == provenance
        assert task.version == version + 1


@pytest.mark.parametrize("backlog", [False, True])
async def test_subtree_deletion_fences_survive_rollback_and_repeated_restoration(delivery_store, backlog):
    from app.models.recovery import TaskDeletionFence
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        iteration_id = None if backlog else scenario.iterations[1]
        root = await service.create(iteration_id, TaskCreate(title="Group", project_id=scenario.projects[1]))
        child = await service.create(iteration_id, TaskCreate(title="Child", project_id=scenario.projects[1], parent_id=root.id))
        root_id, child_id = root.id, child.id
        root = await service.get_by_id(root_id)
        versions = {root_id: root.version, child_id: child.version}
        snapshots = BacklogSnapshotService(db) if backlog else SnapshotService(db)
        saved = await snapshots.capture(scenario.projects[1]) if backlog else await snapshots.create_snapshot(iteration_id, "original")
        with pytest.raises(RuntimeError, match="Abort deletion"):
            async with command_transaction(db):
                await service.delete(root_id, expected_version=versions[root_id])
                assert await db.scalar(select(func.count()).select_from(TaskDeletionFence)) == 2
                raise RuntimeError("Abort deletion")
        assert await db.scalar(select(func.count()).select_from(TaskDeletionFence)) == 0
        assert await db.get(Task, child_id) is not None
        await service.delete(root_id, expected_version=versions[root_id])
        assert dict((await db.execute(select(TaskDeletionFence.original_task_id, TaskDeletionFence.last_version))).all()) == versions
        if backlog:
            await snapshots.restore(scenario.projects[1], saved, {}, reason="Restore group")
        else:
            await snapshots.restore(iteration_id, saved)
        for task_id, old_version in versions.items():
            assert (await service.get_by_id(task_id)).version > old_version
        assert (await service.get_by_id(child_id)).parent_id == root_id
        latest = (await service.get_by_id(root_id)).version
        await service.delete(root_id, expected_version=latest)
        assert await db.scalar(select(TaskDeletionFence.last_version).where(TaskDeletionFence.original_task_id == root_id)) == latest


async def test_restore_removals_record_deletion_fences(delivery_store):
    from app.models.recovery import TaskDeletionFence
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        snapshots = BacklogSnapshotService(db)
        saved = await snapshots.capture(scenario.projects[1])
        task = await service.create(None, TaskCreate(title="Later capture", project_id=scenario.projects[1]))
        task_id, version = task.id, task.version
        await snapshots.restore(scenario.projects[1], saved, {task_id: version}, reason="Restore empty backlog")
        assert await db.get(Task, task_id) is None
        assert await db.scalar(select(TaskDeletionFence.last_version).where(TaskDeletionFence.original_task_id == task_id)) == version


async def test_project_move_rolls_back_both_scope_snapshots_on_failure(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        task = await service.create(None, TaskCreate(title="Move atomically", project_id=scenario.projects[0]))
        task_id, version = task.id, task.version
        before = set((await db.scalars(select(ApplicationSnapshot.id))).all())
        async def fail(*_args, **_kwargs):
            raise RuntimeError("Abort project move")
        monkeypatch.setattr(service, "record_task_event", fail)
        with pytest.raises(RuntimeError, match="Abort project move"):
            await service.update(task_id, TaskUpdate(expected_version=version, project_id=scenario.projects[1]))
        task = await service.get_by_id(task_id)
        assert (task.version, task.project_id) == (version, scenario.projects[0])
        assert set((await db.scalars(select(ApplicationSnapshot.id))).all()) == before


async def test_opposite_backlog_moves_use_one_project_lock_order(delivery_store):
    import asyncio
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        first = await service.create(None, TaskCreate(title="Move to second", project_id=scenario.projects[0]))
        second = await service.create(None, TaskCreate(title="Move to first", project_id=scenario.projects[1]))
        inputs = [(first.id, first.version, scenario.projects[1]), (second.id, second.version, scenario.projects[0])]
    async def move(task_id, version, project_id):
        async with factory() as db:
            return await TaskService(db).update(task_id, TaskUpdate(expected_version=version, project_id=project_id))
    results = await asyncio.wait_for(asyncio.gather(*(move(*values) for values in inputs)), timeout=20)
    assert [(task.id, task.project_id) for task in results] == [(task_id, project) for task_id, _, project in inputs]
