# TriageItem

**Location:** `frontend/src/types/triage.ts:6`
**Kind:** Class
**Bases:** —
**Module:** [types_triage](../modules/types_triage.md)

## Description

_Auto-generated from `TriageItem` in `frontend/src/types/triage.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `brief` | `TaskBrief \| null` | No | — | — |
| `id` | `number` | Yes | — | — |
| `title` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `source` | `string \| null` | No | — | — |
| `source_url` | `string \| null` | No | — | — |
| `external_key` | `string \| null` | No | — | — |
| `status` | `TriageItemStatus` | Yes | — | — |
| `priority_hint` | `number \| null` | No | — | — |
| `assignee_hint` | `string \| null` | No | — | — |
| `project_hint_id` | `number \| null` | No | — | — |
| `iteration_hint_id` | `number \| null` | No | — | — |
| `labels` | `string[]` | Yes | — | — |
| `metadata_json` | `Record<string, unknown>` | Yes | — | — |
| `snoozed_until` | `string \| null` | No | — | — |
| `duplicate_of_id` | `number \| null` | No | — | — |
| `duplicate_task_id` | `number \| null` | No | — | — |
| `converted_task_id` | `number \| null` | No | — | — |
| `request_count` | `number` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItem (frontend/src/types/triage.ts)"]
    n1["frontend/src/pages/TriagePage.tsx"]
    n2["frontend/src/services/triageService.ts"]
    n3["frontend/src/types/task.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_triage.md"
    click n1 "../modules/TriagePage.md"
    click n2 "../modules/triageService.md"
    click n3 "../modules/types_task.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_triage](../modules/types_triage.md) | 0 | `assignee_hint`, `brief`, `converted_task_id`, `created_at`, `description`, `duplicate_of_id`, `duplicate_task_id`, `external_key`, `id`, `iteration_hint_id`, `labels`, `metadata_json` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `triageService` | import | [triageService](../modules/triageService.md) | — |
| `task` | import | [types_task](../modules/types_task.md) | — |
