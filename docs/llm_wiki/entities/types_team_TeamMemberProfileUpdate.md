# TeamMemberProfileUpdate

**Location:** `frontend/src/types/team.ts:99`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberProfileUpdate` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `display_name` | `string` | *required* | — |
| `email` | `string \| null` | *required* | — |
| `headline` | `string \| null` | *required* | — |
| `summary` | `string \| null` | *required* | — |
| `notes` | `string \| null` | *required* | — |
| `automation_enabled` | `boolean` | *required* | — |
| `profile_kind` | `TeamMemberProfileKind` | *required* | — |
| `assignment_modes` | `TeamMemberAssignmentMode[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfileUpdate (frontend/src/types/team.ts)"]
    n1["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n2["frontend/src/components/team/TeamProfileManager.tsx"]
    n3["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/TeamProfileManager.test.md"
    click n2 "../modules/TeamProfileManager.md"
    click n3 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `assignment_modes`, `automation_enabled`, `display_name`, `email`, `headline`, `notes`, `profile_kind`, `summary` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
