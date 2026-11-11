# IterationOutlook.test Module

**Path:** `frontend/src/components/analytics/IterationOutlook.test.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/IterationOutlook.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `../../types/task` | `TaskStatusLog` | Declaration | erased |
| `./OnTrackSummary` | `OnTrackSummary` | — | compiler-dependent |
| `./StatusDistribution` | `StatusDistribution` | — | compiler-dependent |
| `./TaskStatusFlow` | `TaskStatusFlow` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n1["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n2["frontend/src/components/analytics/StatusDistribution.tsx"]
    n3["frontend/src/components/analytics/TaskStatusFlow.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/iteration.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n2 --> n5
    n2 --> n6
    n3 --> n6
    click n0 "../modules/IterationOutlook.test.md"
    click n1 "../modules/OnTrackSummary.md"
    click n2 "../modules/StatusDistribution.md"
    click n3 "../modules/TaskStatusFlow.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_iteration.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Outbound | [StatusDistribution](../modules/StatusDistribution.md) |
| Outbound | [TaskStatusFlow](../modules/TaskStatusFlow.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
