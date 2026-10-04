# TaskBulkOperationResponse

**Location:** `frontend/src/types/task.ts:341`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskBulkOperationResponse` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `input_revisions` | `Record<number, number>` | No | — | — |
| `task_versions` | `Record<number, number>` | No | — | — |
| `requested_count` | `number` | Yes | — | — |
| `succeeded_count` | `number` | Yes | — | — |
| `failed_count` | `number` | Yes | — | — |
| `dry_run` | `boolean` | Yes | — | — |
| `results` | `TaskBulkOperationResult[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBulkOperationResponse (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n2["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskBulkOperationsPanel.md"
    click n2 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `dry_run`, `failed_count`, `input_revisions`, `requested_count`, `results`, `succeeded_count`, `task_versions` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskBulkOperationsPanel` | import | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
