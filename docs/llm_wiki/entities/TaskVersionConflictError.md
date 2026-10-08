# TaskVersionConflictError

**Location:** `backend/app/services/task_service.py:50`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [task_service](../modules/task_service.md)

## Description

Raised when an optimistic task write no longer matches the stored version.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(expected_version: int, current_task: dict[str, Any])` | — | — |
| `detail` | `() -> dict[str, Any]` | — | Return the stable API conflict envelope. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskVersionConflictError (backend/app/services/task_service.py)"]
    n1["RuntimeError"]
    n2["backend/app/mcp_server.py"]
    n3["backend/app/routers/agent.py"]
    n4["backend/app/routers/agent_planning.py"]
    n5["backend/app/routers/gantt.py"]
    n6["backend/app/routers/task_domain.py"]
    n7["_raise_task_version_conflict (backend/app/routers/tasks.py)"]
    n8["AgentRoutingService._build_preview (backend/app/services/agent_routing_service.py)"]
    n9["AgentRoutingService.create_assessment (backend/app/services/agent_routing_service.py)"]
    n10["AgentWorkService._terminal_work (backend/app/services/agent_work_service.py)"]
    n11["AgentWorkService.begin (backend/app/services/agent_work_service.py)"]
    n12["AgentWorkService.create_assignment (backend/app/services/agent_work_service.py)"]
    n13["AgentWorkService.renew_work (backend/app/services/agent_work_service.py)"]
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
    click n0 "../modules/task_service.md"
    click n2 "../modules/mcp_server.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/routers_gantt.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/tasks.md"
    click n8 "../modules/agent_routing_service.md"
    click n9 "../modules/agent_routing_service.md"
    click n10 "../modules/agent_work_service.md"
    click n11 "../modules/agent_work_service.md"
    click n12 "../modules/agent_work_service.md"
    click n13 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_service](../modules/task_service.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `gantt` | import | [routers_gantt](../modules/routers_gantt.md) | — |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `_raise_task_version_conflict` | type_reference | [tasks](../modules/tasks.md) | — |
| `AgentRoutingService._build_preview` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentRoutingService.create_assessment` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AgentWorkService._terminal_work` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.begin` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.create_assignment` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.renew_work` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |

> References: showing 12 of 25 logical references; 13 omitted by the 12-row generated summary limit.
