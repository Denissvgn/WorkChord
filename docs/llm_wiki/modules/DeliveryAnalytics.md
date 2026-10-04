# DeliveryAnalytics Module

**Path:** `frontend/src/components/analytics/DeliveryAnalytics.tsx`

## Description

The human Analytics extension reads delivery reports through ordinary project/iteration authority. A compact duration table exposes means, medians, sample counts, missing starts and incomplete histories. Nonzero durations below the displayed precision use a less-than label, preserving the distinction between a short elapsed interval, zero and an unknown sample. Project selection works without an iteration or agent credential. Failed reads hide cached private queues; loading, retry, empty scopes and missing samples remain explicit.

_Auto-generated from `frontend/src/components/analytics/DeliveryAnalytics.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/deliveryMetricsService` | `deliveryMetricsService` |
| `../../services/projectService` | `projectService` |
| `../../types/deliveryMetrics` | `DeliveryQueueItem` |
| `../feedback/QueryState` | `QueryErrorState` |
| `./ExecutionUsagePanel` | `ExecutionUsagePanel` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DeliveryAnalytics` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.test.tsx"]
    n1["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n2["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/pages/AnalyticsPage.tsx"]
    n5["frontend/src/services/deliveryMetricsService.ts"]
    n6["frontend/src/services/projectService.ts"]
    n7["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n1
    n0 --> n7
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n4 --> n1
    n4 --> n3
    n5 --> n7
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/ExecutionUsagePanel.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/AnalyticsPage.md"
    click n5 "../modules/deliveryMetricsService.md"
    click n6 "../modules/projectService.md"
    click n7 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics.test](../modules/DeliveryAnalytics.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [ExecutionUsagePanel](../modules/ExecutionUsagePanel.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [deliveryMetricsService](../modules/deliveryMetricsService.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [deliveryMetrics](../modules/deliveryMetrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DeliveryAnalytics` | `({ iterationId }: { iterationId?: number })` | — | — |