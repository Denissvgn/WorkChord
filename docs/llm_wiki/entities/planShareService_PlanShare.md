# PlanShare

**Location:** `frontend/src/services/planShareService.ts:41`
**Kind:** Class
**Bases:** —
**Module:** [planShareService](../modules/planShareService.md)

## Description

_Auto-generated from `PlanShare` in `frontend/src/services/planShareService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `public_id` | `string` | Yes | — | — |
| `iteration_id` | `number` | Yes | — | — |
| `iteration_name` | `string` | Yes | — | — |
| `created_by_display` | `string` | Yes | — | — |
| `snapshot_data` | `PlanShareSnapshot` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `revoked_at` | `string \| null` | No | — | — |

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
