"""Dual-dialect migration coverage for the autonomous control-plane mirror."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.script import ScriptDirectory
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.config import get_settings
from app.models.autonomy import (
    AgentAutonomyTopologyMember,
    AgentObservationJob,
    AgentVerificationEvent,
    AgentVerificationRequirement,
)
from app.services.upgrade_service import alembic_config


@pytest.fixture
def autonomy_migration_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database_path = tmp_path / "workchord_test_autonomy_migration.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{database_path}")
    get_settings.cache_clear()
    config = alembic_config()
    yield config, database_path
    get_settings.cache_clear()


@pytest.mark.sqlite
def test_autonomy_projection_upgrade_downgrade_upgrade(autonomy_migration_config) -> None:
    config, database_path = autonomy_migration_config
    command.upgrade(config, "head")
    engine = create_engine(f"sqlite:///{database_path}")
    try:
        inspector = inspect(engine)
        expected = {
            "agent_autonomy_topologies",
            "agent_autonomy_topology_members",
            "agent_work_packages",
            "agent_verification_requirements",
            "agent_verification_events",
            "agent_observation_jobs",
        }
        assert expected.issubset(inspector.get_table_names())
        assert {
            "artifact_set_digest",
            "contract_manifest_digest",
            "external_journal_revision",
            "external_journal_head_digest",
        }.issubset(
            column["name"] for column in inspector.get_columns("agent_work_packages")
        )
        with engine.connect() as connection:
            assert connection.execute(
                text("SELECT version_num FROM alembic_version")
                ).scalar_one() == "20260728_0035"
    finally:
        engine.dispose()

    command.downgrade(config, "20260718_0032")
    downgraded = create_engine(f"sqlite:///{database_path}")
    try:
        inspector = inspect(downgraded)
        assert "agent_work_packages" not in inspector.get_table_names()
        assert "agent_autonomy_topologies" not in inspector.get_table_names()
    finally:
        downgraded.dispose()

    command.upgrade(config, "head")
    upgraded = create_engine(f"sqlite:///{database_path}")
    try:
        with upgraded.connect() as connection:
            assert connection.execute(
                text("SELECT version_num FROM alembic_version")
                ).scalar_one() == "20260728_0035"
    finally:
        upgraded.dispose()


@pytest.mark.contract
def test_autonomy_projection_postgresql_ddl_preserves_fences() -> None:
    dialect = postgresql.dialect()
    member_ddl = str(
        CreateTable(AgentAutonomyTopologyMember.__table__).compile(dialect=dialect)
    )
    requirement_ddl = str(
        CreateTable(AgentVerificationRequirement.__table__).compile(dialect=dialect)
    )
    observation_ddl = str(
        CreateTable(AgentObservationJob.__table__).compile(dialect=dialect)
    )
    assert "REFERENCES agent_autonomy_topologies (id) ON DELETE RESTRICT" in member_ddl
    assert "REFERENCES agent_work_packages (id) ON DELETE RESTRICT" in requirement_ddl
    assert "REFERENCES agent_verification_requirements (id) ON DELETE RESTRICT" in str(
        CreateTable(AgentVerificationEvent.__table__).compile(dialect=dialect)
    )
    assert "executor_independence_group <> verifier_independence_group" in requirement_ddl
    assert "attempt_start_digest IS NOT NULL" in requirement_ddl
    assert "minimum_elapsed_seconds >= 1" in observation_ddl
    assert "starts_at < due_at AND due_at < valid_until" in observation_ddl


@pytest.mark.contract
def test_autonomy_migration_chain_has_one_head() -> None:
    script = ScriptDirectory.from_config(alembic_config())
    assert script.get_heads() == ["20260728_0035"]
