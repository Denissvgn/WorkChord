# AppSidebar.planProgress.test Module

**Path:** `frontend/src/components/layout/AppSidebar.planProgress.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppSidebar.planProgress.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./AppSidebar` | `AppSidebar` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `iteration`, `readinessResponse` |
| Module calls | `services = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.planProgress.test.tsx"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["frontend/src/store/iterationStore.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    click n0 "../modules/AppSidebar.planProgress.test.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/iterationStore.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AppSidebar](../modules/AppSidebar.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
