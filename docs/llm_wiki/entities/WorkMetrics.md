# WorkMetrics

**Location:** `frontend/src/types/workMetrics.ts:1`
**Kind:** Class
**Bases:** —
**Module:** [workMetrics](../modules/workMetrics.md)

## Description

_Auto-generated from `WorkMetrics` in `frontend/src/types/workMetrics.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `metric_contract_version` | `number` | *required* | — |
| `total_tasks` | `number` | *required* | — |
| `required_tasks` | `number` | *required* | — |
| `optional_tasks` | `number` | *required* | — |
| `structural_tasks` | `number` | *required* | — |
| `implemented_tasks` | `number` | *required* | — |
| `accepted_tasks` | `number` | *required* | — |
| `overdue_tasks` | `number` | *required* | — |
| `late_start_tasks` | `number` | *required* | — |
| `iteration_overflow_tasks` | `number` | *required* | — |
| `project_target_overflow_tasks` | `number` | *required* | — |
| `acceptance_unknown_tasks` | `number` | *required* | — |
| `accepted_percent` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkMetrics (frontend/src/types/workMetrics.ts)"]
    n1["IterationSummary (frontend/src/types/iteration.ts)"]
    n2["ProjectPortfolioSummary (frontend/src/types/project.ts)"]
    n3["ProjectSummary (frontend/src/types/project.ts)"]
    n4["Release (frontend/src/types/release.ts)"]
    n5["WorkMetricsLine (frontend/src/components/tasks/WorkMetricsLine.tsx)"]
    n6["frontend/src/types/iteration.ts"]
    n7["frontend/src/types/project.ts"]
    n8["frontend/src/types/release.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/workMetrics.md"
    click n1 "../modules/types_iteration.md"
    click n2 "../modules/types_project.md"
    click n3 "../modules/types_project.md"
    click n4 "../modules/types_release.md"
    click n5 "../modules/WorkMetricsLine.md"
    click n6 "../modules/types_iteration.md"
    click n7 "../modules/types_project.md"
    click n8 "../modules/types_release.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [workMetrics](../modules/workMetrics.md) | 0 | `acceptance_unknown_tasks`, `accepted_percent`, `accepted_tasks`, `implemented_tasks`, `iteration_overflow_tasks`, `late_start_tasks`, `metric_contract_version`, `optional_tasks`, `overdue_tasks`, `project_target_overflow_tasks`, `required_tasks`, `structural_tasks` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `IterationSummary` | [types_iteration](../modules/types_iteration.md) |
| Subclass | `ProjectPortfolioSummary` | [types_project](../modules/types_project.md) |
| Subclass | `ProjectSummary` | [types_project](../modules/types_project.md) |
| Subclass | `Release` | [types_release](../modules/types_release.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `WorkMetricsLine` | type_reference | [WorkMetricsLine](../modules/WorkMetricsLine.md) | — |
| `iteration` | import | [types_iteration](../modules/types_iteration.md) | — |
| `project` | import | [types_project](../modules/types_project.md) | — |
| `release` | import | [types_release](../modules/types_release.md) | — |
