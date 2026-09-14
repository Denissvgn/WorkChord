# TriageClassificationSuggestion

**Location:** `frontend/src/types/triage.ts:91`
**Kind:** Class
**Bases:** —
**Module:** [types_triage](../modules/types_triage.md)

## Description

_Auto-generated from `TriageClassificationSuggestion` in `frontend/src/types/triage.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `triage_item_id` | `number` | *required* | — |
| `suggested_type_label_slug` | `string \| null` | *required* | — |
| `suggested_area_label_slug` | `string \| null` | *required* | — |
| `suggested_priority` | `number \| null` | *required* | — |
| `suggested_label_slugs` | `string[]` | *required* | — |
| `unmatched_label_text` | `string[]` | *required* | — |
| `suggested_assignee_id` | `number \| null` | *required* | — |
| `suggested_assignee_hint` | `string \| null` | *required* | — |
| `suggested_project_id` | `number \| null` | *required* | — |
| `duplicate_candidates` | `Array<Record<string, unknown>>` | *required* | — |
| `confidence` | `number` | *required* | — |
| `rationale` | `string \| null` | *required* | — |
| `language` | `string \| null` | *required* | — |
| `provider` | `string \| null` | *required* | — |
| `model` | `string \| null` | *required* | — |
| `is_fallback` | `boolean` | *required* | — |
| `created_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageClassificationSuggestion (frontend/src/types/triage.ts)"]
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
| [types_triage](../modules/types_triage.md) | 0 | `confidence`, `created_at`, `duplicate_candidates`, `id`, `is_fallback`, `language`, `model`, `provider`, `rationale`, `suggested_area_label_slug`, `suggested_assignee_hint`, `suggested_assignee_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `triageService` | import | [triageService](../modules/triageService.md) | — |
