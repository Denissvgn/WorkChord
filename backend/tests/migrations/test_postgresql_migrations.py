"""Real PostgreSQL migration, locking, and schema contract tests."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC
import importlib
import json
import os
from pathlib import Path
import threading

from alembic import command
import pytest
from sqlalchemy import create_engine, inspect, select, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app import models  # noqa: F401 - register mapped metadata
from app.config import get_settings
from app.database import Base
from app.database_config import parse_database_configuration
from app.models.task_status_log import TaskStatusLog
from app.services.upgrade_service import (
    LEGACY_BASELINE_REVISION,
    UpgradeError,
    alembic_config,
    bootstrap_database_schema,
    head_revision,
    inspect_database,
    run_alembic_upgrade,
)
from tests.support import cross_dialect_schema_diff, schema_snapshot


ALIGNMENT_MIGRATION = importlib.import_module(
    "app.migrations.versions.20260718_0031_align_postgresql_types"
)


def sync_engine(database_url: str):
    return create_engine(database_url, poolclass=NullPool)


def seed_postgresql_legacy_baseline(database_url: str) -> None:
    engine = sync_engine(database_url)
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO calendars (id, name, year) "
                    "VALUES (100, 'Legacy', 2026)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO iterations "
                    "(id, name, start_date, end_date, calendar_id) "
                    "VALUES (100, 'Legacy iteration', '2026-01-01', "
                    "'2026-01-31', 100)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO team_members (id, name, position, iteration_id) "
                    "VALUES (100, 'Legacy member', 'Developer', 100)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO tasks (id, title, iteration_id) "
                    "VALUES (100, 'Legacy task', 100)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO task_status_logs "
                    "(id, task_id, from_status, to_status, changed_at, triggered_by) "
                    "VALUES (100, 100, 'planned', 'active', "
                    "'2026-01-02 03:04:05', 'user')"
                )
            )
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_fresh_postgresql_schema_only_bootstrap(postgres_database, configure_database) -> None:
    configure_database(postgres_database.url)

    before, _, after = bootstrap_database_schema()

    assert before.state == "empty"
    assert after.current_revision == head_revision()
    assert after.table_count == len(Base.metadata.tables) + 1
    assert postgres_database.encoding == "UTF8"
    assert postgres_database.locale_provider == "builtin"
    assert postgres_database.locale == "PG_UNICODE_FAST"
    assert postgres_database.timezone in {"UTC", "Etc/UTC"}
    assert postgres_database.search_path.replace(" ", "") == "workchord,pg_catalog"
    assert postgres_database.role_timezone in {"UTC", "Etc/UTC"}
    assert (
        postgres_database.role_search_path.replace(" ", "")
        == "workchord,pg_catalog"
    )
    assert postgres_database.runtime_can_create_public is False
    assert postgres_database.runtime_can_create_application_schema is False
    assert postgres_database.default_table_privileges == (
        "DELETE",
        "INSERT",
        "SELECT",
        "UPDATE",
    )
    assert postgres_database.default_sequence_privileges == (
        "SELECT",
        "UPDATE",
        "USAGE",
    )

    engine = sync_engine(postgres_database.url)
    try:
        with engine.connect() as connection:
            runtime_role = postgres_database.runtime_role
            assert connection.execute(
                text(
                    "SELECT has_table_privilege(:role, "
                    "'workchord.alembic_version', 'SELECT')"
                ),
                {"role": runtime_role},
            ).scalar_one() is True
            assert connection.execute(
                text(
                    "SELECT has_table_privilege(:role, "
                    "'workchord.tasks', 'INSERT, SELECT, UPDATE, DELETE')"
                ),
                {"role": runtime_role},
            ).scalar_one() is True
            assert connection.execute(
                text(
                    "SELECT has_sequence_privilege(:role, "
                    "'workchord.calendars_id_seq', 'USAGE, SELECT, UPDATE')"
                ),
                {"role": runtime_role},
            ).scalar_one() is True
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_postgresql_legacy_to_head_repairs_utc_nullability_and_sequences(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    command.upgrade(alembic_config(), LEGACY_BASELINE_REVISION)
    seed_postgresql_legacy_baseline(postgres_database.url)

    before, _, after = run_alembic_upgrade(
        backup=False,
        run_repairs=False,
        external_backup_reference="test-fixture-recovery-point",
    )

    assert before.current_revision == LEGACY_BASELINE_REVISION
    assert after.current_revision == head_revision()
    engine = sync_engine(postgres_database.url)
    try:
        with engine.begin() as connection:
            task = connection.execute(
                text(
                    "SELECT priority, effort_days, effort_hours, status, is_optional, "
                    "is_deferred, sort_order FROM tasks WHERE id = 100"
                )
            ).one()
            next_calendar_id = connection.execute(
                text(
                    "INSERT INTO calendars "
                    "(name, year, holidays, weekend_days, short_days) "
                    "VALUES ('Sequence probe', 2027, '[]', '[5, 6]', '[]') "
                    "RETURNING id"
                )
            ).scalar_one()
        assert task == (5, 1.0, 8.0, "planned", False, False, 0)
        assert next_calendar_id == 101
        with Session(engine) as session:
            changed_at = session.scalar(
                select(TaskStatusLog.changed_at).where(TaskStatusLog.id == 100)
            )
        assert changed_at is not None
        assert changed_at.tzinfo == UTC
        assert changed_at.isoformat() == "2026-01-02T03:04:05+00:00"
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_nonempty_postgresql_upgrade_requires_external_backup_gate(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    command.upgrade(alembic_config(), LEGACY_BASELINE_REVISION)

    with pytest.raises(UpgradeError, match="backup/PITR"):
        run_alembic_upgrade(backup=False, run_repairs=False)

    assert inspect_database().current_revision == LEGACY_BASELINE_REVISION


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_concurrent_postgresql_migration_runners_serialize(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    barrier = threading.Barrier(2)

    def migrate() -> str:
        barrier.wait(timeout=10)
        _before, _backup, after = run_alembic_upgrade(
            backup=False,
            run_repairs=False,
        )
        return after.current_revision or ""

    with ThreadPoolExecutor(max_workers=2) as executor:
        revisions = list(executor.map(lambda _index: migrate(), range(2)))

    assert revisions == [head_revision(), head_revision()]


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_postgresql_utc_types_partial_indexes_and_sequence_ownership(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    engine = sync_engine(postgres_database.url)
    try:
        inspector = inspect(engine)
        for table_name, column_name in ALIGNMENT_MIGRATION.UTC_COLUMNS:
            columns = {
                column["name"]: column
                for column in inspector.get_columns(table_name)
            }
            assert columns[column_name]["type"].timezone is True

        partial_indexes = {
            index["name"]: index
            for table_name in Base.metadata.tables
            for index in inspector.get_indexes(table_name)
            if index["name"].startswith("uq_")
        }
        assert {
            "uq_agent_task_assignments_live_purpose",
            "uq_agent_runs_running_assignment",
            "uq_agent_run_events_run_id_idempotency_key",
            "uq_task_events_agent_idempotency_key",
            "uq_agent_model_bindings_default_enabled",
        }.issubset(partial_indexes)

        with engine.connect() as connection:
            sequence_rows = connection.execute(
                text(
                    """
                    SELECT table_name, column_name,
                           pg_get_serial_sequence(
                               format('%I.%I', table_schema, table_name),
                               column_name
                           ) AS sequence_name
                    FROM information_schema.columns
                    WHERE table_schema = current_schema()
                      AND column_default LIKE 'nextval(%'
                    ORDER BY table_name, column_name
                    """
                )
            ).mappings().all()
        assert sequence_rows
        assert all(row["sequence_name"] for row in sequence_rows)
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_sync_postgresql_driver_select_one(postgres_database, configure_database) -> None:
    configure_database(postgres_database.url)
    configuration = parse_database_configuration(get_settings())
    engine = create_engine(
        configuration.sync_url,
        poolclass=NullPool,
        connect_args=dict(configuration.connect_args),
    )
    try:
        with engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_async_postgresql_driver_select_one(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    configuration = parse_database_configuration(get_settings())
    engine = create_async_engine(
        configuration.async_url,
        **configuration.async_engine_kwargs(),
    )
    try:
        async with engine.connect() as connection:
            assert (await connection.execute(text("SELECT 1"))).scalar_one() == 1
    finally:
        await engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_cross_dialect_schema_diff_is_machine_readable(
    postgres_database,
    configure_database,
    tmp_path: Path,
) -> None:
    sqlite_path = tmp_path / "schema-diff.db"
    configure_database(f"sqlite+aiosqlite:///{sqlite_path}")
    bootstrap_database_schema()
    sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")
    try:
        sqlite_contract = schema_snapshot(sqlite_engine)
    finally:
        sqlite_engine.dispose()

    configure_database(postgres_database.url)
    bootstrap_database_schema()
    postgresql_engine = sync_engine(postgres_database.url)
    try:
        postgresql_contract = schema_snapshot(postgresql_engine)
    finally:
        postgresql_engine.dispose()

    difference = cross_dialect_schema_diff(
        sqlite_contract,
        postgresql_contract,
    )
    artifact_path = Path(
        os.environ.get(
            "WORKCHORD_SCHEMA_DIFF_ARTIFACT",
            str(tmp_path / "schema-diff.json"),
        )
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(difference, indent=2, sort_keys=True) + "\n")

    assert difference["missing_from_sqlite"] == []
    assert difference["missing_from_postgresql"] == []
    assert difference["structural_differences"] == []
    assert all(
        item["sqlite"]["family"] == item["postgresql"]["family"] == "datetime"
        and item["sqlite"]["timezone"] is False
        and item["postgresql"]["timezone"] is True
        for item in difference["column_type_differences"]
    )
    assert artifact_path.is_file()
