# database_config Module

**Path:** `backend/app/database_config.py`

## Description

Driver-neutral database URL, connection, and engine configuration.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `dataclasses` | `dataclass` |
| `pathlib` | `Path` |
| `re` | `re` |
| `sqlalchemy.engine` | `URL`, `make_url` |
| `typing` | `Any`, `Mapping` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/database.py"]
    n2["backend/app/database_config.py"]
    n3["backend/app/migrations/env.py"]
    n4["backend/app/services/upgrade_service.py"]
    n5["backend/tests/database/test_database_configuration.py"]
    n6["backend/tests/database/test_postgresql_concurrency.py"]
    n7["backend/tests/migrations/test_postgresql_migrations.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n5 --> n0
    n5 --> n2
    n6 --> n0
    n6 --> n2
    n6 --> n4
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n4
    click n0 "../modules/config.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/database_config.md"
    click n3 "../modules/migrations_env.md"
    click n4 "../modules/upgrade_service.md"
    click n5 "../modules/test_database_configuration.md"
    click n6 "../modules/test_postgresql_concurrency.md"
    click n7 "../modules/test_postgresql_migrations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [config](../modules/config.md) |
| Inbound | [app_database](../modules/app_database.md) |
| Inbound | [migrations_env](../modules/migrations_env.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_database_configuration](../modules/test_database_configuration.md) |
| Inbound | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) |
| Inbound | [test_postgresql_migrations](../modules/test_postgresql_migrations.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DatabaseConfigurationError](../entities/DatabaseConfigurationError.md) | 39 | `ValueError` | Raised when database settings are unsupported or unsafe. |
| [DatabaseConfiguration](../entities/DatabaseConfiguration.md) | 44 | — | Validated, dialect-specific database configuration. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_settings_value` | `(settings: Any, name: str) -> Any` | — | — |
| `_certificate_path` | `(value: str, *, setting_name: str) -> str` | — | — |
| `redact_database_url` | `(value: str \| URL) -> str` | — | Render a URL without exposing passwords or secret query values. |
| `alembic_safe_url` | `(value: str \| URL) -> str` | — | Render a URL for Alembic ConfigParser without percent interpolation. |
| `parse_database_configuration` | `(settings: Any) -> DatabaseConfiguration` | — | Validate settings and build driver-specific runtime/migration URLs. |
