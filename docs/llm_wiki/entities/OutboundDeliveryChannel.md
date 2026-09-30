# OutboundDeliveryChannel

**Location:** `backend/app/models/outbound_webhook.py:29`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_outbound_webhook](../modules/models_outbound_webhook.md)

## Description

Transport selected by the durable outbound delivery worker.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `WEBHOOK` | `'webhook'` | — |
| `EMAIL` | `'email'` | — |
| `INBOX` | `'inbox'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundDeliveryChannel (backend/app/models/outbound_webhook.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/outbound_webhook_service.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    click n0 "../modules/models_outbound_webhook.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_outbound_webhook](../modules/models_outbound_webhook.md) | 0 | `EMAIL`, `INBOX`, `WEBHOOK` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `outbound_webhook_service` | import | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
