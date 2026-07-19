"""Alembic and cross-dialect DDL coverage for routing Wave 1."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from alembic import command
from alembic.script import ScriptDirectory
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

from app.config import get_settings
from app.models.agent import (
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskRoutingAssessment,
)
from app.services.upgrade_service import alembic_config


@pytest.fixture
def routing_migration_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database_path = tmp_path / "workchord_test_routing_migration.db"
    monkeypatch.setenv(
        "DATABASE_URL",
        f"sqlite+aiosqlite:///{database_path}",
    )
    get_settings.cache_clear()
    config = alembic_config()
    yield config, database_path
    get_settings.cache_clear()


def _sync_url(path: Path) -> str:
    return f"sqlite:///{path}"


@pytest.mark.sqlite
def test_upgrade_downgrade_upgrade_from_empty_database(routing_migration_config) -> None:
    config, database_path = routing_migration_config
    command.upgrade(config, "head")

    engine = create_engine(_sync_url(database_path))
    try:
        inspector = inspect(engine)
        assert {
            "agent_model_catalog_entries",
            "agent_model_bindings",
            "task_routing_assessments",
        }.issubset(inspector.get_table_names())
        assert {
            "model_binding_id",
            "model_binding_revision",
        }.issubset(
            column["name"]
            for column in inspector.get_columns("agent_task_assignments")
        )
        assert {
            "model_binding_id",
            "model_binding_revision",
            "configured_model_alias",
            "resolved_model_id",
            "model",
        }.issubset(column["name"] for column in inspector.get_columns("agent_runs"))
        with engine.connect() as connection:
            assert connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one() == "20260719_0033"
    finally:
        engine.dispose()

    command.downgrade(config, "20260711_0028")
    downgraded = create_engine(_sync_url(database_path))
    try:
        inspector = inspect(downgraded)
        assert "agent_model_bindings" not in inspector.get_table_names()
        assert "task_routing_assessments" not in inspector.get_table_names()
        assert "model_binding_id" not in {
            column["name"]
            for column in inspector.get_columns("agent_task_assignments")
        }
    finally:
        downgraded.dispose()

    command.upgrade(config, "head")
    upgraded = create_engine(_sync_url(database_path))
    try:
        with upgraded.connect() as connection:
            assert connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one() == "20260719_0033"
    finally:
        upgraded.dispose()


@pytest.mark.sqlite
def test_legacy_assignment_and_model_less_run_survive_upgrade(
    routing_migration_config,
) -> None:
    config, database_path = routing_migration_config
    command.upgrade(config, "20260711_0028")
    engine = create_engine(_sync_url(database_path))
    timestamp = datetime(2026, 7, 18, tzinfo=UTC).isoformat()
    try:
        with engine.begin() as connection:
            connection.execute(text("PRAGMA foreign_keys=ON"))
            connection.execute(
                text(
                    "INSERT INTO calendars (id, name, year) "
                    "VALUES (1, 'Legacy', 2026)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO iterations "
                    "(id, name, start_date, end_date, calendar_id) "
                    "VALUES (1, 'Legacy', '2026-07-01', '2026-07-31', 1)"
                )
            )
            connection.execute(
                text(
                    "INSERT INTO agent_actors "
                    "(id, name, display_name, api_key_hash, created_at) "
                    "VALUES (1, 'legacy-worker', 'Legacy Worker', "
                    "'legacy-worker-key-hash', :timestamp)"
                ),
                {"timestamp": timestamp},
            )
            connection.execute(
                text(
                    "INSERT INTO tasks "
                    "(id, title, iteration_id, version, claim_generation, updated_at) "
                    "VALUES (1, 'Legacy task', 1, 4, 0, :timestamp)"
                ),
                {"timestamp": timestamp},
            )
            connection.execute(
                text(
                    "INSERT INTO agent_task_assignments "
                    "(id, task_id, actor_id, purpose, queue_class, state, queue_rank, "
                    "task_version, routing_snapshot, created_at, updated_at) "
                    "VALUES (1, 1, 1, 'execution', 'normal', 'fulfilled', 1000, "
                    "4, '{}', :timestamp, :timestamp)"
                ),
                {"timestamp": timestamp},
            )
            connection.execute(
                text(
                    "INSERT INTO agent_runs "
                    "(id, task_id, actor_id, assignment_id, status, model, "
                    "run_metadata, artifact_links, started_at) "
                    "VALUES (1, 1, 1, 1, 'succeeded', NULL, '{}', '[]', :timestamp)"
                ),
                {"timestamp": timestamp},
            )
    finally:
        engine.dispose()

    command.upgrade(config, "head")
    upgraded = create_engine(_sync_url(database_path))
    try:
        with upgraded.connect() as connection:
            assignment = connection.execute(
                text(
                    "SELECT routing_snapshot, model_binding_id, "
                    "model_binding_revision FROM agent_task_assignments WHERE id = 1"
                )
            ).mappings().one()
            run = connection.execute(
                text(
                    "SELECT model, model_binding_id, model_binding_revision, "
                    "configured_model_alias, resolved_model_id "
                    "FROM agent_runs WHERE id = 1"
                )
            ).mappings().one()
        assert assignment == {
            "routing_snapshot": "{}",
            "model_binding_id": None,
            "model_binding_revision": None,
        }
        assert run == {
            "model": None,
            "model_binding_id": None,
            "model_binding_revision": None,
            "configured_model_alias": None,
            "resolved_model_id": None,
        }
    finally:
        upgraded.dispose()

    command.downgrade(config, "20260711_0028")
    command.upgrade(config, "head")
    round_tripped = create_engine(_sync_url(database_path))
    try:
        with round_tripped.connect() as connection:
            assert connection.execute(
                text("SELECT routing_snapshot FROM agent_task_assignments WHERE id = 1")
            ).scalar_one() == "{}"
            assert connection.execute(
                text("SELECT model FROM agent_runs WHERE id = 1")
            ).scalar_one_or_none() is None
    finally:
        round_tripped.dispose()


@pytest.mark.contract
def test_postgresql_ddl_contains_partial_default_and_audit_foreign_keys() -> None:
    dialect = postgresql.dialect()
    catalog_ddl = str(
        CreateTable(AgentModelCatalogEntry.__table__).compile(dialect=dialect)
    )
    binding_ddl = str(CreateTable(AgentModelBinding.__table__).compile(dialect=dialect))
    assessment_ddl = str(
        CreateTable(TaskRoutingAssessment.__table__).compile(dialect=dialect)
    )
    default_index = next(
        index
        for index in AgentModelBinding.__table__.indexes
        if index.name == "uq_agent_model_bindings_default_enabled"
    )
    default_index_ddl = str(CreateIndex(default_index).compile(dialect=dialect))

    assert "JSON" in catalog_ddl
    assert "ON DELETE RESTRICT" in binding_ddl
    assert "UNIQUE (task_id, task_version, policy_version)" in assessment_ddl
    assert "CREATE UNIQUE INDEX" in default_index_ddl
    assert "WHERE is_default AND enabled" in default_index_ddl

    assignment_fk = next(
        foreign_key
        for foreign_key in AgentTaskAssignment.__table__.c.model_binding_id.foreign_keys
    )
    run_fk = next(
        foreign_key for foreign_key in AgentRun.__table__.c.model_binding_id.foreign_keys
    )
    assert assignment_fk.ondelete == "RESTRICT"
    assert run_fk.ondelete == "RESTRICT"


@pytest.mark.contract
def test_alembic_reports_exactly_one_head() -> None:
    script = ScriptDirectory.from_config(alembic_config())
    assert script.get_heads() == ["20260719_0033"]
