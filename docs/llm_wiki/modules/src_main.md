# main Module

**Path:** `frontend/src/main.tsx`

## Description

_Auto-generated from `frontend/src/main.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `./App` | `App` |
| `./components/feedback/ToastProvider` | `ToastProvider` |
| `./features/identity/IdentityProvider` | `IdentityProvider` |
| `./features/planningMasters/planningNavigationInvalidation` | `installPlanningNavigationInvalidation` |
| `./features/workQueryFreshness` | `installWorkFreshness` |
| `./i18n/SystemLanguageProvider` | `SystemLanguageProvider` |
| `@tanstack/react-query` | `QueryClient`, `QueryClientProvider` |
| `react` | `React` |
| `react-dom/client` | `ReactDOM` |
| `react-router-dom` | `createBrowserRouter`, `RouterProvider` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `queryClient`, `router` |
| Module calls | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `installWorkFreshness`, `router = createBrowserRouter`, `render` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/feedback/ToastProvider.tsx"]
    n2["frontend/src/features/identity/IdentityProvider.tsx"]
    n3["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n4["frontend/src/features/workQueryFreshness.ts"]
    n5["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n6["frontend/src/main.tsx"]
    n2 --> n4
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/App.md"
    click n1 "../modules/ToastProvider.md"
    click n2 "../modules/IdentityProvider.md"
    click n3 "../modules/planningNavigationInvalidation.md"
    click n4 "../modules/workQueryFreshness.md"
    click n5 "../modules/SystemLanguageProvider.md"
    click n6 "../modules/src_main.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [App](../modules/App.md) |
| Outbound | [ToastProvider](../modules/ToastProvider.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |
| Outbound | [SystemLanguageProvider](../modules/SystemLanguageProvider.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
