# AgentRecoveryListResponse

**Location:** `backend/app/schemas/agent.py:1069`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Paginated PM recovery projection.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `items` | `list[AgentRecoveryItem]` | `items` | No | No | factory: `list` | — | — | — |
| `pagination` | `AgentPaginationMetadata` | `pagination` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRecoveryListResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["list_agent_recovery_tasks (backend/app/routers/agent.py)"]
    n3["AgentWorkService.list_recovery_tasks (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `items`, `pagination` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_agent_recovery_tasks` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.list_recovery_tasks` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.list_recovery_tasks` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
