# OverviewPage.test Module

**Path:** `frontend/src/pages/OverviewPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/OverviewPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../features/planningMasters/usePlanningReadiness` | `PlanningTeamMember` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `../types/iteration` | `Iteration`, `IterationSummary` |
| `../types/task` | `Task`, `TaskStatus` |
| `../utils/selectWorkNowTasks` | `selectWorkNowTasks` |
| `./OverviewPage` | `OverviewPage` |
| `@testing-library/react` | `screen`, `waitFor`, `within` |
| `@testing-library/user-event` | `UserEvent` |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `planningReadinessMock`, `serviceMocks`, `iteration`, `iterationSummary` |
| Module calls | `planningReadinessMock = hoisted`, `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n1["frontend/src/pages/OverviewPage.test.tsx"]
    n2["frontend/src/pages/OverviewPage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/iteration.ts"]
    n5["frontend/src/types/task.ts"]
    n6["frontend/src/utils/selectWorkNowTasks.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n6 --> n5
    click n0 "../modules/usePlanningReadiness.md"
    click n1 "../modules/OverviewPage.test.md"
    click n2 "../modules/OverviewPage.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_iteration.md"
    click n5 "../modules/types_task.md"
    click n6 "../modules/selectWorkNowTasks.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [selectWorkNowTasks](../modules/selectWorkNowTasks.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
