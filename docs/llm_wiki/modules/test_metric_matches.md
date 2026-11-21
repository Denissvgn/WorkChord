# test_metric_matches Module

**Path:** `backend/tests/test_metric_matches.py`

## Description

A work-metric count and the list it opens are chosen by the same predicate.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.task` | `Task` |
| `app.services.work_metrics` | `METRIC_MATCHES`, `aggregate_metrics` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/task.py"]
    n1["backend/app/services/work_metrics.py"]
    n2["backend/tests/test_delivery_scenarios.py"]
    n3["backend/tests/test_managed_authority.py"]
    n4["backend/tests/test_metric_matches.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/models_task.md"
    click n1 "../modules/services_work_metrics.md"
    click n2 "../modules/test_delivery_scenarios.md"
    click n3 "../modules/test_managed_authority.md"
    click n4 "../modules/test_metric_matches.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [services_work_metrics](../modules/services_work_metrics.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `expected` | `(counts, metric)` | — | — |
| `test_every_metric_list_has_as_many_tasks_as_its_count` | *(async)* `(delivery_store)` | — | — |
| `test_metric_matches_route_scopes_and_rejects_unknown_metrics` | *(async)* `(delivery_store)` | — | — |
| `test_metric_matches_pages_return_every_task_once` | *(async)* `(delivery_store)` | — | — |
