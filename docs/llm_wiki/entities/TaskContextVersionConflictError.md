# TaskContextVersionConflictError

**Location:** `backend/app/services/task_context_revision_service.py:14`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [task_context_revision_service](../modules/task_context_revision_service.md)

## Description

Raised when another transaction reserves the task context version first.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskContextVersionConflictError (backend/app/services/task_context_revision_service.py)"]
    n1["RuntimeError"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["reserve_task_context_revision (backend/app/services/task_context_revision_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/task_context_revision_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/task_context_revision_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_context_revision_service](../modules/task_context_revision_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `reserve_task_context_revision` | call | [task_context_revision_service](../modules/task_context_revision_service.md) | 1 |
