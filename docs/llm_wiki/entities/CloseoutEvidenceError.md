# CloseoutEvidenceError

**Location:** `backend/app/database_migration/closeout.py:149`
**Kind:** Class
**Bases:** `CutoverEvidenceError`
**Module:** [database_migration_closeout](../modules/database_migration_closeout.md)

## Description

A post-cutover publication or closure input is incomplete or unsafe.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CloseoutEvidenceError (backend/app/database_migration/closeout.py)"]
    n1["CutoverEvidenceError (backend/app/database_migration/cutover.py)"]
    n2["_artifact_references (backend/app/database_migration/closeout.py)"]
    n3["_dependency_summary (backend/app/database_migration/closeout.py)"]
    n4["_evaluate_closeout_input (backend/app/database_migration/closeout.py)"]
    n5["_installed_application_version (backend/app/database_migration/closeout.py)"]
    n6["_integer (backend/app/database_migration/closeout.py)"]
    n7["_number (backend/app/database_migration/closeout.py)"]
    n8["_publication_exceptions (backend/app/database_migration/closeout.py)"]
    n9["_repository_document_set (backend/app/database_migration/closeout.py)"]
    n10["_safe_identifier (backend/app/database_migration/closeout.py)"]
    n11["_safe_public_uri (backend/app/database_migration/closeout.py)"]
    n12["_validate_availability (backend/app/database_migration/closeout.py)"]
    n13["_validate_backup_restore (backend/app/database_migration/closeout.py)"]
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
    click n0 "../modules/database_migration_closeout.md"
    click n1 "../modules/database_migration_cutover.md"
    click n2 "../modules/database_migration_closeout.md"
    click n3 "../modules/database_migration_closeout.md"
    click n4 "../modules/database_migration_closeout.md"
    click n5 "../modules/database_migration_closeout.md"
    click n6 "../modules/database_migration_closeout.md"
    click n7 "../modules/database_migration_closeout.md"
    click n8 "../modules/database_migration_closeout.md"
    click n9 "../modules/database_migration_closeout.md"
    click n10 "../modules/database_migration_closeout.md"
    click n11 "../modules/database_migration_closeout.md"
    click n12 "../modules/database_migration_closeout.md"
    click n13 "../modules/database_migration_closeout.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [database_migration_closeout](../modules/database_migration_closeout.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `CutoverEvidenceError` | [database_migration_cutover](../modules/database_migration_cutover.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_artifact_references` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 5 |
| `_dependency_summary` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 10 |
| `_evaluate_closeout_input` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 10 |
| `_installed_application_version` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 2 |
| `_integer` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 1 |
| `_number` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 2 |
| `_publication_exceptions` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 4 |
| `_repository_document_set` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 7 |
| `_safe_identifier` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 1 |
| `_safe_public_uri` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 5 |
| `_validate_availability` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 12 |
| `_validate_backup_restore` | call | [database_migration_closeout](../modules/database_migration_closeout.md) | 4 |

> References: showing 12 of 27 logical references; 15 omitted by the 12-row generated summary limit.
