# TaskStatusFlow Module

**Path:** `frontend/src/components/analytics/TaskStatusFlow.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/TaskStatusFlow.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `TaskStatus`, `TaskStatusLog` |
| `../../utils/formatDate` | `formatDateTime` |
| `../ui/tone` | `STATUS_TONE`, `toneBorderClassName` |
| `clsx` | `clsx` |
| `lucide-react` | `ArrowRight` |
| `react` | `React` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskStatusFlow` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/TaskStatusFlow.tsx"]
    n1["frontend/src/components/ui/tone.ts"]
    n2["frontend/src/pages/AnalyticsPage.tsx"]
    n3["frontend/src/types/task.ts"]
    n4["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n0 --> n3
    n0 --> n4
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/TaskStatusFlow.md"
    click n1 "../modules/tone.md"
    click n2 "../modules/AnalyticsPage.md"
    click n3 "../modules/types_task.md"
    click n4 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskStatusFlowProps](../entities/TaskStatusFlowProps.md) | Class | 9 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskStatusFlow` | `({ logs })` | — | — |
