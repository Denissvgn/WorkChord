# security Module

**Path:** `backend/app/security.py`

## Description

Shared request authorization helpers.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `fastapi` | `Header`, `HTTPException`, `status`, `Request` |
| `secrets` | `secrets` |
| `typing` | `Annotated`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/http_authority.py"]
    n2["backend/app/routers/agent.py"]
    n3["backend/app/routers/export.py"]
    n4["backend/app/routers/identity.py"]
    n5["backend/app/routers/llm.py"]
    n6["backend/app/routers/snapshots.py"]
    n7["backend/app/security.py"]
    n8["backend/app/settings_read.py"]
    n1 --> n0
    n1 --> n7
    n1 --> n8
    n2 --> n0
    n2 --> n7
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n7
    n5 --> n7
    n6 --> n3
    n6 --> n7
    n7 --> n0
    n8 --> n7
    click n0 "../modules/config.md"
    click n1 "../modules/http_authority.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/export.md"
    click n4 "../modules/routers_identity.md"
    click n5 "../modules/routers_llm.md"
    click n6 "../modules/snapshots.md"
    click n7 "../modules/security.md"
    click n8 "../modules/settings_read.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [http_authority](../modules/http_authority.md) |
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Inbound | [export](../modules/export.md) |
| Inbound | [routers_identity](../modules/routers_identity.md) |
| Inbound | [routers_llm](../modules/routers_llm.md) |
| Inbound | [snapshots](../modules/snapshots.md) |
| Inbound | [settings_read](../modules/settings_read.md) |
| Outbound | [config](../modules/config.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `admin_api_key_is_valid` | `(api_key: Optional[str]) -> bool` | — | Return whether a provided admin API key matches configured settings. |
| `require_admin_api_key` | *(async)* `(api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None, request: Request = None) -> None` | — | Require the configured admin API key for control-plane API routes. |
