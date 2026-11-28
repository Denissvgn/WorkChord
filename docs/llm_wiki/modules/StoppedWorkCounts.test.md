# StoppedWorkCounts.test Module

**Path:** `frontend/src/components/analytics/StoppedWorkCounts.test.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/StoppedWorkCounts.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `../tasks/WorkMetricsLine` | `WorkMetricsLine` | — | compiler-dependent |
| `./OnTrackSummary` | `OnTrackSummary` | — | compiler-dependent |
| `./StatusDistribution` | `StatusDistribution` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `mock`, `beforeEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/analytics/StoppedWorkCounts.test.tsx"]
    n3["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/types/iteration.ts"]
    n0 --> n7
    n1 --> n7
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n5
    n6 --> n4
    click n0 "../modules/OnTrackSummary.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/StoppedWorkCounts.test.md"
    click n3 "../modules/WorkMetricsLine.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Outbound | [StatusDistribution](../modules/StatusDistribution.md) |
| Outbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
