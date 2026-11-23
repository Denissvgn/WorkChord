# ExecutionUsagePanel.test Module

**Path:** `frontend/src/components/analytics/ExecutionUsagePanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/ExecutionUsagePanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../../pages/AnalyticsPage` | `AnalyticsPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/executionUsage` | `ExecutionUsageSummary` | Declaration | erased |
| `./ExecutionUsagePanel` | `ExecutionUsagePanel` | — | compiler-dependent |
| `@testing-library/react` | `fireEvent`, `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `delivery`, `service`, `report` |
| Module calls | `delivery = hoisted`, `mock`, `mock`, `service = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/ExecutionUsagePanel.test.tsx"]
    n1["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n2["frontend/src/features/scope/scopeStore.ts"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/executionUsage.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n3 --> n1
    click n0 "../modules/ExecutionUsagePanel.test.md"
    click n1 "../modules/ExecutionUsagePanel.md"
    click n2 "../modules/scopeStore.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/executionUsage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ExecutionUsagePanel](../modules/ExecutionUsagePanel.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [executionUsage](../modules/executionUsage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
