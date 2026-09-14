# IterationSummary

**Location:** `frontend/src/types/iteration.ts:56`
**Kind:** Class
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `IterationSummary` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `project` | `IterationProject \| null` | *required* | — |
| `start_date` | `string` | *required* | — |
| `end_date` | `string` | *required* | — |
| `working_days` | `number` | *required* | — |
| `total_tasks` | `number` | *required* | — |
| `completed_tasks` | `number` | *required* | — |
| `total_effort_days` | `number` | *required* | — |
| `team_capacity_days` | `number` | *required* | — |
| `overdue_tasks_count` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationSummary (frontend/src/types/iteration.ts)"]
    n1["frontend/src/pages/OverviewPage.test.tsx"]
    n2["frontend/src/services/iterationService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/OverviewPage.test.md"
    click n2 "../modules/iterationService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `completed_tasks`, `end_date`, `id`, `name`, `overdue_tasks_count`, `project`, `project_id`, `start_date`, `team_capacity_days`, `total_effort_days`, `total_tasks`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `OverviewPage.test` | import | [OverviewPage.test](../modules/OverviewPage.test.md) | — |
| `iterationService` | import | [iterationService](../modules/iterationService.md) | — |
