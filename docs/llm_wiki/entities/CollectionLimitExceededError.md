# CollectionLimitExceededError

**Location:** `backend/app/query_limits.py:14`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [query_limits](../modules/query_limits.md)

## Description

A synchronous endpoint would exceed its documented response bound.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(resource: str, maximum: int)` | — | — |
| `detail` | `() -> dict[str, object]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CollectionLimitExceededError (backend/app/query_limits.py)"]
    n1["RuntimeError"]
    n2["collection_limit_error (backend/app/main.py)"]
    n3["AgentModelCatalogService.list_bindings (backend/app/services/agent_model_catalog_service.py)"]
    n4["AgentModelCatalogService.list_catalog (backend/app/services/agent_model_catalog_service.py)"]
    n5["AgentRoutingService._build_preview (backend/app/services/agent_routing_service.py)"]
    n6["AgentRoutingService._preview_context (backend/app/services/agent_routing_service.py)"]
    n7["AgentService.get_pipeline (backend/app/services/agent_service.py)"]
    n8["AgentWorkService.list_actor_roster (backend/app/services/agent_work_service.py)"]
    n9["DeliveryMetricsService.report (backend/app/services/delivery_metrics_service.py)"]
    n10["IterationService._reconcile_tasks_for_project_scope (backend/app/services/iteration_service.py)"]
    n11["IterationService.get_all (backend/app/services/iteration_service.py)"]
    n12["ProjectService.get_tasks (backend/app/services/project_service.py)"]
    n13["ProjectService.list_initiatives (backend/app/services/project_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/query_limits.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/agent_model_catalog_service.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/agent_work_service.md"
    click n9 "../modules/delivery_metrics_service.md"
    click n10 "../modules/iteration_service.md"
    click n11 "../modules/iteration_service.md"
    click n12 "../modules/project_service.md"
    click n13 "../modules/project_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [query_limits](../modules/query_limits.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `collection_limit_error` | type_reference | [app_main](../modules/app_main.md) | — |
| `AgentModelCatalogService.list_bindings` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService.list_catalog` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentRoutingService._build_preview` | call | [agent_routing_service](../modules/agent_routing_service.md) | 3 |
| `AgentRoutingService._preview_context` | call | [agent_routing_service](../modules/agent_routing_service.md) | 4 |
| `AgentService.get_pipeline` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentWorkService.list_actor_roster` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `DeliveryMetricsService.report` | call | [delivery_metrics_service](../modules/delivery_metrics_service.md) | 3 |
| `IterationService._reconcile_tasks_for_project_scope` | call | [iteration_service](../modules/iteration_service.md) | 1 |
| `IterationService.get_all` | call | [iteration_service](../modules/iteration_service.md) | 1 |
| `ProjectService.get_tasks` | call | [project_service](../modules/project_service.md) | 1 |
| `ProjectService.list_initiatives` | call | [project_service](../modules/project_service.md) | 1 |

> References: showing 12 of 28 logical references; 16 omitted by the 12-row generated summary limit.
