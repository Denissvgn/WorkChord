"""DBM-DEP-001 and DBM-CFG-001 configuration contract tests."""

from __future__ import annotations

from pathlib import Path
import tomllib

from pydantic import ValidationError
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Settings
from app.database_config import (
    DatabaseConfigurationError,
    alembic_safe_url,
    parse_database_configuration,
    redact_database_url,
)
from app.services.system_settings_service import RESTART_REQUIRED_SETTINGS


BACKEND_ROOT = Path(__file__).resolve().parents[2]


def settings(**overrides) -> Settings:
    values = {
        "database_url": "sqlite+aiosqlite:///:memory:",
        "deployment_environment": "test",
        "database_ssl_mode": "disable",
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_psycopg_is_hash_locked_as_the_only_runtime_postgresql_driver() -> None:
    with (BACKEND_ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)

    runtime_dependencies = project["project"]["dependencies"]
    test_dependencies = project["dependency-groups"]["test"]
    runtime_lock = (BACKEND_ROOT / "requirements.lock").read_text()
    test_lock = (BACKEND_ROOT / "test-requirements.lock").read_text()

    assert "psycopg[binary]>=3.2,<4" in runtime_dependencies
    assert all(not dependency.startswith("psycopg") for dependency in test_dependencies)
    assert "psycopg==" in runtime_lock
    assert "psycopg-binary==" in runtime_lock
    assert "psycopg==" not in test_lock
    assert "asyncpg==" not in runtime_lock
    assert "psycopg2" not in runtime_lock.lower()


@pytest.mark.parametrize(
    ("database_url", "backend", "sync_driver"),
    [
        ("sqlite+aiosqlite:///:memory:", "sqlite", "sqlite"),
        (
            "postgresql+psycopg://workchord:p%40ss%25word@localhost/workchord_test",
            "postgresql",
            "postgresql+psycopg",
        ),
    ],
)
def test_urls_are_parsed_structurally(
    database_url: str,
    backend: str,
    sync_driver: str,
) -> None:
    configuration = parse_database_configuration(
        settings(database_url=database_url)
    )

    assert configuration.backend == backend
    assert configuration.sync_url.drivername == sync_driver
    assert configuration.async_url.password in {None, "p@ss%word"}


@pytest.mark.parametrize(
    "database_url",
    [
        "postgresql+asyncpg://user:secret@localhost/workchord_test",
        "postgresql://user:secret@localhost/workchord_test",
        "sqlite+pysqlite:///:memory:",
        "mysql+pymysql://user:secret@localhost/workchord_test",
    ],
)
def test_unapproved_database_drivers_fail_before_startup(database_url: str) -> None:
    with pytest.raises(ValidationError, match="DATABASE_URL"):
        settings(database_url=database_url)


def test_sqlite_and_postgresql_receive_only_dialect_specific_arguments() -> None:
    sqlite = parse_database_configuration(settings())
    postgres = parse_database_configuration(
        settings(
            database_url="postgresql+psycopg://user:secret@localhost/workchord_test",
            database_pool_size=12,
            database_max_overflow=3,
        )
    )

    assert sqlite.connect_args == {"timeout": 10.0}
    assert "sslmode" not in sqlite.connect_args
    assert sqlite.pool_size is None
    assert postgres.connect_args["connect_timeout"] == 10
    assert "timeout" not in postgres.connect_args
    assert "statement_timeout=30000" in postgres.connect_args["options"]
    assert "lock_timeout=5000" in postgres.connect_args["options"]
    assert postgres.bounded_connection_capacity == 15


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("database_pool_size", 0, "DATABASE_POOL_SIZE"),
        ("database_max_overflow", -1, "DATABASE_MAX_OVERFLOW"),
        ("database_pool_timeout_seconds", 0, "DATABASE_POOL_TIMEOUT_SECONDS"),
        ("database_pool_recycle_seconds", 30, "DATABASE_POOL_RECYCLE_SECONDS"),
        ("database_connect_timeout_seconds", 0, "DATABASE_CONNECT_TIMEOUT_SECONDS"),
        ("database_statement_timeout_ms", 99, "DATABASE_STATEMENT_TIMEOUT_MS"),
        ("database_lock_timeout_ms", 99, "DATABASE_LOCK_TIMEOUT_MS"),
    ],
)
def test_pool_and_timeout_bounds_are_validated(
    field: str,
    value: int | float,
    message: str,
) -> None:
    with pytest.raises(ValidationError, match=message):
        settings(**{field: value})


def test_total_pool_capacity_is_bounded() -> None:
    configuration = parse_database_configuration(
        settings(
            database_url="postgresql+psycopg://user:secret@localhost/workchord_test",
            database_pool_size=15,
            database_max_overflow=5,
        )
    )
    assert configuration.process_role == "web"
    assert configuration.bounded_connection_capacity == 20
    assert configuration.approved_connection_capacity == 20


