# OutboundDeliveryAttemptError

**Location:** `backend/app/services/outbound_webhook_service.py:142`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [outbound_webhook_service](../modules/outbound_webhook_service.md)

## Description

Classify a transport failure as retryable or terminal.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(message: str, *, retryable: bool)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundDeliveryAttemptError (backend/app/services/outbound_webhook_service.py)"]
    n1["RuntimeError"]
    n2["OutboundWebhookService._attempt_delivery (backend/app/services/outbound_webhook_service.py)"]
    n3["OutboundWebhookService._attempt_email (backend/app/services/outbound_webhook_service.py)"]
    n4["OutboundWebhookService._attempt_webhook (backend/app/services/outbound_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/outbound_webhook_service.md"
    click n2 "../modules/outbound_webhook_service.md"
    click n3 "../modules/outbound_webhook_service.md"
    click n4 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `OutboundWebhookService._attempt_delivery` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 |
| `OutboundWebhookService._attempt_email` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 |
| `OutboundWebhookService._attempt_webhook` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 2 |
