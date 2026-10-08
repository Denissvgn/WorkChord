# VacationCsvImport Module

**Path:** `frontend/src/components/team/VacationCsvImport.tsx`

## Description

Vacation CSV selection opens a bounded shared-person scope preview. Import sends the retained file text and map; scope conflicts preserve the preview, and partial-success errors remain visible.

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/usePlanningObservation` | `usePlanningObservation` |
| `../../services/planningInputService` | `ObservedRevisions` |
| `../../services/teamService` | `teamService` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../tasks/useDraftDismissal` | `useActiveMount` |
| `@tanstack/react-query` | `useMutation` |
| `react` | `useEffect`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `VacationCsvImport` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/useDraftDismissal.ts"]
    n2["frontend/src/components/team/VacationCsvImport.tsx"]
    n3["frontend/src/components/team/VacationManager.tsx"]
    n4["frontend/src/features/usePlanningObservation.ts"]
    n5["frontend/src/pages/CalendarPage.tsx"]
    n6["frontend/src/services/planningInputService.ts"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n0
    n3 --> n2
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n6
    n4 --> n8
    n5 --> n0
    n5 --> n2
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n7 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/useDraftDismissal.md"
    click n2 "../modules/VacationCsvImport.md"
    click n3 "../modules/VacationManager.md"
    click n4 "../modules/usePlanningObservation.md"
    click n5 "../modules/CalendarPage.md"
    click n6 "../modules/planningInputService.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [VacationManager](../modules/VacationManager.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [usePlanningObservation](../modules/usePlanningObservation.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `VacationCsvImport` | `({ iterationId, onSuccess, onBusyChange }: { iterationId: number; onSuccess: () => void; onBusyChange?: (busy: boolean) => void })` | — | — |
