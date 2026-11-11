# TeamMember

**Location:** `frontend/src/types/team.ts:110`
**Kind:** Interface
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMember` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `iteration_id` | `number` | Yes | — | — |
| `profile_id` | `number \| null` | No | — | — |
| `name` | `string` | Yes | — | — |
| `position` | `string` | Yes | — | — |
| `email` | `string` | No | — | — |
| `availability_percent` | `number` | Yes | — | — |
| `professionalism_coefficient` | `number` | Yes | — | — |
| `operational_utilization` | `number` | Yes | — | — |
| `profile` | `TeamMemberProfileCompact \| null` | No | — | — |
| `vacations` | `Vacation[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMember (frontend/src/types/team.ts)"]
    n1["frontend/src/components/planning/PlanQuickAddCapacity.test.tsx"]
    n2["PlanQuickAddCapacity (frontend/src/components/planning/PlanQuickAddCapacity.tsx)"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx"]
    n4["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n5["frontend/src/components/team/TeamForm.test.tsx"]
    n6["frontend/src/components/team/TeamForm.tsx"]
    n7["frontend/src/components/team/TeamList.tsx"]
    n8["frontend/src/components/team/VacationManager.tsx"]
    n9["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n10["countPlanningExceptions (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n11["enrichPlanningTeamMembers (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n12["frontend/src/pages/CalendarPage.tsx"]
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
    click n0 "../modules/types_team.md"
    click n1 "../modules/PlanQuickAddCapacity.test.md"
    click n2 "../modules/PlanQuickAddCapacity.md"
    click n3 "../modules/KanbanBoard.test.md"
    click n4 "../modules/ImportTeamModal.test.md"
    click n5 "../modules/TeamForm.test.md"
    click n6 "../modules/TeamForm.md"
    click n7 "../modules/TeamList.md"
    click n8 "../modules/VacationManager.md"
    click n9 "../modules/usePlanningReadiness.test.md"
    click n10 "../modules/usePlanningReadiness.md"
    click n11 "../modules/usePlanningReadiness.md"
    click n12 "../modules/CalendarPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `availability_percent`, `email`, `id`, `iteration_id`, `name`, `operational_utilization`, `position`, `professionalism_coefficient`, `profile`, `profile_id`, `vacations` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanQuickAddCapacity.test` | import | [PlanQuickAddCapacity.test](../modules/PlanQuickAddCapacity.test.md) | — |
| `PlanQuickAddCapacity` | type_reference | [PlanQuickAddCapacity](../modules/PlanQuickAddCapacity.md) | — |
| `KanbanBoard.test` | import | [KanbanBoard.test](../modules/KanbanBoard.test.md) | — |
| `ImportTeamModal.test` | import | [ImportTeamModal.test](../modules/ImportTeamModal.test.md) | — |
| `TeamForm.test` | import | [TeamForm.test](../modules/TeamForm.test.md) | — |
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `TeamList` | import | [TeamList](../modules/TeamList.md) | — |
| `VacationManager` | import | [VacationManager](../modules/VacationManager.md) | — |
| `usePlanningReadiness.test` | import | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) | — |
| `countPlanningExceptions` | type_reference | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `enrichPlanningTeamMembers` | type_reference | [usePlanningReadiness](../modules/usePlanningReadiness.md) | — |
| `CalendarPage` | import | [CalendarPage](../modules/CalendarPage.md) | — |

> References: showing 12 of 15 logical references; 3 omitted by the 12-row generated summary limit.
