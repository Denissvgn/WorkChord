# AgentTaskContextResponse

**Location:** `backend/app/schemas/agent.py:760`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Complete task context for an assigned worker.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `assignment` | `Optional[AgentTaskAssignmentResponse]` | `assignment` | No | Yes | `None` | — | — | — |
| `task_brief` | `dict[str, str]` | `task_brief` | No | No | factory: `dict` | — | — | — |
| `parent_chain` | `list[dict[str, Any]]` | `parent_chain` | No | No | factory: `list` | — | — | — |
| `dependencies` | `list[AgentDependencyContext]` | `dependencies` | No | No | factory: `list` | — | — | — |
| `request_sources` | `list[RequestSourceLinkWithSourceResponse]` | `request_sources` | No | No | factory: `list` | — | — | — |
| `timeline` | `list[TaskTimelineItem]` | `timeline` | No | No | factory: `list` | — | — | — |
| `definition_ready` | `bool` | `definition_ready` | No | No | `False` | — | — | — |
| `start_ready` | `bool` | `start_ready` | No | No | `False` | — | — | — |
| `blocker_codes` | `list[str]` | `blocker_codes` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTaskContextResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["get_agent_task_context (backend/app/routers/agent.py)"]
    n3["AgentWorkService.get_task_context (backend/app/services/agent_work_service.py)"]
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
| [schemas_agent](../modules/schemas_agent.md) | 0 | `assignment`, `blocker_codes`, `definition_ready`, `dependencies`, `parent_chain`, `request_sources`, `start_ready`, `task`, `task_brief`, `timeline` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_agent_task_context` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.get_task_context` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.get_task_context` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
