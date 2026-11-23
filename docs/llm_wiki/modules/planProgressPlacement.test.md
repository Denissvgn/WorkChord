# planProgressPlacement.test Module

**Path:** `frontend/src/components/layout/planProgressPlacement.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/planProgressPlacement.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/planningReturn` | `PLANNING_STEP_IDS` | — | compiler-dependent |
| `../../pages/OverviewPage` | `OverviewPage` | — | compiler-dependent |
| `../../pages/PlanPage` | `PlanPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `Iteration`, `IterationSummary` | Declaration | erased |
| `./AppSidebar` | `AppSidebar` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `mocks`, `iteration`, `iterationSummary`, `PROGRESS_TEXT` |
| Module calls | `mocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.tsx"]
    n1["frontend/src/components/layout/planProgressPlacement.test.tsx"]
    n2["frontend/src/features/planningMasters/planningReturn.ts"]
    n3["frontend/src/pages/OverviewPage.tsx"]
    n4["frontend/src/pages/PlanPage.tsx"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n4 --> n6
    click n0 "../modules/AppSidebar.md"
    click n1 "../modules/planProgressPlacement.test.md"
    click n2 "../modules/planningReturn.md"
    click n3 "../modules/OverviewPage.md"
    click n4 "../modules/PlanPage.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AppSidebar](../modules/AppSidebar.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [PlanPage](../modules/PlanPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
