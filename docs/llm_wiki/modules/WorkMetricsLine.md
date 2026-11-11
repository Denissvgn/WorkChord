# WorkMetricsLine Module

**Path:** `frontend/src/components/tasks/WorkMetricsLine.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/WorkMetricsLine.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `MetricScope`, `WorkMetricName` | Declaration | erased |
| `../../types/workMetrics` | `WorkMetrics` | Declaration | erased |
| `../../utils/workNumbers` | `formatCount` | — | compiler-dependent |
| `./MetricCount` | `MetricCount` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkMetricsLine` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/MetricCount.test.tsx"]
    n1["frontend/src/components/tasks/MetricCount.tsx"]
    n2["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/pages/OverviewPage.tsx"]
    n5["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/workMetrics.ts"]
    n8["frontend/src/utils/workNumbers.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n7
    n1 --> n6
    n2 --> n1
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n4 --> n8
    n5 --> n2
    click n0 "../modules/MetricCount.test.md"
    click n1 "../modules/MetricCount.md"
    click n2 "../modules/WorkMetricsLine.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/OverviewPage.md"
    click n5 "../modules/ProjectReleaseDetailPage.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/workMetrics.md"
    click n8 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MetricCount.test](../modules/MetricCount.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Outbound | [MetricCount](../modules/MetricCount.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [workMetrics](../modules/workMetrics.md) |
| Outbound | [workNumbers](../modules/workNumbers.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `WorkMetricsLine` | `({ metrics, scope = null }: { metrics?: WorkMetrics \| null; scope?: MetricScope \| null })` | — | Delivery counts; with a scope, each one opens the tasks it counts. |
