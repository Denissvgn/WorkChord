# Release

**Location:** `frontend/src/types/release.ts:13`
**Kind:** Class
**Bases:** `WorkMetrics`
**Module:** [types_release](../modules/types_release.md)

## Description

_Auto-generated from `Release` in `frontend/src/types/release.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `project_id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `status` | `ReleaseStatus` | Yes | — | — |
| `target_date` | `string \| null` | No | — | — |
| `shipped_at` | `string \| null` | No | — | — |
| `version` | `string \| null` | No | — | — |
| `environment` | `string \| null` | No | — | — |
| `task_ids` | `number[]` | Yes | — | — |
| `tasks` | `ReleaseTaskSummary[]` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Release (frontend/src/types/release.ts)"]
    n1["WorkMetrics (frontend/src/types/workMetrics.ts)"]
    n2["ReleaseForm (frontend/src/components/releases/ReleaseForm.tsx)"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n5["frontend/src/services/releaseService.ts"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_release.md"
    click n1 "../modules/workMetrics.md"
    click n2 "../modules/ReleaseForm.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectReleaseDetailPage.md"
    click n5 "../modules/releaseService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_release](../modules/types_release.md) | 0 | `created_at`, `description`, `environment`, `id`, `name`, `project_id`, `shipped_at`, `status`, `target_date`, `task_ids`, `tasks`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `WorkMetrics` | [workMetrics](../modules/workMetrics.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ReleaseForm` | type_reference | [ReleaseForm](../modules/ReleaseForm.md) | — |
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
| `ProjectReleaseDetailPage` | import | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) | — |
| `releaseService` | import | [releaseService](../modules/releaseService.md) | — |
