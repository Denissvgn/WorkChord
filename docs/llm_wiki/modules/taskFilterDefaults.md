# taskFilterDefaults Module

**Path:** `frontend/src/utils/taskFilterDefaults.ts`

## Description

_Auto-generated from `frontend/src/utils/taskFilterDefaults.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `defaultFilters` |
| Constants | `defaultFilters` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
<!-- Thick arrows (==>) mark edges inside an import cycle. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/pages/TasksPage.tsx"]
    n2["frontend/src/utils/savedViewState.test.ts"]
    n3["frontend/src/utils/savedViewState.ts"]
    n4["frontend/src/utils/taskFilterDefaults.ts"]
    n5["frontend/src/utils/taskFilters.test.ts"]
    n6["frontend/src/utils/visibleWork.test.ts"]
    n0 ==> n4
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n3 --> n0
    n3 --> n4
    n4 ==> n0
    n5 --> n4
    n6 --> n4
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TasksPage.md"
    click n2 "../modules/savedViewState.test.md"
    click n3 "../modules/savedViewState.md"
    click n4 "../modules/taskFilterDefaults.md"
    click n5 "../modules/taskFilters.test.md"
    click n6 "../modules/visibleWork.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [savedViewState.test](../modules/savedViewState.test.md) |
| Inbound | [savedViewState](../modules/savedViewState.md) |
| Inbound | [taskFilters.test](../modules/taskFilters.test.md) |
| Inbound | [visibleWork.test](../modules/visibleWork.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
