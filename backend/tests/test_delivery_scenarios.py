"""Delivery contracts and strict reproductions of unresolved behavior."""

from datetime import date

import httpx
from fastapi import Request
import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.models.task import Task
from app.models.team_member import TeamMember
from app.services import snapshot_service, task_service
from app.services.task_service import TaskService
from app.services.agent_service import AgentService
from tests.support.delivery import seed_delivery_scenario
from app.commands import command_transaction


class KnownDeliveryDiscrepancy(AssertionError):
    """Only the specific observed behavior may satisfy an expected failure."""


@pytest_asyncio.fixture(params=[
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
])
async def delivery_store(request, sqlite_engine, tmp_path, monkeypatch):
    engine = sqlite_engine
    if request.param == "postgresql":
        database = request.getfixturevalue("postgres_database")
        engine = create_async_engine(database.url)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    snapshots = tmp_path / "snapshots"
    monkeypatch.setattr(snapshot_service, "SNAPSHOTS_DIR", snapshots)

    class ScenarioDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 20)

    monkeypatch.setattr(task_service, "date", ScenarioDate)
    async with factory() as db:
        scenario = await seed_delivery_scenario(db)

    from app.database import request_command_mode

    async def isolated_db(request: Request):
        async with factory() as db:
            async with command_transaction(db, mode=await request_command_mode(request)):
                yield db

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = isolated_db
    try:
        yield factory, scenario, snapshots
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        if engine is not sqlite_engine:
            await engine.dispose()


async def test_shared_owner_nested_work_and_independent_actors(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        members = (await db.scalars(select(TeamMember))).all()
        assert len(members) == 2
        assert {member.profile_id for member in members} == {scenario.profile}
        assert len(set(scenario.actors)) == len(set(scenario.sessions)) == 2
        authenticated = [await AgentService(db).authenticate(key) for key in scenario.actor_keys]
        assert tuple(actor.id for actor in authenticated) == scenario.actors
        assert await AgentService(db).authenticate("unrecognized-scenario-key") is None
        rows = (await db.scalars(select(Task))).all()
        assert {task.status for task in rows} == {"planned", "active", "resolved", "closed"}
        assert (await db.get(Task, scenario.tasks["nested"])).parent_id == scenario.tasks["parent"]
        assert len(set(scenario.projects)) == 2


async def test_two_editors_reject_stale_write_and_keep_first_value(delivery_store):
    _, scenario, _ = delivery_store
    path = f"/api/tasks/{scenario.tasks['planned']}"
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as first, \
               httpx.AsyncClient(transport=transport, base_url="http://test") as second:
        before = await first.get(path)
        assert before.status_code == 200, before.text
        other = await second.get(path)
        assert other.status_code == 200, other.text
        version = before.json()["version"]
        assert other.json()["version"] == version
        saved = await first.put(path, json={"title": "First editor", "expected_version": version})
        assert saved.status_code == 200, saved.text
        stale = await second.put(path, json={"title": "Second editor", "expected_version": version})
        assert stale.status_code == 409, stale.text
        assert stale.json()["detail"]["code"] == "task_version_conflict"
        assert stale.json()["detail"]["current_task"]["version"] == saved.json()["version"]
        readback = await second.get(path)
        assert readback.json()["title"] == "First editor"
        assert readback.json()["version"] == version + 1


async def preview_edit(scenario):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        path = f"/api/tasks/{scenario.tasks['planned']}"
        before = (await client.get(path)).json()
        response = await client.post(f"/api/iterations/{scenario.iterations[0]}/schedule/preview", json={
            "changes": [{"task_id": scenario.tasks["planned"], "expected_version": before["version"],
                         "update": {"title": "Preview only", "effort_days": 2}}],
        })
        assert response.status_code == 200, response.text
        after = (await client.get(path)).json()
        return before, after


async def test_preview_rolls_back_database_edits(delivery_store):
    _, scenario, _ = delivery_store
    before, after = await preview_edit(scenario)
    assert after == before


async def test_preview_leaves_snapshot_storage_unchanged(delivery_store):
    _, scenario, snapshots = delivery_store
    before = set(snapshots.rglob("*"))
    await preview_edit(scenario)
    if set(snapshots.rglob("*")) != before:
        raise KnownDeliveryDiscrepancy("Preview changed snapshot storage")


async def merged_closed_parent(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        parent = await TaskService(db).merge_tasks(scenario.iterations[0],
            [scenario.tasks["closed_urgent"], scenario.tasks["closed_low"]], "Combined delivery")
        assert parent is not None
        return parent


async def test_closed_merge_preserves_leaf_completion(delivery_store):
    parent = await merged_closed_parent(delivery_store)
    assert {child.status for child in parent.children} == {"closed"}
    if parent.status != "closed":
        raise KnownDeliveryDiscrepancy(f"Parent is {parent.status}")


async def test_merge_inherits_most_urgent_leaf_priority(delivery_store):
    parent = await merged_closed_parent(delivery_store)
    if parent.priority != min(child.priority for child in parent.children):
        raise KnownDeliveryDiscrepancy(f"Parent priority is {parent.priority}")


async def test_active_past_end_date_is_overdue(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        service = TaskService(db)
        task = await service.get_by_id(scenario.tasks["active"])
        assert task.end_date < date(2026, 1, 20)
        if not service.task_to_response(task, date(2026, 1, 30)).is_overdue:
            raise KnownDeliveryDiscrepancy("Active work past its end date is not overdue")


async def test_legacy_triage_missing_iteration_has_field_localized_error(delivery_store):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/triage/999/convert-to-task", json={})
        assert response.status_code == 422, response.text
        assert {"type": "missing", "loc": ["body", "iteration_id"], "msg": "Field required"} in response.json()["detail"]
        assert (await client.post("/api/triage/999/convert", json={})).status_code == 404
