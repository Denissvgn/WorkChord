# PlanIterations.test Module

**Path:** `frontend/src/pages/PlanIterations.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanIterations.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../navigation/LegacyRedirect` | `LegacyRedirect` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/iteration` | `IterationPlanningReadinessSummary`, `PlanCheckpoint` | Declaration | erased |
| `./PlanPage` | `PlanPage` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `ITERATIONS`, `PROJECTS` |
| Module calls | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/ScopeBar.tsx"]
    n1["frontend/src/features/scope/scopeStore.ts"]
    n2["frontend/src/navigation/LegacyRedirect.tsx"]
    n3["frontend/src/pages/PlanIterations.test.tsx"]
    n4["frontend/src/pages/PlanPage.tsx"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/iteration.ts"]
    n0 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n6
    click n0 "../modules/ScopeBar.md"
    click n1 "../modules/scopeStore.md"
    click n2 "../modules/LegacyRedirect.md"
    click n3 "../modules/PlanIterations.test.md"
    click n4 "../modules/PlanPage.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [LegacyRedirect](../modules/LegacyRedirect.md) |
| Outbound | [PlanPage](../modules/PlanPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
