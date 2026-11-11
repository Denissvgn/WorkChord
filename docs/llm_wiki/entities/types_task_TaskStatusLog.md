# TaskStatusLog

**Location:** `frontend/src/types/task.ts:373`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskStatusLog` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `task_id` | `number` | Yes | — | — |
| `task_title` | `string` | No | — | — |
| `from_status` | `TaskStatus` | Yes | — | — |
| `to_status` | `TaskStatus` | Yes | — | — |
| `changed_at` | `string` | Yes | — | — |
| `reason` | `string` | No | — | — |
| `triggered_by` | `string` | Yes | — | — |
| `affected_task_ids` | `number[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskStatusLog (frontend/src/types/task.ts)"]
    n1["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n2["TaskStatusFlow (frontend/src/components/analytics/TaskStatusFlow.tsx)"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/IterationOutlook.test.md"
    click n2 "../modules/TaskStatusFlow.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `affected_task_ids`, `changed_at`, `from_status`, `id`, `reason`, `task_id`, `task_title`, `to_status`, `triggered_by` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationOutlook.test` | import | [IterationOutlook.test](../modules/IterationOutlook.test.md) | — |
| `TaskStatusFlow` | type_reference | [TaskStatusFlow](../modules/TaskStatusFlow.md) | — |
| `AnalyticsPage` | import | [AnalyticsPage](../modules/AnalyticsPage.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
