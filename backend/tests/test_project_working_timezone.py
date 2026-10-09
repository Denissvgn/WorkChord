"""Declared project working zones survive transport and drive local work dates."""

from datetime import UTC, date, datetime

import httpx
import pytest

from app.main import app
from app.models.identity import WorkspaceMembership
from app.schemas.task import TaskCreate
from app.schemas.task_domain import TaskActionRequest
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService
from app.services.work_metrics import task_signals, working_today
from tests.test_managed_authority import managed_store, client
from tests.test_delivery_scenarios import delivery_store


@pytest.mark.parametrize("zone", ["Asia/Tokyo", "America/Los_Angeles"])
async def test_managed_creation_read_and_update_preserve_declared_zone(managed_store, zone):
    factory, _, tokens, principal_ids = managed_store
    async with factory() as db:
        db.add(WorkspaceMembership(principal_id=principal_ids[0], role="owner"))
        await db.commit()
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0", "Origin": "https://test"}) as owner:
        created = await owner.post("/api/projects", json={"name": "Zoned work", "timezone": zone})
        assert created.status_code == 201, created.text
        project_id = created.json()["id"]
        assert created.json()["timezone"] == zone
        read = await owner.get(f"/api/projects/{project_id}")
        assert read.json()["timezone"] == zone
        updated = await owner.put(f"/api/projects/{project_id}", json={"description": "Keep declared zone"})
        assert updated.status_code == 200 and updated.json()["timezone"] == zone
        default = await owner.post("/api/projects", json={"name": "Default working zone"})
        assert default.status_code == 201 and default.json()["timezone"] == "UTC"
        invalid = await owner.post("/api/projects", json={"name": "Invalid zone", "timezone": "Not/ARealZone"})
        assert invalid.status_code == 422


@pytest.mark.parametrize(("zone", "expected"), [
    ("Asia/Tokyo", date(2026, 1, 21)), ("America/Los_Angeles", date(2026, 1, 20))])
async def test_project_zone_drives_actual_manual_day_and_metric_day(managed_store, monkeypatch, zone, expected):
    from app.authority import Authority
    from app.schemas.project import ProjectCreate
    from app.services.project_service import ProjectService
    from app.services import work_metrics
    from app.utils import time

    factory, _, _, principal_ids = managed_store
    instant = datetime(2026, 1, 20, 23, 30, tzinfo=UTC)
    monkeypatch.setattr(work_metrics, "utc_now", lambda: instant)
    monkeypatch.setattr(time, "utc_now", lambda: instant)
    async with factory() as db:
        db.info["authority"] = Authority(principal_ids[0], "human", workspace_role="owner")
        project = await ProjectService(db).create(ProjectCreate(name="Boundary work", timezone=zone))
        task = await TaskService(db).create(None, TaskCreate(title="Unscheduled work", project_id=project.id))
        started = await TaskDomainService(db).command(task.id, TaskActionRequest(
            action="start_manual", expected_version=task.version, reason="Manual boundary execution"))
        assert started.actual_start_date == expected
        assert working_today(zone, instant) == expected
        current = await TaskService(db).get_by_id(task.id)
        current.end_date = date(2026, 1, 20)
        assert task_signals(current, timezone=zone, now=instant)["is_overdue"] is (expected > date(2026, 1, 20))
