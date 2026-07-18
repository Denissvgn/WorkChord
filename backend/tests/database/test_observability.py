"""DBM-OBS-001 readiness, drain, and safe-metrics tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.exc import TimeoutError as SQLAlchemyTimeoutError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.config import get_settings
from app.observability import install_database_instrumentation, readiness_snapshot
from app.runtime_telemetry import MetricRegistry, activity


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    yield
    get_settings.cache_clear()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_stale_schema_is_live_but_not_database_ready(
    db_session_factory: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("app.database.async_session_maker", db_session_factory)
    monkeypatch.setattr("app.observability.head_revision", lambda: "wave2-head")
    monkeypatch.setattr(
        "app.database.database_runtime_summary",
        lambda: {"backend": "sqlite", "url": "sqlite:///[redacted]"},
    )

    ready, payload = await readiness_snapshot()

    assert ready is False
    assert payload["status"] == "not_ready"
    assert payload["database"]["connected"] is True
    assert payload["database"]["schema_current"] is False
    assert payload["database"]["schema_error_kind"] == "OperationalError"


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_current_schema_exports_queue_process_and_drain_evidence(
    db_session_factory: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with db_session_factory() as db:
        await db.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(64))"))
        await db.execute(
            text("INSERT INTO alembic_version (version_num) VALUES ('wave2-head')")
        )
        await db.commit()

    monkeypatch.setenv("MAINTENANCE_MODE", "validation-only")
    monkeypatch.setenv("MAINTENANCE_REVISION", "ready-test")
    monkeypatch.setenv("MAINTENANCE_REPLICA_ID", "ready-replica")
    get_settings.cache_clear()
    monkeypatch.setattr("app.database.async_session_maker", db_session_factory)
    monkeypatch.setattr("app.observability.head_revision", lambda: "wave2-head")
    monkeypatch.setattr(
        "app.database.database_runtime_summary",
        lambda: {"backend": "sqlite", "url": "sqlite:///[redacted]"},
    )

    ready, payload = await readiness_snapshot()

    assert ready is True
    assert payload["database"]["connected"] is True
    assert payload["database"]["schema_current"] is True
    assert payload["migration_gate"] == {
        "clear": True,
        "blocking_run_id": None,
        "blocking_status": None,
        "error_kind": None,
    }
    assert payload["queue"] == {
        "ready_depth": 0,
        "oldest_ready_age_seconds": 0.0,
        "active_leases": 0,
        "error_kind": None,
    }
    assert payload["writer_drain"]["drained"] is True
    assert payload["writer_drain"]["replica_agreement_required"] is True
    assert payload["process"]["active_transactions"] == 0
    assert payload["maintenance"]["replica_id"] == "ready-replica"
    assert len(payload["maintenance"]["configuration_fingerprint"]) == 64


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_incomplete_migration_gate_keeps_current_schema_unready(
    db_session_factory: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with db_session_factory() as db:
        await db.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(64))"))
        await db.execute(
            text("INSERT INTO alembic_version (version_num) VALUES ('wave3-head')")
        )
        await db.execute(
            text(
                "INSERT INTO database_migration_gates ("
                "run_id, source_manifest_sha256, source_snapshot_sha256, "
                "target_identity_sha256, status, completed_tables, created_at, updated_at"
                ") VALUES ('run-1', :source, :snapshot, :target, 'loaded', '[]', "
                ":created, :updated)"
            ),
            {
                "source": "a" * 64,
                "snapshot": "b" * 64,
                "target": "c" * 64,
                "created": "2026-07-18 12:00:00",
                "updated": "2026-07-18 12:00:00",
            },
        )
        await db.commit()

    monkeypatch.setattr("app.database.async_session_maker", db_session_factory)
    monkeypatch.setattr("app.observability.head_revision", lambda: "wave3-head")
    monkeypatch.setattr(
        "app.database.database_runtime_summary",
        lambda: {"backend": "sqlite", "url": "sqlite:///[redacted]"},
    )

    ready, payload = await readiness_snapshot()

    assert ready is False
    assert payload["database"]["schema_current"] is True
    assert payload["migration_gate"]["clear"] is False
    assert payload["migration_gate"]["blocking_run_id"] == "run-1"
    assert payload["migration_gate"]["blocking_status"] == "loaded"


class FailingSession:
    async def execute(self, _statement: Any) -> None:
        raise SQLAlchemyTimeoutError("test pool timeout")

    async def rollback(self) -> None:
        return None


class FailingSessionContext:
    async def __aenter__(self) -> FailingSession:
        return FailingSession()

    async def __aexit__(self, *_args: Any) -> None:
        return None


@pytest.mark.asyncio
async def test_pool_timeout_removes_only_the_unready_replica(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.database.async_session_maker",
        lambda: FailingSessionContext(),
    )
    monkeypatch.setattr("app.observability.head_revision", lambda: "wave2-head")
    monkeypatch.setattr(
        "app.database.database_runtime_summary",
        lambda: {"backend": "postgresql", "url": "postgresql:///[redacted]"},
    )

    ready, payload = await readiness_snapshot()

    assert ready is False
    assert payload["database"]["error_kind"] == "TimeoutError"
    assert payload["writer_drain"]["drained"] is False


def test_metrics_registry_contains_only_aggregate_safe_values() -> None:
    registry = MetricRegistry()
    registry.increment("workchord_requests_total", labels={"method": "GET"})
    registry.set_gauge("workchord_database_connections_checked_out", 3)
    registry.observe("workchord_database_query_duration_seconds", 0.125)

    rendered = registry.render_prometheus()

    assert "workchord_requests_total{method=\"GET\"} 1" in rendered
    assert "workchord_database_connections_checked_out 3" in rendered
    assert "workchord_database_query_duration_seconds_count 1" in rendered
    assert "SELECT " not in rendered
    assert "DATABASE_URL" not in rendered
    assert "password" not in rendered.lower()
    assert activity.snapshot().checked_out_connections >= 0


def test_production_gateway_exports_attempts_and_routes_public_synthetic_probe() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    gateway = (
        repository_root / "deploy/nginx.production.conf.template"
    ).read_text(encoding="utf-8")

    assert "log_format workchord_attempt escape=json" in gateway
    assert '"path":"$uri"' in gateway
    assert "access_log /dev/stdout workchord_attempt" in gateway
    assert "location = /health" in gateway
    assert "proxy_set_header X-Correlation-ID $request_id" in gateway


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_active_transaction_gauge_returns_to_zero(
    sqlite_engine: AsyncEngine,
) -> None:
    install_database_instrumentation(sqlite_engine)
    baseline = activity.snapshot().active_transactions

    async with sqlite_engine.begin() as connection:
        await connection.execute(text("SELECT 1"))
        assert activity.snapshot().active_transactions == baseline + 1

    assert activity.snapshot().active_transactions == baseline
