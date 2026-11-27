# TaskFilters

**Location:** `frontend/src/components/tasks/TaskFiltersBar.tsx:14`
**Kind:** Interface
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
| `milestoneId` | `number \| null` | Yes | — | — |
| `needsAttention` | `boolean \| null` | Yes | — | — |
| `priority` | `number \| null` | Yes | — | — |
| `status` | `string \| null` | Yes | — | — |
| `hasDependency` | `boolean \| null` | Yes | — | — |
| `isOverdue` | `boolean \| null` | Yes | — | — |
| `isIterationOverflow` | `boolean \| null` | No | — | — |
| `isBlocked` | `boolean \| null` | No | — | — |
| `agentReady` | `boolean \| null` | Yes | — | — |
| `startDateFrom` | `string` | Yes | — | — |
| `startDateTo` | `string` | Yes | — | — |
| `endDateFrom` | `string` | Yes | — | — |
| `endDateTo` | `string` | Yes | — | — |
| `labelSlugs` | `string[]` | Yes | — | — |
| `labelGroupKeys` | `string[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskFilters (frontend/src/components/tasks/TaskFiltersBar.tsx)"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n2["PipelineView (frontend/src/components/tasks/PipelineView.tsx)"]
    n3["frontend/src/components/tasks/StoppedWork.test.tsx"]
    n4["frontend/src/components/tasks/TaskFiltersBar.test.tsx"]
    n5["TaskFiltersBar (frontend/src/components/tasks/TaskFiltersBar.tsx)"]
    n6["frontend/src/components/tasks/TaskList.test.tsx"]
    n7["frontend/src/components/tasks/TaskList.tsx"]
    n8["frontend/src/components/tasks/useSavedViewManager.tsx"]
    n9["overviewListFilters (frontend/src/features/overview/overviewSignals.ts)"]
    n10["activeFilterCount (frontend/src/features/savedViews/taskViewParams.ts)"]
    n11["filtersFromSearchParams (frontend/src/features/savedViews/taskViewParams.ts)"]
    n12["writeFiltersToSearchParams (frontend/src/features/savedViews/taskViewParams.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/KanbanBoard.md"
    click n2 "../modules/PipelineView.md"
    click n3 "../modules/StoppedWork.test.md"
    click n4 "../modules/TaskFiltersBar.test.md"
    click n5 "../modules/TaskFiltersBar.md"
    click n6 "../modules/TaskList.test.md"
    click n7 "../modules/TaskList.md"
    click n8 "../modules/useSavedViewManager.md"
    click n9 "../modules/overviewSignals.md"
    click n10 "../modules/taskViewParams.md"
    click n11 "../modules/taskViewParams.md"
    click n12 "../modules/taskViewParams.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskFiltersBar](../modules/TaskFiltersBar.md) | 0 | `agentReady`, `assigneeId`, `endDateFrom`, `endDateTo`, `hasDependency`, `isBlocked`, `isIterationOverflow`, `isOverdue`, `labelGroupKeys`, `labelSlugs`, `milestoneId`, `needsAttention` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `PipelineView` | type_reference | [PipelineView](../modules/PipelineView.md) | — |
| `StoppedWork.test` | import | [StoppedWork.test](../modules/StoppedWork.test.md) | — |
| `TaskFiltersBar.test` | import | [TaskFiltersBar.test](../modules/TaskFiltersBar.test.md) | — |
| `TaskFiltersBar` | type_reference | [TaskFiltersBar](../modules/TaskFiltersBar.md) | — |
| `TaskList.test` | import | [TaskList.test](../modules/TaskList.test.md) | — |
| `TaskList` | import | [TaskList](../modules/TaskList.md) | — |
| `useSavedViewManager` | import | [useSavedViewManager](../modules/useSavedViewManager.md) | — |
| `overviewListFilters` | type_reference | [overviewSignals](../modules/overviewSignals.md) | — |
| `activeFilterCount` | type_reference | [taskViewParams](../modules/taskViewParams.md) | — |
| `filtersFromSearchParams` | type_reference | [taskViewParams](../modules/taskViewParams.md) | — |
| `writeFiltersToSearchParams` | type_reference | [taskViewParams](../modules/taskViewParams.md) | — |

> References: showing 12 of 21 logical references; 9 omitted by the 12-row generated summary limit.
