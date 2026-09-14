# AgentPermissionError

**Location:** `backend/app/services/agent_service.py:58`
**Kind:** Class
**Bases:** `Exception`
**Module:** [agent_service](../modules/agent_service.md)

## Description

Raised when an agent lacks a required scope.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentPermissionError (backend/app/services/agent_service.py)"]
    n1["Exception"]
    n2["_require_scope_requirement (backend/app/mcp_server.py)"]
    n3["backend/app/routers/agent.py"]
    n4["backend/app/routers/agent_planning.py"]
    n5["AgentModelCatalogService._execute (backend/app/services/agent_model_catalog_service.py)"]
    n6["AgentModelCatalogService._require_read (backend/app/services/agent_model_catalog_service.py)"]
    n7["AgentRoutingService._require_assessment_write (backend/app/services/agent_routing_service.py)"]
    n8["AgentRoutingService._require_read (backend/app/services/agent_routing_service.py)"]
    n9["AgentRoutingService.preview_task_routing (backend/app/services/agent_routing_service.py)"]
    n10["AgentRoutingService.validate_assignment_selection (backend/app/services/agent_routing_service.py)"]
    n11["AgentService._validate_run_fence (backend/app/services/agent_service.py)"]
    n12["AgentService.claim_task (backend/app/services/agent_service.py)"]
    n13["AgentService.create_task (backend/app/services/agent_service.py)"]
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
    click n0 "../modules/agent_service.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/agent_model_catalog_service.md"
    click n6 "../modules/agent_model_catalog_service.md"
    click n7 "../modules/agent_routing_service.md"
    click n8 "../modules/agent_routing_service.md"
    click n9 "../modules/agent_routing_service.md"
    click n10 "../modules/agent_routing_service.md"
    click n11 "../modules/agent_service.md"
    click n12 "../modules/agent_service.md"
    click n13 "../modules/agent_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_service](../modules/agent_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_require_scope_requirement` | call | [mcp_server](../modules/mcp_server.md) | 1 |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `AgentModelCatalogService._execute` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentModelCatalogService._require_read` | call | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | 1 |
| `AgentRoutingService._require_assessment_write` | call | [agent_routing_service](../modules/agent_routing_service.md) | 2 |
| `AgentRoutingService._require_read` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService.preview_task_routing` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService.validate_assignment_selection` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentService._validate_run_fence` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentService.claim_task` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentService.create_task` | call | [agent_service](../modules/agent_service.md) | 1 |

> References: showing 12 of 37 logical references; 25 omitted by the 12-row generated summary limit.
