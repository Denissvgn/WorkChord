# usePlanningObservation Module

**Path:** `frontend/src/features/usePlanningObservation.ts`

## Description

Editor observations are retained with drafts. Only explicit conflict reapply reads or successful writes advance them; obsolete reads are ignored. The hook separates context loading from user input.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../services/planningInputService` | `ObservedPlanningInput`, `PlanningInputKind`, `MemberPlanningIntent` | Specifier | compiler-dependent |
| `../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../utils/apiError` | `getApiErrorStatus` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `usePlanningObservation` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanningInputBoundary.tsx"]
    n1["frontend/src/components/projects/ProjectIterationsSection.tsx"]
    n2["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n5["frontend/src/components/team/ImportTeamModal.tsx"]
    n6["frontend/src/components/team/TeamProfileManager.tsx"]
    n7["frontend/src/components/team/VacationCsvImport.tsx"]
    n8["frontend/src/features/usePlanningObservation.ts"]
    n9["frontend/src/services/planningInputService.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n0 --> n8
    n0 --> n9
    n1 --> n8
    n1 --> n9
    n1 --> n10
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n3 --> n4
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n8
    n5 --> n10
    n6 --> n8
    n6 --> n9
    n6 --> n10
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n8 --> n9
    n8 --> n10
    click n0 "../modules/PlanningInputBoundary.md"
    click n1 "../modules/ProjectIterationsSection.md"
    click n2 "../modules/WorkCalendarSettings.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/TaskWorkPanel.md"
    click n5 "../modules/ImportTeamModal.md"
    click n6 "../modules/TeamProfileManager.md"
    click n7 "../modules/VacationCsvImport.md"
    click n8 "../modules/usePlanningObservation.md"
    click n9 "../modules/planningInputService.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) |
| Inbound | [ProjectIterationsSection](../modules/ProjectIterationsSection.md) |
| Inbound | [WorkCalendarSettings](../modules/WorkCalendarSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Inbound | [ImportTeamModal](../modules/ImportTeamModal.md) |
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Inbound | [VacationCsvImport](../modules/VacationCsvImport.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `usePlanningObservation` | `<T>()` | — | — |
