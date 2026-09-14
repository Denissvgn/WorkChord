# MemberCapacity

**Location:** `frontend/src/types/team.ts:154`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

Detailed capacity breakdown from GET /team-members/{id}/capacity.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `team_member_id` | `number` | *required* | — |
| `working_days` | `number` | *required* | — |
| `vacation_days` | `number` | *required* | — |
| `available_days` | `number` | *required* | — |
| `effective_days` | `number` | *required* | — |
| `adjusted_days` | `number` | *required* | — |
| `hours` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MemberCapacity (frontend/src/types/team.ts)"]
    n1["frontend/src/components/team/TeamList.tsx"]
    n2["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/TeamList.md"
    click n2 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `adjusted_days`, `available_days`, `effective_days`, `hours`, `team_member_id`, `vacation_days`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamList` | import | [TeamList](../modules/TeamList.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
