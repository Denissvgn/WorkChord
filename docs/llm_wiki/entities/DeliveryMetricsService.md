# DeliveryMetricsService

**Location:** `backend/app/services/delivery_metrics_service.py:100`
**Kind:** Class
**Bases:** —
**Module:** [delivery_metrics_service](../modules/delivery_metrics_service.md)

## Description

_Auto-generated from `DeliveryMetricsService` in `backend/app/services/delivery_metrics_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `_window_observations` | *(async)* `(observed, start)` | — | Read the window and at most four prior state facts per relevant identity. |
| `report` | *(async)* `(*, project_id = None, iteration_id = None, lookback_days = 30, now = None)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryMetricsService (backend/app/services/delivery_metrics_service.py)"]
    n1["delivery_metrics (backend/app/routers/task_domain.py)"]
    n2["ExecutionUsageService.summary (backend/app/services/execution_usage_service.py)"]
    n3["test_observation_rollback_and_unknown_legacy_dates (backend/tests/test_delivery_metrics.py)"]
    n4["test_observations_survive_hierarchy_moves_reopen_and_deletion (backend/tests/test_delivery_metrics.py)"]
    n5["test_pre_window_seeds_keep_scope_boundaries_and_unknown_histories (backend/tests/test_delivery_metrics.py)"]
    n6["test_scope_at_event_and_permission_isolation_are_preserved (backend/tests/test_delivery_metrics.py)"]
    n7["test_window_report_ignores_large_completed_history_and_seeds_episodes (backend/tests/test_delivery_metrics.py)"]
    n8["test_oversized_reads_reject_before_relationship_or_history_hydration (backend/tests/test_task_pagination.py)"]
    n9["scripts/load/service_worksets.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/delivery_metrics_service.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/execution_usage_service.md"
    click n3 "../modules/test_delivery_metrics.md"
    click n4 "../modules/test_delivery_metrics.md"
    click n5 "../modules/test_delivery_metrics.md"
    click n6 "../modules/test_delivery_metrics.md"
    click n7 "../modules/test_delivery_metrics.md"
    click n8 "../modules/test_task_pagination.md"
    click n9 "../modules/service_worksets.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [delivery_metrics_service](../modules/delivery_metrics_service.md) | 3 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `delivery_metrics` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `ExecutionUsageService.summary` | call | [execution_usage_service](../modules/execution_usage_service.md) | 1 |
| `test_observation_rollback_and_unknown_legacy_dates` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 1 |
| `test_observations_survive_hierarchy_moves_reopen_and_deletion` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 1 |
| `test_pre_window_seeds_keep_scope_boundaries_and_unknown_histories` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 1 |
| `test_scope_at_event_and_permission_isolation_are_preserved` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 3 |
| `test_window_report_ignores_large_completed_history_and_seeds_episodes` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 2 |
| `test_oversized_reads_reject_before_relationship_or_history_hydration` | call | [test_task_pagination](../modules/test_task_pagination.md) | 1 |
| `service_worksets` | import | [service_worksets](../modules/service_worksets.md) | — |
