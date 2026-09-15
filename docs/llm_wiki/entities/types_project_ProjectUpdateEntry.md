# ProjectUpdateEntry

**Location:** `frontend/src/types/project.ts:103`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectUpdateEntry` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `project_id` | `number` | *required* | — |
| `health` | `ProjectHealth` | *required* | — |
| `summary` | `string` | *required* | — |
| `progress_text` | `string \| null` | *required* | — |
| `risks_text` | `string \| null` | *required* | — |
| `decisions_text` | `string \| null` | *required* | — |
| `next_steps_text` | `string \| null` | *required* | — |
| `created_by_session_id` | `number \| null` | *required* | — |
| `created_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectUpdateEntry (frontend/src/types/project.ts)"]
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
| [types_project](../modules/types_project.md) | 0 | `created_at`, `created_by_session_id`, `decisions_text`, `health`, `id`, `next_steps_text`, `progress_text`, `project_id`, `risks_text`, `summary` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
