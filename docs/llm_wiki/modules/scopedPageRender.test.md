# scopedPageRender.test Module

**Path:** `frontend/src/test/scopedPageRender.test.tsx`

## Description

_Auto-generated from `frontend/src/test/scopedPageRender.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../features/scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../navigation/routeModules` | `routeModuleLoaders` | — | compiler-dependent |
| `./pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./workspaceApi` | `installWorkspaceApi` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `Outlet` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `SCOPED_PAGES`, `SCOPES` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/ScopeBar.tsx"]
    n1["frontend/src/features/scope/scopeStore.ts"]
    n2["frontend/src/features/scope/useWorkScope.ts"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/navigation/routeModules.ts"]
    n5["frontend/src/test/pageChrome.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/test/scopedPageRender.test.tsx"]
    n8["frontend/src/test/workspaceApi.ts"]
    n0 --> n2
    n2 --> n1
    n6 --> n3
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    click n0 "../modules/ScopeBar.md"
    click n1 "../modules/scopeStore.md"
    click n2 "../modules/useWorkScope.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/routeModules.md"
    click n5 "../modules/pageChrome.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/scopedPageRender.test.md"
    click n8 "../modules/workspaceApi.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [routeModules](../modules/routeModules.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [workspaceApi](../modules/workspaceApi.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
