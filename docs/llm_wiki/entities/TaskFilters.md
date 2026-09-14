# TaskFilters

**Location:** `frontend/src/components/tasks/TaskFiltersBar.tsx:15`
**Kind:** Class
**Bases:** —
**Module:** [TaskFiltersBar](../modules/TaskFiltersBar.md)

## Description

_Auto-generated from `TaskFilters` in `frontend/src/components/tasks/TaskFiltersBar.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `planningIssue` | `PlanningTaskIssue \| null` | *required* | — |
| `assigneeId` | `number \| null` | *required* | — |
| `projectId` | `number \| null` | *required* | — |
| `priority` | `number \| null` | *required* | — |
| `status` | `string \| null` | *required* | — |
| `hasDependency` | `boolean \| null` | *required* | — |
| `isOverdue` | `boolean \| null` | *required* | — |
| `agentReady` | `boolean \| null` | *required* | — |
| `startDateFrom` | `string` | *required* | — |
| `startDateTo` | `string` | *required* | — |
| `endDateFrom` | `string` | *required* | — |
| `endDateTo` | `string` | *required* | — |
| `labelSlugs` | `string[]` | *required* | — |
| `labelGroupKeys` | `string[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskFilters (frontend/src/components/tasks/TaskFiltersBar.tsx)"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n2["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n3["TaskFiltersBar (frontend/src/components/tasks/TaskFiltersBar.tsx)"]
    n4["frontend/src/components/tasks/TaskList.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/utils/taskFilterDefaults.ts"]
    n7["filterTaskWithChildren (frontend/src/utils/taskFilters.ts)"]
    n8["taskMatchesFilters (frontend/src/utils/taskFilters.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/KanbanBoard.md"
    click n2 "../modules/SavedViewsControl.md"
    click n3 "../modules/TaskFiltersBar.md"
    click n4 "../modules/TaskList.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/taskFilterDefaults.md"
    click n7 "../modules/taskFilters.md"
    click n8 "../modules/taskFilters.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskFiltersBar](../modules/TaskFiltersBar.md) | 0 | `agentReady`, `assigneeId`, `endDateFrom`, `endDateTo`, `hasDependency`, `isOverdue`, `labelGroupKeys`, `labelSlugs`, `planningIssue`, `priority`, `projectId`, `startDateFrom` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `SavedViewsControl` | import | [SavedViewsControl](../modules/SavedViewsControl.md) | — |
| `TaskFiltersBar` | type_reference | [TaskFiltersBar](../modules/TaskFiltersBar.md) | — |
| `TaskList` | import | [TaskList](../modules/TaskList.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
| `taskFilterDefaults` | import | [taskFilterDefaults](../modules/taskFilterDefaults.md) | — |
| `filterTaskWithChildren` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
| `taskMatchesFilters` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
