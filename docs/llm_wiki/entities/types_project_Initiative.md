# Initiative

**Location:** `frontend/src/types/project.ts:13`
**Kind:** Interface
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `Initiative` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `owner_id` | `number \| null` | Yes | — | — |
| `owner` | `ProjectOwner \| null` | Yes | — | — |
| `owner_profile_id` | `number \| null` | Yes | — | — |
| `owner_profile` | `ProjectProfileOwner \| null` | Yes | — | — |
| `health` | `ProjectHealth` | Yes | — | — |
| `target_date` | `string \| null` | No | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Initiative (frontend/src/types/project.ts)"]
    n1["InitiativeForm (frontend/src/components/projects/InitiativeForm.tsx)"]
    n2["compareInitiatives (frontend/src/components/projects/projectPortfolio.ts)"]
    n3["groupByInitiative (frontend/src/components/projects/projectPortfolio.ts)"]
    n4["frontend/src/components/projects/RoadmapView.test.tsx"]
    n5["RoadmapView (frontend/src/components/projects/RoadmapView.tsx)"]
    n6["frontend/src/pages/ProjectsPage.tsx"]
    n7["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/InitiativeForm.md"
    click n2 "../modules/projectPortfolio.md"
    click n3 "../modules/projectPortfolio.md"
    click n4 "../modules/RoadmapView.test.md"
    click n5 "../modules/RoadmapView.md"
    click n6 "../modules/ProjectsPage.md"
    click n7 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `created_at`, `description`, `health`, `id`, `name`, `owner`, `owner_id`, `owner_profile`, `owner_profile_id`, `target_date`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `InitiativeForm` | type_reference | [InitiativeForm](../modules/InitiativeForm.md) | — |
| `compareInitiatives` | type_reference | [projectPortfolio](../modules/projectPortfolio.md) | — |
| `groupByInitiative` | type_reference | [projectPortfolio](../modules/projectPortfolio.md) | — |
| `RoadmapView.test` | import | [RoadmapView.test](../modules/RoadmapView.test.md) | — |
| `RoadmapView` | type_reference | [RoadmapView](../modules/RoadmapView.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
