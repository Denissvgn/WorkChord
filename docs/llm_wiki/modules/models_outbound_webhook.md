# outbound_webhook Module

**Path:** `backend/app/models/outbound_webhook.py`

## Description

Outbound webhook configuration and delivery log models.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/outbound_webhook.py"]
    n3["backend/app/observability.py"]
    n4["backend/app/services/outbound_webhook_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/database/test_postgresql_concurrency.py"]
    n7["backend/tests/test_agent_routing_observability.py"]
    n8["backend/tests/test_agent_routing_rollout.py"]
    n0 --> n3
    n1 --> n2
    n2 --> n0
    n2 --> n5
    n3 --> n0
    n3 --> n2
    n3 --> n5
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n6 --> n2
    n6 --> n4
    n6 --> n5
    n7 --> n2
    n7 --> n4
    n8 --> n2
    n8 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_outbound_webhook.md"
    click n3 "../modules/observability.md"
    click n4 "../modules/outbound_webhook_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_postgresql_concurrency.md"
    click n7 "../modules/test_agent_routing_observability.md"
    click n8 "../modules/test_agent_routing_rollout.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [observability](../modules/observability.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) |
| Inbound | [test_agent_routing_observability](../modules/test_agent_routing_observability.md) |
| Inbound | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OutboundWebhookDeliveryStatus](../entities/models_outbound_webhook_OutboundWebhookDeliveryStatus.md) | Enum | 21 | `str`, `Enum` | Delivery states for outbound webhook attempts. |
| [OutboundDeliveryChannel](../entities/OutboundDeliveryChannel.md) | Enum | 29 | `str`, `Enum` | Transport selected by the durable outbound delivery worker. |
| [OutboundWebhookTarget](../entities/models_outbound_webhook_OutboundWebhookTarget.md) | Class | 36 | `Base` | Configurable subscriber for outbound domain events. |
| [OutboundWebhookEvent](../entities/models_outbound_webhook_OutboundWebhookEvent.md) | Class | 79 | `Base` | Normalized domain event available for webhook delivery. |
| [OutboundWebhookDelivery](../entities/models_outbound_webhook_OutboundWebhookDelivery.md) | Class | 114 | `Base` | One delivery attempt log for one target and event. |
