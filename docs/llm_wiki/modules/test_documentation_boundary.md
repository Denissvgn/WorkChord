# test_documentation_boundary Module

**Path:** `backend/tests/database_migration/test_documentation_boundary.py`

## Description

A concise entrypoint still binds release evidence to authoritative operator policy.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database_migration.closeout` | `REPOSITORY_DOCUMENTS`, `CloseoutEvidenceError`, `_repository_document_set` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `shutil` | `shutil` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/closeout.py"]
    n1["backend/tests/database_migration/test_documentation_boundary.py"]
    n1 --> n0
    click n0 "../modules/database_migration_closeout.md"
    click n1 "../modules/test_documentation_boundary.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [database_migration_closeout](../modules/database_migration_closeout.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_linked_operator_boundary_cannot_be_removed_from_release_docs` | `(tmp_path)` | — | — |
