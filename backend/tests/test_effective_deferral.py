"""Complete ancestry policy, working lifecycle parity and rejected-write atomicity."""

import httpx
import pytest
from sqlalchemy import func, select, update

from app.authority import AuthorityError
from app.commands import PlanningConflict
from app.main import app
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_domain import TaskActionRequest
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService, TaskVersionConflictError
from tests.test_delivery_scenarios import delivery_store


def test_unhydrated_parent_policy_fails_closed():
    from app.services.work_metrics import effective_work_flags
    task = Task(id=1, title="Incomplete ancestry", parent_id=2, is_deferred=False, is_optional=False)
    with pytest.raises(ValueError, match="incomplete"):
        effective_work_flags(task)


async def test_reparenting_recomputes_inherited_deferral_without_copying_the_flag(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        await service.update(scenario.tasks["parent"], TaskUpdate(is_deferred=True, expected_version=1))
        leaf = await service.get_by_id(scenario.tasks["planned"])
        leaf_id, parent_id, iteration_id = leaf.id, scenario.tasks["parent"], scenario.iterations[0]
        revision = (await db.get(Iteration, iteration_id)).revision
        leaf = await service.move_task(leaf_id, iteration_id, parent_id=parent_id,
            expected_version=leaf.version, expected_revisions={iteration_id: revision})
        assert leaf.is_deferred is False
        actions = await TaskDomainService(db).allowed_actions(leaf_id)
        assert not next(row for row in actions.actions if row.action == "start_manual").allowed
        revision = (await db.get(Iteration, iteration_id)).revision
        leaf = await service.move_task(leaf_id, iteration_id, parent_id=None,
            expected_version=leaf.version, expected_revisions={iteration_id: revision})
        actions = await TaskDomainService(db).allowed_actions(leaf_id)
        assert next(row for row in actions.actions if row.action == "start_manual").allowed
        assert leaf.is_deferred is False


async def test_deep_ancestor_deferral_clearing_and_unscheduled_manual_freedom(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        tasks = TaskService(db)
        leaf = await tasks.create(scenario.iterations[0], TaskCreate(title="Deep work",
            project_id=scenario.projects[0], parent_id=scenario.tasks["nested"]))
        leaf_id = leaf.id
        parent = await tasks.get_by_id(scenario.tasks["parent"])
        parent = await tasks.update(parent.id, TaskUpdate(is_deferred=True, expected_version=parent.version))
        actions = await TaskDomainService(db).allowed_actions(leaf_id)
        assert not next(row for row in actions.actions if row.action == "start_manual").allowed
        parent = await tasks.update(parent.id, TaskUpdate(is_deferred=False, expected_version=parent.version))
        leaf = await tasks.get_by_id(leaf_id)
        assert leaf.start_date is None and leaf.end_date is None
        started = await TaskDomainService(db).command(leaf_id, TaskActionRequest(
            action="start_manual", expected_version=leaf.version, reason="Execute unscheduled work"))
        assert started.status == "active" and started.execution_mode == "manual"
        assert started.start_date is None and started.end_date is None


@pytest.mark.parametrize("transition", ["active", "resolved"])
async def test_deferred_lifecycle_rejection_preserves_version_history_revisions_and_claims(delivery_store, transition):
    from app.models.agent import TaskEvent
    from app.models.outbound_webhook import OutboundWebhookEvent
    from app.models.task_status_log import TaskStatusLog

    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["nested"]
    async with factory() as db:
        task = await db.get(Task, task_id)
        if transition == "resolved":
            task.status, task.execution_mode = "active", "manual"
            await db.commit()
        await TaskService(db).update(scenario.tasks["parent"], TaskUpdate(is_deferred=True, expected_version=1))
        task = await TaskService(db).get_by_id(task_id)
        before = (task.status, task.version, task.claim_id, task.claim_generation, task.started_at)
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        models = [ApplicationSnapshot, TaskEvent, TaskStatusLog, OutboundWebhookEvent]
        counts = [await db.scalar(select(func.count()).select_from(model)) for model in models]
        with pytest.raises(PlanningConflict, match="deferral"):
            await TaskService(db).change_status(task_id, transition, expected_version=task.version,
                manual_execution=transition == "resolved")
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert (task.status, task.version, task.claim_id, task.claim_generation, task.started_at) == before
        assert (await db.get(Iteration, scenario.iterations[0])).revision == revision
        assert [await db.scalar(select(func.count()).select_from(model)) for model in models] == counts


async def test_stale_session_cannot_ignore_a_committed_ancestor_deferral(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as stale:
        leaf = await TaskService(stale).get_by_id(scenario.tasks["nested"])
        version = leaf.version
        await stale.rollback()
        async with factory() as other:
            await TaskService(other).update(scenario.tasks["parent"], TaskUpdate(is_deferred=True, expected_version=1))
        with pytest.raises((AuthorityError, TaskVersionConflictError)):
            await TaskDomainService(stale).command(scenario.tasks["nested"], TaskActionRequest(
                action="start_manual", expected_version=version, reason="Stale session start"))
    async with factory() as db:
        assert (await db.get(Task, scenario.tasks["nested"])).status == "planned"


async def test_cyclic_ancestry_is_a_typed_conflict_at_http_execution_boundary(delivery_store):
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["nested"]
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == task_id).values(parent_id=task_id))
        await db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(f"/api/tasks/{task_id}/commands", json={
            "action": "start_manual", "expected_version": 1, "reason": "Invalid ancestry"})
        assert response.status_code == 409, response.text
        assert response.json()["detail"]["code"] == "task_ancestry_invalid"
    async with factory() as db:
        assert (await db.get(Task, task_id)).status == "planned"
