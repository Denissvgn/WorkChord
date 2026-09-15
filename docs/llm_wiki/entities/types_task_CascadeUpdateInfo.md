# CascadeUpdateInfo

**Location:** `frontend/src/types/task.ts:322`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `CascadeUpdateInfo` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `task_id` | `number` | *required* | — |
| `task_title` | `string` | *required* | — |
| `old_start_date` | `string \| null` | *required* | — |
| `new_start_date` | `string \| null` | *required* | — |
| `old_end_date` | `string \| null` | *required* | — |
| `new_end_date` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CascadeUpdateInfo (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/StatusChangeControl.tsx"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/StatusChangeControl.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `new_end_date`, `new_start_date`, `old_end_date`, `old_start_date`, `task_id`, `task_title` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `StatusChangeControl` | import | [StatusChangeControl](../modules/StatusChangeControl.md) | — |
