# AgentRecoveryRequeueResponse

**Location:** `backend/app/schemas/agent.py:1054`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Authoritative result of stale-work reconciliation and requeue.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `assignment` | `AgentTaskAssignmentResponse` | `assignment` | Yes | No | — | — | — | — |
| `cancelled_assignment_ids` | `list[int]` | `cancelled_assignment_ids` | No | No | factory: `list` | — | — | — |
| `cancelled_run_ids` | `list[int]` | `cancelled_run_ids` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRecoveryRequeueResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["requeue_agent_recovery_task (backend/app/routers/agent.py)"]
    n3["AgentWorkService.requeue_recovery (backend/app/services/agent_work_service.py)"]
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
| [schemas_agent](../modules/schemas_agent.md) | 0 | `assignment`, `cancelled_assignment_ids`, `cancelled_run_ids`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `requeue_agent_recovery_task` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.requeue_recovery` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.requeue_recovery` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
