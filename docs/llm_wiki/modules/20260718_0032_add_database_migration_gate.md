# 20260718_0032_add_database_migration_gate Module

**Path:** `backend/app/migrations/versions/20260718_0032_add_database_migration_gate.py`

## Description

add target-owned database migration gate

Revision ID: 20260718_0032
Revises: 20260718_0031
Create Date: 2026-07-18

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic` | `op` |
| `app.utils.time` | `UTCDateTime` |
| `sqlalchemy` | `sa` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/migrations/versions/20260718_0032_add_database_migration_gate.py"]
    n1["backend/app/utils/time.py"]
    n0 --> n1
    click n0 "../modules/20260718_0032_add_database_migration_gate.md"
    click n1 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `upgrade` | `() -> None` | — | — |
| `downgrade` | `() -> None` | — | — |
