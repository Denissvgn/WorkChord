# __init__ Module

**Path:** `backend/app/database_migration/__init__.py`

## Description

Fail-closed SQLite-to-PostgreSQL migration tooling.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database_migration.source` | `MigrationDataError`, `preflight_source` |
| `app.database_migration.transfer` | `load_snapshot`, `reconcile_snapshot` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/__init__.py"]
    n1["backend/app/database_migration/source.py"]
    n2["backend/app/database_migration/transfer.py"]
    n0 --> n1
    n0 --> n2
    n2 --> n1
    click n0 "../modules/database_migration___init__.md"
    click n1 "../modules/source.md"
    click n2 "../modules/transfer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [source](../modules/source.md) |
| Outbound | [transfer](../modules/transfer.md) |
