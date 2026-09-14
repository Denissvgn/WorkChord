# agent_preflight Module

**Path:** `backend/app/cli/agent_preflight.py`

## Description

Fail-closed local diagnostic for the autonomous PostgreSQL start gate.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `sha256_hex` |
| `app.autonomy.contracts.postgresql` | `load_postgresql_contract_bundle` |
| `app.autonomy.preflight` | `evaluate_agent_preflight` |
| `argparse` | `argparse` |
| `json` | `json` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/canonical.py"]
    n1["backend/app/autonomy/contracts/postgresql/__init__.py"]
    n2["backend/app/autonomy/preflight.py"]
    n3["backend/app/cli/agent_preflight.py"]
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/autonomy_canonical.md"
    click n1 "../modules/postgresql___init__.md"
    click n2 "../modules/preflight.md"
    click n3 "../modules/agent_preflight.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |
| Outbound | [postgresql___init__](../modules/postgresql___init__.md) |
| Outbound | [preflight](../modules/preflight.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_release_fingerprint` | `() -> str` | — | — |
| `parse_args` | `(argv: list[str] \| None = None) -> argparse.Namespace` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
