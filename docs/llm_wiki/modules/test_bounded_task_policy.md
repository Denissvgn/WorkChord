# test_bounded_task_policy Module

**Path:** `backend/tests/test_bounded_task_policy.py`

## Description

Nested UI detail observes inherited policy without loading an execution graph.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.models.identity` | `CommandAudit` |
| `app.models.task` | `Task` |
| `app.services.project_service` | `ProjectService` |
| `app.services.task_detail_service` | `TaskDetailService` |
| `app.services.task_service` | `TaskService` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/identity.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/services/project_service.py"]
    n4["backend/app/services/task_detail_service.py"]
    n5["backend/app/services/task_service.py"]
    n6["backend/tests/test_bounded_task_policy.py"]
    n7["backend/tests/test_delivery_scenarios.py"]
    n8["backend/tests/test_managed_authority.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n2
    n4 --> n0
    n4 --> n2
    n5 --> n0
    n5 --> n2
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n7 --> n2
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n7
    click n0 "../modules/authority.md"
    click n1 "../modules/models_identity.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/project_service.md"
    click n4 "../modules/task_detail_service.md"
    click n5 "../modules/task_service.md"
    click n6 "../modules/test_bounded_task_policy.md"
    click n7 "../modules/test_delivery_scenarios.md"
    click n8 "../modules/test_managed_authority.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [project_service](../modules/project_service.md) |
| Outbound | [task_detail_service](../modules/task_detail_service.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_nested_detail_returns_current_flags_without_graph_hydration` | *(async)* `(delivery_store)` | — | — |
| `test_deep_policy_is_complete_while_displayed_ancestry_remains_bounded` | *(async)* `(delivery_store)` | — | — |
| `test_hidden_parent_policy_cannot_disclose_private_scope` | *(async)* `(managed_store)` | — | — |
| `test_project_tree_serialization_preserves_loaded_parent_policy` | *(async)* `(delivery_store)` | — | — |
