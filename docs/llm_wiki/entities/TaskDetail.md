# TaskDetail

**Location:** `frontend/src/types/task.ts:472`
**Kind:** Interface
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
| `reviewer_name` | `string \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDetail (frontend/src/types/task.ts)"]
    n1["frontend/src/components/gantt/TaskEditModal.test.tsx"]
    n2["frontend/src/components/tasks/CurrentTaskModal.test.tsx"]
    n3["TaskContextSummary (frontend/src/components/tasks/TaskContextSummary.tsx)"]
    n4["frontend/src/components/tasks/TaskEditorDrawer.test.tsx"]
    n5["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskEditModal.test.md"
    click n2 "../modules/CurrentTaskModal.test.md"
    click n3 "../modules/TaskContextSummary.md"
    click n4 "../modules/TaskEditorDrawer.test.md"
    click n5 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `ancestors`, `ancestors_complete`, `children`, `dependencies`, `execution_context_complete`, `reviewer_name`, `task` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskEditModal.test` | import | [TaskEditModal.test](../modules/TaskEditModal.test.md) | — |
| `CurrentTaskModal.test` | import | [CurrentTaskModal.test](../modules/CurrentTaskModal.test.md) | — |
| `TaskContextSummary` | type_reference | [TaskContextSummary](../modules/TaskContextSummary.md) | — |
| `TaskEditorDrawer.test` | import | [TaskEditorDrawer.test](../modules/TaskEditorDrawer.test.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
