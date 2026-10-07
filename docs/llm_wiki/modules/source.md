# source Module

**Path:** `backend/app/database_migration/source.py`

## Description

Read-only SQLite snapshot creation and source preflight.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database_migration.canonical` | `canonical_value`, `digest_rows` |
| `app.database_migration.catalog` | `TEXT_JSON_COLUMNS`, `TRANSFER_CATALOG_VERSION`, `application_tables`, `catalog_entries`, `column_family`, `column_max_length`, `transfer_order`, `transfer_tables` |
| `app.database_migration.manifest` | `ManifestError`, `canonical_json_bytes`, `read_document`, `sha256_bytes`, `verify_document`, `write_document` |
| `app.services.upgrade_service` | `head_revision` |
| `contextlib` | `contextmanager` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `shutil` | `shutil` |
| `sqlalchemy` | `Index`, `UniqueConstraint` |
| `sqlalchemy.dialects` | `sqlite` |
| `sqlalchemy.sql.schema` | `Table` |
| `sqlite3` | `sqlite3` |
| `typing` | `Any`, `Iterator`, `Mapping` |
| `urllib.parse` | `quote` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/cli/database_migration.py"]
    n1["backend/app/database_migration/__init__.py"]
    n2["backend/app/database_migration/canonical.py"]
    n3["backend/app/database_migration/catalog.py"]
    n4["backend/app/database_migration/manifest.py"]
    n5["backend/app/database_migration/source.py"]
    n6["backend/app/database_migration/transfer.py"]
    n7["backend/app/services/upgrade_service.py"]
    n8["backend/tests/database_migration/test_postgresql_transfer.py"]
    n9["backend/tests/database_migration/test_source_preflight.py"]
    n10["scripts/ci/installed_wheel_postgresql_qualification.py"]
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n1 --> n5
    n1 --> n6
    n2 --> n3
    n2 --> n4
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n7
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n7
    n10 --> n4
    n10 --> n5
    n10 --> n6
    n10 --> n7
    click n0 "../modules/cli_database_migration.md"
    click n1 "../modules/database_migration___init__.md"
    click n2 "../modules/database_migration_canonical.md"
    click n3 "../modules/catalog.md"
    click n4 "../modules/database_migration_manifest.md"
    click n5 "../modules/source.md"
    click n6 "../modules/transfer.md"
    click n7 "../modules/upgrade_service.md"
    click n8 "../modules/test_postgresql_transfer.md"
    click n9 "../modules/test_source_preflight.md"
    click n10 "../modules/installed_wheel_postgresql_qualification.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [cli_database_migration](../modules/cli_database_migration.md) |
| Inbound | [database_migration___init__](../modules/database_migration___init__.md) |
| Inbound | [transfer](../modules/transfer.md) |
| Inbound | [test_postgresql_transfer](../modules/test_postgresql_transfer.md) |
| Inbound | [test_source_preflight](../modules/test_source_preflight.md) |
| Inbound | [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md) |
| Outbound | [database_migration_canonical](../modules/database_migration_canonical.md) |
| Outbound | [catalog](../modules/catalog.md) |
| Outbound | [database_migration_manifest](../modules/database_migration_manifest.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [MigrationDataError](../entities/MigrationDataError.md) | 48 | `RuntimeError` | A fail-closed source, transfer, or reconciliation condition. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_quoted` | `(identifier: str) -> str` | — | — |
| `_file_sha256` | `(path: Path) -> str` | — | — |
| `_source_file_set` | `(path: Path) -> dict[str, dict[str, Any]]` | — | — |
| `read_only_sqlite` | `(path: Path) -> Iterator[sqlite3.Connection]` | `@contextmanager` | Open an existing SQLite database with URI-enforced read-only access. |
| `_parse_utc` | `(value: Any, *, field: str) -> datetime` | — | — |
| `validate_writer_drain_evidence` | `(document: Mapping[str, Any], *, now: datetime \| None = None) -> str` | — | Validate controller plus all-replica writer-drain evidence. |
| `_snapshot_database` | `(source: Path, destination: Path) -> None` | — | — |
| `_table_names` | `(connection: sqlite3.Connection) -> set[str]` | — | — |
| `_rows` | `(connection: sqlite3.Connection, table: Table) -> Iterator[Mapping[str, Any]]` | — | — |
| `_validate_inventory` | `(connection: sqlite3.Connection) -> str` | — | — |
| `_validate_integrity` | `(connection: sqlite3.Connection) -> None` | — | — |
| `_validate_orphans` | `(connection: sqlite3.Connection) -> None` | — | — |
| `_validate_keys` | `(connection: sqlite3.Connection) -> None` | — | — |
| `_validate_task_graphs` | `(connection: sqlite3.Connection) -> None` | — | — |
| `_validate_values` | `(connection: sqlite3.Connection) -> None` | — | — |
| `_inspect_snapshot` | `(connection: sqlite3.Connection) -> tuple[str, dict[str, Any]]` | — | — |
| `preflight_source` | `(*, source_path: Path, snapshot_path: Path, writer_drain_evidence_path: Path, manifest_path: Path, now: datetime \| None = None) -> dict[str, Any]` | — | Create, validate, and manifest a stable SQLite migration snapshot. |
