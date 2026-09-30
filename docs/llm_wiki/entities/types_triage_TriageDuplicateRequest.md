# TriageDuplicateRequest

**Location:** `frontend/src/types/triage.ts:64`
**Kind:** Class
**Bases:** —
**Module:** [types_triage](../modules/types_triage.md)

## Description

_Auto-generated from `TriageDuplicateRequest` in `frontend/src/types/triage.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `duplicate_of_id` | `number \| null` | No | — | — |
| `duplicate_task_id` | `number \| null` | No | — | — |
| `link_request_to_duplicate_task` | `boolean` | No | — | — |
| `reason` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageDuplicateRequest (frontend/src/types/triage.ts)"]
    n1["frontend/src/pages/TriagePage.tsx"]
    n2["frontend/src/services/triageService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_triage.md"
    click n1 "../modules/TriagePage.md"
    click n2 "../modules/triageService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_triage](../modules/types_triage.md) | 0 | `duplicate_of_id`, `duplicate_task_id`, `link_request_to_duplicate_task`, `reason` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `triageService` | import | [triageService](../modules/triageService.md) | — |
