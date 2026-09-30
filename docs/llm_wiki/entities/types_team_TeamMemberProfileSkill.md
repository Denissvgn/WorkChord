# TeamMemberProfileSkill

**Location:** `frontend/src/types/team.ts:24`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberProfileSkill` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `profile_id` | `number` | Yes | — | — |
| `skill_key` | `string` | Yes | — | — |
| `skill_name` | `string` | Yes | — | — |
| `category` | `string \| null` | No | — | — |
| `level` | `number` | Yes | — | — |
| `interest` | `number` | Yes | — | — |
| `is_weakness` | `boolean` | Yes | — | — |
| `keywords_json` | `string[]` | Yes | — | — |
| `notes` | `string \| null` | No | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfileSkill (frontend/src/types/team.ts)"]
    n1["frontend/src/components/team/TeamProfileManager.tsx"]
    n2["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/TeamProfileManager.md"
    click n2 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `category`, `created_at`, `id`, `interest`, `is_weakness`, `keywords_json`, `level`, `notes`, `profile_id`, `skill_key`, `skill_name`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
