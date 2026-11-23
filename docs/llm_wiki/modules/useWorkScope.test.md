# useWorkScope.test Module

**Path:** `frontend/src/features/scope/useWorkScope.test.tsx`

## Description

_Auto-generated from `frontend/src/features/scope/useWorkScope.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient` | — | compiler-dependent |
| `./scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./useWorkScope` | `WorkScopeValue` | Specifier | compiler-dependent |
| `./useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `render`, `screen`, `waitFor` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `RouterProvider`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `iterationServiceMock`, `ITERATIONS` |
| Module calls | `iterationServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/scope/scopeStore.ts"]
    n1["frontend/src/features/scope/useWorkScope.test.tsx"]
    n2["frontend/src/features/scope/useWorkScope.ts"]
    n3["frontend/src/store/iterationStore.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n3 --> n0
    click n0 "../modules/scopeStore.md"
    click n1 "../modules/useWorkScope.test.md"
    click n2 "../modules/useWorkScope.md"
    click n3 "../modules/iterationStore.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |
