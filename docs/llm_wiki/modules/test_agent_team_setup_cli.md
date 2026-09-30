# test_agent_team_setup_cli Module

**Path:** `backend/tests/test_agent_team_setup_cli.py`

## Description

No-network contract coverage for the agent-team setup CLI.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `importlib.util` | `importlib.util` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `types` | `SimpleNamespace` |
| `typing` | `Any` |

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
| `test_cli_apply_sends_only_exact_actions_and_audit_headers` | `(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None` | — | — |
| `test_cli_refuses_unknown_or_implicitly_confirmed_actions` | `(tmp_path: Path) -> None` | — | — |
| `test_cli_report_exports_only_the_selected_topology` | `(monkeypatch: pytest.MonkeyPatch) -> None` | — | — |
