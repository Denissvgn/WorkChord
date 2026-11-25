# GanttResponse

**Location:** `frontend/src/types/gantt.ts:67`
**Kind:** Interface
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

_Auto-generated from `GanttResponse` in `frontend/src/types/gantt.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `iteration` | `Iteration` | Yes | — | — |
| `tasks` | `GanttTask[]` | Yes | — | — |
| `overdue_task_ids` | `number[]` | Yes | — | — |
| `inverted_dependencies` | `InvertedDependency[]` | No | — | — |
| `holidays` | `string[]` | Yes | — | — |
| `weekends` | `string[]` | Yes | — | — |
| `member_vacations` | `Record<number, string[]>` | Yes | — | — |
| `schedule_result` | `ScheduleResult \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttResponse (frontend/src/types/gantt.ts)"]
    n1["PlanReviewSection (frontend/src/components/planning/PlanReviewSection.tsx)"]
    n2["PlanScheduleSection (frontend/src/components/planning/PlanScheduleSection.tsx)"]
    n3["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n4["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n5["frontend/src/pages/GanttPage.test.tsx"]
    n6["frontend/src/services/ganttService.ts"]
    n7["frontend/src/test/ganttChrome.test.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/PlanReviewSection.md"
    click n2 "../modules/PlanScheduleSection.md"
    click n3 "../modules/usePlanningReadiness.test.md"
    click n4 "../modules/usePlanningReadiness.md"
    click n5 "../modules/GanttPage.test.md"
    click n6 "../modules/ganttService.md"
    click n7 "../modules/ganttChrome.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_gantt](../modules/types_gantt.md) | 0 | `holidays`, `inverted_dependencies`, `iteration`, `member_vacations`, `overdue_task_ids`, `schedule_result`, `tasks`, `weekends` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanReviewSection` | type_reference | [PlanReviewSection](../modules/PlanReviewSection.md) | — |
| `PlanScheduleSection` | type_reference | [PlanScheduleSection](../modules/PlanScheduleSection.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `usePlanningReadiness` | import | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `ganttService` | import | [ganttService](../modules/ganttService.md) | — |
| `ganttChrome.test` | import | [ganttChrome.test](../modules/ganttChrome.test.md) | — |
