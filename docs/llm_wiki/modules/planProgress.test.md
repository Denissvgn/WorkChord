# planProgress.test Module

**Path:** `frontend/src/features/planningMasters/planProgress.test.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planProgress.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `Iteration`, `IterationPlanningReadinessSummary` | Declaration | erased |
| `./planningReturn` | `PLANNING_STEP_IDS` | — | compiler-dependent |
| `./usePlanningNavigationSummary` | `planProgress` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `iteration` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/planningReturn.ts"]
    n1["frontend/src/features/planningMasters/planProgress.test.ts"]
    n2["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n3["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/planningReturn.md"
    click n1 "../modules/planProgress.test.md"
    click n2 "../modules/usePlanningNavigationSummary.md"
    click n3 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
