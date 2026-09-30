# InitiativeUpdate

**Location:** `frontend/src/types/project.ts:36`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `InitiativeUpdate` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | `string` | No | — | — |
| `description` | `string \| null` | No | — | — |
| `owner_id` | `number \| null` | No | — | — |
| `owner_profile_id` | `number \| null` | No | — | — |
| `health` | `ProjectHealth` | No | — | — |
| `target_date` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["InitiativeUpdate (frontend/src/types/project.ts)"]
    n1["frontend/src/services/projectService.ts"]
    n1 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `description`, `health`, `name`, `owner_id`, `owner_profile_id`, `target_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `projectService` | import | [projectService](../modules/projectService.md) | — |
