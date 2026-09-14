# AnalyticsPage Module

**Path:** `frontend/src/pages/AnalyticsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/AnalyticsPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/analytics/TaskStatusFlow` | `TaskStatusFlow` |
| `../components/dashboard/SavedViewDashboardCards` | `SavedViewDashboardCards` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/notifications/NotificationsPanel` | `NotificationsPanel` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../services/taskService` | `taskService` |
| `../store/iterationStore` | `useIterationStore` |
| `../types/task` | `TaskStatusLog` |
| `@tanstack/react-query` | `useQuery` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useNavigate` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/TaskStatusFlow.tsx"]
    n1["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/notifications/NotificationsPanel.tsx"]
    n4["frontend/src/components/ui/index.ts"]
    n5["frontend/src/pages/AnalyticsPage.tsx"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/store/iterationStore.ts"]
    n8["frontend/src/types/task.ts"]
    n0 --> n8
    n1 --> n2
    n3 --> n2
    n3 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n6 --> n8
    click n0 "../modules/TaskStatusFlow.md"
    click n1 "../modules/SavedViewDashboardCards.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/NotificationsPanel.md"
    click n4 "../modules/index.md"
    click n5 "../modules/AnalyticsPage.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/iterationStore.md"
    click n8 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskStatusFlow](../modules/TaskStatusFlow.md) |
| Outbound | [SavedViewDashboardCards](../modules/SavedViewDashboardCards.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [NotificationsPanel](../modules/NotificationsPanel.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [HistoryGroup](../entities/HistoryGroup.md) | Class | 13 | — | — |
