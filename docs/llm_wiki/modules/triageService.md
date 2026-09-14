# triageService Module

**Path:** `frontend/src/services/triageService.ts`

## Description

_Auto-generated from `frontend/src/services/triageService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/team` | `AssigneeRecommendation` |
| `../types/triage` | `TriageActionRequest`, `TriageClassificationSuggestion`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestionsResponse`, `TriageItem`, `TriageItemCreate`, `TriageItemUpdate`, `TriageListParams`, `TriageSnoozeRequest`, `TriageTaskDraftRequest`, `TriageTaskDraftResponse` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendTriageService`, `triageService` |
| Constants | `triageService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/components/tasks/TaskForm.tsx"]
    n2["frontend/src/components/team/AssigneeRecommendationsPanel.tsx"]
    n3["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/services/triageService.ts"]
    n7["frontend/src/types/team.ts"]
    n8["frontend/src/types/triage.ts"]
    n0 --> n6
    n1 --> n2
    n1 --> n6
    n1 --> n8
    n2 --> n6
    n3 --> n6
    n3 --> n7
    n4 --> n2
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n6 --> n5
    n6 --> n7
    n6 --> n8
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/TaskForm.md"
    click n2 "../modules/AssigneeRecommendationsPanel.md"
    click n3 "../modules/usePlanningReadiness.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/api.md"
    click n6 "../modules/triageService.md"
    click n7 "../modules/types_team.md"
    click n8 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
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
| [FrontendTriageService](../entities/FrontendTriageService.md) | Class | 47 | — | — |
