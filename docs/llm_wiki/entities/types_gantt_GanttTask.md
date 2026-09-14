# GanttTask

**Location:** `frontend/src/types/gantt.ts:6`
**Kind:** Class
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

_Auto-generated from `GanttTask` in `frontend/src/types/gantt.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `title` | `string` | *required* | — |
| `description` | `string` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `milestone_id` | `number \| null` | *required* | — |
| `start_date` | `string \| null` | *required* | — |
| `end_date` | `string \| null` | *required* | — |
| `actual_start_date` | `string \| null` | *required* | — |
| `actual_end_date` | `string \| null` | *required* | — |
| `min_start_date` | `string \| null` | *required* | — |
| `max_end_date` | `string \| null` | *required* | — |
| `effort_days` | `number` | *required* | — |
| `effort_hours` | `number` | *required* | — |
| `calculated_effort_days` | `number \| null` | *required* | — |
| `progress` | `number` | *required* | — |
| `priority` | `number` | *required* | — |
| `status` | `'planned' \| 'active' \| 'resolved' \| 'closed'` | *required* | — |
| `is_composite` | `boolean` | *required* | — |
| `is_overdue` | `boolean` | *required* | — |
| `is_delayed` | `boolean` | *required* | — |
| `is_optional` | `boolean` | *required* | — |
| `is_deferred` | `boolean` | *required* | — |
| `is_outside_constraints` | `boolean` | *required* | — |
| `tags` | `string[]` | *required* | — |
| `milestone` | `{         id: number;         project_id: number;         name: string;         status: string;         target_date?: string \| null;     } \| null` | *required* | — |
| `assignee` | `{ id: number; name: string } \| null` | *required* | — |
| `assignees` | `Array<{ id: number; name: string }>` | *required* | — |
| `children` | `GanttTask[]` | *required* | — |
| `dependencies` | `number[]` | *required* | — |
| `version` | `number` | *required* | — |
| `sandbox_update` | `TaskUpdate` | *required* | — |
| `isSandboxModified` | `boolean` | *required* | — |
| `schedule_result` | `{         scheduled_start: string;         scheduled_end: string;         issues: Array<{             is_overload: boolean;             description: string;         }>;     }` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttTask (frontend/src/types/gantt.ts)"]
    n1["FlattenedTask (frontend/src/components/gantt/GanttChart.tsx)"]
    n2["frontend/src/components/gantt/GanttChart.test.tsx"]
    n3["frontend/src/components/gantt/GanttChart.tsx"]
    n4["frontend/src/components/gantt/ScheduleExplanationDetails.tsx"]
    n5["frontend/src/components/gantt/TaskEditModal.tsx"]
    n6["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n7["frontend/src/pages/GanttPage.test.tsx"]
    n8["frontend/src/pages/GanttPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/GanttChart.test.md"
    click n3 "../modules/GanttChart.md"
    click n4 "../modules/ScheduleExplanationDetails.md"
    click n5 "../modules/TaskEditModal.md"
    click n6 "../modules/usePlanningReadiness.test.md"
    click n7 "../modules/GanttPage.test.md"
    click n8 "../modules/GanttPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_gantt](../modules/types_gantt.md) | 0 | `actual_end_date`, `actual_start_date`, `assignee`, `assignees`, `calculated_effort_days`, `children`, `dependencies`, `description`, `effort_days`, `effort_hours`, `end_date`, `id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `FlattenedTask` | [GanttChart](../modules/GanttChart.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `GanttChart.test` | import | [GanttChart.test](../modules/GanttChart.test.md) | — |
| `GanttChart` | import | [GanttChart](../modules/GanttChart.md) | — |
| `ScheduleExplanationDetails` | import | [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md) | — |
| `TaskEditModal` | import | [TaskEditModal](../modules/TaskEditModal.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `GanttPage` | import | [GanttPage](../modules/GanttPage.md) | — |
