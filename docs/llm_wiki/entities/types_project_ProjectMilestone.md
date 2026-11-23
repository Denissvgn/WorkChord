# ProjectMilestone

**Location:** `frontend/src/types/project.ts:125`
**Kind:** Interface
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectMilestone` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `project_id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `target_date` | `string \| null` | No | — | — |
| `completed_at` | `string \| null` | No | — | — |
| `sort_order` | `number` | Yes | — | — |
| `status` | `ProjectMilestoneStatus` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMilestone (frontend/src/types/project.ts)"]
    n1["frontend/src/components/projects/AddMilestoneModal.tsx"]
    n2["MilestonesSection (frontend/src/components/projects/MilestonesSection.tsx)"]
    n3["buildMilestonePayload (frontend/src/components/projects/projectDetailShared.ts)"]
    n4["createMilestoneFormFromRecord (frontend/src/components/projects/projectDetailShared.ts)"]
    n5["frontend/src/components/projects/RoadmapView.tsx"]
    n6["frontend/src/pages/ProjectDetailPage.tsx"]
    n7["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/AddMilestoneModal.md"
    click n2 "../modules/MilestonesSection.md"
    click n3 "../modules/projectDetailShared.md"
    click n4 "../modules/projectDetailShared.md"
    click n5 "../modules/RoadmapView.md"
    click n6 "../modules/ProjectDetailPage.md"
    click n7 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `completed_at`, `created_at`, `description`, `id`, `name`, `project_id`, `sort_order`, `status`, `target_date`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AddMilestoneModal` | import | [AddMilestoneModal](../modules/AddMilestoneModal.md) | — |
| `MilestonesSection` | type_reference | [MilestonesSection](../modules/MilestonesSection.md) | — |
| `buildMilestonePayload` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `createMilestoneFormFromRecord` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `RoadmapView` | import | [RoadmapView](../modules/RoadmapView.md) | — |
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
