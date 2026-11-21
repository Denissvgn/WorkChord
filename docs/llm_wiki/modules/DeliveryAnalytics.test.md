# DeliveryAnalytics.test Module

**Path:** `frontend/src/components/analytics/DeliveryAnalytics.test.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/DeliveryAnalytics.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../types/deliveryMetrics` | `DeliveryMetrics` | Declaration | erased |
| `../layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `./DeliveryAnalytics` | `DeliveryAnalytics` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `metrics`, `iterationsMock`, `projects`, `report`, `unavailable` |
| Module calls | `metrics = hoisted`, `iterationsMock = hoisted`, `projects = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.test.tsx"]
    n1["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n2["frontend/src/components/layout/ScopeBar.tsx"]
    n3["frontend/src/features/scope/scopeStore.ts"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n6
    n5 --> n4
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/ScopeBar.md"
    click n3 "../modules/scopeStore.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [deliveryMetrics](../modules/deliveryMetrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
