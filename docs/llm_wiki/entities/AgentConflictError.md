# AgentConflictError

**Location:** `backend/app/services/agent_service.py:54`
**Kind:** Class
**Bases:** `Exception`
**Module:** [agent_service](../modules/agent_service.md)

## Description

Raised when an agent operation conflicts with current task state.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentConflictError (backend/app/services/agent_service.py)"]
    n1["Exception"]
    n2["AgentModelConflictError (backend/app/services/agent_model_catalog_service.py)"]
    n3["AgentRoutingConflictError (backend/app/services/agent_routing_service.py)"]
    n4["AgentTeamSetupConflictError (backend/app/services/agent_team_setup_service.py)"]
    n5["_triage_command_replay (backend/app/mcp_agent_tools.py)"]
    n6["create_request_source_link (backend/app/mcp_agent_tools.py)"]
    n7["backend/app/mcp_server.py"]
    n8["backend/app/routers/agent.py"]
    n9["backend/app/routers/agent_planning.py"]
    n10["backend/app/services/agent_model_catalog_service.py"]
    n11["AgentPlanningService._lock_schedule_task_set (backend/app/services/agent_planning_service.py)"]
    n12["AgentPlanningService._replay (backend/app/services/agent_planning_service.py)"]
    n13["AgentPlanningService._schedule_input_digest (backend/app/services/agent_planning_service.py)"]
    n14["backend/app/services/agent_routing_service.py"]
    n15["AgentService._command_receipt_replay (backend/app/services/agent_service.py)"]
    n16["AgentService._validate_run_fence (backend/app/services/agent_service.py)"]
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
    n14 --> n0
    n15 --> n0
    n16 --> n0
    click n0 "../modules/agent_service.md"
    click n2 "../modules/agent_model_catalog_service.md"
    click n3 "../modules/agent_routing_service.md"
    click n4 "../modules/agent_team_setup_service.md"
    click n5 "../modules/mcp_agent_tools.md"
    click n6 "../modules/mcp_agent_tools.md"
    click n7 "../modules/mcp_server.md"
    click n8 "../modules/routers_agent.md"
    click n9 "../modules/routers_agent_planning.md"
    click n10 "../modules/agent_model_catalog_service.md"
    click n11 "../modules/agent_planning_service.md"
    click n12 "../modules/agent_planning_service.md"
    click n13 "../modules/agent_planning_service.md"
    click n14 "../modules/agent_routing_service.md"
    click n15 "../modules/agent_service.md"
    click n16 "../modules/agent_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_service](../modules/agent_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |
| Subclass | `AgentModelConflictError` | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) |
| Subclass | `AgentRoutingConflictError` | [agent_routing_service](../modules/agent_routing_service.md) |
| Subclass | `AgentTeamSetupConflictError` | [agent_team_setup_service](../modules/agent_team_setup_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_triage_command_replay` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 3 |
| `create_request_source_link` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 3 |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `agent_model_catalog_service` | import | [agent_model_catalog_service](../modules/agent_model_catalog_service.md) | — |
| `AgentPlanningService._lock_schedule_task_set` | call | [agent_planning_service](../modules/agent_planning_service.md) | 2 |
| `AgentPlanningService._replay` | call | [agent_planning_service](../modules/agent_planning_service.md) | 2 |
| `AgentPlanningService._schedule_input_digest` | call | [agent_planning_service](../modules/agent_planning_service.md) | 1 |
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `AgentService._command_receipt_replay` | call | [agent_service](../modules/agent_service.md) | 3 |
| `AgentService._validate_run_fence` | call | [agent_service](../modules/agent_service.md) | 1 |

> References: showing 12 of 50 logical references; 38 omitted by the 12-row generated summary limit.
