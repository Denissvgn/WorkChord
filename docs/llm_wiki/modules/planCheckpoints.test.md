# planCheckpoints.test Module

**Path:** `frontend/src/features/planningMasters/planCheckpoints.test.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planCheckpoints.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `IterationPlanningReadinessSummary` | Declaration | erased |
| `./planCheckpoints` | `planCheckpointSections` | — | compiler-dependent |
| `./planningReturn` | `PLANNING_STEP_IDS` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/planCheckpoints.test.ts"]
    n1["frontend/src/features/planningMasters/planCheckpoints.ts"]
    n2["frontend/src/features/planningMasters/planningReturn.ts"]
    n3["frontend/src/types/iteration.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    click n0 "../modules/planCheckpoints.test.md"
    click n1 "../modules/planCheckpoints.md"
    click n2 "../modules/planningReturn.md"
    click n3 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planCheckpoints](../modules/planCheckpoints.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
