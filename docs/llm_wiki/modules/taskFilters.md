# taskFilters Module

**Path:** `frontend/src/utils/taskFilters.ts`

## Description

_Auto-generated from `frontend/src/utils/taskFilters.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` |
| `../features/planningMasters/planningTaskIssues` | `taskMatchesPlanningIssue` |
| `../types/label` | `LabelGroup` |
| `../types/task` | `Task` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `filterTaskWithChildren`, `taskMatchesFilters` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/components/tasks/TaskList.tsx"]
    n3["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n4["frontend/src/types/label.ts"]
    n5["frontend/src/types/task.ts"]
    n6["frontend/src/utils/taskFilters.test.ts"]
    n7["frontend/src/utils/taskFilters.ts"]
    n0 --> n1
    n0 --> n5
    n0 --> n7
    n1 --> n3
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n7
    n3 --> n5
    n6 --> n5
    n6 --> n7
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/TaskList.md"
    click n3 "../modules/planningTaskIssues.md"
    click n4 "../modules/types_label.md"
    click n5 "../modules/types_task.md"
    click n6 "../modules/taskFilters.test.md"
    click n7 "../modules/taskFilters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [taskFilters.test](../modules/taskFilters.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Outbound | [types_label](../modules/types_label.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `taskMatchesFilters` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = []) -> boolean` | — | — |
| `filterTaskWithChildren` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = []) -> Task \| null` | — | — |
