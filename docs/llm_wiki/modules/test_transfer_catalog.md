# test_transfer_catalog Module

**Path:** `backend/tests/database_migration/test_transfer_catalog.py`

## Description

Versioned transfer catalog invariants.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database_migration.catalog` | `TARGET_OWNED_TABLES`, `application_tables`, `catalog_entries`, `staged_reference_columns`, `transfer_order`, `transfer_tables` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/catalog.py"]
    n1["backend/tests/database_migration/test_transfer_catalog.py"]
    n1 --> n0
    click n0 "../modules/catalog.md"
    click n1 "../modules/test_transfer_catalog.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [catalog](../modules/catalog.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_catalog_disposes_every_packaged_table_exactly_once` | `() -> None` | — | — |
| `test_nullable_cycles_are_staged_without_weakening_required_foreign_keys` | `() -> None` | — | — |
