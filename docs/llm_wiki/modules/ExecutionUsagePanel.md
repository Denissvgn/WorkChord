# ExecutionUsagePanel Module

**Path:** `frontend/src/components/analytics/ExecutionUsagePanel.tsx`

## Description

Human Analytics preserves exact decimal strings for costs and separates currency buckets, estimates, unknown human effort and simulations. Advisory comparison requires an explicit currency and keeps local inputs editable after read failures; no agent credential or default spending currency is introduced.

_Auto-generated from `frontend/src/components/analytics/ExecutionUsagePanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/executionUsageService` | `executionUsageService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ExecutionUsagePanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n1["frontend/src/components/analytics/ExecutionUsagePanel.test.tsx"]
    n2["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n3["frontend/src/components/common/Button.tsx"]
    n4["frontend/src/components/feedback/QueryState.tsx"]
    n5["frontend/src/services/executionUsageService.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n2
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n4 --> n3
    click n0 "../modules/DeliveryAnalytics.md"
    click n1 "../modules/ExecutionUsagePanel.test.md"
    click n2 "../modules/ExecutionUsagePanel.md"
    click n3 "../modules/Button.md"
    click n4 "../modules/QueryState.md"
    click n5 "../modules/executionUsageService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Inbound | [ExecutionUsagePanel.test](../modules/ExecutionUsagePanel.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [executionUsageService](../modules/executionUsageService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ExecutionUsagePanel` | `({ scope }: { scope: { project_id?: number; iteration_id?: number; lookback_days: number } })` | — | — |
