# masters.test Module

**Path:** `frontend/src/features/planningMasters/masters.test.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/masters.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./masters` | `PlanReadiness` | Declaration | erased |
| `./masters` | `derivePlanningRecovery`, `deriveStatus`, `EMPTY_READINESS`, `nextStep` | — | compiler-dependent |
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
    n0["frontend/src/features/planningMasters/masters.test.ts"]
    n1["frontend/src/features/planningMasters/masters.ts"]
    n0 --> n1
    click n0 "../modules/planningMasters_masters.test.md"
    click n1 "../modules/planningMasters_masters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
