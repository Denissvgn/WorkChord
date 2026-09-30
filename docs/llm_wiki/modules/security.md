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
    n3["backend/app/routers/email_settings.py"]
    n4["backend/app/routers/export.py"]
    n5["backend/app/routers/identity.py"]
    n6["backend/app/routers/llm.py"]
    n7["backend/app/routers/outbound_webhooks.py"]
    n8["backend/app/routers/scheduling_rules.py"]
    n9["backend/app/routers/snapshots.py"]
    n10["backend/app/routers/system_settings.py"]
    n11["backend/app/security.py"]
    n1 --> n0
    n1 --> n11
    n2 --> n0
    n2 --> n11
    n3 --> n11
    n4 --> n11
    n5 --> n0
    n5 --> n1
    n5 --> n11
    n6 --> n11
    n7 --> n11
    n8 --> n11
    n9 --> n4
    n9 --> n11
    n10 --> n11
    n11 --> n0
    click n0 "../modules/config.md"
    click n1 "../modules/http_authority.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/routers_email_settings.md"
    click n4 "../modules/export.md"
    click n5 "../modules/routers_identity.md"
    click n6 "../modules/routers_llm.md"
    click n7 "../modules/outbound_webhooks.md"
    click n8 "../modules/routers_scheduling_rules.md"
    click n9 "../modules/snapshots.md"
    click n10 "../modules/routers_system_settings.md"
    click n11 "../modules/security.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [http_authority](../modules/http_authority.md) |
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Inbound | [routers_email_settings](../modules/routers_email_settings.md) |
| Inbound | [export](../modules/export.md) |
| Inbound | [routers_identity](../modules/routers_identity.md) |
| Inbound | [routers_llm](../modules/routers_llm.md) |
| Inbound | [outbound_webhooks](../modules/outbound_webhooks.md) |
| Inbound | [routers_scheduling_rules](../modules/routers_scheduling_rules.md) |
| Inbound | [snapshots](../modules/snapshots.md) |
| Inbound | [routers_system_settings](../modules/routers_system_settings.md) |
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
