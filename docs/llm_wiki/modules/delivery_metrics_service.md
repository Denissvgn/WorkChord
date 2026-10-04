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
    n0["backend"]
    n1["backend/app/services/delivery_metrics_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/delivery_metrics_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (3) |
| Outbound | `backend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryMetricsService](../entities/DeliveryMetricsService.md) | 100 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_samples` | `(values, *, censored = 0, unknown = 0)` | — | — |
| `summarize_observations` | `(rows, start, end)` | — | Use immutable leaf facts, keeping reopened episodes and incomplete histories visible. |