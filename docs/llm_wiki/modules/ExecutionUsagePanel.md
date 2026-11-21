# ExecutionUsagePanel Module

**Path:** `frontend/src/components/analytics/ExecutionUsagePanel.tsx`

## Description

Human Analytics preserves exact decimal strings for costs and separates currency buckets, estimates, unknown human effort and simulations. Advisory comparison requires an explicit currency and keeps local inputs editable after read failures; no agent credential or default spending currency is introduced.

_Auto-generated from `frontend/src/components/analytics/ExecutionUsagePanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/executionUsageService` | `executionUsageService` | — | compiler-dependent |
| `../../types/analyticsScope` | `AnalyticsScope` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ExecutionUsagePanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/ExecutionUsagePanel.test.tsx"]
    n1["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n2["frontend/src/components/common/Button.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/pages/AnalyticsPage.tsx"]
    n5["frontend/src/services/executionUsageService.ts"]
    n6["frontend/src/types/analyticsScope.ts"]
    n7["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n3 --> n2
    n4 --> n1
    n4 --> n3
    n5 --> n6
    click n0 "../modules/ExecutionUsagePanel.test.md"
    click n1 "../modules/ExecutionUsagePanel.md"
    click n2 "../modules/Button.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/AnalyticsPage.md"
    click n5 "../modules/executionUsageService.md"
    click n6 "../modules/analyticsScope.md"
    click n7 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ExecutionUsagePanel.test](../modules/ExecutionUsagePanel.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [executionUsageService](../modules/executionUsageService.md) |
| Outbound | [analyticsScope](../modules/analyticsScope.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ExecutionUsagePanel` | `({ scope }: { scope: AnalyticsScope })` | — | — |
