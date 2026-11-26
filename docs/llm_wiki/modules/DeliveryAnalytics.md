# DeliveryAnalytics Module

**Path:** `frontend/src/components/analytics/DeliveryAnalytics.tsx`

## Description

The human Analytics extension reads delivery reports through ordinary project/iteration authority. A compact duration table exposes means, medians, sample counts, missing starts and incomplete histories. Nonzero durations below the displayed precision use a less-than label, preserving the distinction between a short elapsed interval, zero and an unknown sample. Project selection works without an iteration or agent credential. Failed reads hide cached private queues; loading, retry, empty scopes and missing samples remain explicit.

_Auto-generated from `frontend/src/components/analytics/DeliveryAnalytics.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../../services/deliveryMetricsService` | `deliveryMetricsService` | — | compiler-dependent |
| `../../types/deliveryMetrics` | `DeliveryQueueItem` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `./useAnalyticsScope` | `useAnalyticsScope` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DeliveryAnalytics` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.test.tsx"]
    n1["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n2["frontend/src/components/analytics/useAnalyticsScope.ts"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/features/scope/useScopeLink.ts"]
    n5["frontend/src/pages/AnalyticsPage.tsx"]
    n6["frontend/src/services/deliveryMetricsService.ts"]
    n7["frontend/src/types/deliveryMetrics.ts"]
    n8["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n0 --> n7
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n6 --> n7
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/useAnalyticsScope.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/useScopeLink.md"
    click n5 "../modules/AnalyticsPage.md"
    click n6 "../modules/deliveryMetricsService.md"
    click n7 "../modules/deliveryMetrics.md"
    click n8 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics.test](../modules/DeliveryAnalytics.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [useAnalyticsScope](../modules/useAnalyticsScope.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [deliveryMetricsService](../modules/deliveryMetricsService.md) |
| Outbound | [deliveryMetrics](../modules/deliveryMetrics.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DeliveryAnalytics` | `({ days }: { days: number })` | — | Delivery history for the scope chosen in the scope bar. |
