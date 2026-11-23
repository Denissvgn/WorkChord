# backlogScope.test Module

**Path:** `frontend/src/features/scope/backlogScope.test.tsx`

## Description

_Auto-generated from `frontend/src/features/scope/backlogScope.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/feedback/ToastProvider` | `ToastProvider` | — | compiler-dependent |
| `../../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../pages/TasksPage` | `TasksPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient` | — | compiler-dependent |
| `./scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `render`, `screen`, `waitFor` | — | compiler-dependent |
| `@testing-library/user-event` | `userEvent` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `Outlet`, `RouterProvider`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `iterationServiceMock`, `projectServiceMock`, `taskServiceMock`, `savedViewServiceMock`, `ITERATIONS`, `PROJECTS` |
| Module calls | `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/ToastProvider.tsx"]
    n1["frontend/src/components/layout/ScopeBar.tsx"]
    n2["frontend/src/features/scope/backlogScope.test.tsx"]
    n3["frontend/src/features/scope/scopeStore.ts"]
    n4["frontend/src/features/scope/useWorkScope.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n4
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n4 --> n3
    n6 --> n4
    n7 --> n0
    n7 --> n5
    click n0 "../modules/ToastProvider.md"
    click n1 "../modules/ScopeBar.md"
    click n2 "../modules/backlogScope.test.md"
    click n3 "../modules/scopeStore.md"
    click n4 "../modules/useWorkScope.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ToastProvider](../modules/ToastProvider.md) |
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |
