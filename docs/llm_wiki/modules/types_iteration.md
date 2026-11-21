# iteration Module

**Path:** `frontend/src/types/iteration.ts`

## Description

_Auto-generated from `frontend/src/types/iteration.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./workMetrics` | `WorkMetrics` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Iteration`, `IterationCreate`, `IterationPlanningReadinessSummary`, `IterationProject`, `IterationSeriesCreate`, `IterationSeriesResponse`, `IterationSeriesStop`, `IterationSummary`, `IterationUpdate`, `PlanCheckpoint` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/iteration.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/types_iteration.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (50) |
| Outbound | `frontend` (1) |

> All 51 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationProject](../entities/IterationProject.md) | Interface | 2 | — | — |
| [Iteration](../entities/types_iteration_Iteration.md) | Interface | 9 | — | — |
| [IterationCreate](../entities/types_iteration_IterationCreate.md) | Interface | 25 | — | — |
| [IterationUpdate](../entities/types_iteration_IterationUpdate.md) | Interface | 35 | — | — |
| [IterationSeriesCreate](../entities/types_iteration_IterationSeriesCreate.md) | Interface | 49 | — | — |
| [IterationSeriesResponse](../entities/types_iteration_IterationSeriesResponse.md) | Interface | 60 | — | — |
| [IterationSummary](../entities/types_iteration_IterationSummary.md) | Interface | 64 | `WorkMetrics` | — |
| [IterationPlanningReadinessSummary](../entities/types_iteration_IterationPlanningReadinessSummary.md) | Interface | 88 | — | — |
| [PlanCheckpoint](../entities/types_iteration_PlanCheckpoint.md) | Interface | 112 | — | — |
| [IterationSeriesStop](../entities/types_iteration_IterationSeriesStop.md) | Type alias | 45 | <pre><code>&#124; &#123; mode&#58; &#39;count&#39;&#59; count&#58; number &#125;&#10;    &#124; &#123; mode&#58; &#39;until&#95;date&#39;&#59; until&#95;date&#58; string &#125;</code></pre> | — |
