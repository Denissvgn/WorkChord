"""SQLite side of the fresh/legacy/inspection migration matrix."""

from __future__ import annotations

from datetime import UTC
from pathlib import Path
import sqlite3

from alembic import command
import pytest
from sqlalchemy import create_engine, inspect, select, text
from sqlalchemy.orm import Session

from app import models  # noqa: F401 - register mapped metadata
from app.database import Base
from app.models.task_status_log import TaskStatusLog
from app.services.upgrade_service import (
    LEGACY_BASELINE_REVISION,
    UpgradeError,
    alembic_config,
    assert_database_current,
    bootstrap_database_schema,
    head_revision,
    inspect_database,
    run_alembic_upgrade,
)
from tests.support import schema_snapshot


def sqlite_url(path: Path) -> str:
    return f"sqlite+aiosqlite:///{path}"


def seed_legacy_baseline(database_path: Path) -> None:
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            "INSERT INTO calendars (id, name, year) VALUES (1, 'Legacy', 2026)"
        )
        connection.execute(
            "INSERT INTO iterations "
            "(id, name, start_date, end_date, calendar_id) "
            "VALUES (1, 'Legacy iteration', '2026-01-01', '2026-01-31', 1)"
        )
        connection.execute(
            "INSERT INTO team_members (id, name, position, iteration_id) "
            "VALUES (1, 'Legacy member', 'Developer', 1)"
        )
        connection.execute(
            "INSERT INTO tasks (id, title, iteration_id) "
            "VALUES (1, 'Legacy task', 1)"
        )
        connection.execute(
            "INSERT INTO task_status_logs "
            "(id, task_id, from_status, to_status, changed_at, triggered_by) "
            "VALUES (1, 1, 'planned', 'active', '2026-01-02 03:04:05', 'user')"
        )


def test_single_head_invariant() -> None:
    assert head_revision() == "20260718_0031"


@pytest.mark.sqlite
def test_schema_only_bootstrap_is_current_and_data_empty(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "schema-only.db"
    configure_database(sqlite_url(path))

    before, backup, after = bootstrap_database_schema()

    assert before.state == "empty"
    assert backup is None
    assert after.state == "alembic_managed"
    assert after.is_current
    engine = create_engine(f"sqlite:///{path}")
    try:
        snapshot = schema_snapshot(engine)
        assert set(snapshot) == set(Base.metadata.tables)
        with engine.connect() as connection:
            for table_name in sorted(snapshot):
                quoted = connection.dialect.identifier_preparer.quote(table_name)
                assert connection.execute(
                    text(f"SELECT count(*) FROM {quoted}")
                ).scalar_one() == 0
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_representative_legacy_sqlite_upgrades_with_explicit_semantics(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "legacy.db"
    configure_database(sqlite_url(path))
    command.upgrade(alembic_config(), LEGACY_BASELINE_REVISION)
    seed_legacy_baseline(path)

    before, backup, after = run_alembic_upgrade(
        backup=False,
        run_repairs=False,
    )

    assert before.current_revision == LEGACY_BASELINE_REVISION
    assert backup is None
    assert after.current_revision == head_revision()
    engine = create_engine(f"sqlite:///{path}")
    try:
        with engine.connect() as connection:
            calendar = connection.execute(
                text(
                    "SELECT holidays, weekend_days, short_days FROM calendars WHERE id = 1"
                )
            ).one()
            member = connection.execute(
                text(
                    "SELECT availability_percent, professionalism_coefficient, "
                    "operational_utilization FROM team_members WHERE id = 1"
                )
            ).one()
            task = connection.execute(
                text(
                    "SELECT priority, effort_days, effort_hours, status, is_optional, "
                    "is_deferred, sort_order FROM tasks WHERE id = 1"
                )
            ).one()
        assert calendar == ("[]", "[5, 6]", "[]")
        assert member == (100.0, 1.0, 20.0)
        assert task == (5, 1.0, 8.0, "planned", 0, 0, 0)
        with Session(engine) as session:
            changed_at = session.scalar(
                select(TaskStatusLog.changed_at).where(TaskStatusLog.id == 1)
            )
        assert changed_at is not None
        assert changed_at.tzinfo == UTC
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_live_schema_column_contract_matches_model_metadata(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "metadata.db"
    configure_database(sqlite_url(path))
    bootstrap_database_schema()
    engine = create_engine(f"sqlite:///{path}")
    try:
        inspector = inspect(engine)
        for table_name, model_table in Base.metadata.tables.items():
            live_columns = {
                column["name"]: column
                for column in inspector.get_columns(table_name)
            }
            assert set(live_columns) == {column.name for column in model_table.columns}
            for model_column in model_table.columns:
                assert live_columns[model_column.name]["nullable"] == model_column.nullable
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_unknown_nonempty_schema_is_refused(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "unknown.db"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE foreign_application_data (id INTEGER)")
    configure_database(sqlite_url(path))

    with pytest.raises(UpgradeError, match="not recognized"):
        run_alembic_upgrade(backup=False, run_repairs=False)


@pytest.mark.sqlite
def test_unknown_alembic_revision_is_refused(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "unknown-revision.db"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
        )
        connection.execute(
            "INSERT INTO alembic_version (version_num) VALUES ('not_a_revision')"
        )
    configure_database(sqlite_url(path))

    with pytest.raises(UpgradeError, match="unknown Alembic revision"):
        run_alembic_upgrade(backup=False, run_repairs=False)


@pytest.mark.sqlite
def test_startup_assertion_refuses_stale_schema_without_mutation(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "stale.db"
    configure_database(sqlite_url(path))
    command.upgrade(alembic_config(), LEGACY_BASELINE_REVISION)

    with pytest.raises(UpgradeError, match="Database schema is not ready"):
        assert_database_current()

    assert inspect_database().current_revision == LEGACY_BASELINE_REVISION


@pytest.mark.sqlite
def test_target_alignment_revision_supports_reviewed_downgrade(
    tmp_path: Path,
    configure_database,
) -> None:
    path = tmp_path / "downgrade.db"
    configure_database(sqlite_url(path))
    bootstrap_database_schema()

    command.downgrade(alembic_config(), "20260718_0030")
    assert inspect_database().current_revision == "20260718_0030"
    command.upgrade(alembic_config(), "head")
    assert inspect_database().current_revision == head_revision()


def test_alembic_config_preserves_percent_encoded_values(configure_database) -> None:
    database_url = "sqlite+aiosqlite:////tmp/workchord%25encoded.db"
    configure_database(database_url)
    assert alembic_config().get_main_option("sqlalchemy.url") == (
        "sqlite:////tmp/workchord%25encoded.db"
    )
