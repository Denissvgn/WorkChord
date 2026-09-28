# TriageTaskDraftRequest

**Location:** `frontend/src/types/triage.ts:114`
**Kind:** Class
**Bases:** —
**Module:** [types_triage](../modules/types_triage.md)

## Description

_Auto-generated from `TriageTaskDraftRequest` in `frontend/src/types/triage.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `template_id` | `number \| null` | No | — | — |
| `classification_suggestion_id` | `number \| null` | No | — | — |
| `current_title` | `string \| null` | No | — | — |
| `current_description` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageTaskDraftRequest (frontend/src/types/triage.ts)"]
    n1["frontend/src/services/triageService.ts"]
    n1 --> n0
    click n0 "../modules/types_triage.md"
    click n1 "../modules/triageService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_triage](../modules/types_triage.md) | 0 | `classification_suggestion_id`, `current_description`, `current_title`, `template_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `triageService` | import | [triageService](../modules/triageService.md) | — |
