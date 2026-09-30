# run_disposable_checks Module

**Path:** `scripts/ci/run_disposable_checks.py`

## Description

Runs explicit SQLite, PostgreSQL, frontend or browser scopes through native executables. The browser-only mode starts an isolated SQLite-backed API and frontend without repeating database or frontend result suites. Legacy combined and backend-only invocations remain supported. Only the PostgreSQL scope requires a validated loopback admin endpoint; URL overrides cannot escape that boundary.

The shared runner checkpoints receipts, streams logs and enforces deadlines. Selected scopes own their required evidence: nonempty successful JUnit records for database/frontend scopes, explicit browser write/read/reload evidence or completed managed assertions for browser scope, and schema parity for the full PostgreSQL scope. Source drift, failed commands, incomplete evidence and cleanup errors prevent success. Browser writes retain the invocation nonce fence. Frontend worker concurrency is bounded.

The managed browser receives the runner's exact Python executable through `WORKCHORD_BROWSER_PYTHON`. Its copied `browser_worker.mjs` helper dispatches inbox delivery with that absolute path, preserving virtual-environment identity independently of `PATH`. Missing or relative interpreter paths fail explicitly; the disposable database and invocation nonce remain required.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `ci_runtime` | `RunReceipt`, `junit_counts`, `positive_seconds`, `stop_process_group` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `shutil` | `shutil` |
| `socket` | `socket` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `urllib.parse` | `urlsplit` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `runtime_environment` | `()` | — | Inherit toolchain settings without inheriting an operator's application secrets. |
| `require_free_browser_ports` | `(ports = (8001, 8002, 4173))` | — | — |
| `validate_admin_url` | `(value)` | — | Keep libpq connection overrides from escaping the loopback fixture boundary. |
| `source_digest` | `(check_cancel = None)` | — | — |
| `bind_source` | `(run, digest = source_digest)` | — | — |
| `validate_results` | `(run, selected, managed)` | — | — |
| `parse_args` | `()` | — | — |
| `main` | `()` | — | — |
