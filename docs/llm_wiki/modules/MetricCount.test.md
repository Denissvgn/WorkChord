# MetricCount.test Module

**Path:** `frontend/src/components/tasks/MetricCount.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/MetricCount.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/workMetrics` | `WorkMetrics` | Declaration | erased |
| `./MetricCount` | `MetricCount` | — | compiler-dependent |
| `./WorkMetricsLine` | `WorkMetricsLine` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/MetricCount.test.tsx"]
    n1["frontend/src/components/tasks/MetricCount.tsx"]
    n2["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/workMetrics.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n2 --> n1
    n2 --> n4
    click n0 "../modules/MetricCount.test.md"
    click n1 "../modules/MetricCount.md"
    click n2 "../modules/WorkMetricsLine.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/workMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [MetricCount](../modules/MetricCount.md) |
| Outbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [workMetrics](../modules/workMetrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
