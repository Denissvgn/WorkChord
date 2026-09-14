# GanttResponse

**Location:** `frontend/src/types/gantt.ts:56`
**Kind:** Class
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

_Auto-generated from `GanttResponse` in `frontend/src/types/gantt.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `iteration` | `Iteration` | *required* | — |
| `tasks` | `GanttTask[]` | *required* | — |
| `overdue_task_ids` | `number[]` | *required* | — |
| `holidays` | `string[]` | *required* | — |
| `weekends` | `string[]` | *required* | — |
| `member_vacations` | `Record<number, string[]>` | *required* | — |
| `schedule_result` | `ScheduleResult \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttResponse (frontend/src/types/gantt.ts)"]
    n1["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n2["enrichPlanningTeamMembers (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n3["frontend/src/pages/GanttPage.test.tsx"]
    n4["frontend/src/services/ganttService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/usePlanningReadiness.test.md"
    click n2 "../modules/usePlanningReadiness.md"
    click n3 "../modules/GanttPage.test.md"
    click n4 "../modules/ganttService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_gantt](../modules/types_gantt.md) | 0 | `holidays`, `iteration`, `member_vacations`, `overdue_task_ids`, `schedule_result`, `tasks`, `weekends` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `enrichPlanningTeamMembers` | type_reference | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `ganttService` | import | [ganttService](../modules/ganttService.md) | — |
