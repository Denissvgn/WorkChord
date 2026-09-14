# database Module

**Path:** `backend/app/database.py`

## Description

_Auto-generated from `backend/app/database.py`._

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.database_config` | `parse_database_configuration` |
| `app.observability` | `install_database_instrumentation` |
| `app.services.upgrade_service` | `assert_database_current` |
| `collections.abc` | `AsyncGenerator` |
| `sqlalchemy` | `event` |
| `sqlalchemy.ext.asyncio` | `AsyncSession`, `create_async_engine`, `async_sessionmaker` |
| `sqlalchemy.orm` | `DeclarativeBase` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/database.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/app_database.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (63) |
| Outbound | `backend` (4) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 65 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [Base](../entities/Base.md) | 36 | `DeclarativeBase` | Base class for all models. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `enable_sqlite_foreign_keys` | `(dbapi_connection, _connection_record) -> None` | `@event.listens_for(engine.sync_engine, 'connect')` | — |
| `get_db` | *(async)* `() -> AsyncGenerator[AsyncSession, None]` | — | Dependency for getting database session. |
| `init_db` | *(async)* `() -> None` | — | Verify the database schema is Alembic-current before serving traffic. |
| `close_database` | *(async)* `() -> None` | — | Release every pooled connection during process shutdown. |
| `database_runtime_summary` | `() -> dict[str, object]` | — | Return restart-bound pool policy without exposing credentials. |
