# TeamMemberProfile

**Location:** `frontend/src/types/team.ts:60`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberProfile` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `seed_key` | `string \| null` | *required* | — |
| `display_name` | `string` | *required* | — |
| `email` | `string \| null` | *required* | — |
| `headline` | `string \| null` | *required* | — |
| `summary` | `string \| null` | *required* | — |
| `notes` | `string \| null` | *required* | — |
| `automation_enabled` | `boolean` | *required* | — |
| `profile_kind` | `TeamMemberProfileKind` | *required* | — |
| `assignment_modes` | `TeamMemberAssignmentMode[]` | *required* | — |
| `skills` | `TeamMemberProfileSkill[]` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfile (frontend/src/types/team.ts)"]
    n1["frontend/src/components/team/TeamForm.tsx"]
    n2["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n3["frontend/src/components/team/TeamProfileManager.tsx"]
    n4["frontend/src/pages/TeamPage.tsx"]
    n5["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/TeamForm.md"
    click n2 "../modules/TeamProfileManager.test.md"
    click n3 "../modules/TeamProfileManager.md"
    click n4 "../modules/TeamPage.md"
    click n5 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `assignment_modes`, `automation_enabled`, `created_at`, `display_name`, `email`, `headline`, `id`, `notes`, `profile_kind`, `seed_key`, `skills`, `summary` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
| `TeamPage` | import | [TeamPage](../modules/TeamPage.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
