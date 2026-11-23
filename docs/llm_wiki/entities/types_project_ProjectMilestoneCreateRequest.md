# ProjectMilestoneCreateRequest

**Location:** `frontend/src/types/project.ts:143`
**Kind:** Interface
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectMilestoneCreateRequest` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `target_date` | `string \| null` | No | — | — |
| `completed_at` | `string \| null` | No | — | — |
| `sort_order` | `number` | No | — | — |
| `status` | `ProjectMilestoneStatus` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMilestoneCreateRequest (frontend/src/types/project.ts)"]
    n1["buildMilestonePayload (frontend/src/components/projects/projectDetailShared.ts)"]
    n2["frontend/src/pages/ProjectDetailPage.tsx"]
    n3["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/projectDetailShared.md"
    click n2 "../modules/ProjectDetailPage.md"
    click n3 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `completed_at`, `description`, `name`, `sort_order`, `status`, `target_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `buildMilestonePayload` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
