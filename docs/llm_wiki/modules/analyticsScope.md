# analyticsScope Module

**Path:** `frontend/src/types/analyticsScope.ts`

## Description

_Auto-generated from `frontend/src/types/analyticsScope.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AnalyticsScope` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n1["frontend/src/components/analytics/useAnalyticsScope.ts"]
    n2["frontend/src/services/deliveryMetricsService.ts"]
    n3["frontend/src/services/executionUsageService.ts"]
    n4["frontend/src/types/analyticsScope.ts"]
    n0 --> n3
    n0 --> n4
    n1 --> n4
    n2 --> n4
    n3 --> n4
    click n0 "../modules/ExecutionUsagePanel.md"
    click n1 "../modules/useAnalyticsScope.md"
    click n2 "../modules/deliveryMetricsService.md"
    click n3 "../modules/executionUsageService.md"
    click n4 "../modules/analyticsScope.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ExecutionUsagePanel](../modules/ExecutionUsagePanel.md) |
| Inbound | [useAnalyticsScope](../modules/useAnalyticsScope.md) |
| Inbound | [deliveryMetricsService](../modules/deliveryMetricsService.md) |
| Inbound | [executionUsageService](../modules/executionUsageService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AnalyticsScope](../entities/AnalyticsScope.md) | Interface | 1 | — | — |
