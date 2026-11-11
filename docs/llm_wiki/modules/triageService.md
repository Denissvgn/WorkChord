# triageService Module

**Path:** `frontend/src/services/triageService.ts`

## Description

_Auto-generated from `frontend/src/services/triageService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/team` | `AssigneeRecommendation` | Declaration | erased |
| `../types/triage` | `TriageActionRequest`, `TriageClassificationSuggestion`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestionsResponse`, `TriageItem`, `TriageItemCreate`, `TriageItemUpdate`, `TriageListParams`, `TriageSnoozeRequest`, `TriageTaskDraftRequest`, `TriageTaskDraftResponse` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendTriageService`, `triageService` |
| Constants | `triageService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/components/tasks/QuickCapture.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/team/AssigneeRecommendationsPanel.tsx"]
    n4["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n5["frontend/src/pages/TriagePage.tsx"]
    n6["frontend/src/services/api.ts"]
    n7["frontend/src/services/triageService.ts"]
    n8["frontend/src/types/team.ts"]
    n9["frontend/src/types/triage.ts"]
    n0 --> n7
    n1 --> n7
    n1 --> n9
    n2 --> n3
    n2 --> n7
    n2 --> n9
    n3 --> n7
    n4 --> n7
    n4 --> n8
    n5 --> n1
    n5 --> n3
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n7 --> n6
    n7 --> n8
    n7 --> n9
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/QuickCapture.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/AssigneeRecommendationsPanel.md"
    click n4 "../modules/usePlanningReadiness.md"
    click n5 "../modules/TriagePage.md"
    click n6 "../modules/api.md"
    click n7 "../modules/triageService.md"
    click n8 "../modules/types_team.md"
    click n9 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [QuickCapture](../modules/QuickCapture.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [AssigneeRecommendationsPanel](../modules/AssigneeRecommendationsPanel.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [types_triage](../modules/types_triage.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendTriageService](../entities/FrontendTriageService.md) | Interface | 47 | — | — |
