# project_identity Module

**Path:** `backend/app/database_migration/project_identity.py`

## Description

Read-only project identity qualification and retained allocation floors. The allocation floor includes live references, retained time and correction scope, durable delivery and usage observations, and bounded historical audit, outbox and recovery payloads. Contradictory creation/deletion provenance or incomplete historical scans stop qualification without reassociating or changing stored records. Diagnostic output includes bounded identities and reasons, never private notes.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `sqlalchemy` | `JSON`, `MetaData`, `String`, `Table`, `cast`, `create_engine`, `func`, `inspect`, `select`, `text` |
| `sqlalchemy.pool` | `NullPool` |
| `sqlite3` | `sqlite3` |
| `urllib.parse` | `quote` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/allocation_identity.py"]
    n1["backend/app/database_migration/project_identity.py"]
    n2["backend/app/database_migration/source.py"]
    n3["backend/app/database_migration/transfer.py"]
    n4["backend/app/migrations/env.py"]
    n5["backend/app/migrations/versions/20261008_0009_project_identity.py"]
    n6["backend/app/services/upgrade_service.py"]
    n7["backend/tests/database_migration/test_project_identity_scope.py"]
    n0 --> n1
    n2 --> n1
    n2 --> n6
    n3 --> n1
    n3 --> n2
    n3 --> n6
    n4 --> n1
    n5 --> n1
    n6 --> n1
    n7 --> n1
    n7 --> n2
    n7 --> n6
    click n0 "../modules/allocation_identity.md"
    click n1 "../modules/project_identity.md"
    click n2 "../modules/source.md"
    click n3 "../modules/transfer.md"
    click n4 "../modules/migrations_env.md"
    click n5 "../modules/20261008_0009_project_identity.md"
    click n6 "../modules/upgrade_service.md"
    click n7 "../modules/test_project_identity_scope.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [allocation_identity](../modules/allocation_identity.md) |
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
| [ProjectIdentityError](../entities/ProjectIdentityError.md) | 19 | `RuntimeError` | Refuse an ambiguous identity without changing historical associations. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_utc` | `(value)` | — | — |
| `_project_ids` | `(value)` | — | — |
| `_pages` | `(connection, history, columns, *, page_rows, joined = None)` | — | Yield one history table's rows in id order, a bounded keyset page at a time. |
| `decode_history_value` | `(column, value)` | — | Decode one encoded value from ``history_values`` the way the checks have always read it. |
| `history_values` | `(connection, history, column, columns = (), *, admit, page_rows = HISTORY_PAGE_ROWS)` | — | Yield ``(row, encoded value)`` for every row of one history table, in id order. |
| `inspect_project_identity` | `(connection, *, max_history_rows = None, max_history_bytes = None, page_rows = HISTORY_PAGE_ROWS)` | — | Check every retained history row in bounded pages; never inspect private text fields. |
| `project_allocation_floor` | `(connection)` | — | Require identity qualification before returning a safe allocation floor. |
| `sqlite_project_allocation_floor` | `(path)` | — | Qualify one immutable SQLite source through a separately owned read-only handle. |