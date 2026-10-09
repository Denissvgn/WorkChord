# PlanningInputBoundary Module

**Path:** `frontend/src/components/planning/PlanningInputBoundary.tsx`

## Description

Existing planning editors start from one coherent server resource and complete revision map. Explicit comparison retains user input; explicit reload starts a new editor generation. Scope and permission failures remain visible, and denied observations remove server data. Pending editors disable comparison controls.

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/usePlanningObservation` | `usePlanningObservation` |
| `../../services/planningInputService` | `MemberPlanningIntent`, `ObservedPlanningInput`, `PlanningInputKind` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `react` | `useEffect`, `useState`, `ReactNode` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanningInputBoundary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/iteration/IterationForm.tsx"]
    n3["frontend/src/components/planning/PlanningInputBoundary.test.tsx"]
    n4["frontend/src/components/planning/PlanningInputBoundary.tsx"]
    n5["frontend/src/components/projects/ProjectForm.tsx"]
    n6["frontend/src/components/team/TeamForm.tsx"]
    n7["frontend/src/components/team/VacationManager.tsx"]
    n8["frontend/src/features/usePlanningObservation.ts"]
    n9["frontend/src/services/planningInputService.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n4
    n2 --> n9
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n8
    n4 --> n9
    n5 --> n0
    n5 --> n1
    n5 --> n4
    n5 --> n9
    n6 --> n0
    n6 --> n1
    n6 --> n4
    n6 --> n9
    n7 --> n0
    n7 --> n4
    n7 --> n9
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/IterationForm.md"
    click n3 "../modules/PlanningInputBoundary.test.md"
    click n4 "../modules/PlanningInputBoundary.md"
    click n5 "../modules/ProjectForm.md"
    click n6 "../modules/TeamForm.md"
    click n7 "../modules/VacationManager.md"
    click n8 "../modules/usePlanningObservation.md"
    click n9 "../modules/planningInputService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationForm](../modules/IterationForm.md) |
| Inbound | [PlanningInputBoundary.test](../modules/PlanningInputBoundary.test.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TeamForm](../modules/TeamForm.md) |
| Inbound | [VacationManager](../modules/VacationManager.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [usePlanningObservation](../modules/usePlanningObservation.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanningInputBoundary` | `({ kind, resourceId, creatingMember = false, getIntent, onCancel, children }: {     kind: PlanningInputKind; resourceId: number; creatingMember?: boolean;     onCancel?: () => void;     getIntent?: () => MemberPlanningIntent;     children: (observation: ObservedPlanningInput<T>, controls: ReactNode, onSaved: () => void) => ReactNode; })` | — | — |
