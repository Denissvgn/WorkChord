# execution_mode Module

**Path:** `backend/app/autonomy/execution_mode.py`

## Description

Execution-mode guards shared by legacy and autonomous migration tools.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `os` | `os` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/execution_mode.py"]
    n1["backend/app/database_migration/cutover.py"]
    n1 --> n0
    click n0 "../modules/execution_mode.md"
    click n1 "../modules/database_migration_cutover.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [database_migration_cutover](../modules/database_migration_cutover.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `zero_human_execution_enabled` | `() -> bool` | — | Return whether fail-closed autonomous execution rules are active. |
| `local_signing_rejection_message` | `() -> str` | — | Return one stable diagnostic used by file-key signing/trust boundaries. |
