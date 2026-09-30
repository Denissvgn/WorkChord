# OutboundWebhookTargetCreate

**Location:** `backend/app/schemas/outbound_webhook.py:96`
**Kind:** Pydantic model
**Bases:** `OutboundWebhookTargetBase`
**Module:** [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md)

## Description

Create an outbound webhook target.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookTargetCreate (backend/app/schemas/outbound_webhook.py)"]
    n1["OutboundWebhookTargetBase (backend/app/schemas/outbound_webhook.py)"]
    n2["create_outbound_webhook_target (backend/app/routers/outbound_webhooks.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["OutboundWebhookService.create_target (backend/app/services/outbound_webhook_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_outbound_webhook.md"
    click n1 "../modules/schemas_outbound_webhook.md"
    click n2 "../modules/outbound_webhooks.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `OutboundWebhookTargetBase` | [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_outbound_webhook_target` | type_reference | [outbound_webhooks](../modules/outbound_webhooks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `OutboundWebhookService.create_target` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
