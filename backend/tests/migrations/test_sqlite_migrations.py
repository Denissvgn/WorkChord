"""SQLite side of the fresh schema and inspection migration matrix."""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pytest
from sqlalchemy import create_engine, inspect, text

from app import models  # noqa: F401 - register mapped metadata
from app.database import Base
from app.services.upgrade_service import (
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


def test_single_head_invariant() -> None:
    assert head_revision() == "20261004_0007"


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
    bootstrap_database_schema()
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE alembic_version SET version_num = 'unreleased_revision'")

    with pytest.raises(UpgradeError, match="Database schema is not ready"):
        assert_database_current()

    assert inspect_database().current_revision == "unreleased_revision"


def test_alembic_config_preserves_percent_encoded_values(configure_database) -> None:
    database_url = "sqlite+aiosqlite:////tmp/workchord%25encoded.db"
    configure_database(database_url)
    assert alembic_config().get_main_option("sqlalchemy.url") == (
        "sqlite:////tmp/workchord%25encoded.db"
    )
