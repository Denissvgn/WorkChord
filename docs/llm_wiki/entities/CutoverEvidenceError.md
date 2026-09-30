# CutoverEvidenceError

**Location:** `backend/app/database_migration/cutover.py:142`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [database_migration_cutover](../modules/database_migration_cutover.md)

## Description

A cutover input is unsafe, stale, incomplete, or internally inconsistent.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CutoverEvidenceError (backend/app/database_migration/cutover.py)"]
    n1["ValueError"]
    n2["CloseoutEvidenceError (backend/app/database_migration/closeout.py)"]
    n3["backend/app/cli/closeout.py"]
    n4["backend/app/cli/cutover.py"]
    n5["backend/app/database_migration/closeout.py"]
    n6["_canonical_public_key (backend/app/database_migration/cutover.py)"]
    n7["_cross_validate_dependencies (backend/app/database_migration/cutover.py)"]
    n8["_exact_keys (backend/app/database_migration/cutover.py)"]
    n9["_number (backend/app/database_migration/cutover.py)"]
    n10["_private_key (backend/app/database_migration/cutover.py)"]
    n11["_read_json_object (backend/app/database_migration/cutover.py)"]
    n12["_reject_secret_material (backend/app/database_migration/cutover.py)"]
    n13["_release_identity (backend/app/database_migration/cutover.py)"]
    n14["_require_new_output (backend/app/database_migration/cutover.py)"]
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
    n14 --> n0
    click n0 "../modules/database_migration_cutover.md"
    click n2 "../modules/database_migration_closeout.md"
    click n3 "../modules/cli_closeout.md"
    click n4 "../modules/cli_cutover.md"
    click n5 "../modules/database_migration_closeout.md"
    click n6 "../modules/database_migration_cutover.md"
    click n7 "../modules/database_migration_cutover.md"
    click n8 "../modules/database_migration_cutover.md"
    click n9 "../modules/database_migration_cutover.md"
    click n10 "../modules/database_migration_cutover.md"
    click n11 "../modules/database_migration_cutover.md"
    click n12 "../modules/database_migration_cutover.md"
    click n13 "../modules/database_migration_cutover.md"
    click n14 "../modules/database_migration_cutover.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [database_migration_cutover](../modules/database_migration_cutover.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |
| Subclass | `CloseoutEvidenceError` | [database_migration_closeout](../modules/database_migration_closeout.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `closeout` | import | [cli_closeout](../modules/cli_closeout.md) | — |
| `cutover` | import | [cli_cutover](../modules/cli_cutover.md) | — |
| `closeout` | import | [database_migration_closeout](../modules/database_migration_closeout.md) | — |
| `_canonical_public_key` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 1 |
| `_cross_validate_dependencies` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 2 |
| `_exact_keys` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 1 |
| `_number` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 2 |
| `_private_key` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 3 |
| `_read_json_object` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 2 |
| `_reject_secret_material` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 3 |
| `_release_identity` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 4 |
| `_require_new_output` | call | [database_migration_cutover](../modules/database_migration_cutover.md) | 1 |

> References: showing 12 of 36 logical references; 24 omitted by the 12-row generated summary limit.
