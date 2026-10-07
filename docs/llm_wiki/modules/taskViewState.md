# taskViewState Module

**Path:** `frontend/src/features/savedViews/taskViewState.ts`

## Description

Saved task-view parsing is a pure shared boundary for accepted filter types, planning-issue keys and supported sorting choices. Page queries, scope changes and editor dismissal remain with the owning route.

_Auto-generated from `frontend/src/features/savedViews/taskViewState.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../components/tasks/TaskFiltersBar` | `TaskFilters` |
| `../../components/tasks/TaskList` | `SortKey` |
| `../../types/savedView` | `SavedView` |
| `../../utils/taskFilterDefaults` | `defaultFilters` |
| `../planningMasters/planningTaskIssues` | `parsePlanningTaskIssue` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `filtersFromSavedView`, `sortKeyFromSavedView` |
| Constants | `SORT_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/components/tasks/TaskList.tsx"]
    n2["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n3["frontend/src/features/savedViews/taskViewState.ts"]
    n4["frontend/src/pages/TasksPage.tsx"]
    n5["frontend/src/types/savedView.ts"]
    n6["frontend/src/utils/taskFilterDefaults.ts"]
    n0 --> n2
    n0 --> n6
    n1 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n6 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TaskList.md"
    click n2 "../modules/planningTaskIssues.md"
    click n3 "../modules/taskViewState.md"
    click n4 "../modules/TasksPage.md"
    click n5 "../modules/savedView.md"
    click n6 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [TaskList](../modules/TaskList.md) |
| Outbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Outbound | [savedView](../modules/savedView.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `filtersFromSavedView` | `(view: SavedView) -> TaskFilters` | — | — |
| `sortKeyFromSavedView` | `(view: SavedView) -> SortKey \| null` | — | — |