# TaskStatusChangeResponse

**Location:** `frontend/src/types/task.ts:360`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskStatusChangeResponse` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task` | `Task` | Yes | — | — |
| `cascade_updates` | `CascadeUpdateInfo[]` | Yes | — | — |
| `notifications_sent` | `boolean` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskStatusChangeResponse (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `cascade_updates`, `notifications_sent`, `task` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
