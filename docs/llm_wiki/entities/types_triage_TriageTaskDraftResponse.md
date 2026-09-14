# TriageTaskDraftResponse

**Location:** `frontend/src/types/triage.ts:119`
**Kind:** Class
**Bases:** —
**Module:** [types_triage](../modules/types_triage.md)

## Description

_Auto-generated from `TriageTaskDraftResponse` in `frontend/src/types/triage.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `triage_item_id` | `number` | *required* | — |
| `suggested_title` | `string` | *required* | — |
| `suggested_description` | `string` | *required* | — |
| `suggested_checklist` | `string[]` | *required* | — |
| `acceptance_criteria` | `string[]` | *required* | — |
| `risks` | `string[]` | *required* | — |
| `template_id` | `number \| null` | *required* | — |
| `classification_suggestion_id` | `number \| null` | *required* | — |
| `is_fallback` | `boolean` | *required* | — |
| `provider` | `string \| null` | *required* | — |
| `model` | `string \| null` | *required* | — |
| `language` | `'en' \| 'ru'` | *required* | — |
| `finish_reason` | `string \| null` | *required* | — |
| `is_truncated` | `boolean` | *required* | — |
| `grounded_facts` | `Array<{ claim: string; source: string }>` | *required* | — |
| `implementation_notes` | `string[]` | *required* | — |
| `open_questions` | `string[]` | *required* | — |
| `ungrounded_suggestions` | `string[]` | *required* | — |
| `warnings` | `string[]` | *required* | — |
| `rationale` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageTaskDraftResponse (frontend/src/types/triage.ts)"]
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
| [types_triage](../modules/types_triage.md) | 0 | `acceptance_criteria`, `classification_suggestion_id`, `finish_reason`, `grounded_facts`, `implementation_notes`, `is_fallback`, `is_truncated`, `language`, `model`, `open_questions`, `provider`, `rationale` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `triageService` | import | [triageService](../modules/triageService.md) | — |
