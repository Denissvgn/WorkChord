# project_identity Module

**Path:** `backend/app/database_migration/project_identity.py`

## Description

Read-only project identity qualification and retained allocation floors. The allocation floor includes live references, retained time and correction scope, durable delivery and usage observations, and bounded historical audit, outbox and recovery payloads. Contradictory creation/deletion provenance or incomplete historical scans stop qualification without reassociating or changing stored records. Diagnostic output includes bounded identities and reasons, never private notes.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `sqlalchemy` | `MetaData`, `String`, `Table`, `cast`, `create_engine`, `func`, `inspect`, `select`, `text` |
| `sqlalchemy.pool` | `NullPool` |
| `sqlite3` | `sqlite3` |
| `urllib.parse` | `quote` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/project_identity.py"]
    n1["backend/app/database_migration/source.py"]
    n2["backend/app/database_migration/transfer.py"]
    n3["backend/app/migrations/env.py"]
    n4["backend/app/migrations/versions/20261008_0009_project_identity.py"]
    n5["backend/app/services/upgrade_service.py"]
    n6["backend/tests/database_migration/test_project_identity_scope.py"]
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n5
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n6 --> n1
    n6 --> n5
    click n0 "../modules/project_identity.md"
    click n1 "../modules/source.md"
    click n2 "../modules/transfer.md"
    click n3 "../modules/migrations_env.md"
    click n4 "../modules/20261008_0009_project_identity.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/test_project_identity_scope.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [source](../modules/source.md) |
| Inbound | [transfer](../modules/transfer.md) |
| Inbound | [migrations_env](../modules/migrations_env.md) |
| Inbound | [20261008_0009_project_identity](../modules/20261008_0009_project_identity.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_project_identity_scope](../modules/test_project_identity_scope.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ProjectIdentityError](../entities/ProjectIdentityError.md) | 12 | `RuntimeError` | Refuse an ambiguous identity without changing historical associations. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_utc` | `(value)` | — | — |
| `_project_ids` | `(value)` | — | — |
| `inspect_project_identity` | `(connection, *, max_history_rows = 10000, max_history_bytes = 256 * 1024 * 1024)` | — | Bound diagnostics and historical JSON scans; never inspect private text fields. |
| `project_allocation_floor` | `(connection)` | — | Require identity qualification before returning a safe allocation floor. |
| `sqlite_project_allocation_floor` | `(path)` | — | Qualify one immutable SQLite source through a separately owned read-only handle. |