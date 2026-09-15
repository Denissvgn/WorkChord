# AgentRoutingConflictError

**Location:** `backend/app/services/agent_routing_service.py:114`
**Kind:** Class
**Bases:** `AgentConflictError`
**Module:** [agent_routing_service](../modules/agent_routing_service.md)

## Description

Stable routing conflict shared by REST, MCP, and assignment commands.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, message: str, **context: Any)` | — | — |
| `detail` | `() -> dict[str, Any]` | — | Return the client-safe structured conflict envelope. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingConflictError (backend/app/services/agent_routing_service.py)"]
    n1["AgentConflictError (backend/app/services/agent_service.py)"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/routers/agent.py"]
    n4["backend/app/routers/agent_planning.py"]
    n5["AgentRoutingService._assessment_replay (backend/app/services/agent_routing_service.py)"]
    n6["AgentRoutingService._build_preview (backend/app/services/agent_routing_service.py)"]
    n7["AgentRoutingService._completed_prior_lineage (backend/app/services/agent_routing_service.py)"]
    n8["AgentRoutingService._parse_preview_id (backend/app/services/agent_routing_service.py)"]
    n9["AgentRoutingService._preview_context (backend/app/services/agent_routing_service.py)"]
    n10["AgentRoutingService._preview_signing_key (backend/app/services/agent_routing_service.py)"]
    n11["AgentRoutingService._require_preview_rollout (backend/app/services/agent_routing_service.py)"]
    n12["AgentRoutingService.create_assessment (backend/app/services/agent_routing_service.py)"]
    n13["AgentRoutingService.validate_assignment_selection (backend/app/services/agent_routing_service.py)"]
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
    click n0 "../modules/agent_routing_service.md"
    click n1 "../modules/agent_service.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/agent_routing_service.md"
    click n8 "../modules/agent_routing_service.md"
    click n9 "../modules/agent_routing_service.md"
    click n10 "../modules/agent_routing_service.md"
    click n11 "../modules/agent_routing_service.md"
    click n12 "../modules/agent_routing_service.md"
    click n13 "../modules/agent_routing_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_service](../modules/agent_routing_service.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentConflictError` | [agent_service](../modules/agent_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `AgentRoutingService._assessment_replay` | call | [agent_routing_service](../modules/agent_routing_service.md) | 2 |
| `AgentRoutingService._build_preview` | call | [agent_routing_service](../modules/agent_routing_service.md) | 4 |
| `AgentRoutingService._completed_prior_lineage` | call | [agent_routing_service](../modules/agent_routing_service.md) | 2 |
| `AgentRoutingService._parse_preview_id` | call | [agent_routing_service](../modules/agent_routing_service.md) | 3 |
| `AgentRoutingService._preview_context` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService._preview_signing_key` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService._require_preview_rollout` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService.create_assessment` | call | [agent_routing_service](../modules/agent_routing_service.md) | 3 |
| `AgentRoutingService.validate_assignment_selection` | call | [agent_routing_service](../modules/agent_routing_service.md) | 8 |

> References: showing 12 of 23 logical references; 11 omitted by the 12-row generated summary limit.
