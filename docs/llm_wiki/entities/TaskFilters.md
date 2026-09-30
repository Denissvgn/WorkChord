# TaskFilters

**Location:** `frontend/src/components/tasks/TaskFiltersBar.tsx:15`
**Kind:** Class
**Bases:** —
**Module:** [TaskFiltersBar](../modules/TaskFiltersBar.md)

## Description

_Auto-generated from `TaskFilters` in `frontend/src/components/tasks/TaskFiltersBar.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `planningIssue` | `PlanningTaskIssue \| null` | Yes | — | — |
| `assigneeId` | `number \| null` | Yes | — | — |
| `projectId` | `number \| null` | Yes | — | — |
| `priority` | `number \| null` | Yes | — | — |
| `status` | `string \| null` | Yes | — | — |
| `hasDependency` | `boolean \| null` | Yes | — | — |
| `isOverdue` | `boolean \| null` | Yes | — | — |
| `isIterationOverflow` | `boolean \| null` | No | — | — |
| `agentReady` | `boolean \| null` | Yes | — | — |
| `startDateFrom` | `string` | Yes | — | — |
| `startDateTo` | `string` | Yes | — | — |
| `endDateFrom` | `string` | Yes | — | — |
| `endDateTo` | `string` | Yes | — | — |
| `labelSlugs` | `string[]` | Yes | — | — |
| `labelGroupKeys` | `string[]` | Yes | — | — |

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
    n9["selectVisibleWork (frontend/src/utils/visibleWork.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/KanbanBoard.md"
    click n2 "../modules/SavedViewsControl.md"
    click n3 "../modules/TaskFiltersBar.md"
    click n4 "../modules/TaskList.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/taskFilterDefaults.md"
    click n7 "../modules/taskFilters.md"
    click n8 "../modules/taskFilters.md"
    click n9 "../modules/visibleWork.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskFiltersBar](../modules/TaskFiltersBar.md) | 0 | `agentReady`, `assigneeId`, `endDateFrom`, `endDateTo`, `hasDependency`, `isIterationOverflow`, `isOverdue`, `labelGroupKeys`, `labelSlugs`, `planningIssue`, `priority`, `projectId` |

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
| `selectVisibleWork` | type_reference | [visibleWork](../modules/visibleWork.md) | — |
