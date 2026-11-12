# GanttTask

**Location:** `frontend/src/types/gantt.ts:6`
**Kind:** Interface
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

_Auto-generated from `GanttTask` in `frontend/src/types/gantt.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `description` | `string` | No | — | — |
| `project_id` | `number \| null` | No | — | — |
| `milestone_id` | `number \| null` | No | — | — |
| `start_date` | `string \| null` | Yes | — | — |
| `end_date` | `string \| null` | Yes | — | — |
| `actual_start_date` | `string \| null` | No | — | — |
| `actual_end_date` | `string \| null` | No | — | — |
| `min_start_date` | `string \| null` | No | — | — |
| `max_end_date` | `string \| null` | No | — | — |
| `effort_days` | `number \| null` | Yes | — | — |
| `effort_hours` | `number \| null` | No | — | — |
| `calculated_effort_days` | `number \| null` | Yes | — | — |
| `progress` | `number` | Yes | — | — |
| `priority` | `number` | Yes | — | — |
| `status` | `'planned' \| 'active' \| 'resolved' \| 'closed'` | Yes | — | — |
| `is_composite` | `boolean` | Yes | — | — |
| `is_overdue` | `boolean` | Yes | — | — |
| `is_delayed` | `boolean` | Yes | — | — |
| `is_optional` | `boolean` | Yes | — | — |
| `is_deferred` | `boolean` | No | — | — |
| `is_outside_constraints` | `boolean` | Yes | — | — |
| `tags` | `string[]` | Yes | — | — |
| `milestone` | <pre><code>&#123;&#10;        id&#58; number&#59;&#10;        project&#95;id&#58; number&#59;&#10;        name&#58; string&#59;&#10;        status&#58; string&#59;&#10;        target&#95;date&#63;&#58; string &#124; null&#59;&#10;    &#125; &#124; null</code></pre> | No | — | — |
| `assignee` | `{ id: number; name: string } \| null` | No | — | — |
| `assignees` | `Array<{ id: number; name: string }>` | Yes | — | — |
| `children` | `GanttTask[]` | Yes | — | — |
| `dependencies` | `number[]` | Yes | — | — |
| `version` | `number` | No | — | — |
| `sandbox_update` | `TaskUpdate` | No | — | — |
| `isSandboxModified` | `boolean` | No | — | — |
| `schedule_result` | <pre><code>&#123;&#10;        scheduled&#95;start&#58; string&#59;&#10;        scheduled&#95;end&#58; string&#59;&#10;        issues&#58; Array&#60;&#123;&#10;            is&#95;overload&#58; boolean&#59;&#10;            description&#58; string&#59;&#10;        &#125;&#62;&#59;&#10;    &#125;</code></pre> | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttTask (frontend/src/types/gantt.ts)"]
    n1["FlattenedTask (frontend/src/components/gantt/GanttChart.tsx)"]
    n2["frontend/src/components/gantt/GanttBarInputs.tsx"]
    n3["frontend/src/components/gantt/GanttChart.test.tsx"]
    n4["frontend/src/components/gantt/GanttChart.tsx"]
    n5["frontend/src/components/gantt/ScheduleExplanationDetails.tsx"]
    n6["frontend/src/components/gantt/TaskEditModal.test.tsx"]
    n7["frontend/src/components/gantt/TaskEditModal.tsx"]
    n8["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n9["frontend/src/pages/GanttPage.test.tsx"]
    n10["frontend/src/pages/GanttPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/GanttBarInputs.md"
    click n3 "../modules/GanttChart.test.md"
    click n4 "../modules/GanttChart.md"
    click n5 "../modules/ScheduleExplanationDetails.md"
    click n6 "../modules/TaskEditModal.test.md"
    click n7 "../modules/TaskEditModal.md"
    click n8 "../modules/usePlanningReadiness.test.md"
    click n9 "../modules/GanttPage.test.md"
    click n10 "../modules/GanttPage.md"
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
| `GanttBarInputs` | import | [GanttBarInputs](../modules/GanttBarInputs.md) | — |
| `GanttChart.test` | import | [GanttChart.test](../modules/GanttChart.test.md) | — |
| `GanttChart` | import | [GanttChart](../modules/GanttChart.md) | — |
| `ScheduleExplanationDetails` | import | [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md) | — |
| `TaskEditModal.test` | import | [TaskEditModal.test](../modules/TaskEditModal.test.md) | — |
| `TaskEditModal` | import | [TaskEditModal](../modules/TaskEditModal.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `GanttPage` | import | [GanttPage](../modules/GanttPage.md) | — |
