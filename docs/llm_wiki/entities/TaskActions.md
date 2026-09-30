# TaskActions

**Location:** `frontend/src/types/task.ts:461`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskActions` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task_id` | `number` | Yes | — | — |
| `version` | `number` | Yes | — | — |
| `actions` | `TaskActionAvailability[]` | Yes | — | — |
| `claim_generation` | `number` | Yes | — | — |
| `running_run_ids` | `number[]` | Yes | — | — |
| `live_assignment_ids` | `number[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskActions (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `actions`, `claim_generation`, `live_assignment_ids`, `running_run_ids`, `task_id`, `version` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
