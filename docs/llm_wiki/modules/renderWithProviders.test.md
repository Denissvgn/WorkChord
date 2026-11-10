# renderWithProviders.test Module

**Path:** `frontend/src/test/renderWithProviders.test.tsx`

## Description

_Auto-generated from `frontend/src/test/renderWithProviders.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/feedback/toast` | `useToast` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `@tanstack/react-query` | `useQueryClient` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/toast.ts"]
    n1["frontend/src/test/renderWithProviders.test.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    click n0 "../modules/toast.md"
    click n1 "../modules/renderWithProviders.test.md"
    click n2 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [toast](../modules/toast.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |
