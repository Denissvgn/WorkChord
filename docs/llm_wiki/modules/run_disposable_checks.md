# run_disposable_checks Module

**Path:** `scripts/ci/run_disposable_checks.py`

## Description

Runs database, frontend and browser validation through native executables in copied temporary workspaces. The caller supplies a marked local PostgreSQL cluster and the Python/Node toolchain. Application settings are isolated from the operator environment; libpq URL overrides cannot leave loopback. Browser writes require an invocation nonce from the fixture API. Owned process groups are stopped and reaped, and receipts retain source digests, command outcomes, artifacts and cleanup failures.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `datetime` | `datetime`, `timezone` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `shutil` | `shutil` |
| `signal` | `signal` |
| `socket` | `socket` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `urllib.parse` | `urlsplit` |
| `uuid` | `uuid4` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `runtime_environment` | `()` | — | Inherit toolchain settings without inheriting an operator's application secrets. |
| `require_free_browser_ports` | `()` | — | — |
| `validate_admin_url` | `(value)` | — | Keep libpq connection overrides from escaping the loopback fixture boundary. |
| `stop_process_group` | `(process)` | — | Stop the owned service and its descendants, and always reap the parent. |
| `source_digest` | `()` | — | — |
| `main` | `()` | — | — |