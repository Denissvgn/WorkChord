# TaskBulkOperationResult

**Location:** `frontend/src/types/task.ts:331`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskBulkOperationResult` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task_id` | `number` | Yes | — | — |
| `outcome` | `TaskBulkOutcome` | Yes | — | — |
| `changes` | `Record<string, { old: unknown; new: unknown } \| unknown>` | Yes | — | — |
| `warnings` | `string[]` | Yes | — | — |
| `error` | `string \| null` | No | — | — |
| `task` | `Task \| null` | No | — | — |
| `assignee_recommendation` | `AssigneeRecommendation \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBulkOperationResult (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskBulkOperationsPanel.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `assignee_recommendation`, `changes`, `error`, `outcome`, `task`, `task_id`, `warnings` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskBulkOperationsPanel` | import | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) | — |
