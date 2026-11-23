# useAnalyticsScope Module

**Path:** `frontend/src/components/analytics/useAnalyticsScope.ts`

## Description

_Auto-generated from `frontend/src/components/analytics/useAnalyticsScope.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `../../types/analyticsScope` | `AnalyticsScope` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useAnalyticsScope` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n1["frontend/src/components/analytics/useAnalyticsScope.ts"]
    n2["frontend/src/features/scope/useWorkScope.ts"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/types/analyticsScope.ts"]
    n0 --> n1
    n1 --> n2
    n1 --> n4
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/DeliveryAnalytics.md"
    click n1 "../modules/useAnalyticsScope.md"
    click n2 "../modules/useWorkScope.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/analyticsScope.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [analyticsScope](../modules/analyticsScope.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAnalyticsScope` | `(days: number) -> AnalyticsScope \| undefined` | — | — |