@pytest.mark.parametrize(
    ("process_role", "pool_size", "max_overflow", "approved_capacity"),
    [
        ("web", 16, 5, 20),
        ("delivery_worker", 9, 2, 10),
        ("migration", 2, 1, 2),
        ("repair", 2, 1, 2),
    ],
)
def test_pool_capacity_cannot_exceed_the_approved_process_budget(
    process_role: str,
    pool_size: int,
    max_overflow: int,
    approved_capacity: int,
) -> None:
    with pytest.raises(ValidationError, match=f"budget of {approved_capacity}"):
        settings(
            database_process_role=process_role,
            database_pool_size=pool_size,
            database_max_overflow=max_overflow,
        )


def test_production_postgresql_requires_verified_tls(tmp_path: Path) -> None:
    database_url = "postgresql+psycopg://workchord:secret@db.example/workchord"
    with pytest.raises(ValidationError, match="verify-full"):
        settings(
            database_url=database_url,
            deployment_environment="production",
            database_ssl_mode="require",
        )

    root_cert = tmp_path / "root-ca.pem"
    root_cert.write_text("test-only-ca")
    production = settings(
        database_url=database_url,
        deployment_environment="production",
        database_ssl_mode="verify-full",
        database_ssl_root_cert=str(root_cert),
    )
    configuration = parse_database_configuration(production)
    assert configuration.connect_args["sslmode"] == "verify-full"
    assert configuration.connect_args["sslrootcert"] == str(root_cert)


def test_client_tls_certificate_requires_matching_key(tmp_path: Path) -> None:
    cert = tmp_path / "client.pem"
    cert.write_text("test-only-client-certificate")
    with pytest.raises(ValidationError, match="must be configured together"):
        settings(
            database_url="postgresql+psycopg://user:secret@localhost/workchord_test",
            database_ssl_mode="prefer",
            database_ssl_cert=str(cert),
        )


def test_production_sqlite_fallback_gate_is_explicit() -> None:
    allowed = settings(
        database_url="sqlite+aiosqlite:////app/data/workchord.db",
        deployment_environment="production",
        database_postgresql_required=False,
    )
    assert parse_database_configuration(allowed).backend == "sqlite"

    with pytest.raises(ValidationError, match="DATABASE_POSTGRESQL_REQUIRED"):
        settings(
            database_url="sqlite+aiosqlite:////app/data/workchord.db",
            deployment_environment="production",
            database_postgresql_required=True,
        )


def test_production_web_cannot_enable_an_embedded_worker() -> None:
    with pytest.raises(ValidationError, match="embedded delivery worker"):
        settings(
            database_url="sqlite+aiosqlite:////app/data/workchord.db",
            deployment_environment="production",
            outbound_delivery_worker_enabled=True,
        )


def test_production_fenced_mode_requires_an_explicit_revision() -> None:
    with pytest.raises(ValidationError, match="MAINTENANCE_REVISION"):
        settings(
            database_url="sqlite+aiosqlite:////app/data/workchord.db",
            deployment_environment="production",
            maintenance_mode="validation-only",
        )


def test_url_credentials_and_secret_query_values_are_redacted() -> None:
    database_url = (
        "postgresql+psycopg://user:p%40ss%25word@localhost/workchord_test"
        "?api_token=very-secret&client_label=qa"
    )
    rendered = redact_database_url(database_url)

    assert "p%40ss" not in rendered
    assert "very-secret" not in rendered
    assert "***" in rendered
    assert "client_label=qa" in rendered


def test_percent_encoded_url_is_safe_for_alembic_interpolation() -> None:
    rendered = alembic_safe_url(
        "postgresql+psycopg://user:p%40ss%25word@localhost/workchord_test"
    )
    assert "p%%40ss%%25word" in rendered


def test_connection_policy_query_keys_must_use_database_settings() -> None:
    with pytest.raises(ValidationError, match=r"DATABASE_\* settings"):
        settings(
            database_url=(
                "postgresql+psycopg://user:secret@localhost/workchord_test"
                "?sslmode=require"
            )
        )


def test_pool_settings_are_exposed_as_restart_required() -> None:
    keys = {setting.key for setting in RESTART_REQUIRED_SETTINGS}
    assert {
        "DATABASE_URL",
        "DATABASE_PROCESS_ROLE",
        "DATABASE_POOL_SIZE",
        "DATABASE_MAX_OVERFLOW",
        "DATABASE_POOL_TIMEOUT_SECONDS",
        "DATABASE_SSL_MODE",
        "DATABASE_SSL_ROOT_CERT",
    }.issubset(keys)


def test_sync_sqlite_engine_select_one_smoke() -> None:
    configuration = parse_database_configuration(settings())
    engine = create_engine(
        configuration.sync_url,
        connect_args=dict(configuration.connect_args),
    )
    try:
        with engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        engine.dispose()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_async_sqlite_engine_select_one_smoke() -> None:
    configuration = parse_database_configuration(settings())
    engine = create_async_engine(
        configuration.async_url,
        **configuration.async_engine_kwargs(),
    )
    try:
        async with engine.connect() as connection:
            assert (await connection.execute(text("SELECT 1"))).scalar_one() == 1
    finally:
        await engine.dispose()
