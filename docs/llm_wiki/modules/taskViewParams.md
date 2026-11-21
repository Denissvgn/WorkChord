# taskViewParams Module

**Path:** `frontend/src/features/savedViews/taskViewParams.ts`

## Description

_Auto-generated from `frontend/src/features/savedViews/taskViewParams.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `../../components/tasks/TaskList` | `SortKey` | Declaration | erased |
| `../../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `../planningMasters/planningTaskIssues` | `PLANNING_TASK_ISSUE_PARAM`, `parsePlanningTaskIssue` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TASK_CLEARED_VIEW_PARAM`, `TASK_CLEARED_VIEW_VALUE`, `TASK_FILTER_PARAMS`, `TASK_GROUP_PARAM`, `TASK_SORT_PARAM`, `activeFilterCount`, `filtersFromSearchParams`, `groupByStatusFromSearchParams`, `searchParamsNameView`, `sortKeyFromSearchParams`, `writeClearedViewMarker`, `writeFiltersToSearchParams`, `writeSortKeyToSearchParams` |
| Constants | `TASK_FILTER_PARAMS`, `TASK_SORT_PARAM`, `TASK_GROUP_PARAM`, `TASK_CLEARED_VIEW_PARAM`, `TASK_CLEARED_VIEW_VALUE`, `TASK_STATUSES`, `DATE_PATTERN`, `UNASSIGNED_VALUE`, `SORT_PARAM_VALUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/components/tasks/TaskList.tsx"]
    n2["frontend/src/features/overview/overviewSignals.test.ts"]
    n3["frontend/src/features/overview/overviewSignals.ts"]
    n4["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n5["frontend/src/features/savedViews/taskViewParams.test.ts"]
    n6["frontend/src/features/savedViews/taskViewParams.ts"]
    n7["frontend/src/pages/TasksPage.tsx"]
    n8["frontend/src/utils/taskFilterDefaults.ts"]
    n0 --> n4
    n0 --> n8
    n1 --> n0
    n2 --> n3
    n2 --> n6
    n3 --> n0
    n3 --> n6
    n3 --> n8
    n5 --> n6
    n5 --> n8
    n6 --> n0
    n6 --> n1
    n6 --> n4
    n6 --> n8
    n7 --> n0
    n7 --> n1
    n7 --> n4
    n7 --> n6
    n7 --> n8
    n8 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TaskList.md"
    click n2 "../modules/overviewSignals.test.md"
    click n3 "../modules/overviewSignals.md"
    click n4 "../modules/planningTaskIssues.md"
    click n5 "../modules/taskViewParams.test.md"
    click n6 "../modules/taskViewParams.md"
    click n7 "../modules/TasksPage.md"
    click n8 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [overviewSignals.test](../modules/overviewSignals.test.md) |
| Inbound | [overviewSignals](../modules/overviewSignals.md) |
| Inbound | [taskViewParams.test](../modules/taskViewParams.test.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [TaskList](../modules/TaskList.md) |
| Outbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `filtersFromSearchParams` | `(params: URLSearchParams) -> TaskFilters` | — | — |
| `writeFiltersToSearchParams` | `(params: URLSearchParams, filters: TaskFilters)` | — | Writes every filter into `params`, removing the ones that are off. |
| `searchParamsNameView` | `(params: URLSearchParams)` | — | True when the URL names any filter or a sort, or says they were all removed, so it carries a view of its own. |
| `writeClearedViewMarker` | `(params: URLSearchParams, viewShown: boolean)` | — | After a change to the filters or order: while a saved view is shown and the URL names no filter and no order, |
| `sortKeyFromSearchParams` | `(params: URLSearchParams) -> SortKey` | — | — |
| `writeSortKeyToSearchParams` | `(params: URLSearchParams, sortKey: SortKey)` | — | — |
| `groupByStatusFromSearchParams` | `(params: URLSearchParams)` | — | — |
| `activeFilterCount` | `(filters: TaskFilters)` | — | Number of active conditions, one per chip. |
