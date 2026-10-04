# DeliveryAnalytics.test Module

**Path:** `frontend/src/components/analytics/DeliveryAnalytics.test.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/DeliveryAnalytics.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` |
| `../../types/deliveryMetrics` | `DeliveryMetrics` |
| `./DeliveryAnalytics` | `DeliveryAnalytics` |
| `@testing-library/react` | `fireEvent`, `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `metrics`, `projects`, `report` |
| Module calls | `metrics = hoisted`, `projects = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/DeliveryAnalytics.test.tsx"]
    n1["frontend/src/components/analytics/DeliveryAnalytics.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/deliveryMetrics.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/DeliveryAnalytics.test.md"
    click n1 "../modules/DeliveryAnalytics.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/deliveryMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [DeliveryAnalytics](../modules/DeliveryAnalytics.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [deliveryMetrics](../modules/deliveryMetrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
