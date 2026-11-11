# StatusDistribution Module

**Path:** `frontend/src/components/analytics/StatusDistribution.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/StatusDistribution.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `../../types/task` | `TaskStatus` | Declaration | erased |
| `../../utils/workNumbers` | `formatCount`, `formatPercent` | — | compiler-dependent |
| `../tasks/MetricCount` | `MetricCount` | — | compiler-dependent |
| `../ui/tone` | `STATUS_TONE`, `toneSoftVar`, `toneVar` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `StatusDistribution` |
| Constants | `ORDER` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/tasks/MetricCount.tsx"]
    n3["frontend/src/components/ui/tone.ts"]
    n4["frontend/src/pages/AnalyticsPage.tsx"]
    n5["frontend/src/types/iteration.ts"]
    n6["frontend/src/types/task.ts"]
    n7["frontend/src/utils/workNumbers.ts"]
    n0 --> n1
    n0 --> n5
    n0 --> n6
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n3 --> n6
    n4 --> n1
    n4 --> n6
    click n0 "../modules/IterationOutlook.test.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/MetricCount.md"
    click n3 "../modules/tone.md"
    click n4 "../modules/AnalyticsPage.md"
    click n5 "../modules/types_iteration.md"
    click n6 "../modules/types_task.md"
    click n7 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationOutlook.test](../modules/IterationOutlook.test.md) |
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
