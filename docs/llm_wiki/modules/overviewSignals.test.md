# overviewSignals.test Module

**Path:** `frontend/src/features/overview/overviewSignals.test.ts`

## Description

_Auto-generated from `frontend/src/features/overview/overviewSignals.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/task` | `Task`, `TaskReference` | Declaration | erased |
| `../savedViews/taskViewParams` | `filtersFromSearchParams` | — | compiler-dependent |
| `./overviewSignals` | `backlogRoots`, `calendarDaysLeft`, `daysLeftToLatestEnd`, `iterationsInView`, `listTasks`, `overviewCountListHref`, `parseOverviewCountList`, `pickAttention`, `pipelineTasksInScope`, `selectWorkNow`, `taskListHref` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/overview/overviewSignals.test.ts"]
    n1["frontend/src/features/overview/overviewSignals.ts"]
    n2["frontend/src/features/savedViews/taskViewParams.ts"]
    n3["frontend/src/types/iteration.ts"]
    n4["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n3 --> n4
    click n0 "../modules/overviewSignals.test.md"
    click n1 "../modules/overviewSignals.md"
    click n2 "../modules/taskViewParams.md"
    click n3 "../modules/types_iteration.md"
    click n4 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [overviewSignals](../modules/overviewSignals.md) |
| Outbound | [taskViewParams](../modules/taskViewParams.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
