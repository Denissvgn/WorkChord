# OutboundWebhookValidationError

**Location:** `backend/app/services/outbound_webhook_service.py:134`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [outbound_webhook_service](../modules/outbound_webhook_service.md)

## Description

Raised when outbound webhook input is invalid.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookValidationError (backend/app/services/outbound_webhook_service.py)"]
    n1["ValueError"]
    n2["backend/app/routers/outbound_webhooks.py"]
    n3["OutboundWebhookService._enqueue_event_records (backend/app/services/outbound_webhook_service.py)"]
    n4["OutboundWebhookService._normalize_headers (backend/app/services/outbound_webhook_service.py)"]
    n5["OutboundWebhookService._normalize_subscriptions (backend/app/services/outbound_webhook_service.py)"]
    n6["OutboundWebhookService.list_deliveries (backend/app/services/outbound_webhook_service.py)"]
    n7["OutboundWebhookService.retry_delivery (backend/app/services/outbound_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/outbound_webhook_service.md"
    click n2 "../modules/outbound_webhooks.md"
    click n3 "../modules/outbound_webhook_service.md"
    click n4 "../modules/outbound_webhook_service.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/outbound_webhook_service.md"
    click n7 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [outbound_webhook_service](../modules/outbound_webhook_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `outbound_webhooks` | import | [outbound_webhooks](../modules/outbound_webhooks.md) | — |
| `OutboundWebhookService._enqueue_event_records` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
| `OutboundWebhookService._normalize_headers` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
| `OutboundWebhookService._normalize_subscriptions` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
| `OutboundWebhookService.list_deliveries` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
| `OutboundWebhookService.retry_delivery` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
