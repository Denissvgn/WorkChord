# TeamMemberProfileCompact

**Location:** `frontend/src/types/team.ts:76`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberProfileCompact` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `display_name` | `string` | *required* | — |
| `email` | `string \| null` | *required* | — |
| `headline` | `string \| null` | *required* | — |
| `automation_enabled` | `boolean` | *required* | — |
| `profile_kind` | `TeamMemberProfileKind` | *required* | — |
| `assignment_modes` | `TeamMemberAssignmentMode[]` | *required* | — |
| `skills` | `TeamMemberProfileSkill[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfileCompact (frontend/src/types/team.ts)"]
    n1["frontend/src/types/project.ts"]
    n2["frontend/src/utils/teamMemberLabels.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/types_project.md"
    click n2 "../modules/teamMemberLabels.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `assignment_modes`, `automation_enabled`, `display_name`, `email`, `headline`, `id`, `profile_kind`, `skills` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `project` | import | [types_project](../modules/types_project.md) | — |
| `teamMemberLabels` | import | [teamMemberLabels](../modules/teamMemberLabels.md) | — |
