# create_agent_actor Module

**Path:** `scripts/api_keys/create_agent_actor.py`

## Description

Provision a WorkChord AgentActor through the REST Agent API.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `json` | `json` |
| `os` | `os` |
| `shlex` | `shlex` |
| `sys` | `sys` |
| `typing` | `Any` |
| `urllib` | `error`, `request` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalize_base_url` | `(value: str) -> str` | — | Return a base URL without trailing slash. |
| `normalize_api_prefix` | `(value: str) -> str` | — | Return an API prefix beginning with one slash and without trailing slash. |
| `actor_url` | `(base_url: str, api_prefix: str) -> str` | — | Build the agent actor creation endpoint URL. |
| `normalize_scopes` | `(scopes: list[str], admin: bool) -> list[str]` | — | Validate and de-duplicate scopes while preserving caller order. |
| `title_from_name` | `(name: str) -> str` | — | Derive a display name from an actor name. |
| `create_actor` | `(*, url: str, bootstrap_key: str, name: str, display_name: str, scopes: list[str], role: str, profile_id: int \| None, work_policy: str, max_parallel_work: int, enabled: bool, model_catalog_key: str \| None, model_tool_tags: list[str], model_data_policy_tags: list[str], model_binding_is_default: bool, timeout: float) -> dict[str, Any]` | — | Call POST /agent/actors and return the response body. |
| `render_env` | `(data: dict[str, Any], *, comments: bool) -> str` | — | Render dotenv-style output for the one-time actor key. |
| `render_shell` | `(data: dict[str, Any], *, comments: bool) -> str` | — | Render shell export output for the one-time actor key. |
| `parse_args` | `() -> argparse.Namespace` | — | — |
| `main` | `() -> None` | — | — |
