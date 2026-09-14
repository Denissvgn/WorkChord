# closeout Module

**Path:** `backend/app/cli/closeout.py`

## Description

Command-line interface for PostgreSQL release publication and closeout.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database_migration.closeout` | `finalize_closeout`, `publish_postcutover_release`, `render_release_notes`, `verify_closeout_report` |
| `app.database_migration.cutover` | `CutoverEvidenceError` |
| `app.database_migration.manifest` | `ManifestError` |
| `argparse` | `argparse` |
| `pathlib` | `Path` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/cli/closeout.py"]
    n1["backend/app/database_migration/closeout.py"]
    n2["backend/app/database_migration/cutover.py"]
    n3["backend/app/database_migration/manifest.py"]
    n4["scripts/ci/installed_wheel_postgresql_qualification.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n2 --> n3
    n4 --> n0
    n4 --> n3
    click n0 "../modules/cli_closeout.md"
    click n1 "../modules/database_migration_closeout.md"
    click n2 "../modules/database_migration_cutover.md"
    click n3 "../modules/database_migration_manifest.md"
    click n4 "../modules/installed_wheel_postgresql_qualification.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md) |
| Outbound | [database_migration_closeout](../modules/database_migration_closeout.md) |
| Outbound | [database_migration_cutover](../modules/database_migration_cutover.md) |
| Outbound | [database_migration_manifest](../modules/database_migration_manifest.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_signing_arguments` | `(parser: argparse.ArgumentParser) -> None` | — | — |
| `_optional_closeout_dependencies` | `(parser: argparse.ArgumentParser) -> None` | — | — |
| `build_parser` | `() -> argparse.ArgumentParser` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
