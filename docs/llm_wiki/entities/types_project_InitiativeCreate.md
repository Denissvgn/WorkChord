# InitiativeCreate

**Location:** `frontend/src/types/project.ts:27`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `InitiativeCreate` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `owner_id` | `number \| null` | *required* | — |
| `owner_profile_id` | `number \| null` | *required* | — |
| `health` | `ProjectHealth` | *required* | — |
| `target_date` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["InitiativeCreate (frontend/src/types/project.ts)"]
    n1["frontend/src/components/projects/InitiativeForm.tsx"]
    n2["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/InitiativeForm.md"
    click n2 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `description`, `health`, `name`, `owner_id`, `owner_profile_id`, `target_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `InitiativeForm` | import | [InitiativeForm](../modules/InitiativeForm.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
