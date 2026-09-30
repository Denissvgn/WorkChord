# TeamMemberOption

**Location:** `frontend/src/types/team.ts:124`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `TeamMemberOption` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `iteration_id` | `number \| null` | No | — | — |
| `iteration_name` | `string \| null` | No | — | — |
| `name` | `string` | Yes | — | — |
| `position` | `string` | Yes | — | — |
| `email` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberOption (frontend/src/types/team.ts)"]
    n1["frontend/src/services/teamService.ts"]
    n2["frontend/src/types/project.ts"]
    n3["frontend/src/utils/teamMemberLabels.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/teamService.md"
    click n2 "../modules/types_project.md"
    click n3 "../modules/teamMemberLabels.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `email`, `id`, `iteration_id`, `iteration_name`, `name`, `position` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `teamService` | import | [teamService](../modules/teamService.md) | — |
| `project` | import | [types_project](../modules/types_project.md) | — |
| `teamMemberLabels` | import | [teamMemberLabels](../modules/teamMemberLabels.md) | — |
