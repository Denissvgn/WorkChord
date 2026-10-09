# allocation_identity Module

**Path:** `backend/app/database_migration/allocation_identity.py`

## Description

Reserve numeric allocation identities retained by immutable recovery history.

Forward identity qualification reserves live, referenced and retained recovery/audit allocation IDs with bounded history scans. Ambiguous or oversized history fails closed before changing identity state.

## Imports

| Source | Symbols |
|--------|---------|
| `json` | `json` |
| `sqlalchemy` | `MetaData`, `Table`, `cast`, `String`, `func`, `inspect`, `select`, `text` |

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
| Inbound | [20261009_0010_allocation_identity](../modules/20261009_0010_allocation_identity.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `allocation_floor` | `(connection)` | — | — |
