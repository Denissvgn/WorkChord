# TeamMemberCreate

**Location:** `frontend/src/types/team.ts:133`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberCreate` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | `string` | Yes | — | — |
| `position` | `string` | Yes | — | — |
| `email` | `string` | No | — | — |
| `profile_id` | `number \| null` | No | — | — |
| `availability_percent` | `number` | Yes | — | — |
| `professionalism_coefficient` | `number` | Yes | — | — |
| `operational_utilization` | `number` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberCreate (frontend/src/types/team.ts)"]
    n1["frontend/src/components/team/TeamForm.test.tsx"]
    n2["frontend/src/components/team/TeamForm.tsx"]
    n3["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/TeamForm.test.md"
    click n2 "../modules/TeamForm.md"
    click n3 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `availability_percent`, `email`, `name`, `operational_utilization`, `position`, `professionalism_coefficient`, `profile_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamForm.test` | import | [TeamForm.test](../modules/TeamForm.test.md) | — |
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
