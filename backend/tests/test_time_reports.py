"""Recorded coverage and manager totals preserve private entry boundaries."""

from datetime import date
import pytest

from app.authority import Authority, AuthorityError
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.services.time_entry_service import TimeEntryService
from app.services.time_report_service import TimeReportService
from tests.test_delivery_scenarios import delivery_store
from tests.test_time_entries import prepare, entry_data, isolated_time_settings

START, END = date(2026, 10, 1), date(2026, 10, 31)


async def test_deleted_project_time_is_not_visible_to_replacement_manager(delivery_store, monkeypatch):
    from app.config import get_settings
    from app.schemas.project import ProjectCreate
    from app.services.project_service import ProjectService

    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, manager_id = await prepare(db, scenario, monkeypatch)
        db.info["authority"] = Authority(author.principal_id, "human", workspace_role="owner")
        original = await ProjectService(db).create(ProjectCreate(name="Original recording scope"))
        original_id = original.id
        await TimeEntryService(db).create(entry_data(scenario).model_copy(update={
            "project_id": original_id, "task_id": None, "minutes": 90}))
        # Isolate retained scope from the separately tested authenticated audit path.
        db.info.pop("authority")
        monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
        get_settings.cache_clear()
        assert await ProjectService(db).delete(original_id) == "deleted"
        monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
        get_settings.cache_clear()
        db.info["authority"] = Authority(author.principal_id, "human", workspace_role="owner")
        replacement = await ProjectService(db).create(ProjectCreate(name="Unrelated replacement"))
        db.info["authority"] = Authority(manager_id, "human", projects={replacement.id: "manager"})
        report = await TimeReportService(db).page(replacement.id, START, END, scope="project")
        assert report["totals"]["recorded_minutes"] is None, (original_id, replacement.id, report)
        assert replacement.id != original_id


async def test_personal_and_manager_totals_do_not_expose_private_records(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, other = await prepare(db, scenario, monkeypatch)
        await TimeEntryService(db).create(entry_data(scenario))
        db.info["authority"] = Authority(other, "human", projects={scenario.projects[0]: "reviewer"})
        await TimeEntryService(db).create(entry_data(scenario).model_copy(update={"minutes": 30, "note": "Other author's private evidence"}))
        with pytest.raises(AuthorityError, match="manager"):
            await TimeReportService(db).page(scenario.projects[0], START, END, scope="project")
        personal = await TimeReportService(db).page(scenario.projects[0], START, END)
        assert personal["totals"]["recorded_minutes"] == 30
        db.info["authority"] = author
        report = await TimeReportService(db).page(scenario.projects[0], START, END, scope="project")
        assert report["totals"]["recorded_minutes"] == 45
        assert "note" not in repr(report) and "principal_id" not in repr(report)
        assert "Other author's private evidence" not in await TimeReportService(db).export(scenario.projects[0], START, END)
        assert "Other author's private evidence" not in await TimeReportService(db).export(scenario.projects[0], START, END, kind="entries")
        with pytest.raises(AuthorityError, match="Only authors"):
            await TimeReportService(db).export(scenario.projects[0], START, END, scope="project", kind="entries")
        with pytest.raises(AuthorityError):
            await TimeReportService(db).page(scenario.projects[1], START, END)


async def test_unknown_time_zero_estimates_project_work_and_finite_pages(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await prepare(db, scenario, monkeypatch)
        task = await TaskService(db).create(None, TaskCreate(title="Zero estimate", project_id=scenario.projects[0], effort_hours=0))
        service = TimeReportService(db)
        empty = await service.page(scenario.projects[0], START, END)
        assert empty["totals"]["recorded_minutes"] is None
        zero = next(row for row in empty["items"] if row["task_id"] == task.id)
        assert zero["recorded_minutes"] is None and zero["estimate_hours"] == 0 and zero["estimate_state"] == "known"
        page = await service.page(scenario.projects[0], START, END, limit=1)
        later = await TaskService(db).create(None, TaskCreate(title="Later insert", project_id=scenario.projects[0]))
        rows = []
        while page["has_more"]:
            page = await service.page(scenario.projects[0], START, END, after_id=page["next_after_id"], upper_id=page["upper_id"], limit=1)
            rows.extend(page["items"])
        assert later.id not in {row["task_id"] for row in rows}
        await TimeEntryService(db).create(entry_data(scenario).model_copy(update={"task_id": None, "minutes": 25}))
        report = await service.page(scenario.projects[0], START, END)
        assert report["totals"]["project_work_minutes"] == 25 and report["totals"]["recorded_minutes"] == 25
        assert report["totals"]["tasks_with_records"] == 0


async def test_moved_task_keeps_original_scope_and_does_not_expose_new_title(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, _ = await prepare(db, scenario, monkeypatch)
        tasks = TaskService(db)
        task = await tasks.create(None, TaskCreate(title="Original scope label", project_id=scenario.projects[0], effort_hours=2.5))
        task_id = task.id
        await TimeEntryService(db).create(entry_data(scenario).model_copy(update={"task_id": task_id}))
        db.info["authority"] = Authority(author.principal_id, "human", workspace_role="owner")
        await tasks.update(task_id, TaskUpdate(project_id=scenario.projects[1], title="Private destination label", expected_version=task.version))
        db.info["authority"] = author
        report = await TimeReportService(db).page(scenario.projects[0], START, END)
        row = next(row for row in report["items"] if row["task_id"] == task_id)
        assert row["task_title"] == "Original scope label" and row["estimate_hours"] is None
        assert row["estimate_state"] == "unavailable" and row["recorded_minutes"] == 15
        assert "Private destination label" not in repr(report)


def test_csv_rejects_spreadsheet_formula_interpretation_without_manufacturing_missing_values():
    csv = TimeReportService.csv([["safe", "=SUM(A1:A2)", "  +2", "@cmd", "\tcommand", None, 0]])
    assert "'=SUM" in csv and "'  +2" in csv and "'@cmd" in csv and "'\tcommand" in csv
    assert csv.endswith(",,0\r\n")


async def test_personal_export_bound_is_explicit(delivery_store, monkeypatch):
    from datetime import timedelta
    from uuid import uuid4
    from sqlalchemy import insert
    from app.models.time_entry import TimeEntry
    from app.query_limits import CollectionLimitExceededError
    from app.utils.time import utc_now
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, _ = await prepare(db, scenario, monkeypatch)
        # Trusted fixture insertion; every nominal work date stays below the personal daily bound.
        rows = [dict(project_id=scenario.projects[0], task_id=None, principal_id=author.principal_id,
            task_title=None, request_id=str(uuid4()), creation_digest="0" * 64,
            work_date=START + timedelta(days=index // 1000), timezone="UTC", minutes=1,
            note="Synthetic export-bound row", version=1, voided=False, created_at=utc_now(), updated_at=utc_now()) for index in range(5001)]
        await db.execute(insert(TimeEntry.__table__), rows)
        await db.commit()
        with pytest.raises(CollectionLimitExceededError) as error:
            await TimeReportService(db).export(scenario.projects[0], START, END, kind="entries")
        assert error.value.maximum == 5000
