# taskFilterDefaults Module

**Path:** `frontend/src/utils/taskFilterDefaults.ts`

## Description

_Auto-generated from `frontend/src/utils/taskFilterDefaults.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `defaultFilters` |
| Constants | `defaultFilters` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.test.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/features/savedViews/taskViewState.ts"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n4["frontend/src/utils/savedViewState.test.ts"]
    n5["frontend/src/utils/savedViewState.ts"]
    n6["frontend/src/utils/taskFilterDefaults.ts"]
    n7["frontend/src/utils/taskFilters.test.ts"]
    n8["frontend/src/utils/visibleWork.test.ts"]
    n0 --> n1
    n0 --> n6
    n1 --> n6
    n2 --> n1
    n2 --> n6
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n4 --> n5
    n4 --> n6
    n5 --> n1
    n5 --> n6
    n6 --> n1
    n7 --> n6
    n8 --> n6
    click n0 "../modules/TaskFiltersBar.test.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/taskViewState.md"
    click n3 "../modules/TasksPage.md"
    click n4 "../modules/savedViewState.test.md"
    click n5 "../modules/savedViewState.md"
    click n6 "../modules/taskFilterDefaults.md"
    click n7 "../modules/taskFilters.test.md"
    click n8 "../modules/visibleWork.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskFiltersBar.test](../modules/TaskFiltersBar.test.md) |
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [taskViewState](../modules/taskViewState.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [savedViewState.test](../modules/savedViewState.test.md) |
| Inbound | [savedViewState](../modules/savedViewState.md) |
| Inbound | [taskFilters.test](../modules/taskFilters.test.md) |
| Inbound | [visibleWork.test](../modules/visibleWork.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
