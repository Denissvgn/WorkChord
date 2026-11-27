# ReactivationRequirementInput

**Location:** `frontend/src/types/task.ts:554`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `ReactivationRequirementInput` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `kind` | `ReactivationRequirementKind` | Yes | — | — |
| `task_id` | `number` | No | — | — |
| `triage_item_id` | `number` | No | — | — |
| `on_date` | `string` | No | — | — |
| `description` | `string` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReactivationRequirementInput (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/TaskPostponeForm.tsx"]
    n2["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskPostponeForm.md"
    click n2 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `description`, `kind`, `on_date`, `task_id`, `triage_item_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskPostponeForm` | import | [TaskPostponeForm](../modules/TaskPostponeForm.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
