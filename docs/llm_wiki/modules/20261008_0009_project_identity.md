# 20261008_0009_project_identity Module

**Path:** `backend/app/migrations/versions/20261008_0009_project_identity.py`

## Description

Preserve project allocation identity across retained history.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `app.database_migration.project_identity` | `project_allocation_floor` |
| `sqlalchemy` | `text` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/project_identity.py"]
    n1["backend/app/migrations/versions/20261008_0009_project_identity.py"]
    n1 --> n0
    click n0 "../modules/project_identity.md"
    click n1 "../modules/20261008_0009_project_identity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [project_identity](../modules/project_identity.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `upgrade` | `()` | — | — |
| `downgrade` | `()` | — | — |
