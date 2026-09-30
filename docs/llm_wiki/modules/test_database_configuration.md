# test_database_configuration Module

**Path:** `backend/tests/database/test_database_configuration.py`

## Description

DBM-DEP-001 and DBM-CFG-001 configuration contract tests.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `Settings` |
| `app.database_config` | `DatabaseConfigurationError`, `alembic_safe_url`, `parse_database_configuration`, `redact_database_url` |
| `app.services.system_settings_service` | `RESTART_REQUIRED_SETTINGS` |
| `pathlib` | `Path` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `text` |
| `sqlalchemy.ext.asyncio` | `create_async_engine` |
| `tomllib` | `tomllib` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/database_config.py"]
    n2["backend/app/services/system_settings_service.py"]
    n3["backend/tests/database/test_database_configuration.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/config.md"
    click n1 "../modules/database_config.md"
    click n2 "../modules/system_settings_service.md"
    click n3 "../modules/test_database_configuration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [database_config](../modules/database_config.md) |
| Outbound | [system_settings_service](../modules/system_settings_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `settings` | `(**overrides) -> Settings` | — | — |
| `test_psycopg_is_hash_locked_as_the_only_runtime_postgresql_driver` | `() -> None` | — | — |
| `test_urls_are_parsed_structurally` | `(database_url: str, backend: str, sync_driver: str) -> None` | `@pytest.mark.parametrize(('database_url', 'backend', 'sync_driver'), [('sqlite+aiosqlite:///:memory:', 'sqlite', 'sqlite'), ('postgresql+psycopg://workchord:p%40ss%25word@localhost/workchord_test', 'postgresql', 'postgresql+psycopg')])` | — |
| `test_unapproved_database_drivers_fail_before_startup` | `(database_url: str) -> None` | `@pytest.mark.parametrize('database_url', ['postgresql+asyncpg://user:secret@localhost/workchord_test', 'postgresql://user:secret@localhost/workchord_test', 'sqlite+pysqlite:///:memory:', 'mysql+pymysql://user:secret@localhost/workchord_test'])` | — |
| `test_sqlite_and_postgresql_receive_only_dialect_specific_arguments` | `() -> None` | — | — |
| `test_only_migration_roles_can_assume_the_no_login_owner_role` | `() -> None` | — | — |
| `test_pool_and_timeout_bounds_are_validated` | `(field: str, value: int \| float, message: str) -> None` | `@pytest.mark.parametrize(('field', 'value', 'message'), [('database_pool_size', 0, 'DATABASE_POOL_SIZE'), ('database_max_overflow', -1, 'DATABASE_MAX_OVERFLOW'), ('database_pool_timeout_seconds', 0, 'DATABASE_POOL_TIMEOUT_SECONDS'), ('database_pool_recycle_seconds', 30, 'DATABASE_POOL_RECYCLE_SECONDS'), ('database_connect_timeout_seconds', 0, 'DATABASE_CONNECT_TIMEOUT_SECONDS'), ('database_statement_timeout_ms', 99, 'DATABASE_STATEMENT_TIMEOUT_MS'), ('database_lock_timeout_ms', 99, 'DATABASE_LOCK_TIMEOUT_MS')])` | — |
| `test_total_pool_capacity_is_bounded` | `() -> None` | — | — |
| `test_pool_capacity_cannot_exceed_the_approved_process_budget` | `(process_role: str, pool_size: int, max_overflow: int, approved_capacity: int) -> None` | `@pytest.mark.parametrize(('process_role', 'pool_size', 'max_overflow', 'approved_capacity'), [('web', 16, 5, 20), ('delivery_worker', 9, 2, 10), ('migration', 2, 1, 2), ('repair', 2, 1, 2)])` | — |
| `test_production_postgresql_requires_verified_tls` | `(tmp_path: Path) -> None` | — | — |
| `test_client_tls_certificate_requires_matching_key` | `(tmp_path: Path) -> None` | — | — |
| `test_production_sqlite_fallback_gate_is_explicit` | `() -> None` | — | — |
| `test_production_web_cannot_enable_an_embedded_worker` | `() -> None` | — | — |
| `test_production_fenced_mode_requires_an_explicit_revision` | `() -> None` | — | — |
| `test_url_credentials_and_secret_query_values_are_redacted` | `() -> None` | — | — |
| `test_percent_encoded_url_is_safe_for_alembic_interpolation` | `() -> None` | — | — |
| `test_connection_policy_query_keys_must_use_database_settings` | `() -> None` | — | — |
| `test_pool_settings_are_exposed_as_restart_required` | `() -> None` | — | — |
| `test_sync_sqlite_engine_select_one_smoke` | `() -> None` | — | — |
| `test_async_sqlite_engine_select_one_smoke` | *(async)* `() -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
