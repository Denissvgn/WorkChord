# savedViewService Module

**Path:** `frontend/src/services/savedViewService.ts`

## Description

_Auto-generated from `frontend/src/services/savedViewService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/savedView` | `SavedView`, `SavedViewCreate`, `SavedViewDashboardCard`, `SavedViewDuplicate`, `SavedViewListParams`, `SavedViewUpdate` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendSavedViewService`, `savedViewService` |
| Constants | `savedViewService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/components/tasks/useSavedViewManager.tsx"]
    n2["frontend/src/pages/ProjectsPage.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/services/savedViewService.ts"]
    n7["frontend/src/types/savedView.ts"]
    n0 --> n6
    n0 --> n7
    n1 --> n6
    n1 --> n7
    n2 --> n6
    n2 --> n7
    n3 --> n1
    n3 --> n6
    n3 --> n7
    n4 --> n6
    n6 --> n5
    n6 --> n7
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/useSavedViewManager.md"
    click n2 "../modules/ProjectsPage.md"
    click n3 "../modules/TasksPage.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/api.md"
    click n6 "../modules/savedViewService.md"
    click n7 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CommandMenu](../modules/CommandMenu.md) |
| Inbound | [useSavedViewManager](../modules/useSavedViewManager.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [savedView](../modules/savedView.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendSavedViewService](../entities/FrontendSavedViewService.md) | Interface | 17 | — | — |
