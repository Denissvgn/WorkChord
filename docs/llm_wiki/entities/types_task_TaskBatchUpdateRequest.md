# TaskBatchUpdateRequest

**Location:** `frontend/src/types/task.ts:399`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskBatchUpdateRequest` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expected_revision` | `number` | No | — | — |
| `tasks` | `TaskBatchUpdateItem[]` | Yes | — | — |
| `expected_planning_revision` | `number` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBatchUpdateRequest (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `expected_planning_revision`, `expected_revision`, `tasks` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
