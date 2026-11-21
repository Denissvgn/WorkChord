# TeamMemberProfile

**Location:** `frontend/src/types/team.ts:60`
**Kind:** Interface
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberProfile` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `seed_key` | `string \| null` | No | — | — |
| `display_name` | `string` | Yes | — | — |
| `email` | `string \| null` | No | — | — |
| `headline` | `string \| null` | No | — | — |
| `summary` | `string \| null` | No | — | — |
| `notes` | `string \| null` | No | — | — |
| `automation_enabled` | `boolean` | Yes | — | — |
| `profile_kind` | `TeamMemberProfileKind` | Yes | — | — |
| `assignment_modes` | `TeamMemberAssignmentMode[]` | Yes | — | — |
| `skills` | `TeamMemberProfileSkill[]` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfile (frontend/src/types/team.ts)"]
    n1["frontend/src/components/capacity/TeamForm.tsx"]
    n2["AssigneePicker (frontend/src/components/tasks/AssigneePicker.tsx)"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/team/directoryModel.test.ts"]
    n6["buildDirectory (frontend/src/components/team/directoryModel.ts)"]
    n7["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n8["frontend/src/components/team/TeamProfileManager.tsx"]
    n9["frontend/src/pages/PlanPage.test.tsx"]
    n10["frontend/src/pages/TeamPage.test.tsx"]
    n11["frontend/src/pages/TeamPage.transport.test.tsx"]
    n12["frontend/src/services/teamService.ts"]
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
    click n1 "../modules/TeamForm.md"
    click n2 "../modules/AssigneePicker.md"
    click n3 "../modules/KanbanBoard.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/directoryModel.test.md"
    click n6 "../modules/directoryModel.md"
    click n7 "../modules/TeamProfileManager.test.md"
    click n8 "../modules/TeamProfileManager.md"
    click n9 "../modules/PlanPage.test.md"
    click n10 "../modules/TeamPage.test.md"
    click n11 "../modules/TeamPage.transport.test.md"
    click n12 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `assignment_modes`, `automation_enabled`, `created_at`, `display_name`, `email`, `headline`, `id`, `notes`, `profile_kind`, `seed_key`, `skills`, `summary` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `AssigneePicker` | type_reference | [AssigneePicker](../modules/AssigneePicker.md) | — |
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `directoryModel.test` | import | [directoryModel.test](../modules/directoryModel.test.md) | — |
| `buildDirectory` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
| `PlanPage.test` | import | [PlanPage.test](../modules/PlanPage.test.md) | — |
| `TeamPage.test` | import | [TeamPage.test](../modules/TeamPage.test.md) | — |
| `TeamPage.transport.test` | import | [TeamPage.transport.test](../modules/TeamPage.transport.test.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
