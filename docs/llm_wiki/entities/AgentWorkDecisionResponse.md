# AgentWorkDecisionResponse

**Location:** `backend/app/schemas/agent.py:807`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Server-authoritative current/next work decision.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `actor` | `AgentActorResponse` | `actor` | Yes | No | — | — | — | — |
| `server_time` | `datetime` | `server_time` | Yes | No | — | — | — | — |
| `selection_policy` | `str` | `selection_policy` | No | No | `'assigned-work/v1'` | — | — | — |
| `queue_revision` | `int` | `queue_revision` | Yes | No | — | — | — | — |
| `pagination` | `AgentWorkPaginationMetadata` | `pagination` | Yes | No | — | — | — | — |
| `cursor` | `Optional[str]` | `cursor` | No | Yes | `None` | — | — | — |
| `state` | `Literal['resume', 'start_assigned', 'wait', 'no_work', 'attention_required']` | `state` | Yes | No | — | — | — | — |
| `current` | `Optional[AgentWorkItem]` | `current` | No | Yes | `None` | — | — | — |
| `next` | `Optional[AgentWorkItem]` | `next` | No | Yes | `None` | — | — | — |
| `queue` | `list[AgentWorkItem]` | `queue` | No | No | factory: `list` | — | — | — |
| `blocked_assigned` | `list[AgentWorkItem]` | `blocked_assigned` | No | No | factory: `list` | — | — | — |
| `recovery_codes` | `list[str]` | `recovery_codes` | No | No | factory: `list` | — | — | — |
| `next_poll_after` | `Optional[datetime]` | `next_poll_after` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentWorkDecisionResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["get_my_agent_work (backend/app/routers/agent.py)"]
    n3["AgentWorkService.get_work (backend/app/services/agent_work_service.py)"]
    n4["AgentWorkService.work_etag (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/agent_work_service.md"
    click n4 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `actor`, `blocked_assigned`, `current`, `cursor`, `next`, `next_poll_after`, `pagination`, `queue`, `queue_revision`, `recovery_codes`, `selection_policy`, `server_time` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_my_agent_work` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.get_work` | call | [agent_work_service](../modules/agent_work_service.md) | 5 |
| `AgentWorkService.get_work` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.work_etag` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
