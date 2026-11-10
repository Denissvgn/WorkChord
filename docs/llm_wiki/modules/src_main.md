# main Module

**Path:** `frontend/src/main.tsx`

## Description

_Auto-generated from `frontend/src/main.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./App` | `App` | — | compiler-dependent |
| `./components/feedback/ToastProvider` | `ToastProvider` | — | compiler-dependent |
| `./features/identity/IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `./i18n/SystemLanguageProvider` | `SystemLanguageProvider` | — | compiler-dependent |
| `./i18n/i18n` | — | — | present |
| `./styles/globals.css` | — | — | present |
| `./styles/planning-masters.css` | — | — | present |
| `@fontsource-variable/inter/index.css` | — | — | present |
| `@tanstack/react-query` | `QueryClient`, `QueryClientProvider` | — | compiler-dependent |
| `react` | `React` | — | compiler-dependent |
| `react-dom/client` | `ReactDOM` | — | compiler-dependent |
| `react-router-dom` | `createBrowserRouter`, `RouterProvider` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `queryClient`, `router` |
| Module calls | `queryClient = QueryClient`, `router = createBrowserRouter`, `render` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/feedback/ToastProvider.tsx"]
    n2["frontend/src/features/identity/IdentityProvider.tsx"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n5["frontend/src/main.tsx"]
    n4 --> n3
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/App.md"
    click n1 "../modules/ToastProvider.md"
    click n2 "../modules/IdentityProvider.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/SystemLanguageProvider.md"
    click n5 "../modules/src_main.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [App](../modules/App.md) |
| Outbound | [ToastProvider](../modules/ToastProvider.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [SystemLanguageProvider](../modules/SystemLanguageProvider.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |
