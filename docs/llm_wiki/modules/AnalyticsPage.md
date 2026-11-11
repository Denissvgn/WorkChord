# AnalyticsPage Module

**Path:** `frontend/src/pages/AnalyticsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/AnalyticsPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/analytics/DeliveryAnalytics` | `DeliveryAnalytics` | — | compiler-dependent |
| `../components/analytics/TaskStatusFlow` | `TaskStatusFlow` | — | compiler-dependent |
| `../components/dashboard/SavedViewDashboardCards` | `SavedViewDashboardCards` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/notifications/NotificationsPanel` | `NotificationsPanel` | — | compiler-dependent |
| `../components/tasks/WorkMetricsLine` | `WorkMetricsLine` | — | compiler-dependent |
| `../components/ui` | `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/taskService` | `taskService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../types/task` | `TaskStatusLog` | Declaration | erased |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useNavigate` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n1["frontend/src/components/analytics/TaskStatusFlow.tsx"]
    n2["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/notifications/NotificationsPanel.tsx"]
    n5["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n6["frontend/src/components/ui/index.ts"]
    n7["frontend/src/pages/AnalyticsPage.tsx"]
    n8["frontend/src/services/iterationService.ts"]
    n9["frontend/src/services/taskService.ts"]
    n10["frontend/src/store/iterationStore.ts"]
    n11["frontend/src/types/task.ts"]
    n0 --> n3
    n1 --> n11
    n2 --> n3
    n4 --> n3
    n4 --> n9
    n5 --> n9
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n7 --> n11
    n9 --> n11
    click n0 "../modules/DeliveryAnalytics.md"
    click n1 "../modules/TaskStatusFlow.md"
    click n2 "../modules/SavedViewDashboardCards.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/NotificationsPanel.md"
    click n5 "../modules/WorkMetricsLine.md"
    click n6 "../modules/index.md"
    click n7 "../modules/AnalyticsPage.md"
    click n8 "../modules/iterationService.md"
    click n9 "../modules/taskService.md"
    click n10 "../modules/iterationStore.md"
    click n11 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Outbound | [TaskStatusFlow](../modules/TaskStatusFlow.md) |
| Outbound | [SavedViewDashboardCards](../modules/SavedViewDashboardCards.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [NotificationsPanel](../modules/NotificationsPanel.md) |
| Outbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
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
| [HistoryGroup](../entities/HistoryGroup.md) | Interface | 16 | — | — |
