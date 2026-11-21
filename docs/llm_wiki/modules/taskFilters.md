# taskFilters Module

**Path:** `frontend/src/utils/taskFilters.ts`

## Description

_Auto-generated from `frontend/src/utils/taskFilters.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `../features/planningMasters/planningTaskIssues` | `hasDeliverySignal`, `isFinished`, `taskMatchesPlanningIssue` | — | compiler-dependent |
| `../types/label` | `LabelGroup` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `filterTaskBySearch`, `filterTaskWithChildren`, `taskMatchesFilters`, `taskNeedsAttention` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/PipelineView.tsx"]
    n2["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n5["frontend/src/types/label.ts"]
    n6["frontend/src/types/task.ts"]
    n7["frontend/src/utils/taskFilters.test.ts"]
    n8["frontend/src/utils/taskFilters.ts"]
    n9["frontend/src/utils/visibleWork.ts"]
    n0 --> n2
    n0 --> n6
    n0 --> n8
    n0 --> n9
    n1 --> n2
    n1 --> n5
    n1 --> n6
    n1 --> n8
    n2 --> n4
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n8
    n3 --> n9
    n4 --> n6
    n7 --> n6
    n7 --> n8
    n8 --> n2
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n9 --> n2
    n9 --> n5
    n9 --> n6
    n9 --> n8
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/PipelineView.md"
    click n2 "../modules/TaskFiltersBar.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/planningTaskIssues.md"
    click n5 "../modules/types_label.md"
    click n6 "../modules/types_task.md"
    click n7 "../modules/taskFilters.test.md"
    click n8 "../modules/taskFilters.md"
    click n9 "../modules/visibleWork.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [PipelineView](../modules/PipelineView.md) |
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
| `taskNeedsAttention` | `(task: Task)` | — | Work that needs a person to act: a blocker is recorded, delivery is late or outside its limits, |
| `taskMatchesFilters` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = []) -> boolean` | — | — |
| `filterTaskBySearch` | `(task: Task, query: string) -> Task \| null` | — | Keep a task when its title or #ID matches, or when any child does (children are narrowed too). |
| `filterTaskWithChildren` | `(task: Task, filters: TaskFilters \| undefined, labelGroups: LabelGroup[] = [], inherited = { deferred: false, optional: false }) -> Task \| null` | — | — |
