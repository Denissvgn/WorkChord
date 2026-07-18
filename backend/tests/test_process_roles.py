"""DBM-WORK-001 command ownership and process-role tests."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.cli import upgrade, worker
from app.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    yield
    get_settings.cache_clear()


def _environment(monkeypatch: pytest.MonkeyPatch, role: str) -> None:
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "test")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.setenv("DATABASE_SSL_MODE", "disable")
    monkeypatch.setenv("DATABASE_PROCESS_ROLE", role)
    monkeypatch.setenv("DATABASE_POOL_SIZE", "1")
    monkeypatch.setenv("DATABASE_MAX_OVERFLOW", "0")
    get_settings.cache_clear()


def test_schema_command_rejects_web_role(monkeypatch: pytest.MonkeyPatch) -> None:
    _environment(monkeypatch, "web")
    assert upgrade.main(["--no-repairs"]) == 2


def test_migration_command_cannot_bundle_repairs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _environment(monkeypatch, "migration")
    assert upgrade.main([]) == 2


def test_migration_and_repair_commands_have_disjoint_roles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _environment(monkeypatch, "migration")
    monkeypatch.setattr(
        upgrade,
        "run_alembic_upgrade",
        lambda **_kwargs: (
            SimpleNamespace(state="empty", current_revision=None, head_revision="head"),
            None,
            SimpleNamespace(
                state="alembic_managed",
                current_revision="head",
                head_revision="head",
            ),
        ),
    )
    assert upgrade.main(["--no-repairs"]) == 0

    _environment(monkeypatch, "repair")
    monkeypatch.setattr(
        upgrade,
        "run_database_repairs",
        lambda: (
            SimpleNamespace(state="alembic_managed", current_revision="head"),
            SimpleNamespace(state="alembic_managed", current_revision="head"),
        ),
    )
    assert upgrade.main(["--repairs-only"]) == 0


@pytest.mark.asyncio
async def test_worker_is_drained_without_opening_database_in_fenced_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _environment(monkeypatch, "delivery_worker")
    monkeypatch.setenv("OUTBOUND_DELIVERY_WORKER_ENABLED", "true")
    monkeypatch.setenv("MAINTENANCE_MODE", "validation-only")
    monkeypatch.setenv("MAINTENANCE_REVISION", "worker-drain-test")
    get_settings.cache_clear()

    async def must_not_initialize() -> None:
        raise AssertionError("fenced worker opened the database")

    monkeypatch.setattr(worker, "init_db", must_not_initialize)
    assert await worker._run(once=True) == 0
