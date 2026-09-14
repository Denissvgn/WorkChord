# AgentTaskCreate

**Location:** `backend/app/schemas/agent.py:235`
**Kind:** Pydantic model
**Bases:** `TaskCreate`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Agent task creation request.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTaskCreate (backend/app/schemas/agent.py)"]
    n1["TaskCreate (backend/app/schemas/task.py)"]
    n2["create_task (backend/app/mcp_agent_tools.py)"]
    n3["create_agent_task (backend/app/routers/agent.py)"]
    n4["create_planning_task (backend/app/routers/agent_planning.py)"]
    n5["AgentPlanningService.create_task (backend/app/services/agent_planning_service.py)"]
    n6["AgentService.create_task (backend/app/services/agent_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_agent.md"
    click n1 "../modules/schemas_task.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/routers_agent_planning.md"
    click n5 "../modules/agent_planning_service.md"
    click n6 "../modules/agent_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TaskCreate` | [schemas_task](../modules/schemas_task.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_task` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `create_agent_task` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `create_planning_task` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `AgentPlanningService.create_task` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentService.create_task` | type_reference | [agent_service](../modules/agent_service.md) | — |
