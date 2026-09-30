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
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/components/tasks/TaskList.tsx"]
    n2["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n3["frontend/src/types/label.ts"]
    n4["frontend/src/types/task.ts"]
    n5["frontend/src/utils/taskFilters.test.ts"]
    n6["frontend/src/utils/taskFilters.ts"]
    n7["frontend/src/utils/visibleWork.ts"]
    n0 --> n2
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n1 --> n6
    n1 --> n7
    n2 --> n4
    n5 --> n4
    n5 --> n6
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n7 --> n0
    n7 --> n3
    n7 --> n4
    n7 --> n6
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TaskList.md"
    click n2 "../modules/planningTaskIssues.md"
    click n3 "../modules/types_label.md"
    click n4 "../modules/types_task.md"
    click n5 "../modules/taskFilters.test.md"
    click n6 "../modules/taskFilters.md"
    click n7 "../modules/visibleWork.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [taskFilters.test](../modules/taskFilters.test.md) |
| Inbound | [visibleWork](../modules/visibleWork.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Outbound | [types_label](../modules/types_label.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `taskMatchesFilters` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = []) -> boolean` | — | — |
| `filterTaskWithChildren` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = [], inherited = { deferred: false, optional: false }) -> Task \| null` | — | — |
