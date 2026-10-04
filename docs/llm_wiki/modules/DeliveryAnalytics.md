# DeliveryAnalytics Module

**Path:** `frontend/src/components/analytics/DeliveryAnalytics.tsx`

## Description

The human Analytics extension reads delivery reports through ordinary project/iteration authority. A compact duration table exposes means, medians, sample counts, missing starts and incomplete histories. Project selection works without an iteration or agent credential. Failed reads hide cached private queues; loading, retry, empty scopes and missing samples remain explicit.

_Auto-generated from `frontend/src/components/analytics/DeliveryAnalytics.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/deliveryMetricsService` | `deliveryMetricsService` |
| `../../services/projectService` | `projectService` |
| `../../types/deliveryMetrics` | `DeliveryQueueItem` |
| `../feedback/QueryState` | `QueryErrorState` |
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
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/services/deliveryMetricsService.ts"]
    n5["frontend/src/services/projectService.ts"]
    n6["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n1
    n0 --> n6
    n1 --> n2
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n3 --> n1
    n3 --> n2
    n4 --> n6
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/deliveryMetricsService.md"
    click n5 "../modules/projectService.md"
    click n6 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics.test](../modules/DeliveryAnalytics.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
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
