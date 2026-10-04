# TaskTextContext

**Location:** `frontend/src/types/task.ts:284`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskTextContext` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `text` | `string` | Yes | — | — |
| `iteration_id` | `number` | Yes | — | — |
| `iteration_revision` | `number` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTextContext (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/TaskTextEditorModal.tsx"]
    n2["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskTextEditorModal.md"
    click n2 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `iteration_id`, `iteration_revision`, `text` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskTextEditorModal` | import | [TaskTextEditorModal](../modules/TaskTextEditorModal.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
