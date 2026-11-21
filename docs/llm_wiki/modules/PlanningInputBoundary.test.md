# PlanningInputBoundary.test Module

**Path:** `frontend/src/components/planning/PlanningInputBoundary.test.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanningInputBoundary.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./PlanningInputBoundary` | `PlanningInputBoundary` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `vitest` | `beforeEach`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `reader`, `initial` |
| Module calls | `reader = hoisted`, `mock`, `beforeEach`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/planning/PlanningInputBoundary.test.tsx"]
    n2["frontend/src/components/planning/PlanningInputBoundary.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    click n0 "../modules/Button.md"
    click n1 "../modules/PlanningInputBoundary.test.md"
    click n2 "../modules/PlanningInputBoundary.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
