# savedViewState Module

**Path:** `frontend/src/utils/savedViewState.ts`

## Description

Compares effective saved-view filters and ordering against current defaults, treating label selections as sets. This supports explicit modified-state disclosure instead of implying that local filters are saved or shared.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `../types/savedView` | `SavedView` | Declaration | erased |
| `./taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `filterSignature`, `savedViewFilters`, `savedViewModified` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/components/tasks/useSavedViewManager.tsx"]
    n2["frontend/src/types/savedView.ts"]
    n3["frontend/src/utils/savedViewState.test.ts"]
    n4["frontend/src/utils/savedViewState.ts"]
    n5["frontend/src/utils/taskFilterDefaults.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n5 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/useSavedViewManager.md"
    click n2 "../modules/savedView.md"
    click n3 "../modules/savedViewState.test.md"
    click n4 "../modules/savedViewState.md"
    click n5 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [useSavedViewManager](../modules/useSavedViewManager.md) |
| Inbound | [savedViewState.test](../modules/savedViewState.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [savedView](../modules/savedView.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `savedViewFilters` | `(filters: TaskFilters) -> Record<string, unknown>` | — | The filters a saved view stores. |
| `filterSignature` | `(raw: Record<string, unknown> \| TaskFilters)` | — | — |
| `savedViewModified` | `(view: SavedView \| null \| undefined, filters: TaskFilters, sortKey: string, systemFilters: Partial<TaskFilters> = {})` | — | Whether the shown filters or sort differ from the saved view (or from no filters when none is chosen). |