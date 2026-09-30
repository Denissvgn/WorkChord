# savedViewState Module

**Path:** `frontend/src/utils/savedViewState.ts`

## Description

Compares effective saved-view filters and ordering against current defaults, treating label selections as sets. This supports explicit modified-state disclosure instead of implying that local filters are saved or shared.

## Imports

| Source | Symbols |
|--------|---------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` |
| `../types/savedView` | `SavedView` |
| `./taskFilterDefaults` | `defaultFilters` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `filterSignature`, `savedViewModified` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/pages/TasksPage.tsx"]
    n3["frontend/src/types/savedView.ts"]
    n4["frontend/src/utils/savedViewState.test.ts"]
    n5["frontend/src/utils/savedViewState.ts"]
    n6["frontend/src/utils/taskFilterDefaults.ts"]
    n0 --> n1
    n0 --> n3
    n0 --> n5
    n1 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n5 --> n1
    n5 --> n3
    n5 --> n6
    n6 --> n1
    click n0 "../modules/SavedViewsControl.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/TasksPage.md"
    click n3 "../modules/savedView.md"
    click n4 "../modules/savedViewState.test.md"
    click n5 "../modules/savedViewState.md"
    click n6 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SavedViewsControl](../modules/SavedViewsControl.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [savedViewState.test](../modules/savedViewState.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [savedView](../modules/savedView.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `filterSignature` | `(raw: Record<string, unknown> \| TaskFilters)` | — | — |
| `savedViewModified` | `(view: SavedView \| null \| undefined, filters: TaskFilters, sortKey: string)` | — | — |
