"""Real PostgreSQL migration, locking, and schema contract tests."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import threading

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app import models  # noqa: F401 - register mapped metadata
from app.config import get_settings
from app.database import Base
from app.database_config import parse_database_configuration
from app.services.upgrade_service import (
    UpgradeError,
    alembic_config,
    bootstrap_database_schema,
    head_revision,
    inspect_database,
    run_alembic_upgrade,
)
from tests.support import cross_dialect_schema_diff, schema_snapshot


def sync_engine(database_url: str):
    return create_engine(database_url, poolclass=NullPool)


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
def test_runtime_role_cannot_create_schema_objects_or_roles(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    engine = sync_engine(postgres_database.url).execution_options(
        isolation_level="AUTOCOMMIT"
    )
    try:
        with engine.connect() as connection:
            connection.execute(
                text(f'SET ROLE "{postgres_database.runtime_role}"')
            )
            with pytest.raises(DBAPIError):
                connection.execute(text("CREATE TABLE workchord.runtime_forbidden (id int)"))
            with pytest.raises(DBAPIError):
                connection.execute(text("CREATE ROLE runtime_forbidden"))
            connection.execute(text("RESET ROLE"))
            assert connection.execute(
                text(
                    "SELECT to_regclass('workchord.runtime_forbidden') IS NULL"
                )
            ).scalar_one() is True
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_nonempty_postgresql_upgrade_requires_external_backup_gate(
    postgres_database,
    configure_database,
    monkeypatch,
) -> None:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    original_head = head_revision()
    monkeypatch.setattr("app.services.upgrade_service.head_revision", lambda: "future_revision")

    with pytest.raises(UpgradeError, match="backup/PITR"):
        run_alembic_upgrade(backup=False, run_repairs=False)

    assert inspect_database().current_revision == original_head


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
        from app.utils.time import UTCDateTime
        utc_columns = [(table.name, column.name) for table in Base.metadata.tables.values()
                       for column in table.columns if isinstance(column.type, UTCDateTime)]
        for table_name, column_name in utc_columns:
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
