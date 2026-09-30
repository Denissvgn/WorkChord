# AgentModelCatalogCreate

**Location:** `backend/app/schemas/agent_routing.py:272`
**Kind:** Pydantic model
**Bases:** `AgentModelCatalogFields`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Create payload for a catalog entry.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `revision` | `Literal[1]` | `revision` | No | No | `1` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogCreate (backend/app/schemas/agent_routing.py)"]
    n1["AgentModelCatalogFields (backend/app/schemas/agent_routing.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_agent_model_catalog_entry (backend/app/routers/agent_catalog.py)"]
    n4["AgentModelCatalogService.create_catalog (backend/app/services/agent_model_catalog_service.py)"]
    n5["backend/tests/test_agent_routing_contract.py"]
    n6["backend/tests/test_agent_routing_data.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/agent_catalog.md"
    click n4 "../modules/agent_model_catalog_service.md"
    click n5 "../modules/test_agent_routing_contract.md"
    click n6 "../modules/test_agent_routing_data.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | `revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentModelCatalogFields` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `create_agent_model_catalog_entry` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `AgentModelCatalogService.create_catalog` | type_reference | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `test_agent_routing_contract` | import | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
| `test_agent_routing_data` | import | [test_agent_routing_data](../modules/test_agent_routing_data.md) | — |
