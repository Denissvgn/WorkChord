"""Recorded workflow instants, durable scope and missing history stay distinct."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from sqlalchemy import func, select

from app.authority import Authority, AuthorityError
from app.commands import command_transaction
from app.models.delivery_observation import DeliveryObservation
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.schemas.task_brief import BriefCriterion, CriterionProgress, ProgressWrite, TaskBrief, TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.services.delivery_metrics_service import DeliveryMetricsService, summarize_observations
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context


def test_duration_samples_use_events_and_keep_unknown_and_censored_histories():
    base = datetime(2026, 1, 1, tzinfo=UTC)
    rows = [SimpleNamespace(id=i, original_task_id=1, kind=kind, observed_at=base + timedelta(days=day))
            for i, (kind, day) in enumerate([("captured", 0), ("started", 1), ("resolved", 2), ("accepted", 3)], 1)]
    rows += [SimpleNamespace(id=5, original_task_id=2, kind="accepted", observed_at=base + timedelta(days=3)),
             SimpleNamespace(id=6, original_task_id=3, kind="started", observed_at=base + timedelta(days=2))]
    result = summarize_observations(rows, base, base + timedelta(days=4))
    assert result["accepted_leaf_tasks"] == 2
    assert result["lead_time"].mean == 3 * 86400 and result["lead_time"].unknown_count == 1
    assert result["cycle_time"].mean == 2 * 86400 and result["cycle_time"].sample_count == 1
    assert result["review_delay"].mean == 86400 and result["review_delay"].censored_count == 0
    assert result["cycle_time"].censored_count == 1
    assert summarize_observations([], base, base + timedelta(days=4))["lead_time"].mean is None
    planned = [SimpleNamespace(id=7, original_task_id=4, kind="captured", observed_at=base),
               SimpleNamespace(id=8, original_task_id=4, kind="canceled", observed_at=base + timedelta(days=1)),
               SimpleNamespace(id=9, original_task_id=4, kind="reopened_planned", observed_at=base + timedelta(days=2))]
    reopened = summarize_observations(planned, base, base + timedelta(days=4))
    assert reopened["reopened_events"] == 1 and reopened["cycle_time"].censored_count == 0


async def accepted_work(factory, scenario):
    async with factory() as db:
        worker, reviewer_id = await human_context(db, scenario.projects[0])
        db.info["authority"] = worker
        task = await TaskService(db).create(None, TaskCreate(title="Measured delivery", project_id=scenario.projects[0], owner_profile_id=worker.profile_id,
            brief=TaskBrief(goal="Deliver", acceptance_criteria=[BriefCriterion(id="result", text="Result works")])) )
        task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Implement bounded result"))
        task = await TaskBriefService(db).write_progress(task.id, ProgressWrite(expected_version=task.version,
            criteria=[CriterionProgress(criterion_id="result", criterion_revision=1, state="completed", evidence="Artifact checked")]))
        task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Ready for inspection"))
        db.info["authority"] = Authority(reviewer_id, "human", workspace_role="member", projects={scenario.projects[0]: "reviewer"})
        task = await TaskBriefService(db).review(task.id, TaskReviewWrite(expected_version=task.version, brief_revision=task.brief_revision,
            artifact_revision=task.artifact_revision, verdict="accept", reason="Inspected independently"))
        return task.id, worker


async def test_observations_survive_hierarchy_moves_reopen_and_deletion(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, worker = await accepted_work(factory, scenario)
    async with factory() as db:
        db.info["authority"] = worker
        service = DeliveryMetricsService(db)
        before = await service.report(project_id=scenario.projects[0])
        assert before.accepted_leaf_tasks == 1 and before.acceptance_events == 1
        assert before.lead_time.sample_count == before.cycle_time.sample_count == before.review_delay.sample_count == 1
        parent = await TaskService(db).create(None, TaskCreate(title="Grouping", project_id=scenario.projects[0]))
        task = await db.get(Task, task_id)
        task.parent_id, parent.is_summary = parent.id, True
        await db.commit()
        assert (await service.report(project_id=scenario.projects[0])).accepted_leaf_tasks == 1
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="reopen", expected_version=task.version, reason="Follow-up work required"))
        reopened = await service.report(project_id=scenario.projects[0])
        assert reopened.accepted_leaf_tasks == 1 and reopened.reopened_events == 1
        assert reopened.cycle_time.censored_count >= 1
        await TaskService(db).delete(task_id, expected_version=task.version)
        deleted = await service.report(project_id=scenario.projects[0])
        assert deleted.accepted_leaf_tasks == 1
        assert deleted.cycle_time.censored_count == before.cycle_time.censored_count
        assert await db.scalar(select(func.count()).select_from(DeliveryObservation).where(DeliveryObservation.original_task_id == task_id)) >= 5


async def test_scope_at_event_and_permission_isolation_are_preserved(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, worker = await accepted_work(factory, scenario)
    async with factory() as db:
        task = await db.get(Task, task_id)
        task.project_id = scenario.projects[1]
        await db.commit()
        db.info["authority"] = worker
        assert (await DeliveryMetricsService(db).report(project_id=scenario.projects[0])).accepted_leaf_tasks == 1
        with pytest.raises(AuthorityError):
            await DeliveryMetricsService(db).report(project_id=scenario.projects[1])
        db.info["authority"] = Authority(worker.principal_id, "human", projects={scenario.projects[1]: "viewer"})
        assert (await DeliveryMetricsService(db).report(project_id=scenario.projects[1])).accepted_leaf_tasks == 0


async def test_observation_rollback_and_unknown_legacy_dates(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        before = await db.scalar(select(func.count()).select_from(DeliveryObservation))
        with pytest.raises(RuntimeError, match="Abort"):
            async with command_transaction(db):
                await TaskService(db).create(None, TaskCreate(title="Rolled back capture", project_id=scenario.projects[0]))
                raise RuntimeError("Abort")
        assert await db.scalar(select(func.count()).select_from(DeliveryObservation)) == before
        report = await DeliveryMetricsService(db).report(project_id=scenario.projects[0])
        assert report.accepted_leaf_tasks == 0 and report.lead_time.mean is None
        assert report.coverage["legacy_closed_acceptance_unknown"] >= 2


async def test_ledger_is_immutable_and_restoration_does_not_create_capture_history(delivery_store):
    from app.models.recovery import TaskDeletionFence
    factory, scenario, _ = delivery_store
    async with factory() as db:
        observation = await db.scalar(select(DeliveryObservation).limit(1))
        observation.kind = "accepted"
        with pytest.raises(ValueError, match="append-only"):
            await db.commit()
        await db.rollback()
        db.add(TaskDeletionFence(original_task_id=10000, last_version=7))
        await db.commit()
        restored = Task(id=10000, version=8, title="Restored historical work", project_id=scenario.projects[0], status="planned", baseline_provenance="restored")
        db.add(restored)
        await db.commit()
        kinds = (await db.scalars(select(DeliveryObservation.kind).where(DeliveryObservation.original_task_id == 10000))).all()
        assert kinds == ["restored"]
