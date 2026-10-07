"""Initial schema and cross-dialect routing constraints."""

from __future__ import annotations

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
def test_routing_schema_from_empty_database(routing_migration_config) -> None:
    config, database_path = routing_migration_config
    command.upgrade(config, "20260928_0001")

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
            "model_trust_state",
            "model_match_basis",
            "model",
        }.issubset(column["name"] for column in inspector.get_columns("agent_runs"))
        with engine.connect() as connection:
            assert connection.execute(
                text("SELECT version_num FROM alembic_version")
            ).scalar_one() == "20260928_0001"
    finally:
        engine.dispose()

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
    assert script.get_heads() == ["20261007_0008"]
