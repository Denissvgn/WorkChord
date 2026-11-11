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
    n0["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["frontend/src/components/layout/CommandMenu.tsx"]
    n3["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n4["frontend/src/pages/ProjectsPage.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/pages/TriagePage.tsx"]
    n7["frontend/src/services/api.ts"]
    n8["frontend/src/services/savedViewService.ts"]
    n9["frontend/src/types/savedView.ts"]
    n0 --> n8
    n0 --> n9
    n1 --> n8
    n1 --> n9
    n2 --> n8
    n2 --> n9
    n3 --> n8
    n3 --> n9
    n4 --> n8
    n4 --> n9
    n5 --> n3
    n5 --> n8
    n5 --> n9
    n6 --> n8
    n6 --> n9
    n8 --> n7
    n8 --> n9
    click n0 "../modules/SavedViewDashboardCards.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/CommandMenu.md"
    click n3 "../modules/SavedViewsControl.md"
    click n4 "../modules/ProjectsPage.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/TriagePage.md"
    click n7 "../modules/api.md"
    click n8 "../modules/savedViewService.md"
    click n9 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SavedViewDashboardCards](../modules/SavedViewDashboardCards.md) |
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [CommandMenu](../modules/CommandMenu.md) |
| Inbound | [SavedViewsControl](../modules/SavedViewsControl.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [savedView](../modules/savedView.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendSavedViewService](../entities/FrontendSavedViewService.md) | Interface | 17 | — | — |
