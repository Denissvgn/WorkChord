# MetricCount Module

**Path:** `frontend/src/components/tasks/MetricCount.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/MetricCount.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../../services/taskService` | `MetricScope`, `WorkMetricName` | Declaration | erased |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `MetricCount` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/common/Button.tsx"]
    n3["frontend/src/components/common/Modal.tsx"]
    n4["frontend/src/components/feedback/QueryState.tsx"]
    n5["frontend/src/components/projects/ProjectSummaryTab.tsx"]
    n6["frontend/src/components/tasks/MetricCount.test.tsx"]
    n7["frontend/src/components/tasks/MetricCount.tsx"]
    n8["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n9["frontend/src/features/scope/useScopeLink.ts"]
    n10["frontend/src/services/taskService.ts"]
    n0 --> n7
    n0 --> n9
    n1 --> n7
    n4 --> n2
    n5 --> n2
    n5 --> n7
    n6 --> n7
    n6 --> n8
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n9
    n7 --> n10
    n8 --> n7
    n8 --> n10
    click n0 "../modules/OnTrackSummary.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/Button.md"
    click n3 "../modules/Modal.md"
    click n4 "../modules/QueryState.md"
    click n5 "../modules/ProjectSummaryTab.md"
    click n6 "../modules/MetricCount.test.md"
    click n7 "../modules/MetricCount.md"
    click n8 "../modules/WorkMetricsLine.md"
    click n9 "../modules/useScopeLink.md"
    click n10 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Inbound | [StatusDistribution](../modules/StatusDistribution.md) |
| Inbound | [ProjectSummaryTab](../modules/ProjectSummaryTab.md) |
| Inbound | [MetricCount.test](../modules/MetricCount.test.md) |
| Inbound | [WorkMetricsLine](../modules/WorkMetricsLine.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [taskService](../modules/taskService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `MetricCount` | <pre><code>&#40;&#123; metric&#44; scope&#44; title&#44; children&#44; className&#44; total &#125;&#58; &#123;&#10;    metric&#58; WorkMetricName&#59; scope&#58; MetricScope &#124; null&#59; title&#58; string&#59; children&#58; ReactNode&#59; className&#63;&#58; string&#59; total&#63;&#58; number&#59;&#10;&#125;&#41;</code></pre> | — | A count that opens the tasks it counts. The server picks them with the same |
