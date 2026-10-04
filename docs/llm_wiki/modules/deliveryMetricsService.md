# deliveryMetricsService Module

**Path:** `frontend/src/services/deliveryMetricsService.ts`

## Description

_Auto-generated from `frontend/src/services/deliveryMetricsService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/deliveryMetrics` | `DeliveryMetrics` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `deliveryMetricsService` |
| Constants | `deliveryMetricsService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/deliveryMetricsService.ts"]
    n3["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/DeliveryAnalytics.md"
    click n1 "../modules/api.md"
    click n2 "../modules/deliveryMetricsService.md"
    click n3 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [deliveryMetrics](../modules/deliveryMetrics.md) |
