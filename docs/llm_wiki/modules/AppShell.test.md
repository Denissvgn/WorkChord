# AppShell.test Module

**Path:** `frontend/src/components/layout/AppShell.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppShell.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./AppShell` | `AppShell` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useLayoutEffect`, `useRef` | — | compiler-dependent |
| `react-router-dom` | `useLocation`, `useNavigate` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/layout/AppShell.test.tsx"]
    n2["frontend/src/components/layout/AppShell.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    click n0 "../modules/Button.md"
    click n1 "../modules/AppShell.test.md"
    click n2 "../modules/AppShell.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [AppShell](../modules/AppShell.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
