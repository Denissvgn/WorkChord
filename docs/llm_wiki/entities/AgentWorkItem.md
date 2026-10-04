# AgentWorkItem

**Location:** `backend/app/schemas/agent.py:786`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

One ordered assigned-work item.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `assignment` | `AgentTaskAssignmentResponse` | `assignment` | Yes | No | — | — | — | — |
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `queue_position` | `int` | `queue_position` | Yes | No | — | — | — | — |
| `selection_key` | `list[Any]` | `selection_key` | No | No | factory: `list` | — | — | — |
| `selection_reason` | `str` | `selection_reason` | Yes | No | — | — | — | — |
| `blocker_codes` | `list[str]` | `blocker_codes` | No | No | factory: `list` | — | — | — |
| `claim` | `Optional[dict[str, Any]]` | `claim` | No | Yes | `None` | — | — | — |
| `run` | `Optional[AgentRunResponse]` | `run` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentWorkItem (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["AgentWorkService._paginate_work_collections (backend/app/services/agent_work_service.py)"]
    n3["AgentWorkService._work_item (backend/app/services/agent_work_service.py)"]
    n4["AgentWorkService._work_item_key (backend/app/services/agent_work_service.py)"]
    n5["AgentWorkService._work_snapshot_record (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/agent_work_service.md"
    click n3 "../modules/agent_work_service.md"
    click n4 "../modules/agent_work_service.md"
    click n5 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `assignment`, `blocker_codes`, `claim`, `queue_position`, `run`, `selection_key`, `selection_reason`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentWorkService._paginate_work_collections` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._work_item` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService._work_item` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._work_item_key` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._work_snapshot_record` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
