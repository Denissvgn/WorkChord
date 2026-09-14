# setup_agent_team Module

**Path:** `scripts/api_keys/setup_agent_team.py`

## Description

Validate, plan, apply, and inspect a WorkChord agent-team master.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `secrets` | `secrets` |
| `sys` | `sys` |
| `typing` | `Any` |
| `urllib` | `error`, `parse`, `request` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalize_base_url` | `(value: str) -> str` | — | — |
| `normalize_api_prefix` | `(value: str) -> str` | — | — |
| `endpoint` | `(base_url: str, api_prefix: str, operation: str) -> str` | — | — |
| `load_object` | `(path: Path, *, label: str) -> dict[str, Any]` | — | — |
| `call_api` | `(*, url: str, admin_key: str, method: str, payload: dict[str, Any] \| None, timeout: float, headers: dict[str, str] \| None = None) -> dict[str, Any]` | — | — |
| `common_payload` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `run_validate` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `run_plan` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `run_apply` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `run_status` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `run_report` | `(args: argparse.Namespace) -> dict[str, Any]` | — | — |
| `parse_args` | `() -> argparse.Namespace` | — | — |
| `main` | `() -> int` | — | — |
