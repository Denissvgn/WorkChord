# main Module

**Path:** `frontend/src/main.tsx`

## Description

_Auto-generated from `frontend/src/main.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `./App` | `App` |
| `./components/feedback/ToastProvider` | `ToastProvider` |
| `./features/planningMasters/planningNavigationInvalidation` | `installPlanningNavigationInvalidation` |
| `./i18n/SystemLanguageProvider` | `SystemLanguageProvider` |
| `@tanstack/react-query` | `QueryClient`, `QueryClientProvider` |
| `react` | `React` |
| `react-dom/client` | `ReactDOM` |
| `react-router-dom` | `BrowserRouter` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `queryClient` |
| Module calls | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `render` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/feedback/ToastProvider.tsx"]
    n2["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n3["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n4["frontend/src/main.tsx"]
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/App.md"
    click n1 "../modules/ToastProvider.md"
    click n2 "../modules/planningNavigationInvalidation.md"
    click n3 "../modules/SystemLanguageProvider.md"
    click n4 "../modules/src_main.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [App](../modules/App.md) |
| Outbound | [ToastProvider](../modules/ToastProvider.md) |
| Outbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
| Outbound | [SystemLanguageProvider](../modules/SystemLanguageProvider.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
