# test_task_pagination Module

**Path:** `backend/tests/test_task_pagination.py`

## Description

Keyset coverage, mutation semantics and permission-bounded history reads.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority` |
| `app.models.agent` | `TaskEvent`, `AgentRun`, `AgentRunEvent` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.query_limits` | `CollectionLimitExceededError` |
| `app.services.agent_service` | `AgentService` |
| `app.services.delivery_metrics_service` | `DeliveryMetricsService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.project_service` | `ProjectService` |
| `app.services.task_detail_service` | `TaskDetailService` |
| `app.services.task_hierarchy_service` | `TaskHierarchyService` |
| `app.services.task_service` | `TaskService` |
| `app.services.task_timeline_service` | `TaskTimelineService` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `pytest` | `pytest` |
| `sqlalchemy` | `delete` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_task_pagination.py"]
    n1 --> n0
    click n1 "../modules/test_task_pagination.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_large_reference_pages_are_complete_and_filtered` | *(async)* `(delivery_store, size)` | `@pytest.mark.parametrize('size', [501, 2501])` | — |
| `test_live_page_mutations_keep_ids_monotonic_and_scope_isolated` | *(async)* `(delivery_store)` | — | — |
| `test_history_pages_ties_and_legacy_bound` | *(async)* `(delivery_store)` | — | — |
| `test_scope_pages_hold_an_insert_boundary_and_summary_counts_are_complete` | *(async)* `(delivery_store)` | — | — |
| `test_mixed_timeline_sources_have_stable_ties_and_actor_provenance` | *(async)* `(delivery_store)` | — | — |
| `test_oversized_reads_reject_before_relationship_or_history_hydration` | *(async)* `(delivery_store, monkeypatch)` | — | — |
