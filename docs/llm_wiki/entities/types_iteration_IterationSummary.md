# IterationSummary

**Location:** `frontend/src/types/iteration.ts:59`
**Kind:** Interface
**Bases:** `WorkMetrics`
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `IterationSummary` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `project_id` | `number \| null` | No | — | — |
| `project` | `IterationProject \| null` | No | — | — |
| `start_date` | `string` | Yes | — | — |
| `end_date` | `string` | Yes | — | — |
| `working_days` | `number` | Yes | — | — |
| `total_tasks` | `number` | Yes | — | — |
| `completed_tasks` | `number` | Yes | — | — |
| `total_effort_days` | `number` | Yes | — | — |
| `team_capacity_days` | `number` | Yes | — | — |
| `overdue_tasks_count` | `number` | Yes | — | — |
| `status_counts` | `Partial<Record<'planned' \| 'active' \| 'resolved' \| 'closed', number>>` | No | — | — |
| `blocked_tasks` | `number` | No | — | — |
| `remaining_effort_days` | `number` | No | — | — |
| `unknown_estimate_tasks` | `number` | No | — | — |
| `scheduled_finish` | `string \| null` | No | — | — |
| `remaining_working_days` | `number \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationSummary (frontend/src/types/iteration.ts)"]
    n1["WorkMetrics (frontend/src/types/workMetrics.ts)"]
    n2["frontend/src/components/analytics/IterationOutlook.test.tsx"]
    n3["OnTrackSummary (frontend/src/components/analytics/OnTrackSummary.tsx)"]
    n4["StatusDistribution (frontend/src/components/analytics/StatusDistribution.tsx)"]
    n5["frontend/src/pages/OverviewPage.test.tsx"]
    n6["frontend/src/services/iterationService.ts"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/workMetrics.md"
    click n2 "../modules/IterationOutlook.test.md"
    click n3 "../modules/OnTrackSummary.md"
    click n4 "../modules/StatusDistribution.md"
    click n5 "../modules/OverviewPage.test.md"
    click n6 "../modules/iterationService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `blocked_tasks`, `completed_tasks`, `end_date`, `id`, `name`, `overdue_tasks_count`, `project`, `project_id`, `remaining_effort_days`, `remaining_working_days`, `scheduled_finish`, `start_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `WorkMetrics` | [workMetrics](../modules/workMetrics.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationOutlook.test` | import | [IterationOutlook.test](../modules/IterationOutlook.test.md) | — |
| `OnTrackSummary` | type_reference | [OnTrackSummary](../modules/OnTrackSummary.md) | — |
| `StatusDistribution` | type_reference | [StatusDistribution](../modules/StatusDistribution.md) | — |
| `OverviewPage.test` | import | [OverviewPage.test](../modules/OverviewPage.test.md) | — |
| `iterationService` | import | [iterationService](../modules/iterationService.md) | — |
