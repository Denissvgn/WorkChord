# TaskActionsResponse

**Location:** `backend/app/schemas/task_domain.py:41`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_domain](../modules/schemas_task_domain.md)

## Description

_Auto-generated from `TaskActionsResponse` in `backend/app/schemas/task_domain.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `version` | `int` | `version` | Yes | No | — | — | — | — |
| `actions` | `list[TaskActionAvailability]` | `actions` | Yes | No | — | — | — | — |
| `claim_generation` | `int` | `claim_generation` | Yes | No | — | — | — | — |
| `running_run_ids` | `list[int]` | `running_run_ids` | Yes | No | — | — | — | — |
| `live_assignment_ids` | `list[int]` | `live_assignment_ids` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskActionsResponse (backend/app/schemas/task_domain.py)"]
    n1["BaseModel"]
    n2["task_actions (backend/app/routers/task_domain.py)"]
    n3["TaskDomainService.allowed_actions (backend/app/services/task_domain_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_task_domain.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/task_domain_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_domain](../modules/schemas_task_domain.md) | 0 | `actions`, `claim_generation`, `live_assignment_ids`, `running_run_ids`, `task_id`, `version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `task_actions` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `TaskDomainService.allowed_actions` | call | [task_domain_service](../modules/task_domain_service.md) | 1 |
