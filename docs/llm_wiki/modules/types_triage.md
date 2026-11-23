# triage Module

**Path:** `frontend/src/types/triage.ts`

## Description

_Auto-generated from `frontend/src/types/triage.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./task` | `TaskBrief`, `Task` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TriageActionRequest`, `TriageClassificationSuggestion`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestion`, `TriageDuplicateSuggestionsResponse`, `TriageItem`, `TriageItemCreate`, `TriageItemStatus`, `TriageItemUpdate`, `TriageListParams`, `TriageSnoozeRequest`, `TriageTaskDraftRequest`, `TriageTaskDraftResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/triage.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/types_triage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (18) |
| Outbound | `frontend` (1) |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TriageItem](../entities/types_triage_TriageItem.md) | Interface | 6 | — | — |
| [TriageItemCreate](../entities/types_triage_TriageItemCreate.md) | Interface | 30 | — | — |
| [TriageListParams](../entities/TriageListParams.md) | Interface | 46 | — | — |
| [TriageActionRequest](../entities/types_triage_TriageActionRequest.md) | Interface | 55 | — | — |
| [TriageSnoozeRequest](../entities/types_triage_TriageSnoozeRequest.md) | Interface | 59 | — | — |
| [TriageDuplicateRequest](../entities/types_triage_TriageDuplicateRequest.md) | Interface | 64 | — | — |
| [TriageDuplicateSuggestion](../entities/types_triage_TriageDuplicateSuggestion.md) | Interface | 71 | — | — |
| [TriageDuplicateSuggestionsResponse](../entities/types_triage_TriageDuplicateSuggestionsResponse.md) | Interface | 87 | — | — |
| [TriageClassificationSuggestion](../entities/types_triage_TriageClassificationSuggestion.md) | Interface | 93 | — | — |
| [TriageTaskDraftRequest](../entities/types_triage_TriageTaskDraftRequest.md) | Interface | 114 | — | — |
| [TriageTaskDraftResponse](../entities/types_triage_TriageTaskDraftResponse.md) | Interface | 121 | — | — |
| [TriageConvertToTaskRequest](../entities/types_triage_TriageConvertToTaskRequest.md) | Interface | 145 | — | — |
| [TriageConvertToTaskResponse](../entities/types_triage_TriageConvertToTaskResponse.md) | Interface | 160 | — | — |
| [TriageItemStatus](../entities/types_triage_TriageItemStatus.md) | Type alias | 4 | `'new' \| 'accepted' \| 'declined' \| 'duplicate' \| 'snoozed' \| 'converted'` | — |
| [TriageItemUpdate](../entities/types_triage_TriageItemUpdate.md) | Type alias | 44 | `Partial<TriageItemCreate>` | — |
