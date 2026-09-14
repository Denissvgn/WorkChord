# Iteration

**Location:** `frontend/src/types/iteration.ts:8`
**Kind:** Class
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `Iteration` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `calendar_id` | `number` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `project` | `IterationProject \| null` | *required* | — |
| `start_date` | `string` | *required* | — |
| `end_date` | `string` | *required* | — |
| `manager_email` | `string` | *required* | — |
| `working_days` | `number` | *required* | — |

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
    n6["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n7["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n8["enrichPlanningTeamMembers (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n9["frontend/src/pages/GanttPage.test.tsx"]
    n10["frontend/src/pages/IterationsPage.tsx"]
    n11["frontend/src/pages/OverviewPage.test.tsx"]
    n12["frontend/src/pages/OverviewPage.tsx"]
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
    click n6 "../modules/usePlanningNavigationSummary.md"
    click n7 "../modules/usePlanningReadiness.test.md"
    click n8 "../modules/usePlanningReadiness.md"
    click n9 "../modules/GanttPage.test.md"
    click n10 "../modules/IterationsPage.md"
    click n11 "../modules/OverviewPage.test.md"
    click n12 "../modules/OverviewPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `calendar_id`, `end_date`, `id`, `manager_email`, `name`, `project`, `project_id`, `start_date`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationForm.test` | import | [IterationForm.test](../modules/IterationForm.test.md) | — |
| `IterationForm` | type_reference | [IterationForm](../modules/IterationForm.md) | — |
| `IterationList` | type_reference | [IterationList](../modules/IterationList.md) | — |
| `IterationSelector` | type_reference | [IterationSelector](../modules/IterationSelector.md) | — |
| `ProjectIterationsSection` | type_reference | [ProjectIterationsSection](../modules/ProjectIterationsSection.md) | — |
| `usePlanningNavigationSummary` | import | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `enrichPlanningTeamMembers` | type_reference | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `GanttPage.test` | import | [GanttPage.test](../modules/GanttPage.test.md) | — |
| `IterationsPage` | import | [IterationsPage](../modules/IterationsPage.md) | — |
| `OverviewPage.test` | import | [OverviewPage.test](../modules/OverviewPage.test.md) | — |
| `OverviewPage` | import | [OverviewPage](../modules/OverviewPage.md) | — |

> References: showing 12 of 17 logical references; 5 omitted by the 12-row generated summary limit.
