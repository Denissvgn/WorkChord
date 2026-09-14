# env Module

**Path:** `backend/app/migrations/env.py`

## Description

Alembic environment configuration.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `context` |
| `app` | `models` |
| `app.config` | `get_settings` |
| `app.database` | `Base` |
| `app.database_config` | `alembic_safe_url`, `parse_database_configuration` |
| `logging.config` | `fileConfig` |
| `sqlalchemy` | `engine_from_config`, `pool` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/database.py"]
    n2["backend/app/database_config.py"]
    n3["backend/app/migrations/env.py"]
    n4["backend/app/models/__init__.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    click n0 "../modules/config.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/database_config.md"
    click n3 "../modules/migrations_env.md"
    click n4 "../modules/models___init__.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [database_config](../modules/database_config.md) |
| Outbound | [models___init__](../modules/models___init__.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `run_migrations_offline` | `() -> None` | — | Run migrations in offline mode. |
| `run_migrations_online` | `() -> None` | — | Run migrations in online mode. |
