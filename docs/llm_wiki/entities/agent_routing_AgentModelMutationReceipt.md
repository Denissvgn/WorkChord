# AgentModelMutationReceipt

**Location:** `backend/app/schemas/agent_routing.py:487`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Durable, replay-safe receipt for an operator model mutation.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `operation` | `str` | `operation` | Yes | No | — | max_length=100; min_length=1 | — | — |
| `actor_id` | `int` | `actor_id` | Yes | No | — | ge=1 | — | — |
| `target_type` | `Literal['model_catalog', 'model_binding']` | `target_type` | Yes | No | — | — | — | — |
| `target_id` | `int` | `target_id` | Yes | No | — | ge=1 | — | — |
| `idempotency_key` | `str` | `idempotency_key` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `rationale` | `str` | `rationale` | Yes | No | — | max_length=2000; min_length=1 | — | — |
| `correlation_id` | `str` | `correlation_id` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `authoritative_revision` | `PositiveRevision` | `authoritative_revision` | Yes | No | — | — | — | — |
| `invalidated_assignment_ids` | `list[int]` | `invalidated_assignment_ids` | No | No | factory: `list` | — | — | — |
| `audit_event_ids` | `list[int]` | `audit_event_ids` | No | No | factory: `list` | — | — | — |
| `result` | `dict[str, Any]` | `result` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelMutationReceipt (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n2["create_agent_model_binding (backend/app/routers/agent_catalog.py)"]
    n3["create_agent_model_catalog_entry (backend/app/routers/agent_catalog.py)"]
    n4["disable_agent_model_binding (backend/app/routers/agent_catalog.py)"]
    n5["disable_agent_model_catalog_entry (backend/app/routers/agent_catalog.py)"]
    n6["update_agent_model_binding (backend/app/routers/agent_catalog.py)"]
    n7["update_agent_model_catalog_entry (backend/app/routers/agent_catalog.py)"]
    n8["AgentModelCatalogService._execute (backend/app/services/agent_model_catalog_service.py)"]
    n9["AgentModelCatalogService._replay (backend/app/services/agent_model_catalog_service.py)"]
    n10["AgentModelCatalogService.create_binding (backend/app/services/agent_model_catalog_service.py)"]
    n11["AgentModelCatalogService.create_catalog (backend/app/services/agent_model_catalog_service.py)"]
    n12["AgentModelCatalogService.disable_binding (backend/app/services/agent_model_catalog_service.py)"]
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
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/agent_catalog.md"
    click n3 "../modules/agent_catalog.md"
    click n4 "../modules/agent_catalog.md"
    click n5 "../modules/agent_catalog.md"
    click n6 "../modules/agent_catalog.md"
    click n7 "../modules/agent_catalog.md"
    click n8 "../modules/agent_model_catalog_service.md"
    click n9 "../modules/agent_model_catalog_service.md"
    click n10 "../modules/agent_model_catalog_service.md"
    click n11 "../modules/agent_model_catalog_service.md"
    click n12 "../modules/agent_model_catalog_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | `actor_id`, `audit_event_ids`, `authoritative_revision`, `correlation_id`, `idempotency_key`, `invalidated_assignment_ids`, `operation`, `rationale`, `result`, `target_id`, `target_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_agent_model_binding` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `create_agent_model_catalog_entry` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `disable_agent_model_binding` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `disable_agent_model_catalog_entry` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `update_agent_model_binding` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `update_agent_model_catalog_entry` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `AgentModelCatalogService._execute` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._execute` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService._replay` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService.create_binding` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService.create_catalog` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService.disable_binding` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |

> References: showing 12 of 15 logical references; 3 omitted by the 12-row generated summary limit.
