# OutboundWebhookDeliveryStatus

**Location:** `backend/app/models/outbound_webhook.py:21`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_outbound_webhook](../modules/models_outbound_webhook.md)

## Description

Delivery states for outbound webhook attempts.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PENDING` | `'pending'` | — |
| `DELIVERED` | `'delivered'` | — |
| `FAILED` | `'failed'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookDeliveryStatus (backend/app/models/outbound_webhook.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/observability.py"]
    n5["backend/app/services/outbound_webhook_service.py"]
    n6["backend/tests/database/test_postgresql_concurrency.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/models_outbound_webhook.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/observability.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/test_postgresql_concurrency.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_outbound_webhook](../modules/models_outbound_webhook.md) | 0 | `DELIVERED`, `FAILED`, `PENDING` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `observability` | import | [observability](../modules/observability.md) | — |
| `outbound_webhook_service` | import | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `test_postgresql_concurrency` | import | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) | — |
