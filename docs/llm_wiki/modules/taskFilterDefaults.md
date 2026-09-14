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
    n2["frontend/src/utils/taskFilterDefaults.ts"]
    n3["frontend/src/utils/taskFilters.test.ts"]
    n0 ==> n2
    n1 --> n0
    n1 --> n2
    n2 ==> n0
    n3 --> n2
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TasksPage.md"
    click n2 "../modules/taskFilterDefaults.md"
    click n3 "../modules/taskFilters.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [taskFilters.test](../modules/taskFilters.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
