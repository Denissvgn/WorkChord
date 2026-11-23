# planningScope.test Module

**Path:** `frontend/src/features/scope/planningScope.test.tsx`

## Description

_Auto-generated from `frontend/src/features/scope/planningScope.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `createTestQueryClient` | — | compiler-dependent |
| `../planningMasters/usePlanningReadiness` | `usePlanningReadiness` | — | compiler-dependent |
| `./scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `render`, `screen`, `waitFor` | — | compiler-dependent |
| `@testing-library/user-event` | `userEvent` | — | compiler-dependent |
| `react` | `ReactNode` | Specifier | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `Outlet`, `RouterProvider`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `serviceMocks`, `ITERATIONS` |
| Module calls | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n1["frontend/src/features/scope/planningScope.test.tsx"]
    n2["frontend/src/features/scope/scopeStore.ts"]
    n3["frontend/src/features/scope/useWorkScope.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n3
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n3 --> n2
    click n0 "../modules/usePlanningReadiness.md"
    click n1 "../modules/planningScope.test.md"
    click n2 "../modules/scopeStore.md"
    click n3 "../modules/useWorkScope.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |
