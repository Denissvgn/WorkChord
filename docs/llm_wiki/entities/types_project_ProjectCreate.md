# ProjectCreate

**Location:** `frontend/src/types/project.ts:76`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectCreate` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `status` | `ProjectStatus` | Yes | — | — |
| `health` | `ProjectHealth` | Yes | — | — |
| `owner_id` | `number \| null` | No | — | — |
| `owner_profile_id` | `number \| null` | No | — | — |
| `initiative_id` | `number \| null` | No | — | — |
| `start_date` | `string \| null` | No | — | — |
| `target_date` | `string \| null` | No | — | — |
| `sort_order` | `number` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectCreate (frontend/src/types/project.ts)"]
    n1["frontend/src/components/projects/ProjectForm.tsx"]
    n2["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `description`, `health`, `initiative_id`, `name`, `owner_id`, `owner_profile_id`, `sort_order`, `start_date`, `status`, `target_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ProjectForm` | import | [ProjectForm](../modules/ProjectForm.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
