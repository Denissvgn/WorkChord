# upgrade Module

**Path:** `backend/app/cli/upgrade.py`

## Description

Operational database upgrade command.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.services.upgrade_service` | `UpgradeError`, `bootstrap_database_schema`, `inspect_database`, `run_alembic_upgrade`, `run_database_repairs` |
| `argparse` | `argparse` |
| `pathlib` | `Path` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/cli/upgrade.py"]
    n1["backend/app/config.py"]
    n2["backend/app/services/upgrade_service.py"]
    n3["backend/tests/test_process_roles.py"]
    n0 --> n1
    n0 --> n2
    n2 --> n1
    n3 --> n0
    n3 --> n1
    click n0 "../modules/upgrade.md"
    click n1 "../modules/config.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/test_process_roles.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_process_roles](../modules/test_process_roles.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_print_status` | `(prefix: str) -> None` | — | — |
| `build_parser` | `() -> argparse.ArgumentParser` | — | Build the CLI argument parser. |
| `main` | `(argv: list[str] \| None = None) -> int` | — | Run the upgrade command. |
