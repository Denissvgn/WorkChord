# AgentReviewVerdictResponse

**Location:** `backend/app/schemas/agent.py:1003`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Verification result plus optional rework assignment.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `review_assignment` | `AgentTaskAssignmentResponse` | `review_assignment` | Yes | No | — | — | — | — |
| `task` | `TaskResponse` | `task` | Yes | No | — | — | — | — |
| `rework_assignment` | `Optional[AgentTaskAssignmentResponse]` | `rework_assignment` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentReviewVerdictResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["submit_my_agent_review_verdict (backend/app/routers/agent.py)"]
    n3["AgentWorkService.review (backend/app/services/agent_work_service.py)"]
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
| [schemas_agent](../modules/schemas_agent.md) | 0 | `review_assignment`, `rework_assignment`, `task` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `submit_my_agent_review_verdict` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.review` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.review` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
