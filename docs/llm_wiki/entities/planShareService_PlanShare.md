# PlanShare

**Location:** `frontend/src/services/planShareService.ts:41`
**Kind:** Class
**Bases:** —
**Module:** [planShareService](../modules/planShareService.md)

## Description

_Auto-generated from `PlanShare` in `frontend/src/services/planShareService.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `public_id` | `string` | *required* | — |
| `iteration_id` | `number` | *required* | — |
| `iteration_name` | `string` | *required* | — |
| `created_by_display` | `string` | *required* | — |
| `snapshot_data` | `PlanShareSnapshot` | *required* | — |
| `created_at` | `string` | *required* | — |
| `revoked_at` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanShare (frontend/src/services/planShareService.ts)"]
    n1["frontend/src/pages/PlanMasterPage.tsx"]
    n1 --> n0
    click n0 "../modules/planShareService.md"
    click n1 "../modules/PlanMasterPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planShareService](../modules/planShareService.md) | 0 | `created_at`, `created_by_display`, `id`, `iteration_id`, `iteration_name`, `public_id`, `revoked_at`, `snapshot_data` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanMasterPage` | import | [PlanMasterPage](../modules/PlanMasterPage.md) | — |
