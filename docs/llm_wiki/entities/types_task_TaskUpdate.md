# TaskUpdate

**Location:** `frontend/src/types/task.ts:149`
**Kind:** Class
**Bases:** `Partial`
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskUpdate` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `status` | `string` | *required* | — |
| `expected_version` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskUpdate (frontend/src/types/task.ts)"]
    n1["Partial"]
    n2["frontend/src/components/gantt/TaskEditModal.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n4["toTaskUpdate (frontend/src/components/tasks/taskEditorContract.ts)"]
    n5["TaskEditorDrawer (frontend/src/components/tasks/TaskEditorDrawer.tsx)"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/pages/GanttPage.tsx"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/types/gantt.ts"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/types_task.md"
    click n2 "../modules/TaskEditModal.md"
    click n3 "../modules/KanbanBoard.md"
    click n4 "../modules/taskEditorContract.md"
    click n5 "../modules/TaskEditorDrawer.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/GanttPage.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/types_gantt.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `expected_version`, `status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Partial` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskEditModal` | import | [TaskEditModal](../modules/TaskEditModal.md) | — |
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `toTaskUpdate` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `TaskEditorDrawer` | type_reference | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `GanttPage` | import | [GanttPage](../modules/GanttPage.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
| `gantt` | import | [types_gantt](../modules/types_gantt.md) | — |
