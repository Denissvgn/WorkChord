# AgentWorkBeginResponse

**Location:** `backend/app/schemas/agent.py:884`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Atomic begin result containing all new authoritative state.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `assignment` | `AgentTaskAssignmentResponse` | `assignment` | Yes | No | — | — | — | — |
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `run` | `AgentRunResponse` | `run` | Yes | No | — | — | — | — |
| `claim_id` | `str` | `claim_id` | Yes | No | — | — | — | — |
| `claim_generation` | `int` | `claim_generation` | Yes | No | — | — | — | — |
| `claim_expires_at` | `datetime` | `claim_expires_at` | Yes | No | — | — | — | — |
| `queue_revision` | `int` | `queue_revision` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentWorkBeginResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["begin_my_agent_work (backend/app/routers/agent.py)"]
    n3["renew_my_agent_work (backend/app/routers/agent.py)"]
    n4["AgentWorkService._live_fence_receipt (backend/app/services/agent_work_service.py)"]
    n5["AgentWorkService._replay_live_fence_receipt (backend/app/services/agent_work_service.py)"]
    n6["AgentWorkService.begin (backend/app/services/agent_work_service.py)"]
    n7["AgentWorkService.renew_work (backend/app/services/agent_work_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_work_service.md"
    click n5 "../modules/agent_work_service.md"
    click n6 "../modules/agent_work_service.md"
    click n7 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `assignment`, `claim_expires_at`, `claim_generation`, `claim_id`, `queue_revision`, `run`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `begin_my_agent_work` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `renew_my_agent_work` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService._live_fence_receipt` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService._replay_live_fence_receipt` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.begin` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.begin` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `AgentWorkService.renew_work` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.renew_work` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
