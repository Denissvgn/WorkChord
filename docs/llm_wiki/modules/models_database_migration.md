# database_migration Module

**Path:** `backend/app/models/database_migration.py`

## Description

Target-owned state for controlled SQLite-to-PostgreSQL transfers.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `CheckConstraint`, `Index`, `JSON`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/database_migration/transfer.py"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/database_migration.py"]
    n4["backend/app/utils/time.py"]
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n3 --> n0
    n3 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/transfer.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_database_migration.md"
    click n4 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [transfer](../modules/transfer.md) |
| Inbound | [models___init__](../modules/models___init__.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DatabaseMigrationGate](../entities/DatabaseMigrationGate.md) | 15 | `Base` | Fail-closed progress for one catalogued database transfer. |
