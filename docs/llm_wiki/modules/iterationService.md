# iterationService Module

**Path:** `frontend/src/services/iterationService.ts`

## Description

_Auto-generated from `frontend/src/services/iterationService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/iteration` | `Iteration`, `IterationCreate`, `IterationPlanningReadinessSummary`, `IterationSeriesCreate`, `IterationSeriesResponse`, `IterationSummary`, `IterationUpdate` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |
| `./planningInputService` | `ObservedRevisions` | Specifier | compiler-dependent |
| `./planningInputService` | `revisionHeaders` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `iterationService` |
| Constants | `iterationService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/services/iterationService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/iterationService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (18) |
| Outbound | `frontend` (3) |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
