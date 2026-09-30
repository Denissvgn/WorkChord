# generate_workchord_keys Module

**Path:** `scripts/api_keys/generate_workchord_keys.py`

## Description

Generate local secrets consumed by WorkChord.

This script creates only secrets that WorkChord owns locally. External
provider credentials such as LLM API keys, GitHub PATs, SMTP passwords, and
third-party webhook URLs must still be created in their source systems.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `base64` | `base64` |
| `collections.abc` | `Callable` |
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `os` | `os` |
| `secrets` | `secrets` |
| `shlex` | `shlex` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `generate_fernet_key` | `() -> str` | — | Return a Fernet-compatible base64url-encoded 32-byte key. |
| `generate_prefixed_token` | `(prefix: str) -> str` | — | Return a high-entropy URL-safe token with a human-readable prefix. |
| `selected_keys` | `(raw_keys: list[str] \| None, include_outbound: bool) -> list[str]` | — | Resolve requested keys in stable output order. |
| `build_payload` | `(keys: list[str]) -> dict[str, object]` | — | Generate a structured payload for all requested keys. |
| `render_env` | `(payload: dict[str, object], *, comments: bool) -> str` | — | Render dotenv-style KEY=value lines. |
| `render_shell` | `(payload: dict[str, object], *, comments: bool) -> str` | — | Render shell export lines. |
| `parse_args` | `() -> argparse.Namespace` | — | — |
| `main` | `() -> None` | — | — |
