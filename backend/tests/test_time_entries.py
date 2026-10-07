"""Private explicit minutes, retained corrections and independent recovery behavior."""

import asyncio
from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select, update, delete

from app.authority import Authority, AuthorityError, internal_authority
from app.commands import PlanningConflict
from app.config import get_settings
from app.models.task import Task
from app.models.time_entry import TimeEntry, TimeEntryRevision
from app.schemas.time_entry import TimeEntryCreate, TimeEntryCorrection, TimeEntryVoid
from app.services.time_entry_service import TimeEntryService, TimeEntryVersionConflict
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context


@pytest.fixture(autouse=True)
def isolated_time_settings():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


async def prepare(db, scenario, monkeypatch):
    author, other_id = await human_context(db, scenario.projects[0])
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("TIME_ENTRIES_ENABLED", "true")
    get_settings.cache_clear()
    db.info["authority"] = author
    return author, other_id


def entry_data(scenario, **values):
    return TimeEntryCreate(project_id=scenario.projects[0], task_id=scenario.tasks["planned"],
        request_id=uuid4(), work_date=date(2026, 10, 7), timezone="Europe/Madrid", minutes=15,
        note="Private work note", **values)


async def test_record_correct_void_retains_private_history_and_task_state(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        task = await db.get(Task, scenario.tasks["planned"])
        before = (task.version, task.status, task.effort_hours, task.started_at, task.accepted_at)
        service = TimeEntryService(db)
        recorded = await service.create(entry_data(scenario))
        corrected = await service.correct(recorded["id"], TimeEntryCorrection(work_date="2026-10-06",
            timezone="America/New_York", minutes=30, note="Corrected private note", expected_version=1, reason="Wrong work date"))
        assert corrected["version"] == 2 and corrected["work_date"] == "2026-10-06"
        with pytest.raises(TimeEntryVersionConflict) as conflict:
            await service.correct(recorded["id"], TimeEntryVoid(expected_version=1, reason="Stale correction"), void=True)
        assert conflict.value.detail()["current_entry"]["version"] == 2
        voided = await service.correct(recorded["id"], TimeEntryVoid(expected_version=2, reason="Duplicate work"), void=True)
        assert voided["voided"] and voided["version"] == 3
        page = await service.history(recorded["id"], limit=1)
        assert page["items"][0]["minutes"] == 15 and page["next_after_version"] == 1
        rest = await service.history(recorded["id"], after_version=1)
        assert [r["version"] for r in rest["items"]] == [2, 3]
        assert rest["items"][0]["reason"] == "Wrong work date"
        assert (await service.list())["items"] == []
        assert (await service.list(include_voided=True))["items"][0]["id"] == recorded["id"]
        await db.refresh(task)
        assert (task.version, task.status, task.effort_hours, task.started_at, task.accepted_at) == before
        with pytest.raises(PlanningConflict, match="voided"):
            await service.correct(recorded["id"], TimeEntryVoid(expected_version=3, reason="Retry"), void=True)


async def test_retry_identity_and_payload_conflict(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        service = TimeEntryService(db)
        data = entry_data(scenario)
        first = await service.create(data)
        assert await service.create(data) == first
        assert await db.scalar(select(func.count()).select_from(TimeEntryRevision)) == 1
        with pytest.raises(PlanningConflict, match="request ID"):
            await service.create(data.model_copy(update={"minutes": 16}))
        assert len((await service.list())["items"]) == 1


async def test_other_people_projects_agents_and_disabled_feature_are_protected(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, other_id = await prepare(db, scenario, monkeypatch)
        service = TimeEntryService(db)
        row = await service.create(entry_data(scenario))
        for authority in [Authority(other_id, "human", projects={scenario.projects[0]: "manager"}),
                          Authority(other_id, "human", workspace_role="owner"),
                          Authority(author.principal_id, "human", projects={scenario.projects[1]: "manager"})]:
            db.info["authority"] = authority
            assert (await service.list())["items"] == []
            with pytest.raises((LookupError, AuthorityError)):
                await service.history(row["id"])
            with pytest.raises((LookupError, AuthorityError)):
                await service.correct(row["id"], TimeEntryVoid(expected_version=1, reason="Not my record"), void=True)
        for kind in ("agent", "system", "local"):
            db.info["authority"] = Authority(author.principal_id, kind, workspace_role="owner", local=kind == "local")
            with pytest.raises(AuthorityError, match="human account"):
                await service.list()
        db.info["authority"] = author
        monkeypatch.setenv("TIME_ENTRIES_ENABLED", "false"); get_settings.cache_clear()
        with pytest.raises(AuthorityError, match="disabled"):
            await service.get(row["id"])
        monkeypatch.setenv("TIME_ENTRIES_ENABLED", "true"); get_settings.cache_clear()
        assert (await service.get(row["id"])).minutes == 15


async def test_history_survives_task_removal_and_remains_append_only(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        service = TimeEntryService(db)
        row = await service.create(entry_data(scenario))
        with internal_authority(db):
            await db.execute(delete(Task).where(Task.id == row["task_id"]))
        await db.commit()
        assert (await service.get(row["id"])).task_id == row["task_id"]
        corrected = await service.correct(row["id"], TimeEntryCorrection(work_date="2026-10-07", timezone="UTC",
            minutes=20, expected_version=1, reason="Reconciled work"))
        assert corrected["version"] == 2
        with pytest.raises(ValueError, match="append-only"):
            await db.execute(update(TimeEntryRevision).values(note="Rewrite"))
        await db.rollback()
        with pytest.raises(ValueError, match="versioned"):
            await db.execute(delete(TimeEntry))
        await db.rollback()
        assert len((await service.history(row["id"]))["items"]) == 2


async def test_history_failure_rolls_back_record_and_retry(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        service = TimeEntryService(db)
        async def fail(*_):
            raise RuntimeError("Journal write failed")
        monkeypatch.setattr(service, "append_revision", fail)
        with pytest.raises(RuntimeError, match="Journal"):
            await service.create(entry_data(scenario))
        assert await db.scalar(select(func.count()).select_from(TimeEntry)) == 0
        assert await db.scalar(select(func.count()).select_from(TimeEntryRevision)) == 0
        assert "time_entry_commands" not in db.info


async def test_independent_clients_serialize_the_daily_recorded_total(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, _ = await prepare(db, scenario, monkeypatch)
    async def write():
        async with factory() as db:
            db.info["authority"] = author
            return await TimeEntryService(db).create(entry_data(scenario).model_copy(update={"minutes": 800}))
    results = await asyncio.gather(write(), write(), return_exceptions=True)
    assert sum(isinstance(value, dict) for value in results) == 1
    assert sum(isinstance(value, ValueError) for value in results) == 1
    async with factory() as db:
        db.info["authority"] = author
        assert await db.scalar(select(func.sum(TimeEntry.minutes))) == 800


@pytest.mark.parametrize("field,value", [("minutes", 0), ("minutes", -1), ("minutes", 1.5),
    ("minutes", True), ("minutes", 1441), ("timezone", "Unknown/Zone"), ("timezone", "../etc"),
    ("work_date", "not-a-date"), ("work_date", "2026-10-07T00:00:00Z"), ("work_date", 1791331200),
    ("project_id", True), ("task_id", True)])
def test_invalid_recorded_values_are_rejected(field, value):
    payload = dict(project_id=1, request_id=str(uuid4()), work_date="2026-10-07", timezone="UTC", minutes=15)
    payload[field] = value
    with pytest.raises(ValidationError):
        TimeEntryCreate.model_validate(payload)


async def test_project_work_finite_paging_and_scope_validation(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        service = TimeEntryService(db)
        first = await service.create(entry_data(scenario).model_copy(update={"task_id": None}))
        second = await service.create(entry_data(scenario))
        page = await service.list(project_id=scenario.projects[0], limit=1)
        assert page["items"][0]["id"] == first["id"] and page["has_more"]
        later = await service.create(entry_data(scenario))
        rest = await service.list(project_id=scenario.projects[0], limit=1, after_id=page["next_after_id"], upper_id=page["upper_id"])
        assert rest["items"][0]["id"] == second["id"] and not rest["has_more"]
        assert later["id"] > rest["upper_id"]
        with pytest.raises(LookupError):
            await service.create(entry_data(scenario).model_copy(update={"task_id": scenario.tasks["other_project"]}))
        with pytest.raises(ValueError, match="leaf work"):
            await service.create(entry_data(scenario).model_copy(update={"task_id": scenario.tasks["parent"]}))
        with pytest.raises(ValueError, match="date range"):
            await service.list(start=date(2026, 10, 7), end=date(2026, 10, 6))


async def test_http_privacy_conflict_and_feature_disabled(delivery_store, monkeypatch):
    import httpx
    from app import http_authority
    from app.main import app
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, other = await prepare(db, scenario, monkeypatch)
    async def resolve(request, _db):
        if request.headers.get("X-Test-Account") == "other":
            return Authority(other, "human", projects={scenario.projects[0]: "manager"})
        return author if request.headers.get("X-Test-Account") == "author" else None
    monkeypatch.setattr(http_authority, "resolve_http_identity", resolve)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        assert (await client.get("/api/time-entries")).status_code == 401
        headers = {"X-Test-Account": "author"}
        recorded = await client.post("/api/time-entries", headers=headers, json=entry_data(scenario).model_dump(mode="json"))
        assert recorded.status_code == 201, recorded.text
        row = recorded.json()
        void_data = {"expected_version": 9, "reason": "Stale deletion"}
        conflict = await client.post(f'/api/time-entries/{row["id"]}/void', headers=headers, json=void_data)
        assert conflict.status_code == 409 and conflict.json()["detail"]["current_entry"]["version"] == 1
        assert (await client.get(f'/api/time-entries/{row["id"]}', headers={"X-Test-Account": "other"})).status_code == 404
        monkeypatch.setenv("TIME_ENTRIES_ENABLED", "false"); get_settings.cache_clear()
        assert (await client.get("/api/time-entries/capabilities", headers=headers)).json()["enabled"] is False
        assert (await client.get("/api/time-entries", headers=headers)).status_code == 404


async def test_task_snapshot_restore_does_not_rewind_recorded_time(delivery_store, monkeypatch):
    from app.schemas.task import TaskCreate, TaskUpdate
    from app.services.task_service import TaskService
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        tasks = TaskService(db)
        task = await tasks.create(None, TaskCreate(title="Recorded work", project_id=scenario.projects[0]))
        task_id = task.id
        snapshots = BacklogSnapshotService(db)
        snapshot = await snapshots.capture(scenario.projects[0])
        service = TimeEntryService(db)
        record = await service.create(entry_data(scenario).model_copy(update={"task_id": task_id}))
        await service.correct(record["id"], TimeEntryCorrection(work_date="2026-10-07", timezone="UTC", minutes=45,
            expected_version=1, reason="Reconciled against my notes"))
        task = await tasks.update(task_id, TaskUpdate(title="Later task title", expected_version=task.version))
        rows = (await db.scalars(select(Task).where(Task.project_id == scenario.projects[0], Task.iteration_id.is_(None)))).all()
        def versions(items):
            return {row.id: row.version for row in items}
        await snapshots.restore(scenario.projects[0], snapshot, versions(rows), reason="Task recovery")
        restored = await service.get(record["id"])
        assert restored.version == 2 and restored.minutes == 45
        assert [r["version"] for r in (await service.history(record["id"]))["items"]] == [1, 2]
