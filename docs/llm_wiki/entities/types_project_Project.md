# Project

**Location:** `frontend/src/types/project.ts:56`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `Project` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `status` | `ProjectStatus` | Yes | — | — |
| `health` | `ProjectHealth` | Yes | — | — |
| `owner_id` | `number \| null` | Yes | — | — |
| `owner` | `ProjectOwner \| null` | Yes | — | — |
| `owner_profile_id` | `number \| null` | Yes | — | — |
| `owner_profile` | `ProjectProfileOwner \| null` | Yes | — | — |
| `initiative_id` | `number \| null` | No | — | — |
| `initiative` | `ProjectInitiativeSummary \| null` | No | — | — |
| `start_date` | `string \| null` | No | — | — |
| `target_date` | `string \| null` | No | — | — |
| `completed_at` | `string \| null` | No | — | — |
| `sort_order` | `number` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Project (frontend/src/types/project.ts)"]
    n1["ProjectForm (frontend/src/components/projects/ProjectForm.tsx)"]
    n2["frontend/src/pages/ProjectsPage.tsx"]
    n3["frontend/src/pages/RoadmapPage.tsx"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/ProjectsPage.md"
    click n3 "../modules/RoadmapPage.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `completed_at`, `created_at`, `description`, `health`, `id`, `initiative`, `initiative_id`, `name`, `owner`, `owner_id`, `owner_profile`, `owner_profile_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ProjectForm` | type_reference | [ProjectForm](../modules/ProjectForm.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `RoadmapPage` | import | [RoadmapPage](../modules/RoadmapPage.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
