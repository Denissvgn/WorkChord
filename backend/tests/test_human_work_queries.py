"""Human ownership queries and exact-ID lookup respect project visibility."""

import pytest

from app.authority import Authority
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.services.task_detail_service import TaskDetailService
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context


async def test_my_work_includes_nested_and_backlog_without_private_work(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        service = TaskService(db)
        parent = await service.create(None, TaskCreate(title="Delivery group", project_id=scenario.projects[0]))
        nested = await service.create(None, TaskCreate(title="Nested owned work", project_id=scenario.projects[0], parent_id=parent.id, owner_profile_id=worker.profile_id))
        backlog = await service.create(None, TaskCreate(title="Owned follow-up", project_id=scenario.projects[0], owner_profile_id=worker.profile_id))
        private = Task(title="Private owned work", project_id=scenario.projects[1], owner_profile_id=worker.profile_id)
        db.add(private)
        await db.commit()
        db.info["authority"] = worker
        query = TaskDetailService(db)
        page = await query.my_work(limit=100)
        assert page["state"] == "ready"
        assert {item["id"] for item in page["queues"]["queued"]} == {nested.id, backlog.id}
        assert "Private owned work" not in str(page)
        assert page["queues"]["queued"][0]["project_name"] == "Orchard"
        assert all(item["iteration_id"] is None for item in page["queues"]["queued"])
        db.info["authority"] = Authority(worker.principal_id, "human", projects=worker.projects)
        assert (await query.my_work())["state"] == "profile_unlinked"


async def test_lookup_matches_id_case_and_literal_wildcards_without_private_counts(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        task = await service.create(None, TaskCreate(title="Fix 50% regression", project_id=scenario.projects[0]))
        db.info["authority"] = Authority(None, "human", projects={scenario.projects[0]: "viewer"})
        query = TaskDetailService(db)
        for text in (f"#{task.id}", str(task.id), "FIX 50%"):
            result = await query.lookup(query=text)
            assert [item.id for item in result.items] == [task.id]
        assert (await query.lookup(query="Harbor")).items == []
        assert (await query.lookup(query=f"#{scenario.tasks['other_project']}")).items == []
        with pytest.raises(ValueError, match="limit"):
            await query.lookup(limit=101)


async def test_withdrawn_acceptance_stays_visible_in_owned_blocked_work(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        task = await TaskService(db).create(None, TaskCreate(title="Acceptance requires reconciliation",
            project_id=scenario.projects[0], owner_profile_id=worker.profile_id))
        from app.utils.time import utc_now
        task.status, task.accepted_at, task.accepted_version = "closed", utc_now(), task.version
        task.accepted_by_principal_id = None
        await db.commit()
        db.info["authority"] = worker
        page = await TaskDetailService(db).my_work()
        assert [item["id"] for item in page["queues"]["blocked"]] == [task.id]
        assert page["queues"]["blocked"][0]["acceptance_current"] is False
