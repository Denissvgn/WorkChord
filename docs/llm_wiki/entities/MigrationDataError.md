# MigrationDataError

**Location:** `backend/app/database_migration/source.py:49`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [source](../modules/source.md)

## Description

A fail-closed source, transfer, or reconciliation condition.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, message: str)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MigrationDataError (backend/app/database_migration/source.py)"]
    n1["RuntimeError"]
    n2["main (backend/app/cli/database_migration.py)"]
    n3["backend/app/database_migration/__init__.py"]
    n4["_parse_utc (backend/app/database_migration/source.py)"]
    n5["_snapshot_database (backend/app/database_migration/source.py)"]
    n6["_validate_integrity (backend/app/database_migration/source.py)"]
    n7["_validate_inventory (backend/app/database_migration/source.py)"]
    n8["_validate_keys (backend/app/database_migration/source.py)"]
    n9["_validate_orphans (backend/app/database_migration/source.py)"]
    n10["_validate_task_graphs (backend/app/database_migration/source.py)"]
    n11["_validate_values (backend/app/database_migration/source.py)"]
    n12["preflight_source (backend/app/database_migration/source.py)"]
    n13["validate_writer_drain_evidence (backend/app/database_migration/source.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/source.md"
    click n2 "../modules/cli_database_migration.md"
    click n3 "../modules/database_migration___init__.md"
    click n4 "../modules/source.md"
    click n5 "../modules/source.md"
    click n6 "../modules/source.md"
    click n7 "../modules/source.md"
    click n8 "../modules/source.md"
    click n9 "../modules/source.md"
    click n10 "../modules/source.md"
    click n11 "../modules/source.md"
    click n12 "../modules/source.md"
    click n13 "../modules/source.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [source](../modules/source.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `main` | call | [cli_database_migration](../modules/cli_database_migration.md) | 1 |
| `__init__` | import | [database_migration___init__](../modules/database_migration___init__.md) | — |
| `_parse_utc` | call | [source](../modules/source.md) | 3 |
| `_snapshot_database` | call | [source](../modules/source.md) | 1 |
| `_validate_integrity` | call | [source](../modules/source.md) | 2 |
| `_validate_inventory` | call | [source](../modules/source.md) | 4 |
| `_validate_keys` | call | [source](../modules/source.md) | 3 |
| `_validate_orphans` | call | [source](../modules/source.md) | 1 |
| `_validate_task_graphs` | call | [source](../modules/source.md) | 2 |
| `_validate_values` | call | [source](../modules/source.md) | 6 |
| `preflight_source` | call | [source](../modules/source.md) | 12 |
| `validate_writer_drain_evidence` | call | [source](../modules/source.md) | 17 |

> References: showing 12 of 35 logical references; 23 omitted by the 12-row generated summary limit.
