# workMetrics Module

**Path:** `frontend/src/types/workMetrics.ts`

## Description

_Auto-generated from `frontend/src/types/workMetrics.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkMetrics` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/MetricCount.test.tsx"]
    n1["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n2["frontend/src/types/iteration.ts"]
    n3["frontend/src/types/project.ts"]
    n4["frontend/src/types/release.ts"]
    n5["frontend/src/types/workMetrics.ts"]
    n0 --> n1
    n0 --> n5
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    click n0 "../modules/MetricCount.test.md"
    click n1 "../modules/WorkMetricsLine.md"
    click n2 "../modules/types_iteration.md"
    click n3 "../modules/types_project.md"
    click n4 "../modules/types_release.md"
    click n5 "../modules/workMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MetricCount.test](../modules/MetricCount.test.md) |
| Inbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Inbound | [types_iteration](../modules/types_iteration.md) |
| Inbound | [types_project](../modules/types_project.md) |
| Inbound | [types_release](../modules/types_release.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkMetrics](../entities/WorkMetrics.md) | Interface | 1 | — | — |
