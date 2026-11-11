# workNumbers Module

**Path:** `frontend/src/utils/workNumbers.ts`

## Description

/**
 * One way to write work numbers everywhere: counts, decimals, percent and effort
 * in days, in the reader's locale. A missing value returns null so the caller says
 * "unknown" in words instead of showing 0.
 */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `formatCount`, `formatDecimal`, `formatEffortDays`, `formatPercent` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/iteration/IterationCapacityLine.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n4["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n5["frontend/src/components/team/TeamList.tsx"]
    n6["frontend/src/pages/OverviewPage.tsx"]
    n7["frontend/src/pages/ProjectDetailPage.tsx"]
    n8["frontend/src/pages/ProjectsPage.tsx"]
    n9["frontend/src/utils/workNumbers.ts"]
    n0 --> n9
    n1 --> n9
    n2 --> n9
    n3 --> n9
    n4 --> n9
    n5 --> n9
    n6 --> n4
    n6 --> n9
    n7 --> n9
    n8 --> n9
    click n0 "../modules/OnTrackSummary.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/IterationCapacityLine.md"
    click n3 "../modules/KanbanCard.md"
    click n4 "../modules/WorkMetricsLine.md"
    click n5 "../modules/TeamList.md"
    click n6 "../modules/OverviewPage.md"
    click n7 "../modules/ProjectDetailPage.md"
    click n8 "../modules/ProjectsPage.md"
    click n9 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Inbound | [StatusDistribution](../modules/StatusDistribution.md) |
| Inbound | [IterationCapacityLine](../modules/IterationCapacityLine.md) |
| Inbound | [KanbanCard](../modules/KanbanCard.md) |
| Inbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Inbound | [TeamList](../modules/TeamList.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `formatCount` | `(value: number \| null \| undefined, locale: string)` | — | — |
| `formatDecimal` | `(value: number \| null \| undefined, locale: string, digits = 1)` | — | — |
| `formatPercent` | `(value: number \| null \| undefined, locale: string)` | — | `value` is 0–100, as the server reports completion. |
| `formatEffortDays` | `(value: number \| null \| undefined, locale: string)` | — | — |
