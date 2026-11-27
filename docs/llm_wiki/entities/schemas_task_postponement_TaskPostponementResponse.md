# TaskPostponementResponse

**Location:** `backend/app/schemas/task_postponement.py:158`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_postponement](../modules/schemas_task_postponement.md)

## Description

A task together with its open or most recent postponement. The postponement is absent only for work that was reactivated from a postponed state that never had a record.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `postponement` | `TaskPostponementRecord \| None` | `postponement` | Yes | Yes | — | — | — | The open or most recent postponement; null only for work reactivated from a postponed state that had no record. |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskPostponementResponse (backend/app/schemas/task_postponement.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["postpone_task (backend/app/routers/task_domain.py)"]
    n4["reactivate_task (backend/app/routers/task_domain.py)"]
    n5["record_owner_decision (backend/app/routers/task_domain.py)"]
    n6["task_postponement (backend/app/routers/task_domain.py)"]
    n7["backend/app/services/agent_planning_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_task_postponement.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/agent_planning_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_postponement](../modules/schemas_task_postponement.md) | 0 | `postponement`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `postpone_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `reactivate_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `record_owner_decision` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_postponement` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
