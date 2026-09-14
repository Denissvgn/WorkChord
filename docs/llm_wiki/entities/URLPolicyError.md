# URLPolicyError

**Location:** `backend/app/utils/url_policy.py:14`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [url_policy](../modules/url_policy.md)

## Description

Raised when a URL or host violates outbound egress policy.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["URLPolicyError (backend/app/utils/url_policy.py)"]
    n1["ValueError"]
    n2["backend/app/schemas/agent.py"]
    n3["backend/app/schemas/external_link.py"]
    n4["backend/app/schemas/outbound_webhook.py"]
    n5["backend/app/schemas/request_source.py"]
    n6["backend/app/schemas/task.py"]
    n7["backend/app/services/email_settings_service.py"]
    n8["backend/app/services/outbound_webhook_service.py"]
    n9["backend/app/services/system_settings_service.py"]
    n10["normalize_external_http_url (backend/app/utils/url_policy.py)"]
    n11["validate_public_host (backend/app/utils/url_policy.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/url_policy.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/schemas_external_link.md"
    click n4 "../modules/schemas_outbound_webhook.md"
    click n5 "../modules/schemas_request_source.md"
    click n6 "../modules/schemas_task.md"
    click n7 "../modules/email_settings_service.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/system_settings_service.md"
    click n10 "../modules/url_policy.md"
    click n11 "../modules/url_policy.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [url_policy](../modules/url_policy.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent` | import | [schemas_agent](../modules/schemas_agent.md) | — |
| `external_link` | import | [schemas_external_link](../modules/schemas_external_link.md) | — |
| `outbound_webhook` | import | [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md) | — |
| `request_source` | import | [schemas_request_source](../modules/schemas_request_source.md) | — |
| `task` | import | [schemas_task](../modules/schemas_task.md) | — |
| `email_settings_service` | import | [email_settings_service](../modules/email_settings_service.md) | — |
| `outbound_webhook_service` | import | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `system_settings_service` | import | [system_settings_service](../modules/system_settings_service.md) | — |
| `normalize_external_http_url` | call | [url_policy](../modules/url_policy.md) | 4 |
| `validate_public_host` | call | [url_policy](../modules/url_policy.md) | 6 |
