"""Nonempty upgrade preservation and resumable task-domain backfill evidence."""

import importlib
from datetime import date

from alembic import command
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, JSON, MetaData, select, text
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
import pytest

from app.utils.time import utc_now
from tests.test_authority_migrations import legacy_authority_database


def insert_fixture(connection, table, **values):
    """Fill required scalar data while every relationship remains explicitly supplied."""
    for column in table.columns:
        if column.name in values or column.nullable or column.server_default is not None:
            continue
        if isinstance(column.type, Boolean):
            values[column.name] = False
        elif isinstance(column.type, Integer):
            values[column.name] = 1
        elif isinstance(column.type, Float):
            values[column.name] = 1.0
        elif isinstance(column.type, DateTime):
            values[column.name] = utc_now()
        elif isinstance(column.type, Date):
            values[column.name] = date(2026, 1, 1)
        elif isinstance(column.type, JSON):
            values[column.name] = {}
        else:
            values[column.name] = "fixture"
    connection.execute(table.insert().values(**values))


def test_nonempty_domain_upgrade_preserves_ids_history_and_backfill_provenance(legacy_authority_database):
    config, engine = legacy_authority_database
    command.upgrade(config, "20260915_0037")
    old = MetaData()
    old.reflect(engine)
    t = old.tables
    with engine.begin() as db:
        insert_fixture(db, t["calendars"], id=91, name="Calendar", year=2026, holidays=[], weekend_days=[5, 6], short_days=[])
        insert_fixture(db, t["projects"], id=61, name="Project", status="planned", health="unknown")
        insert_fixture(db, t["iterations"], id=51, name="Iteration", calendar_id=91, project_id=61, start_date=date(2026, 1, 1), end_date=date(2026, 1, 31))
        insert_fixture(db, t["team_member_profiles"], id=71, display_name="Person", profile_kind="human", assignment_modes=[])
        insert_fixture(db, t["team_members"], id=81, iteration_id=51, profile_id=71, name="Person", position="Engineer")
        insert_fixture(db, t["team_members"], id=82, iteration_id=51, name="Unlinked allocation", position="Engineer")
        for task_id, member in ((101, 81), (102, 82)):
            insert_fixture(db, t["tasks"], id=task_id, iteration_id=51, project_id=61, assignee_id=member, title=f"Task {task_id}",
                effort_days=1, effort_hours=8, status="planned", tags="[]", is_summary=False, claim_generation=0, baseline_provenance="legacy_unknown")
        insert_fixture(db, t["task_dependencies"], id=151, task_id=102, depends_on_id=101)
        insert_fixture(db, t["task_status_logs"], id=201, task_id=101, from_status="planned", to_status="active", triggered_by="user", affected_task_ids="[]")
        insert_fixture(db, t["task_events"], id=301, task_id=101, actor_type="user", event_type="legacy_event", payload='{"preserve":true}')
        insert_fixture(db, t["task_schedule_baselines"], id=351, task_id=101, revision=1, timezone="UTC", reason="Original commitment")
        insert_fixture(db, t["application_snapshots"], id=401, iteration_id=51, filename="original.json", schema_version=2,
            input_revision=1, payload={"tasks": [{"id": 101}]}, checksum="a" * 64, provenance="command")
    names = ["task_status_logs", "task_events", "task_dependencies", "task_schedule_baselines", "application_snapshots"]
    with engine.connect() as db:
        before = {name: db.execute(select(t[name]).order_by(t[name].c.id)).all() for name in names}
        db.rollback()
        config.attributes["connection"] = db
        try:
            command.upgrade(config, "head")
        finally:
            config.attributes.pop("connection", None)
    current = MetaData()
    current.reflect(engine)
    with engine.connect() as db:
        for name in names:
            assert db.execute(select(*[current.tables[name].c[column.name] for column in t[name].columns]).order_by(current.tables[name].c.id)).all() == before[name]
        rows = db.execute(select(current.tables["tasks"]).order_by(current.tables["tasks"].c.id)).mappings().all()
        assert [row["id"] for row in rows] == [101, 102]
        assert rows[0]["owner_profile_id"] == 71 and rows[0]["ownership_provenance"] == "legacy_capacity_link"
        assert rows[1]["owner_profile_id"] is None and rows[1]["ownership_provenance"] == "legacy_unlinked"
        assert rows[0]["effort_hours"] is None and rows[0]["estimate_provenance"] == "unknown"
        assert rows[0]["legacy_estimate"] == {"effort_days": 1, "effort_hours": 8}
        assert all(row["domain_backfill_version"] == 1 for row in rows)
        if engine.dialect.name == "sqlite":
            assert db.exec_driver_sql("PRAGMA foreign_key_check").all() == []


def test_backfill_cursor_resumes_without_rewriting_completed_rows(legacy_authority_database):
    config, engine = legacy_authority_database
    command.upgrade(config, "head")
    schema = MetaData()
    schema.reflect(engine)
    t = schema.tables
    with engine.begin() as db:
        insert_fixture(db, t["projects"], id=61, name="Backfill project", status="planned", health="unknown")
        for task_id in (101, 102):
            insert_fixture(db, t["tasks"], id=task_id, project_id=61, title="Imported legacy work", status="planned", effort_days=1,
                effort_hours=8, tags="[]", domain_backfill_version=0, is_summary=False, claim_generation=0)
    migration = importlib.import_module("app.migrations.versions.20260915_0038_canonical_task_domain")
    with engine.begin() as db:
        dry_run = migration.backfill_tasks(db, limit=1, apply=False)
        assert dry_run[0]["task_id"] == 101
        assert db.execute(select(t["tasks"].c.domain_backfill_version).where(t["tasks"].c.id == 101)).scalar_one() == 0
        first = migration.backfill_tasks(db, limit=1)
    # A new connection represents resumption after the first committed chunk.
    with engine.begin() as db:
        assert migration.backfill_tasks(db, after_id=first[-1]["task_id"], limit=1)[0]["task_id"] == 102
    with engine.begin() as db:
        assert migration.backfill_tasks(db) == []
        assert db.execute(select(t["tasks"].c.legacy_estimate).order_by(t["tasks"].c.id)).scalars().all() == [
            {"effort_days": 1, "effort_hours": 8}, {"effort_days": 1, "effort_hours": 8}]


def test_deletion_fence_upgrade_preserves_unknown_history_and_survives_without_tasks(legacy_authority_database):
    config, engine = legacy_authority_database
    command.upgrade(config, "20260915_0038")
    command.upgrade(config, "head")
    schema = MetaData()
    schema.reflect(engine)
    fence = schema.tables["task_deletion_fences"]
    assert inspect(engine).get_foreign_keys(fence.name) == []
    with engine.begin() as db:
        assert db.execute(select(fence)).all() == []
        db.execute(fence.insert().values(original_task_id=9001, last_version=17))
    with engine.begin() as db:
        assert db.execute(select(fence.c.last_version).where(fence.c.original_task_id == 9001)).scalar_one() == 17
    with pytest.raises(IntegrityError), engine.begin() as db:
        db.execute(fence.insert().values(original_task_id=9002, last_version=0))
