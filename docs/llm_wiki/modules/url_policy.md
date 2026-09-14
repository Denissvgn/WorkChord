# url_policy Module

**Path:** `backend/app/utils/url_policy.py`

## Description

Centralized outbound URL and host validation.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `ipaddress` | `ipaddress` |
| `socket` | `socket` |
| `urllib.parse` | `urlparse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/schemas/agent.py"]
    n2["backend/app/schemas/external_link.py"]
    n3["backend/app/schemas/outbound_webhook.py"]
    n4["backend/app/schemas/request_source.py"]
    n5["backend/app/schemas/task.py"]
    n6["backend/app/services/email_settings_service.py"]
    n7["backend/app/services/github_status_service.py"]
    n8["backend/app/services/llm_service.py"]
    n9["backend/app/services/outbound_webhook_service.py"]
    n10["backend/app/services/system_settings_service.py"]
    n11["backend/app/utils/url_policy.py"]
    n1 --> n4
    n1 --> n5
    n1 --> n11
    n2 --> n11
    n3 --> n11
    n4 --> n11
    n5 --> n2
    n5 --> n11
    n6 --> n0
    n6 --> n10
    n6 --> n11
    n7 --> n0
    n7 --> n11
    n8 --> n0
    n8 --> n11
    n9 --> n3
    n9 --> n6
    n9 --> n11
    n10 --> n0
    n10 --> n11
    n11 --> n0
    click n0 "../modules/config.md"
    click n1 "../modules/schemas_agent.md"
    click n2 "../modules/schemas_external_link.md"
    click n3 "../modules/schemas_outbound_webhook.md"
    click n4 "../modules/schemas_request_source.md"
    click n5 "../modules/schemas_task.md"
    click n6 "../modules/email_settings_service.md"
    click n7 "../modules/github_status_service.md"
    click n8 "../modules/llm_service.md"
    click n9 "../modules/outbound_webhook_service.md"
    click n10 "../modules/system_settings_service.md"
    click n11 "../modules/url_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [schemas_agent](../modules/schemas_agent.md) |
| Inbound | [schemas_external_link](../modules/schemas_external_link.md) |
| Inbound | [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md) |
| Inbound | [schemas_request_source](../modules/schemas_request_source.md) |
| Inbound | [schemas_task](../modules/schemas_task.md) |
| Inbound | [email_settings_service](../modules/email_settings_service.md) |
| Inbound | [github_status_service](../modules/github_status_service.md) |
| Inbound | [llm_service](../modules/llm_service.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [system_settings_service](../modules/system_settings_service.md) |
| Outbound | [config](../modules/config.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [URLPolicyError](../entities/URLPolicyError.md) | 14 | `ValueError` | Raised when a URL or host violates outbound egress policy. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_is_blocked_ip` | `(ip: IPAddress) -> bool` | — | — |
| `_literal_ip` | `(host: str) -> IPAddress \| None` | — | — |
| `_host_looks_local` | `(host: str) -> bool` | — | — |
| `validate_public_host` | `(host: str, *, allow_private: bool = False, resolve: bool = True) -> str` | — | Validate a hostname or IP literal for outbound network use. |
| `normalize_external_http_url` | `(value: str, *, require_https: bool = False, allow_http_localhost: bool = False, allow_http_private: bool = False, resolve: bool = True) -> str` | — | Normalize and validate an outbound HTTP(S) URL. |
| `normalize_provider_api_url` | `(value: str) -> str` | — | Validate a provider API URL that may carry credentials in headers. |
| `normalize_stored_display_url` | `(value: str) -> str` | — | Validate externally displayed user-supplied links before persistence. |
