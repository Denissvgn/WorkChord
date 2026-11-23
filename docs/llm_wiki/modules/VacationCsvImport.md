# VacationCsvImport Module

**Path:** `frontend/src/components/team/VacationCsvImport.tsx`

## Description

Vacation CSV selection opens a bounded shared-person scope preview. Import sends the retained file text and map; scope conflicts preserve the preview, and partial-success errors remain visible.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedRevisions` | Declaration | erased |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/buttonStyles` | `buttonClassName` | — | compiler-dependent |
| `../tasks/useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `VacationCsvImport` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/CapacitySection.tsx"]
    n1["frontend/src/components/common/Button.tsx"]
    n2["frontend/src/components/common/buttonStyles.ts"]
    n3["frontend/src/components/tasks/useDraftDismissal.ts"]
    n4["frontend/src/components/team/VacationCsvImport.tsx"]
    n5["frontend/src/features/usePlanningObservation.ts"]
    n6["frontend/src/services/planningInputService.ts"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n0 --> n1
    n0 --> n4
    n0 --> n7
    n0 --> n8
    n1 --> n2
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n5 --> n6
    n5 --> n8
    n7 --> n6
    click n0 "../modules/CapacitySection.md"
    click n1 "../modules/Button.md"
    click n2 "../modules/buttonStyles.md"
    click n3 "../modules/useDraftDismissal.md"
    click n4 "../modules/VacationCsvImport.md"
    click n5 "../modules/usePlanningObservation.md"
    click n6 "../modules/planningInputService.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CapacitySection](../modules/CapacitySection.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [buttonStyles](../modules/buttonStyles.md) |
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