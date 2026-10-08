# usePlanningObservation Module

**Path:** `frontend/src/features/usePlanningObservation.ts`

## Description

Editor observations are retained with drafts. Only explicit conflict reapply reads or successful writes advance them; obsolete reads are ignored. The hook separates context loading from user input.

## Imports

| Source | Symbols |
|--------|---------|
| `../services/planningInputService` | `planningInputService`, `ObservedPlanningInput`, `PlanningInputKind`, `MemberPlanningIntent` |
| `../utils/apiError` | `getApiErrorStatus` |
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `usePlanningObservation` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanningInputBoundary.tsx"]
    n1["frontend/src/components/projects/ProjectIterationsSection.tsx"]
    n2["frontend/src/components/team/ImportTeamModal.tsx"]
    n3["frontend/src/components/team/TeamProfileManager.tsx"]
    n4["frontend/src/components/team/VacationCsvImport.tsx"]
    n5["frontend/src/features/usePlanningObservation.ts"]
    n6["frontend/src/pages/CalendarPage.tsx"]
    n7["frontend/src/services/planningInputService.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n0 --> n5
    n0 --> n7
    n1 --> n5
    n1 --> n7
    n1 --> n8
    n2 --> n5
    n2 --> n8
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n4 --> n5
    n4 --> n7
    n4 --> n8
    n5 --> n7
    n5 --> n8
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    click n0 "../modules/PlanningInputBoundary.md"
    click n1 "../modules/ProjectIterationsSection.md"
    click n2 "../modules/ImportTeamModal.md"
    click n3 "../modules/TeamProfileManager.md"
    click n4 "../modules/VacationCsvImport.md"
    click n5 "../modules/usePlanningObservation.md"
    click n6 "../modules/CalendarPage.md"
    click n7 "../modules/planningInputService.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) |
| Inbound | [ProjectIterationsSection](../modules/ProjectIterationsSection.md) |
| Inbound | [ImportTeamModal](../modules/ImportTeamModal.md) |
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Inbound | [VacationCsvImport](../modules/VacationCsvImport.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `usePlanningObservation` | `()` | — | — |