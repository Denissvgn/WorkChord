# IterationSeriesCreate

**Location:** `frontend/src/types/iteration.ts:42`
**Kind:** Class
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `IterationSeriesCreate` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `base_name` | `string` | *required* | — |
| `calendar_id` | `number \| null` | *required* | — |
| `project_id` | `number \| null` | *required* | — |
| `start_date` | `string` | *required* | — |
| `duration_days` | `number` | *required* | — |
| `stop` | `IterationSeriesStop` | *required* | — |
| `manager_email` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationSeriesCreate (frontend/src/types/iteration.ts)"]
    n1["frontend/src/components/iteration/IterationForm.tsx"]
    n2["frontend/src/services/iterationService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/IterationForm.md"
    click n2 "../modules/iterationService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `base_name`, `calendar_id`, `duration_days`, `manager_email`, `project_id`, `start_date`, `stop` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationForm` | import | [IterationForm](../modules/IterationForm.md) | — |
| `iterationService` | import | [iterationService](../modules/iterationService.md) | — |
