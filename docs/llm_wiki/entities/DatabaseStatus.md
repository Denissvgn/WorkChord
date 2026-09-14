# DatabaseStatus

**Location:** `backend/app/services/upgrade_service.py:75`
**Kind:** Class
**Bases:** —
**Module:** [upgrade_service](../modules/upgrade_service.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Inspected database schema state.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `state` | `DatabaseState` | *required* | — |
| `current_revision` | `Optional[str]` | *required* | — |
| `head_revision` | `str` | *required* | — |
| `table_count` | `int` | *required* | — |
| `tables` | `list[str]` | *required* | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `is_current` | `() -> bool` | `@property` | — |
| `needs_upgrade` | `() -> bool` | `@property` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DatabaseStatus (backend/app/services/upgrade_service.py)"]
    n1["_backup_precondition (backend/app/services/upgrade_service.py)"]
    n2["_inspect_database_connection (backend/app/services/upgrade_service.py)"]
    n3["_run_schema_upgrade (backend/app/services/upgrade_service.py)"]
    n4["_validate_managed_revision (backend/app/services/upgrade_service.py)"]
    n5["bootstrap_database_schema (backend/app/services/upgrade_service.py)"]
    n6["inspect_database (backend/app/services/upgrade_service.py)"]
    n7["run_alembic_upgrade (backend/app/services/upgrade_service.py)"]
    n8["run_database_repairs (backend/app/services/upgrade_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/upgrade_service.md"
    click n1 "../modules/upgrade_service.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/upgrade_service.md"
    click n4 "../modules/upgrade_service.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/upgrade_service.md"
    click n7 "../modules/upgrade_service.md"
    click n8 "../modules/upgrade_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [upgrade_service](../modules/upgrade_service.md) | 2 | `current_revision`, `head_revision`, `state`, `table_count`, `tables` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_backup_precondition` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `_inspect_database_connection` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
| `_inspect_database_connection` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `_run_schema_upgrade` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `_validate_managed_revision` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `bootstrap_database_schema` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `inspect_database` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `run_alembic_upgrade` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
| `run_database_repairs` | type_reference | [upgrade_service](../modules/upgrade_service.md) | — |
