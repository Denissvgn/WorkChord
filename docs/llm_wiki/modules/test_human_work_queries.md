# test_human_work_queries Module

**Path:** `backend/tests/test_human_work_queries.py`

## Description

Human ownership queries and exact-ID lookup respect project visibility.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.models.task` | `Task` |
| `app.schemas.task` | `TaskCreate` |
| `app.services.task_detail_service` | `TaskDetailService` |
| `app.services.task_service` | `TaskService` |
| `app.utils.time` | `utc_now` |
| `pytest` | `pytest` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_task_domain` | `human_context` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/schemas/task.py"]
    n3["backend/app/services/task_detail_service.py"]
    n4["backend/app/services/task_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/test_delivery_scenarios.py"]
    n7["backend/tests/test_human_work_queries.py"]
    n8["backend/tests/test_task_domain.py"]
    n0 --> n1
    n1 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n6 --> n1
    n6 --> n4
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    click n0 "../modules/authority.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/schemas_task.md"
    click n3 "../modules/task_detail_service.md"
    click n4 "../modules/task_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_delivery_scenarios.md"
    click n7 "../modules/test_human_work_queries.md"
    click n8 "../modules/test_task_domain.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [task_detail_service](../modules/task_detail_service.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_task_domain](../modules/test_task_domain.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_my_work_includes_nested_and_backlog_without_private_work` | *(async)* `(delivery_store)` | — | — |
| `test_lookup_matches_id_case_and_literal_wildcards_without_private_counts` | *(async)* `(delivery_store)` | — | — |
| `test_withdrawn_acceptance_stays_visible_in_owned_blocked_work` | *(async)* `(delivery_store)` | — | — |
| `test_my_work_filters_before_pagination_and_preserves_scope` | *(async)* `(delivery_store)` | — | — |
