# OnTrackSummary Module

**Path:** `frontend/src/components/analytics/OnTrackSummary.tsx`

## Description

_Auto-generated from `frontend/src/components/analytics/OnTrackSummary.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/planningReturn` | `planStepHref` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../../utils/workNumbers` | `formatEffortDays` | — | compiler-dependent |
| `../tasks/MetricCount` | `MetricCount` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OnTrackSummary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n1["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n2["frontend/src/components/tasks/MetricCount.tsx"]
    n3["frontend/src/features/planningMasters/planningReturn.ts"]
    n4["frontend/src/features/scope/planningLinks.test.tsx"]
    n5["frontend/src/features/scope/useScopeLink.ts"]
    n6["frontend/src/pages/AnalyticsPage.tsx"]
    n7["frontend/src/types/iteration.ts"]
    n8["frontend/src/utils/formatDate.ts"]
    n9["frontend/src/utils/workNumbers.ts"]
    n0 --> n1
    n0 --> n7
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n2 --> n5
    n4 --> n1
    n4 --> n7
    n6 --> n1
    click n0 "../modules/IterationOutlook.test.md"
    click n1 "../modules/OnTrackSummary.md"
    click n2 "../modules/MetricCount.md"
    click n3 "../modules/planningReturn.md"
    click n4 "../modules/planningLinks.test.md"
    click n5 "../modules/useScopeLink.md"
    click n6 "../modules/AnalyticsPage.md"
    click n7 "../modules/types_iteration.md"
    click n8 "../modules/formatDate.md"
    click n9 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationOutlook.test](../modules/IterationOutlook.test.md) |
| Inbound | [planningLinks.test](../modules/planningLinks.test.md) |
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [MetricCount](../modules/MetricCount.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [formatDate](../modules/formatDate.md) |
| Outbound | [workNumbers](../modules/workNumbers.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Verdict](../entities/Verdict.md) | Type alias | 10 | `'done' \| 'noSchedule' \| 'late' \| 'atRisk' \| 'onTrack'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OnTrackSummary` | `({ summary }: { summary: IterationSummary })` | — | Answers "are we on track for the end date?" in one line, then shows why. |
