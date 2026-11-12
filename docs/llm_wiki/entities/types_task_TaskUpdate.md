# TaskUpdate

**Location:** `frontend/src/types/task.ts:196`
**Kind:** Interface
**Bases:** `Partial<TaskCreate>`
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskUpdate` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `status` | `string` | No | — | — |
| `expected_version` | `number` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskUpdate (frontend/src/types/task.ts)"]
    n1["Partial#60;TaskCreate#62;"]
    n2["frontend/src/components/gantt/TaskEditModal.test.tsx"]
    n3["frontend/src/components/gantt/TaskEditModal.tsx"]
    n4["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n5["toTaskUpdate (frontend/src/components/tasks/taskEditorContract.ts)"]
    n6["TaskEditorDrawer (frontend/src/components/tasks/TaskEditorDrawer.tsx)"]
    n7["frontend/src/components/tasks/TaskForm.tsx"]
    n8["frontend/src/pages/GanttPage.tsx"]
    n9["frontend/src/services/taskService.ts"]
    n10["frontend/src/types/gantt.ts"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/types_task.md"
    click n2 "../modules/TaskEditModal.test.md"
    click n3 "../modules/TaskEditModal.md"
    click n4 "../modules/KanbanBoard.md"
    click n5 "../modules/taskEditorContract.md"
    click n6 "../modules/TaskEditorDrawer.md"
    click n7 "../modules/TaskForm.md"
    click n8 "../modules/GanttPage.md"
    click n9 "../modules/taskService.md"
    click n10 "../modules/types_gantt.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `expected_version`, `status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Partial<TaskCreate>` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskEditModal.test` | import | [TaskEditModal.test](../modules/TaskEditModal.test.md) | — |
| `TaskEditModal` | import | [TaskEditModal](../modules/TaskEditModal.md) | — |
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `toTaskUpdate` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `TaskEditorDrawer` | type_reference | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `GanttPage` | import | [GanttPage](../modules/GanttPage.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
| `gantt` | import | [types_gantt](../modules/types_gantt.md) | — |
