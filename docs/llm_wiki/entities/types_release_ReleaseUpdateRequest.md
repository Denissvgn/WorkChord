# ReleaseUpdateRequest

**Location:** `frontend/src/types/release.ts:39`
**Kind:** Class
**Bases:** —
**Module:** [types_release](../modules/types_release.md)

## Description

_Auto-generated from `ReleaseUpdateRequest` in `frontend/src/types/release.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `status` | `ReleaseStatus` | *required* | — |
| `target_date` | `string \| null` | *required* | — |
| `shipped_at` | `string \| null` | *required* | — |
| `version` | `string \| null` | *required* | — |
| `environment` | `string \| null` | *required* | — |
| `task_ids` | `number[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReleaseUpdateRequest (frontend/src/types/release.ts)"]
    n1["frontend/src/components/releases/ReleaseForm.tsx"]
    n2["frontend/src/services/releaseService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_release.md"
    click n1 "../modules/ReleaseForm.md"
    click n2 "../modules/releaseService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_release](../modules/types_release.md) | 0 | `description`, `environment`, `name`, `shipped_at`, `status`, `target_date`, `task_ids`, `version` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ReleaseForm` | import | [ReleaseForm](../modules/ReleaseForm.md) | — |
| `releaseService` | import | [releaseService](../modules/releaseService.md) | — |
