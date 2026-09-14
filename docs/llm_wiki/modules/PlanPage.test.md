# PlanPage.test Module

**Path:** `frontend/src/pages/PlanPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../features/planningMasters/masters` | `deriveStatus`, `EMPTY_READINESS`, `nextStep`, `readiness` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `./PlanPage` | `PlanPage` |
| `./PlanPage.tsx?raw` | `planPageSource` |
| `@testing-library/react` | `screen`, `within` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `planningReadinessMock` |
| Module calls | `planningReadinessMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/masters.ts"]
    n1["frontend/src/pages/PlanPage.test.tsx"]
    n2["frontend/src/pages/PlanPage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    click n0 "../modules/planningMasters_masters.md"
    click n1 "../modules/PlanPage.test.md"
    click n2 "../modules/PlanPage.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Outbound | [PlanPage](../modules/PlanPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
