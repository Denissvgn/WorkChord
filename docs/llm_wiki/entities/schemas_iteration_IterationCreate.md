# IterationCreate

**Location:** `backend/app/schemas/iteration.py:12`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

Schema for creating an iteration.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `str` | `name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `calendar_id` | `Optional[int]` | `calendar_id` | No | Yes | `None` | — | — | — |
| `project_id` | `Optional[int]` | `project_id` | No | Yes | `None` | — | — | — |
| `start_date` | `date` | `start_date` | Yes | No | — | — | — | — |
| `end_date` | `date` | `end_date` | Yes | No | — | — | — | — |
| `manager_email` | `Optional[str]` | `manager_email` | No | Yes | `None` | max_length=255 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationCreate (backend/app/schemas/iteration.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_iteration (backend/app/routers/agent_planning.py)"]
    n4["import_new_iteration (backend/app/routers/export.py)"]
    n5["create_iteration (backend/app/routers/iterations.py)"]
    n6["backend/app/schemas/__init__.py"]
    n7["AgentPlanningService.create_iteration (backend/app/services/agent_planning_service.py)"]
    n8["IterationService.create (backend/app/services/iteration_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/export.md"
    click n5 "../modules/iterations.md"
    click n6 "../modules/schemas___init__.md"
    click n7 "../modules/agent_planning_service.md"
    click n8 "../modules/iteration_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `calendar_id`, `end_date`, `manager_email`, `name`, `project_id`, `start_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `create_iteration` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `import_new_iteration` | call | [export](../modules/export.md) | 1 |
| `create_iteration` | type_reference | [iterations](../modules/iterations.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `AgentPlanningService.create_iteration` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `IterationService.create` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
