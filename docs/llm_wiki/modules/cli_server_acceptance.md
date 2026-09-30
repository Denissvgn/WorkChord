# server_acceptance Module

**Path:** `backend/app/cli/server_acceptance.py`

## Description

Run the bounded self-hosted server acceptance profile.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.server_acceptance` | `ServerAcceptanceConfig`, `ServerAcceptanceError`, `ServerAcceptanceReceipt`, `build_blocked_result`, `run_server_acceptance`, `verify_receipt_current_build`, `verify_receipt_trusted_signer` |
| `app.build_identity` | `load_backend_build_identity` |
| `argparse` | `argparse` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `tempfile` | `tempfile` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/server_acceptance.py"]
    n1["backend/app/build_identity.py"]
    n2["backend/app/cli/server_acceptance.py"]
    n3["backend/tests/autonomy/test_server_acceptance.py"]
    n0 --> n1
    n2 --> n0
    n2 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/autonomy_server_acceptance.md"
    click n1 "../modules/build_identity.md"
    click n2 "../modules/cli_server_acceptance.md"
    click n3 "../modules/test_server_acceptance.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_server_acceptance](../modules/test_server_acceptance.md) |
| Outbound | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) |
| Outbound | [build_identity](../modules/build_identity.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `parse_args` | `(argv: list[str] \| None = None) -> argparse.Namespace` | — | — |
| `_required` | `(value: str \| None, code: str) -> str` | — | — |
| `_render` | `(result: object) -> str` | — | — |
| `_emit` | `(rendered: str, output: Path \| None) -> None` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
