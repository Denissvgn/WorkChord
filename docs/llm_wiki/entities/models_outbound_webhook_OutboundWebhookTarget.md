# OutboundWebhookTarget

**Location:** `backend/app/models/outbound_webhook.py:37`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_outbound_webhook](../modules/models_outbound_webhook.md)

## Description

Configurable subscriber for outbound domain events.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `url` | `Mapped[str]` | `mapped_column(String(1000), nullable=False)` | — |
| `enabled` | `Mapped[bool]` | `mapped_column(default=True, nullable=False, index=True)` | — |
| `subscribed_events_json` | `Mapped[list[str]]` | `mapped_column(JSON, default=list, nullable=False)` | — |
| `secret` | `Mapped[Optional[str]]` | `mapped_column(String(500), nullable=True)` | — |
| `headers_json` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False, index=True)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True)` | — |
| `deliveries` | `Mapped[list['OutboundWebhookDelivery']]` | `relationship('OutboundWebhookDelivery', back_populates='target', passive_deletes=True, order_by='OutboundWebhookDelivery.created_at.desc(), OutboundWebhookDelivery.id.desc()')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookTarget (backend/app/models/outbound_webhook.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["OutboundWebhookService._enabled_targets (backend/app/services/outbound_webhook_service.py)"]
    n4["OutboundWebhookService._enqueue_event_records (backend/app/services/outbound_webhook_service.py)"]
    n5["OutboundWebhookService._target_response (backend/app/services/outbound_webhook_service.py)"]
    n6["OutboundWebhookService._webhook_delivery (backend/app/services/outbound_webhook_service.py)"]
    n7["OutboundWebhookService.create_target (backend/app/services/outbound_webhook_service.py)"]
    n8["OutboundWebhookService.get_target (backend/app/services/outbound_webhook_service.py)"]
    n9["OutboundWebhookService.list_targets (backend/app/services/outbound_webhook_service.py)"]
    n10["OutboundWebhookService.update_target (backend/app/services/outbound_webhook_service.py)"]
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
    click n0 "../modules/models_outbound_webhook.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/outbound_webhook_service.md"
    click n4 "../modules/outbound_webhook_service.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/outbound_webhook_service.md"
    click n7 "../modules/outbound_webhook_service.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/outbound_webhook_service.md"
    click n10 "../modules/outbound_webhook_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_outbound_webhook](../modules/models_outbound_webhook.md) | 0 | `created_at`, `deliveries`, `description`, `enabled`, `headers_json`, `id`, `name`, `secret`, `subscribed_events_json`, `updated_at`, `url` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `OutboundWebhookService._enabled_targets` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService._enqueue_event_records` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService._target_response` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService._webhook_delivery` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService.create_target` | call | [outbound_webhook_service](../modules/outbound_webhook_service.md) | 1 |
| `OutboundWebhookService.create_target` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService.get_target` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService.list_targets` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
| `OutboundWebhookService.update_target` | type_reference | [outbound_webhook_service](../modules/outbound_webhook_service.md) | — |
