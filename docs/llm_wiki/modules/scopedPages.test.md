# scopedPages.test Module

**Path:** `frontend/src/features/scope/scopedPages.test.tsx`

## Description

_Auto-generated from `frontend/src/features/scope/scopedPages.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/feedback/ToastProvider` | `ToastProvider` | — | compiler-dependent |
| `../../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../pages/AnalyticsPage` | `AnalyticsPage` | — | compiler-dependent |
| `../../pages/GanttPage` | `GanttPage` | — | compiler-dependent |
| `../../pages/TasksPage` | `TasksPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient` | — | compiler-dependent |
| `../overview/overviewTaskThread` | `overviewTaskDrawerHref` | — | compiler-dependent |
| `./scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `./workScope` | `scopedLink` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `cleanup`, `render`, `screen`, `waitFor` | — | compiler-dependent |
| `@testing-library/user-event` | `userEvent` | — | compiler-dependent |
| `react` | `ReactNode` | Specifier | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `Outlet`, `RouterProvider`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `iterationServiceMock`, `ganttServiceMock`, `taskServiceMock`, `savedViewServiceMock`, `projectServiceMock`, `ITERATIONS`, `PROJECTS`, `PAGES`, `SCOPED_URLS` |
| Module calls | `iterationServiceMock = hoisted`, `ganttServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `projectServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/ToastProvider.tsx"]
    n1["frontend/src/components/layout/ScopeBar.tsx"]
    n2["frontend/src/features/overview/overviewTaskThread.ts"]
    n3["frontend/src/features/scope/scopedPages.test.tsx"]
    n4["frontend/src/features/scope/scopeStore.ts"]
    n5["frontend/src/features/scope/useWorkScope.ts"]
    n6["frontend/src/features/scope/workScope.ts"]
    n7["frontend/src/i18n/i18n.ts"]
    n8["frontend/src/pages/AnalyticsPage.tsx"]
    n9["frontend/src/pages/GanttPage.tsx"]
    n10["frontend/src/pages/TasksPage.tsx"]
    n11["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n5
    n1 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n6
    n5 --> n4
    n5 --> n6
    n8 --> n5
    n9 --> n5
    n10 --> n2
    n10 --> n5
    n10 --> n6
    n11 --> n0
    n11 --> n7
    click n0 "../modules/ToastProvider.md"
    click n1 "../modules/ScopeBar.md"
    click n2 "../modules/overviewTaskThread.md"
    click n3 "../modules/scopedPages.test.md"
    click n4 "../modules/scopeStore.md"
    click n5 "../modules/useWorkScope.md"
    click n6 "../modules/workScope.md"
    click n7 "../modules/i18n.md"
    click n8 "../modules/AnalyticsPage.md"
    click n9 "../modules/GanttPage.md"
    click n10 "../modules/TasksPage.md"
    click n11 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ToastProvider](../modules/ToastProvider.md) |
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [overviewTaskThread](../modules/overviewTaskThread.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [workScope](../modules/workScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |
