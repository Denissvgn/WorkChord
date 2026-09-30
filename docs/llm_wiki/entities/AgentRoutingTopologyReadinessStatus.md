# AgentRoutingTopologyReadinessStatus

**Location:** `backend/app/services/agent_routing_rollout.py:30`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_routing_rollout](../modules/agent_routing_rollout.md)

## Description

Closed readiness states supplied by the setup authority.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `UNAVAILABLE` | `'unavailable'` | — |
| `NOT_READY` | `'not_ready'` | — |
| `READY` | `'ready'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingTopologyReadinessStatus (backend/app/services/agent_routing_rollout.py)"]
    n1["StrEnum"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/routers/agent.py"]
    n4["AgentRoutingTopologyReadiness.__post_init__ (backend/app/services/agent_routing_rollout.py)"]
    n5["backend/app/services/agent_routing_service.py"]
    n6["backend/app/services/agent_work_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/agent_routing_rollout.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_routing_rollout.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_rollout](../modules/agent_routing_rollout.md) | 0 | `NOT_READY`, `READY`, `UNAVAILABLE` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `AgentRoutingTopologyReadiness.__post_init__` | call | [agent_routing_rollout](../modules/agent_routing_rollout.md) | 1 |
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `agent_work_service` | import | [agent_work_service](../modules/agent_work_service.md) | — |
