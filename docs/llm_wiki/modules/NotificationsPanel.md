# NotificationsPanel Module

**Path:** `frontend/src/components/notifications/NotificationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/notifications/NotificationsPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../utils/formatDate` | `formatDate`, `formatDateTime` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../ui/tone` | `isTaskStatus`, `statusTextClassName` |
| `@tanstack/react-query` | `useQuery` |
| `clsx` | `clsx` |
| `lucide-react` | `AlertCircle`, `History`, `CheckCircle` |
| `react` | `React`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `NotificationsPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/notifications/NotificationsPanel.tsx"]
    n2["frontend/src/components/ui/tone.ts"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/services/taskService.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n1 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n4
    click n0 "../modules/QueryState.md"
    click n1 "../modules/NotificationsPanel.md"
    click n2 "../modules/tone.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/taskService.md"
    click n5 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [NotificationsPanelProps](../entities/NotificationsPanelProps.md) | Class | 12 | — | — |
| [Tab](../entities/Tab.md) | Type alias | 17 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `NotificationsPanel` | `({ iterationId, className })` | — | — |
