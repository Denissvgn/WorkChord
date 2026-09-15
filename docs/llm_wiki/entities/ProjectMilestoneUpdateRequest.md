# ProjectMilestoneUpdateRequest

**Location:** `frontend/src/types/project.ts:152`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectMilestoneUpdateRequest` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `target_date` | `string \| null` | *required* | — |
| `completed_at` | `string \| null` | *required* | — |
| `sort_order` | `number` | *required* | — |
| `status` | `ProjectMilestoneStatus` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMilestoneUpdateRequest (frontend/src/types/project.ts)"]
    n1["frontend/src/pages/ProjectDetailPage.tsx"]
    n2["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/ProjectDetailPage.md"
    click n2 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `completed_at`, `description`, `name`, `sort_order`, `status`, `target_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
