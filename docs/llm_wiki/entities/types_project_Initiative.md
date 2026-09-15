# Initiative

**Location:** `frontend/src/types/project.ts:13`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `Initiative` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `owner_id` | `number \| null` | *required* | — |
| `owner` | `ProjectOwner \| null` | *required* | — |
| `owner_profile_id` | `number \| null` | *required* | — |
| `owner_profile` | `ProjectProfileOwner \| null` | *required* | — |
| `health` | `ProjectHealth` | *required* | — |
| `target_date` | `string \| null` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Initiative (frontend/src/types/project.ts)"]
    n1["InitiativeForm (frontend/src/components/projects/InitiativeForm.tsx)"]
    n2["frontend/src/pages/ProjectsPage.tsx"]
    n3["frontend/src/pages/RoadmapPage.tsx"]
    n4["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/InitiativeForm.md"
    click n2 "../modules/ProjectsPage.md"
    click n3 "../modules/RoadmapPage.md"
    click n4 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `created_at`, `description`, `health`, `id`, `name`, `owner`, `owner_id`, `owner_profile`, `owner_profile_id`, `target_date`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `InitiativeForm` | type_reference | [InitiativeForm](../modules/InitiativeForm.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `RoadmapPage` | import | [RoadmapPage](../modules/RoadmapPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
