# deliveryMetrics Module

**Path:** `frontend/src/types/deliveryMetrics.ts`

## Description

_Auto-generated from `frontend/src/types/deliveryMetrics.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DeliveryMetrics`, `DeliveryQueueItem`, `DurationSamples` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.test.tsx"]
    n1["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n2["frontend/src/services/deliveryMetricsService.ts"]
    n3["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/deliveryMetricsService.md"
    click n3 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics.test](../modules/DeliveryAnalytics.test.md) |
| Inbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Inbound | [deliveryMetricsService](../modules/deliveryMetricsService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DurationSamples](../entities/deliveryMetrics_DurationSamples.md) | Class | 1 | — | — |
| [DeliveryQueueItem](../entities/deliveryMetrics_DeliveryQueueItem.md) | Class | 10 | — | — |
| [DeliveryMetrics](../entities/DeliveryMetrics.md) | Class | 17 | — | — |
