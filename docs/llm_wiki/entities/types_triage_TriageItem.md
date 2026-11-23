# TriageItem

**Location:** `frontend/src/types/triage.ts:6`
**Kind:** Interface
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

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageItem (frontend/src/types/triage.ts)"]
    n1["frontend/src/components/tasks/QuickCapture.tsx"]
    n2["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n3["frontend/src/components/triage/TriageActionModal.tsx"]
    n4["TriageConvertSource (frontend/src/components/triage/TriageConvertSource.tsx)"]
    n5["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n6["frontend/src/components/triage/TriageList.test.tsx"]
    n7["TriageList (frontend/src/components/triage/TriageList.tsx)"]
    n8["frontend/src/components/triage/TriageRow.tsx"]
    n9["isDueSnoozed (frontend/src/components/triage/triageUtils.ts)"]
    n10["statusClassName (frontend/src/components/triage/triageUtils.ts)"]
    n11["frontend/src/pages/TriagePage.test.tsx"]
    n12["frontend/src/pages/TriagePage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/types_triage.md"
    click n1 "../modules/QuickCapture.md"
    click n2 "../modules/ConvertTriageDrawer.md"
    click n3 "../modules/TriageActionModal.md"
    click n4 "../modules/TriageConvertSource.md"
    click n5 "../modules/TriageDetailPanel.md"
    click n6 "../modules/TriageList.test.md"
    click n7 "../modules/TriageList.md"
    click n8 "../modules/TriageRow.md"
    click n9 "../modules/triageUtils.md"
    click n10 "../modules/triageUtils.md"
    click n11 "../modules/TriagePage.test.md"
    click n12 "../modules/TriagePage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_triage](../modules/types_triage.md) | 0 | `assignee_hint`, `brief`, `converted_task_id`, `created_at`, `description`, `duplicate_of_id`, `duplicate_task_id`, `external_key`, `id`, `iteration_hint_id`, `labels`, `metadata_json` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `QuickCapture` | import | [QuickCapture](../modules/QuickCapture.md) | — |
| `ConvertTriageDrawer` | import | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) | — |
| `TriageActionModal` | import | [TriageActionModal](../modules/TriageActionModal.md) | — |
| `TriageConvertSource` | type_reference | [TriageConvertSource](../modules/TriageConvertSource.md) | — |
| `TriageDetailPanel` | import | [TriageDetailPanel](../modules/TriageDetailPanel.md) | — |
| `TriageList.test` | import | [TriageList.test](../modules/TriageList.test.md) | — |
| `TriageList` | type_reference | [TriageList](../modules/TriageList.md) | — |
| `TriageRow` | import | [TriageRow](../modules/TriageRow.md) | — |
| `isDueSnoozed` | type_reference | [triageUtils](../modules/triageUtils.md) | — |
| `statusClassName` | type_reference | [triageUtils](../modules/triageUtils.md) | — |
| `TriagePage.test` | import | [TriagePage.test](../modules/TriagePage.test.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
