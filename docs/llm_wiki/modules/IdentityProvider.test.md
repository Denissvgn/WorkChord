# IdentityProvider.test Module

**Path:** `frontend/src/features/identity/IdentityProvider.test.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/IdentityProvider.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../planningMasters/usePlanningNavigationSummary` | `planningNavigationSummaryKey` | — | compiler-dependent |
| `../scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./AccountMenu` | `IdentityBadge` | — | compiler-dependent |
| `./IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClient` | Declaration | erased |
| `@tanstack/react-query` | `useQueryClient` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `act` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/AccountMenu.tsx"]
    n1["frontend/src/features/identity/IdentityProvider.test.tsx"]
    n2["frontend/src/features/identity/IdentityProvider.tsx"]
    n3["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n4["frontend/src/features/scope/scopeStore.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n4
    click n0 "../modules/AccountMenu.md"
    click n1 "../modules/IdentityProvider.test.md"
    click n2 "../modules/IdentityProvider.md"
    click n3 "../modules/usePlanningNavigationSummary.md"
    click n4 "../modules/scopeStore.md"
    click n5 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AccountMenu](../modules/AccountMenu.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
