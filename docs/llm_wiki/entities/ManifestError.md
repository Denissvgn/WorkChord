# ManifestError

**Location:** `backend/app/database_migration/manifest.py:15`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [database_migration_manifest](../modules/database_migration_manifest.md)

## Description

A migration document is malformed or has lost integrity.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ManifestError (backend/app/database_migration/manifest.py)"]
    n1["ValueError"]
    n2["backend/app/cli/closeout.py"]
    n3["backend/app/cli/cutover.py"]
    n4["_seal (backend/app/cli/database_migration.py)"]
    n5["backend/app/database_migration/cutover.py"]
    n6["read_document (backend/app/database_migration/manifest.py)"]
    n7["seal_document (backend/app/database_migration/manifest.py)"]
    n8["verify_document (backend/app/database_migration/manifest.py)"]
    n9["backend/app/database_migration/source.py"]
    n10["backend/app/database_migration/transfer.py"]
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
    click n0 "../modules/database_migration_manifest.md"
    click n2 "../modules/cli_closeout.md"
    click n3 "../modules/cli_cutover.md"
    click n4 "../modules/cli_database_migration.md"
    click n5 "../modules/database_migration_cutover.md"
    click n6 "../modules/database_migration_manifest.md"
    click n7 "../modules/database_migration_manifest.md"
    click n8 "../modules/database_migration_manifest.md"
    click n9 "../modules/source.md"
    click n10 "../modules/transfer.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [database_migration_manifest](../modules/database_migration_manifest.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `closeout` | import | [cli_closeout](../modules/cli_closeout.md) | — |
| `cutover` | import | [cli_cutover](../modules/cli_cutover.md) | — |
| `_seal` | call | [cli_database_migration](../modules/cli_database_migration.md) | 3 |
| `cutover` | import | [database_migration_cutover](../modules/database_migration_cutover.md) | — |
| `read_document` | call | [database_migration_manifest](../modules/database_migration_manifest.md) | 2 |
| `seal_document` | call | [database_migration_manifest](../modules/database_migration_manifest.md) | 1 |
| `verify_document` | call | [database_migration_manifest](../modules/database_migration_manifest.md) | 2 |
| `source` | import | [source](../modules/source.md) | — |
| `transfer` | import | [transfer](../modules/transfer.md) | — |
