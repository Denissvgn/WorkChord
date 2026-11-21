# ProjectUpdateEntry

**Location:** `frontend/src/types/project.ts:103`
**Kind:** Interface
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectUpdateEntry` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `project_id` | `number` | Yes | — | — |
| `health` | `ProjectHealth` | Yes | — | — |
| `summary` | `string` | Yes | — | — |
| `progress_text` | `string \| null` | No | — | — |
| `risks_text` | `string \| null` | No | — | — |
| `decisions_text` | `string \| null` | No | — | — |
| `next_steps_text` | `string \| null` | No | — | — |
| `created_by_session_id` | `number \| null` | No | — | — |
| `created_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectUpdateEntry (frontend/src/types/project.ts)"]
    n1["updateDetailFields (frontend/src/components/projects/projectDetailShared.ts)"]
    n2["ProjectSummaryTab (frontend/src/components/projects/ProjectSummaryTab.tsx)"]
    n3["ProjectUpdatesTab (frontend/src/components/projects/ProjectUpdatesTab.tsx)"]
    n4["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/projectDetailShared.md"
    click n2 "../modules/ProjectSummaryTab.md"
    click n3 "../modules/ProjectUpdatesTab.md"
    click n4 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `created_at`, `created_by_session_id`, `decisions_text`, `health`, `id`, `next_steps_text`, `progress_text`, `project_id`, `risks_text`, `summary` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `updateDetailFields` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `ProjectSummaryTab` | type_reference | [ProjectSummaryTab](../modules/ProjectSummaryTab.md) | — |
| `ProjectUpdatesTab` | type_reference | [ProjectUpdatesTab](../modules/ProjectUpdatesTab.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
