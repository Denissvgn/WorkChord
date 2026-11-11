# NotificationsPanel Module

**Path:** `frontend/src/components/notifications/NotificationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/notifications/NotificationsPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDate`, `formatDateTime` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../ui/SegmentedControl` | `SegmentedControl` | — | compiler-dependent |
| `../ui/tone` | `isTaskStatus`, `statusTextClassName` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `History`, `CheckCircle` | — | compiler-dependent |
| `react` | `React`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `NotificationsPanel` |
| Constants | `ACTOR_LABEL_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/notifications/NotificationsPanel.tsx"]
    n2["frontend/src/components/ui/SegmentedControl.tsx"]
    n3["frontend/src/components/ui/tone.ts"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n4 --> n0
    n4 --> n1
    click n0 "../modules/QueryState.md"
    click n1 "../modules/NotificationsPanel.md"
    click n2 "../modules/SegmentedControl.md"
    click n3 "../modules/tone.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [SegmentedControl](../modules/SegmentedControl.md) |
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
| [NotificationsPanelProps](../entities/NotificationsPanelProps.md) | Interface | 21 | — | — |
| [Tab](../entities/Tab.md) | Type alias | 26 | `'history' \| 'overdue'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `NotificationsPanel` | `({ iterationId, className })` | — | — |
