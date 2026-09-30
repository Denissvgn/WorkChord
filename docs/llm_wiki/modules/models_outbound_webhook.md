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
    n4["backend/app/services/discussion_service.py"]
    n5["backend/app/services/outbound_webhook_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/database/test_postgresql_concurrency.py"]
    n8["backend/tests/test_agent_routing_observability.py"]
    n9["backend/tests/test_agent_routing_rollout.py"]
    n10["backend/tests/test_task_discussion.py"]
    n0 --> n3
    n1 --> n2
    n2 --> n0
    n2 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n5 --> n0
    n5 --> n2
    n5 --> n6
    n7 --> n2
    n7 --> n5
    n7 --> n6
    n8 --> n2
    n8 --> n5
    n9 --> n2
    n9 --> n6
    n10 --> n2
    n10 --> n4
    n10 --> n5
    n10 --> n6
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_outbound_webhook.md"
    click n3 "../modules/observability.md"
    click n4 "../modules/discussion_service.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_postgresql_concurrency.md"
    click n8 "../modules/test_agent_routing_observability.md"
    click n9 "../modules/test_agent_routing_rollout.md"
    click n10 "../modules/test_task_discussion.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [observability](../modules/observability.md) |
| Inbound | [discussion_service](../modules/discussion_service.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) |
| Inbound | [test_agent_routing_observability](../modules/test_agent_routing_observability.md) |
| Inbound | [test_agent_routing_rollout](../modules/test_agent_routing_rollout.md) |
| Inbound | [test_task_discussion](../modules/test_task_discussion.md) |
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
| [OutboundWebhookTarget](../entities/models_outbound_webhook_OutboundWebhookTarget.md) | Class | 37 | `Base` | Configurable subscriber for outbound domain events. |
| [OutboundWebhookEvent](../entities/models_outbound_webhook_OutboundWebhookEvent.md) | Class | 80 | `Base` | Normalized domain event available for webhook delivery. |
| [OutboundWebhookDelivery](../entities/models_outbound_webhook_OutboundWebhookDelivery.md) | Class | 115 | `Base` | One delivery attempt log for one target and event. |
