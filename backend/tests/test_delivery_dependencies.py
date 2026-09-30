"""Cross-project readiness, cycle prevention and retained acceptance history."""

from datetime import date

import pytest
from sqlalchemy import select

from app.authority import Authority
from app.commands import PlanningConflict
from app.models.delivery_dependency import DeliveryDependency
from app.models.project import ProjectMilestone
from app.models.task import Task
from app.models.identity import Principal
from app.schemas.task import TaskCreate
from app.schemas.task_domain import TaskActionRequest
from app.services.delivery_dependency_service import DeliveryDependencyService
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


async def pair(db, scenario):
    tasks = TaskService(db)
    first = await tasks.create(None, TaskCreate(title="Deliver component", project_id=scenario.projects[0]))
    second = await tasks.create(None, TaskCreate(title="Integrate component", project_id=scenario.projects[1]))
    return first, second


async def test_dependency_requires_current_acceptance_and_blocks_manual_start(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        service = DeliveryDependencyService(db)
        projection = await service.add(second.id, "task", first.id, second.version)
        assert not projection[0]["ready"]
        actions = await TaskDomainService(db).allowed_actions(second.id)
        assert not next(action for action in actions.actions if action.action == "start_manual").allowed
        first.status, first.accepted_at, first.accepted_version = "closed", utc_now(), first.version
        await db.commit()
        assert not await service.ready(second.id)
        reviewer = Principal(kind="human", display_name="Independent reviewer")
        db.add(reviewer)
        await db.flush()
        first.accepted_by_principal_id = reviewer.id
        await db.commit()
        assert await service.ready(second.id)
        second.progress = {"criteria": []}
        second.accepted_at, second.accepted_version = utc_now(), second.version
        await db.commit()
        prior = second.version
        await TaskDomainService(db).command(first.id, TaskActionRequest(action="reopen", expected_version=first.version,
            reason="Acceptance was withdrawn after delivery review"))
        await db.refresh(second)
        assert second.version == prior + 1
        assert second.progress is None and second.accepted_at is None
        assert not await service.ready(second.id)


async def test_global_cycle_and_referenced_delete_roll_back(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        first_id, second_id = first.id, second.id
        await DeliveryDependencyService(db).add(second_id, "task", first_id, second.version)
        with pytest.raises(PlanningConflict, match="cycle"):
            await DeliveryDependencyService(db).add(first_id, "task", second_id, first.version)
        assert len((await db.scalars(select(DeliveryDependency))).all()) == 1
        with pytest.raises(PlanningConflict, match="Remove incoming"):
            await TaskService(db).delete(first_id)
        assert await db.get(Task, first_id) is not None


async def test_target_revocation_redacts_identity_and_denies_new_edges(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        second_id = second.id
        await DeliveryDependencyService(db).add(second_id, "task", first.id, second.version)
        db.info["authority"] = Authority(None, "human", projects={scenario.projects[1]: "editor"})
        projection = await DeliveryDependencyService(db).projection(second_id)
        assert projection == [{"id": projection[0]["id"], "kind": "task", "ready": False, "reason": "prerequisite_unavailable"}]
        with pytest.raises(ValueError, match="inaccessible"):
            await DeliveryDependencyService(db).add(second_id, "task", first.id, second.version)


async def test_milestone_target_and_own_milestone_cycle(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        milestone = ProjectMilestone(project_id=first.project_id, name="Component ready", status="completed", target_date=date(2026, 2, 1))
        db.add(milestone)
        await db.flush()
        reviewer = Principal(kind="human", display_name="Independent reviewer")
        db.add(reviewer)
        await db.flush()
        first.accepted_by_principal_id = reviewer.id
        first.milestone_id = milestone.id
        first.status, first.accepted_at, first.accepted_version = "closed", utc_now(), first.version
        await db.commit()
        projection = await DeliveryDependencyService(db).add(second.id, "milestone", milestone.id, second.version)
        assert projection[0]["ready"]
        with pytest.raises(PlanningConflict, match="cycle"):
            await DeliveryDependencyService(db).add(first.id, "milestone", milestone.id, first.version)
