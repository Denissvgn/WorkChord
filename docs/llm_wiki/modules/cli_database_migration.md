# database_migration Module

**Path:** `backend/app/cli/database_migration.py`

## Description

Operational SQLite-to-PostgreSQL migration command.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database_migration.manifest` | `ManifestError`, `write_document` |
| `app.database_migration.source` | `MigrationDataError`, `preflight_source` |
| `app.database_migration.transfer` | `load_snapshot`, `reconcile_snapshot`, `record_post_copy_repairs`, `target_identifier` |
| `app.services.upgrade_service` | `database_configuration` |
| `argparse` | `argparse` |
| `json` | `json` |
| `pathlib` | `Path` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/cli/database_migration.py"]
    n1["backend/app/database_migration/manifest.py"]
    n2["backend/app/database_migration/source.py"]
    n3["backend/app/database_migration/transfer.py"]
    n4["backend/app/services/upgrade_service.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n2 --> n1
    n2 --> n4
    n3 --> n1
    n3 --> n2
    n3 --> n4
    click n0 "../modules/cli_database_migration.md"
    click n1 "../modules/database_migration_manifest.md"
    click n2 "../modules/source.md"
    click n3 "../modules/transfer.md"
    click n4 "../modules/upgrade_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [database_migration_manifest](../modules/database_migration_manifest.md) |
| Outbound | [source](../modules/source.md) |
| Outbound | [transfer](../modules/transfer.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `build_parser` | `() -> argparse.ArgumentParser` | — | — |
| `_seal` | `(input_path: Path, output_path: Path) -> dict[str, object]` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
