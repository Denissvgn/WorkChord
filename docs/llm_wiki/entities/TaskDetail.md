# TaskDetail

**Location:** `frontend/src/types/task.ts:463`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskDetail` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task` | `Task` | Yes | — | — |
| `ancestors` | `TaskReference[]` | Yes | — | — |
| `ancestors_complete` | `boolean` | Yes | — | — |
| `children` | `TaskReferencePage` | Yes | — | — |
| `dependencies` | `TaskReferencePage` | Yes | — | — |
| `execution_context_complete` | `false` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDetail (frontend/src/types/task.ts)"]
    n1["frontend/src/components/tasks/CurrentTaskModal.test.tsx"]
    n2["TaskContextSummary (frontend/src/components/tasks/TaskContextSummary.tsx)"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.test.tsx"]
    n4["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/CurrentTaskModal.test.md"
    click n2 "../modules/TaskContextSummary.md"
    click n3 "../modules/TaskEditorDrawer.test.md"
    click n4 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `ancestors`, `ancestors_complete`, `children`, `dependencies`, `execution_context_complete`, `task` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CurrentTaskModal.test` | import | [CurrentTaskModal.test](../modules/CurrentTaskModal.test.md) | — |
| `TaskContextSummary` | type_reference | [TaskContextSummary](../modules/TaskContextSummary.md) | — |
| `TaskEditorDrawer.test` | import | [TaskEditorDrawer.test](../modules/TaskEditorDrawer.test.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
