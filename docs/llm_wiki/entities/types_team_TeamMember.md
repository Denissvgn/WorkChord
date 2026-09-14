# TeamMember

**Location:** `frontend/src/types/team.ts:110`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMember` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `iteration_id` | `number` | *required* | — |
| `profile_id` | `number \| null` | *required* | — |
| `name` | `string` | *required* | — |
| `position` | `string` | *required* | — |
| `email` | `string` | *required* | — |
| `availability_percent` | `number` | *required* | — |
| `professionalism_coefficient` | `number` | *required* | — |
| `operational_utilization` | `number` | *required* | — |
| `profile` | `TeamMemberProfileCompact \| null` | *required* | — |
| `vacations` | `Vacation[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMember (frontend/src/types/team.ts)"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanBoard.test.tsx"]
    n2["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n3["frontend/src/components/team/TeamForm.test.tsx"]
    n4["frontend/src/components/team/TeamForm.tsx"]
    n5["frontend/src/components/team/TeamList.tsx"]
    n6["frontend/src/components/team/VacationManager.tsx"]
    n7["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n8["countPlanningExceptions (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n9["enrichPlanningTeamMembers (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n10["frontend/src/pages/CalendarPage.tsx"]
    n11["frontend/src/pages/TeamPage.tsx"]
    n12["frontend/src/pages/TriagePage.tsx"]
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
    click n1 "../modules/KanbanBoard.test.md"
    click n2 "../modules/ImportTeamModal.test.md"
    click n3 "../modules/TeamForm.test.md"
    click n4 "../modules/TeamForm.md"
    click n5 "../modules/TeamList.md"
    click n6 "../modules/VacationManager.md"
    click n7 "../modules/usePlanningReadiness.test.md"
    click n8 "../modules/usePlanningReadiness.md"
    click n9 "../modules/usePlanningReadiness.md"
    click n10 "../modules/CalendarPage.md"
    click n11 "../modules/TeamPage.md"
    click n12 "../modules/TriagePage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `availability_percent`, `email`, `id`, `iteration_id`, `name`, `operational_utilization`, `position`, `professionalism_coefficient`, `profile`, `profile_id`, `vacations` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
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
| `TeamPage` | import | [TeamPage](../modules/TeamPage.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
