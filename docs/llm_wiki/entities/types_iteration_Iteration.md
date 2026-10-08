# Iteration

**Location:** `frontend/src/types/iteration.ts:9`
**Kind:** Class
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `Iteration` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nominal_day_hours` | `number` | No | — | — |
| `revision` | `number` | No | — | — |
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `calendar_id` | `number` | Yes | — | — |
| `project_id` | `number \| null` | No | — | — |
| `project` | `IterationProject \| null` | No | — | — |
| `start_date` | `string` | Yes | — | — |
| `end_date` | `string` | Yes | — | — |
| `manager_email` | `string` | No | — | — |
| `working_days` | `number` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Iteration (frontend/src/types/iteration.ts)"]
    n1["frontend/src/components/iteration/IterationForm.test.tsx"]
    n2["IterationForm (frontend/src/components/iteration/IterationForm.tsx)"]
    n3["IterationList (frontend/src/components/iteration/IterationList.tsx)"]
    n4["IterationSelector (frontend/src/components/iteration/IterationSelector.tsx)"]
    n5["ProjectIterationsSection (frontend/src/components/projects/ProjectIterationsSection.tsx)"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n8["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n9["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n10["enrichPlanningTeamMembers (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n11["frontend/src/pages/GanttPage.test.tsx"]
    n12["frontend/src/pages/IterationsPage.tsx"]
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
    n11 --> n0
    n12 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/IterationForm.test.md"
    click n2 "../modules/IterationForm.md"
    click n3 "../modules/IterationList.md"
    click n4 "../modules/IterationSelector.md"
    click n5 "../modules/ProjectIterationsSection.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/TaskWorkPanel.md"
    click n8 "../modules/usePlanningNavigationSummary.md"
    click n9 "../modules/usePlanningReadiness.test.md"
    click n10 "../modules/usePlanningReadiness.md"
    click n11 "../modules/GanttPage.test.md"
    click n12 "../modules/IterationsPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `calendar_id`, `end_date`, `id`, `manager_email`, `name`, `nominal_day_hours`, `project`, `project_id`, `revision`, `start_date`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationForm.test` | import | [IterationForm.test](../modules/IterationForm.test.md) | — |
| `IterationForm` | type_reference | [IterationForm](../modules/IterationForm.md) | — |
| `IterationList` | type_reference | [IterationList](../modules/IterationList.md) | — |
| `IterationSelector` | type_reference | [IterationSelector](../modules/IterationSelector.md) | — |
| `ProjectIterationsSection` | type_reference | [ProjectIterationsSection](../modules/ProjectIterationsSection.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `TaskWorkPanel` | import | [TaskWorkPanel](../modules/TaskWorkPanel.md) | — |
| `usePlanningNavigationSummary` | import | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `enrichPlanningTeamMembers` | type_reference | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `IterationsPage` | import | [IterationsPage](../modules/IterationsPage.md) | — |

> References: showing 12 of 19 logical references; 7 omitted by the 12-row generated summary limit.
