# PlanShareTask

**Location:** `frontend/src/services/planShareService.ts:3`
**Kind:** Class
**Bases:** —
**Module:** [planShareService](../modules/planShareService.md)

## Description

_Auto-generated from `PlanShareTask` in `frontend/src/services/planShareService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `priority` | `number` | Yes | — | — |
| `effort_days` | `number \| null` | Yes | — | — |
| `effort_hours` | `number \| null` | Yes | — | — |
| `status` | `string` | Yes | — | — |
| `assignee_name` | `string \| null` | No | — | — |
| `start_date` | `string \| null` | No | — | — |
| `end_date` | `string \| null` | No | — | — |
| `is_optional` | `boolean` | Yes | — | — |
| `is_deferred` | `boolean` | Yes | — | — |
| `tags` | `string[]` | Yes | — | — |
| `dependencies` | `number[]` | Yes | — | — |
| `children` | `PlanShareTask[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanShareTask (frontend/src/services/planShareService.ts)"]
    n1["frontend/src/pages/PlanSharePage.tsx"]
    n1 --> n0
    click n0 "../modules/planShareService.md"
    click n1 "../modules/PlanSharePage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planShareService](../modules/planShareService.md) | 0 | `assignee_name`, `children`, `dependencies`, `effort_days`, `effort_hours`, `end_date`, `id`, `is_deferred`, `is_optional`, `priority`, `start_date`, `status` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanSharePage` | import | [PlanSharePage](../modules/PlanSharePage.md) | — |
