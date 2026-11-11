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
    n0["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n1["frontend/src/pages/OverviewPage.tsx"]
    n2["frontend/src/pages/ProjectDetailPage.tsx"]
    n3["frontend/src/pages/ProjectsPage.tsx"]
    n4["frontend/src/utils/workNumbers.ts"]
    n0 --> n4
    n1 --> n0
    n1 --> n4
    n2 --> n4
    n3 --> n4
    click n0 "../modules/WorkMetricsLine.md"
    click n1 "../modules/OverviewPage.md"
    click n2 "../modules/ProjectDetailPage.md"
    click n3 "../modules/ProjectsPage.md"
    click n4 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
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
