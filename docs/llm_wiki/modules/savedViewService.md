# savedViewService Module

**Path:** `frontend/src/services/savedViewService.ts`

## Description

_Auto-generated from `frontend/src/services/savedViewService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/savedView` | `SavedView`, `SavedViewCreate`, `SavedViewDashboardCard`, `SavedViewDuplicate`, `SavedViewListParams`, `SavedViewUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendSavedViewService`, `savedViewService` |
| Constants | `savedViewService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n3["frontend/src/pages/ProjectsPage.tsx"]
    n4["frontend/src/pages/TasksPage.tsx"]
    n5["frontend/src/pages/TriagePage.tsx"]
    n6["frontend/src/services/api.ts"]
    n7["frontend/src/services/savedViewService.ts"]
    n8["frontend/src/types/savedView.ts"]
    n0 --> n7
    n0 --> n8
    n1 --> n7
    n1 --> n8
    n2 --> n7
    n2 --> n8
    n3 --> n7
    n3 --> n8
    n4 --> n2
    n4 --> n7
    n4 --> n8
    n5 --> n7
    n5 --> n8
    n7 --> n6
    n7 --> n8
    click n0 "../modules/SavedViewDashboardCards.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/SavedViewsControl.md"
    click n3 "../modules/ProjectsPage.md"
    click n4 "../modules/TasksPage.md"
    click n5 "../modules/TriagePage.md"
    click n6 "../modules/api.md"
    click n7 "../modules/savedViewService.md"
    click n8 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SavedViewDashboardCards](../modules/SavedViewDashboardCards.md) |
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [SavedViewsControl](../modules/SavedViewsControl.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [savedView](../modules/savedView.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendSavedViewService](../entities/FrontendSavedViewService.md) | Class | 17 | — | — |
