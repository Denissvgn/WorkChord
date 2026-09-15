# WorkMetricsLine Module

**Path:** `frontend/src/components/tasks/WorkMetricsLine.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/WorkMetricsLine.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/workMetrics` | `WorkMetrics` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkMetricsLine` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n1["frontend/src/pages/AnalyticsPage.tsx"]
    n2["frontend/src/pages/OverviewPage.tsx"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n5["frontend/src/types/workMetrics.ts"]
    n0 --> n5
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/WorkMetricsLine.md"
    click n1 "../modules/AnalyticsPage.md"
    click n2 "../modules/OverviewPage.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectReleaseDetailPage.md"
    click n5 "../modules/workMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Outbound | [workMetrics](../modules/workMetrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `WorkMetricsLine` | `({ metrics }: { metrics?: WorkMetrics \| null })` | — | — |
