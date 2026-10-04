# delivery_observation Module

**Path:** `backend/app/models/delivery_observation.py`

## Description

Delivery facts are appended inside the owning database transaction, with task identity, version and scope captured at the event boundary. Leaf checks exclude structural parents. Acceptance requires matching task, brief and artifact revisions plus a recorded principal. Grouping and removal end incomplete episodes without rewriting accepted facts; restored identities do not invent original capture dates. Nullable scope references detach on resource deletion while original identifiers remain historical evidence.

Immutable workflow observations with scope captured at the event boundary.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.agent` | `TaskEvent` |
| `app.models.recovery` | `TaskDeletionFence` |
| `app.models.task` | `Task` |
| `app.models.task_brief` | `TaskReviewRecord` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `json` | `json` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `UniqueConstraint`, `event`, `select` |
| `sqlalchemy.dialects.postgresql` | `insert` |
| `sqlalchemy.dialects.sqlite` | `insert` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/delivery_observation.py"]
    n4["backend/app/models/recovery.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/models/task_brief.py"]
    n7["backend/app/services/delivery_metrics_service.py"]
    n8["backend/app/utils/time.py"]
    n9["backend/tests/test_delivery_metrics.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n0
    n2 --> n5
    n2 --> n8
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n8
    n4 --> n0
    n4 --> n5
    n4 --> n8
    n5 --> n0
    n5 --> n2
    n5 --> n8
    n6 --> n0
    n6 --> n8
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n8
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n7
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/delivery_observation.md"
    click n4 "../modules/recovery.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/models_task_brief.md"
    click n7 "../modules/delivery_metrics_service.md"
    click n8 "../modules/time.md"
    click n9 "../modules/test_delivery_metrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [delivery_metrics_service](../modules/delivery_metrics_service.md) |
| Inbound | [test_delivery_metrics](../modules/test_delivery_metrics.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [recovery](../modules/recovery.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_task_brief](../modules/models_task_brief.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryObservation](../entities/DeliveryObservation.md) | 16 | `Base` | Retain delivery identity and scope independently of later hierarchy edits. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_record` | `(connection, row, kind, at, source, *, version = None, structural = False)` | — | Join the owning transaction without exposing a client-authored ledger write. |
| `_task_row` | `(connection, task_id)` | — | — |
| `observe_task_insert` | `(_mapper, connection, task)` | — | — |
| `observe_task_event` | `(_mapper, connection, item)` | — | — |
| `observe_review` | `(_mapper, connection, review)` | — | — |
| `observe_task_update` | `(_mapper, connection, task)` | — | — |
| `observe_task_delete` | `(_mapper, connection, task)` | — | — |
| `immutable_observation` | `(*_args)` | — | — |