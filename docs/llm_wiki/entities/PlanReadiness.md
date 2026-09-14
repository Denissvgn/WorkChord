# PlanReadiness

**Location:** `frontend/src/features/planningMasters/masters.ts:93`
**Kind:** Class
**Bases:** —
**Module:** [planningMasters_masters](../modules/planningMasters_masters.md)

## Description

_Auto-generated from `PlanReadiness` in `frontend/src/features/planningMasters/masters.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `iterationCount` | `number` | *required* | — |
| `hasCurrentIteration` | `boolean` | *required* | — |
| `currentIterationName` | `string` | *required* | — |
| `currentIterationStart` | `string` | *required* | — |
| `currentIterationEnd` | `string` | *required* | — |
| `currentIterationDays` | `number` | *required* | — |
| `teamMemberCount` | `number` | *required* | — |
| `teamCapacity` | `number` | *required* | — |
| `teamMembersNoCap` | `number` | *required* | — |
| `taskCount` | `number` | *required* | — |
| `tasksWithoutAssignee` | `number` | *required* | — |
| `tasksWithoutEffort` | `number` | *required* | — |
| `hasGanttSchedule` | `boolean` | *required* | — |
| `ganttLastBuilt` | `string` | *required* | — |
| `riskCount` | `number` | *required* | — |
| `inboxCount` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanReadiness (frontend/src/features/planningMasters/masters.ts)"]
    n1["frontend/src/features/planningMasters/masters.test.ts"]
    n2["derivePlanningRecovery (frontend/src/features/planningMasters/masters.ts)"]
    n3["deriveStatus (frontend/src/features/planningMasters/masters.ts)"]
    n4["localizeStatus (frontend/src/features/planningMasters/masters.ts)"]
    n5["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n6["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n7["frontend/src/pages/PlanMasterPage.test.tsx"]
    n8["frontend/src/pages/PlanMasterPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/planningMasters_masters.md"
    click n1 "../modules/planningMasters_masters.test.md"
    click n2 "../modules/planningMasters_masters.md"
    click n3 "../modules/planningMasters_masters.md"
    click n4 "../modules/planningMasters_masters.md"
    click n5 "../modules/usePlanningNavigationSummary.md"
    click n6 "../modules/usePlanningReadiness.md"
    click n7 "../modules/PlanMasterPage.test.md"
    click n8 "../modules/PlanMasterPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planningMasters_masters](../modules/planningMasters_masters.md) | 0 | `currentIterationDays`, `currentIterationEnd`, `currentIterationName`, `currentIterationStart`, `ganttLastBuilt`, `hasCurrentIteration`, `hasGanttSchedule`, `inboxCount`, `iterationCount`, `riskCount`, `taskCount`, `tasksWithoutAssignee` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `masters.test` | import | [planningMasters_masters.test](../modules/planningMasters_masters.test.md) | — |
| `derivePlanningRecovery` | type_reference | [planningMasters_masters](../modules/planningMasters_masters.md) | — |
| `deriveStatus` | type_reference | [planningMasters_masters](../modules/planningMasters_masters.md) | — |
| `localizeStatus` | type_reference | [planningMasters_masters](../modules/planningMasters_masters.md) | — |
| `usePlanningNavigationSummary` | import | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) | — |
| `usePlanningReadiness` | import | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `PlanMasterPage.test` | import | [PlanMasterPage.test](../modules/PlanMasterPage.test.md) | — |
| `PlanMasterPage` | import | [PlanMasterPage](../modules/PlanMasterPage.md) | — |
