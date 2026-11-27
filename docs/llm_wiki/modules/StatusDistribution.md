# StatusDistribution Module

**Path:** `frontend/src/components/analytics/StatusDistribution.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/StatusDistribution.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `../../types/task` | `TaskDisplayedState` | Declaration | erased |
| `../../utils/workNumbers` | `formatCount`, `formatPercent` | — | compiler-dependent |
| `../tasks/MetricCount` | `MetricCount` | — | compiler-dependent |
| `../ui/tone` | `STATE_TONE`, `toneSoftVar`, `toneVar` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `StatusDistribution` |
| Constants | `ORDER`, `ENDED` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/analytics/StoppedWorkCounts.test.tsx"]
    n3["frontend/src/components/tasks/MetricCount.tsx"]
    n4["frontend/src/components/ui/tone.ts"]
    n5["frontend/src/pages/AnalyticsPage.tsx"]
    n6["frontend/src/types/iteration.ts"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/workNumbers.ts"]
    n0 --> n1
    n0 --> n6
    n1 --> n3
    n1 --> n4
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n2 --> n1
    n2 --> n6
    n4 --> n7
    n5 --> n1
    n6 --> n7
    click n0 "../modules/IterationOutlook.test.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/StoppedWorkCounts.test.md"
    click n3 "../modules/MetricCount.md"
    click n4 "../modules/tone.md"
    click n5 "../modules/AnalyticsPage.md"
    click n6 "../modules/types_iteration.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationOutlook.test](../modules/IterationOutlook.test.md) |
| Inbound | [StoppedWorkCounts.test](../modules/StoppedWorkCounts.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [MetricCount](../modules/MetricCount.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [workNumbers](../modules/workNumbers.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `StatusDistribution` | `({ summary }: { summary: IterationSummary })` | — | How the iteration's tasks split by status, in the canonical status colours, with a table view. |
