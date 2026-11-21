# catalog Module

**Path:** `backend/app/database_migration/catalog.py`

## Description

Derives transfer coverage and ordering from the packaged schema. Nullable references are staged only when aggregate constraints permit it. Task/snapshot scope references and typed delivery targets remain present during insertion, so referenced tasks and milestones load first without disabling constraints.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app` | `models` |
| `app.database` | `Base` |
| `dataclasses` | `dataclass` |
| `sqlalchemy` | `Boolean`, `Date`, `DateTime`, `Float`, `Integer`, `JSON`, `LargeBinary`, `Numeric`, `String` |
| `sqlalchemy.sql.schema` | `Column`, `Table` |
| `sqlalchemy.types` | `TypeDecorator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/database_migration/canonical.py"]
    n2["backend/app/database_migration/catalog.py"]
    n3["backend/app/database_migration/source.py"]
    n4["backend/app/database_migration/transfer.py"]
    n5["backend/app/models/__init__.py"]
    n6["backend/tests/database_migration/test_postgresql_transfer.py"]
    n7["backend/tests/database_migration/test_source_preflight.py"]
    n8["backend/tests/database_migration/test_transfer_catalog.py"]
    n9["backend/tests/test_authority_migrations.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n5
    n3 --> n1
    n3 --> n2
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n7 --> n2
    n7 --> n3
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n9 --> n2
    click n0 "../modules/app_database.md"
    click n1 "../modules/database_migration_canonical.md"
    click n2 "../modules/catalog.md"
    click n3 "../modules/source.md"
    click n4 "../modules/transfer.md"
    click n5 "../modules/models___init__.md"
    click n6 "../modules/test_postgresql_transfer.md"
    click n7 "../modules/test_source_preflight.md"
    click n8 "../modules/test_transfer_catalog.md"
    click n9 "../modules/test_authority_migrations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [database_migration_canonical](../modules/database_migration_canonical.md) |
| Inbound | [source](../modules/source.md) |
| Inbound | [transfer](../modules/transfer.md) |
| Inbound | [test_postgresql_transfer](../modules/test_postgresql_transfer.md) |
| Inbound | [test_source_preflight](../modules/test_source_preflight.md) |
| Inbound | [test_transfer_catalog](../modules/test_transfer_catalog.md) |
| Inbound | [test_authority_migrations](../modules/test_authority_migrations.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models___init__](../modules/models___init__.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CatalogEntry](../entities/CatalogEntry.md) | 48 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_base_type` | `(column: Column[object]) -> object` | — | — |
| `column_family` | `(column: Column[object]) -> str` | — | Return the conversion family used by canonicalization and loading. |
| `column_max_length` | `(column: Column[object]) -> int \| None` | — | Return the target character limit, including decorated string types. |
| `application_tables` | `() -> dict[str, Table]` | — | — |
| `transfer_tables` | `() -> dict[str, Table]` | — | — |
| `staged_reference_columns` | `(table: Table) -> tuple[str, ...]` | — | Stage nullable references so cycles never weaken target constraints. |
| `transfer_order` | `() -> tuple[str, ...]` | — | Order tables by references that must survive their initial insertion. |
| `catalog_entries` | `() -> tuple[CatalogEntry, ...]` | — | — |
