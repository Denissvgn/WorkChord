# OutboundWebhookRetryResponse

**Location:** `backend/app/schemas/outbound_webhook.py:191`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md)

## Description

Response returned by retry and test delivery endpoints.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `delivery` | `OutboundWebhookDeliveryResponse` | `delivery` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookRetryResponse (backend/app/schemas/outbound_webhook.py)"]
    n1["BaseModel"]
    n2["retry_outbound_webhook_delivery (backend/app/routers/outbound_webhooks.py)"]
    n3["test_outbound_webhook_target (backend/app/routers/outbound_webhooks.py)"]
    n4["backend/app/schemas/__init__.py"]
    n5["OutboundWebhookService.retry_delivery (backend/app/services/outbound_webhook_service.py)"]
    n6["OutboundWebhookService.test_target (backend/app/services/outbound_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_outbound_webhook.md"
    click n2 "../modules/outbound_webhooks.md"
    click n3 "../modules/outbound_webhooks.md"
    click n4 "../modules/schemas___init__.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md) | 0 | `delivery` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `retry_outbound_webhook_delivery` | type_reference | [outbound_webhooks](../modules/outbound_webhooks.md) | — |
| `test_outbound_webhook_target` | type_reference | [outbound_webhooks](../modules/outbound_webhooks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `OutboundWebhookService.retry_delivery` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 |
| `OutboundWebhookService.retry_delivery` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService.test_target` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 |
| `OutboundWebhookService.test_target` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
