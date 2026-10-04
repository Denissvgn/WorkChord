# delivery_metrics_service Module

**Path:** `backend/app/services/delivery_metrics_service.py`

## Description

Permission-scoped reports aggregate immutable observations within a declared elapsed-time window. Accepted delivery counts use distinct task identities, with acceptance/rejection/reopen events reported separately. Each duration has its own sample, missing-start and incomplete-episode counts; missing history is never reconstructed from status dates. Bounded current review/recovery queues recheck task visibility and expose unknown ages explicitly.

Event-based scoped delivery metrics; status dates never supply missing instants.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority`, `require_project` |
| `app.models.agent` | `AgentRun` |
| `app.models.delivery_observation` | `DeliveryObservation` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_PROJECT_TREE_TASKS` |
| `app.schemas.delivery_metrics` | `DeliveryMetricsResponse`, `DeliveryQueueItem`, `DurationSamples` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `collections` | `defaultdict` |
| `datetime` | `timedelta` |
| `sqlalchemy` | `select` |
| `statistics` | `mean`, `median` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/delivery_observation.py"]
    n3["backend/app/models/iteration.py"]
    n4["backend/app/models/project.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/query_limits.py"]
    n7["backend/app/routers/task_domain.py"]
    n8["backend/app/schemas/delivery_metrics.py"]
    n9["backend/app/services/delivery_metrics_service.py"]
    n10["backend/app/utils/time.py"]
    n11["backend/tests/test_delivery_metrics.py"]
    n0 --> n1
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n1 --> n10
    n2 --> n1
    n2 --> n5
    n2 --> n10
    n3 --> n4
    n3 --> n5
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n10
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n5 --> n10
    n7 --> n0
    n7 --> n5
    n7 --> n8
    n7 --> n9
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n6
    n9 --> n8
    n9 --> n10
    n11 --> n0
    n11 --> n2
    n11 --> n5
    n11 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/delivery_observation.md"
    click n3 "../modules/models_iteration.md"
    click n4 "../modules/models_project.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/query_limits.md"
    click n7 "../modules/routers_task_domain.md"
    click n8 "../modules/delivery_metrics.md"
    click n9 "../modules/delivery_metrics_service.md"
    click n10 "../modules/time.md"
    click n11 "../modules/test_delivery_metrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [test_delivery_metrics](../modules/test_delivery_metrics.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [delivery_observation](../modules/delivery_observation.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [delivery_metrics](../modules/delivery_metrics.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryMetricsService](../entities/DeliveryMetricsService.md) | 100 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_samples` | `(values, *, censored = 0, unknown = 0)` | — | — |
| `summarize_observations` | `(rows, start, end)` | — | Use immutable leaf facts, keeping reopened episodes and incomplete histories visible. |