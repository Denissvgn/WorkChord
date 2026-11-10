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
    n0["frontend/src/components/tasks/TaskForm.tsx"]
    n1["frontend/src/pages/TriagePage.tsx"]
    n2["frontend/src/services/triageService.ts"]
    n3["frontend/src/types/task.ts"]
    n4["frontend/src/types/triage.ts"]
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n4
    n3 --> n4
    n4 --> n3
    click n0 "../modules/TaskForm.md"
    click n1 "../modules/TriagePage.md"
    click n2 "../modules/triageService.md"
    click n3 "../modules/types_task.md"
    click n4 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Inbound | [triageService](../modules/triageService.md) |
| Inbound | [types_task](../modules/types_task.md) |
| Outbound | [types_task](../modules/types_task.md) |

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
