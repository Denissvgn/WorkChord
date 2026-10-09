# 20261009_0010_allocation_identity Module

**Path:** `backend/app/migrations/versions/20261009_0010_allocation_identity.py`

## Description

Preserve allocation lifetimes across recovery and deletion.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `app.database_migration.allocation_identity` | `allocation_floor` |
| `sqlalchemy` | `sa` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/allocation_identity.py"]
    n1["backend/app/migrations/versions/20261009_0010_allocation_identity.py"]
    n1 --> n0
    click n0 "../modules/allocation_identity.md"
    click n1 "../modules/20261009_0010_allocation_identity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [allocation_identity](../modules/allocation_identity.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `upgrade` | `()` | — | — |
| `downgrade` | `()` | — | — |
