# AgentModelCatalogResponse

**Location:** `backend/app/schemas/agent_routing.py:365`
**Kind:** Pydantic model
**Bases:** `AgentModelCatalogFields`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Persisted catalog projection.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogResponse (backend/app/schemas/agent_routing.py)"]
    n1["AgentModelCatalogFields (backend/app/schemas/agent_routing.py)"]
    n2["get_agent_model_catalog_entry (backend/app/routers/agent_catalog.py)"]
    n3["list_agent_model_catalog (backend/app/routers/agent_catalog.py)"]
    n4["AgentModelCatalogService._catalog_response (backend/app/services/agent_model_catalog_service.py)"]
    n5["AgentModelCatalogService.get_catalog (backend/app/services/agent_model_catalog_service.py)"]
    n6["AgentModelCatalogService.list_catalog (backend/app/services/agent_model_catalog_service.py)"]
    n7["backend/tests/test_agent_routing_data.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/agent_catalog.md"
    click n3 "../modules/agent_catalog.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/agent_model_catalog_service.md"
    click n6 "../modules/agent_model_catalog_service.md"
    click n7 "../modules/test_agent_routing_data.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | `created_at`, `id`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentModelCatalogFields` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_model_catalog_entry` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `list_agent_model_catalog` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `AgentModelCatalogService._catalog_response` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService.get_catalog` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentModelCatalogService.list_catalog` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `test_agent_routing_data` | import | [test_agent_routing_data](../modules/test_agent_routing_data.md) | — |
