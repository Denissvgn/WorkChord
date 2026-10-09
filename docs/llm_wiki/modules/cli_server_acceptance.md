# server_acceptance Module

**Path:** `backend/app/cli/server_acceptance.py`

## Description

Runs container-backed self-hosted acceptance or mutually exclusive offline receipt/archive verification. Archive verification consumes an independently supplied public-key pin, checks exact exported bytes and candidate identities, and requires a valid latest receipt matching the installed build. Invalid artifacts produce a sanitized unsuccessful decision. Successful verification retains the signed non-production boundary and does not qualify production autonomy.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.acceptance_artifacts` | `verify_exported_artifacts` |
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
    n0["backend/app/autonomy/acceptance_artifacts.py"]
    n1["backend/app/autonomy/server_acceptance.py"]
    n2["backend/app/build_identity.py"]
    n3["backend/app/cli/server_acceptance.py"]
    n4["backend/tests/autonomy/test_acceptance_artifacts.py"]
    n5["backend/tests/autonomy/test_server_acceptance.py"]
    n0 --> n1
    n1 --> n2
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n5 --> n1
    n5 --> n2
    n5 --> n3
    click n0 "../modules/acceptance_artifacts.md"
    click n1 "../modules/autonomy_server_acceptance.md"
    click n2 "../modules/build_identity.md"
    click n3 "../modules/cli_server_acceptance.md"
    click n4 "../modules/test_acceptance_artifacts.md"
    click n5 "../modules/test_server_acceptance.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_acceptance_artifacts](../modules/test_acceptance_artifacts.md) |
| Inbound | [test_server_acceptance](../modules/test_server_acceptance.md) |
| Outbound | [acceptance_artifacts](../modules/acceptance_artifacts.md) |
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
