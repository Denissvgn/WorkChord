# savedView Module

**Path:** `frontend/src/types/savedView.ts`

## Description

_Auto-generated from `frontend/src/types/savedView.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SavedView`, `SavedViewCreate`, `SavedViewDashboardCard`, `SavedViewDuplicate`, `SavedViewListParams`, `SavedViewScope`, `SavedViewType`, `SavedViewUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n1["frontend/src/components/layout/AppSidebar.test.tsx"]
    n2["frontend/src/components/layout/AppSidebar.tsx"]
    n3["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n4["frontend/src/i18n/seedDisplay.ts"]
    n5["frontend/src/pages/ProjectsPage.tsx"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/pages/TriagePage.tsx"]
    n8["frontend/src/services/savedViewService.ts"]
    n9["frontend/src/types/savedView.ts"]
    n0 --> n4
    n0 --> n8
    n0 --> n9
    n1 --> n2
    n1 --> n9
    n2 --> n4
    n2 --> n8
    n2 --> n9
    n3 --> n4
    n3 --> n8
    n3 --> n9
    n4 --> n9
    n5 --> n8
    n5 --> n9
    n6 --> n3
    n6 --> n4
    n6 --> n8
    n6 --> n9
    n7 --> n4
    n7 --> n8
    n7 --> n9
    n8 --> n9
    click n0 "../modules/SavedViewDashboardCards.md"
    click n1 "../modules/AppSidebar.test.md"
    click n2 "../modules/AppSidebar.md"
    click n3 "../modules/SavedViewsControl.md"
    click n4 "../modules/seedDisplay.md"
    click n5 "../modules/ProjectsPage.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/TriagePage.md"
    click n8 "../modules/savedViewService.md"
    click n9 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SavedViewDashboardCards](../modules/SavedViewDashboardCards.md) |
| Inbound | [AppSidebar.test](../modules/AppSidebar.test.md) |
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [SavedViewsControl](../modules/SavedViewsControl.md) |
| Inbound | [seedDisplay](../modules/seedDisplay.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Inbound | [savedViewService](../modules/savedViewService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SavedView](../entities/savedView_SavedView.md) | Class | 4 | — | — |
| [SavedViewDashboardCard](../entities/SavedViewDashboardCard.md) | Class | 24 | — | — |
| [SavedViewListParams](../entities/SavedViewListParams.md) | Class | 37 | — | — |
| [SavedViewCreate](../entities/savedView_SavedViewCreate.md) | Class | 41 | — | — |
| [SavedViewUpdate](../entities/savedView_SavedViewUpdate.md) | Class | 52 | — | — |
| [SavedViewDuplicate](../entities/SavedViewDuplicate.md) | Class | 63 | — | — |
| [SavedViewType](../entities/savedView_SavedViewType.md) | Type alias | 1 | — | — |
| [SavedViewScope](../entities/savedView_SavedViewScope.md) | Type alias | 2 | — | — |
