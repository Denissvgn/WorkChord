# capacityMutations Module

**Path:** `frontend/src/components/capacity/capacityMutations.ts`

## Description

_Auto-generated from `frontend/src/components/capacity/capacityMutations.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/team` | `TeamMember`, `TeamMemberCreate` | Declaration | erased |
| `@tanstack/react-query` | `QueryClient` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `addCapacityRows`, `refreshCapacity` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/capacityMutations.ts"]
    n1["frontend/src/components/capacity/CapacitySection.tsx"]
    n2["frontend/src/components/capacity/PlanQuickAddCapacity.tsx"]
    n3["frontend/src/components/capacity/TeamList.tsx"]
    n4["frontend/src/components/capacity/VacationManager.tsx"]
    n5["frontend/src/services/planningInputService.ts"]
    n6["frontend/src/services/teamService.ts"]
    n7["frontend/src/types/team.ts"]
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n6
    n1 --> n7
    n2 --> n0
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n4 --> n0
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n6 --> n5
    n6 --> n7
    click n0 "../modules/capacityMutations.md"
    click n1 "../modules/CapacitySection.md"
    click n2 "../modules/PlanQuickAddCapacity.md"
    click n3 "../modules/TeamList.md"
    click n4 "../modules/VacationManager.md"
    click n5 "../modules/planningInputService.md"
    click n6 "../modules/teamService.md"
    click n7 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CapacitySection](../modules/CapacitySection.md) |
| Inbound | [PlanQuickAddCapacity](../modules/PlanQuickAddCapacity.md) |
| Inbound | [TeamList](../modules/TeamList.md) |
| Inbound | [VacationManager](../modules/VacationManager.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `refreshCapacity` | `(client: QueryClient)` | — | — |
| `addCapacityRows` | *(async)* `(iterationId: number, candidates: TeamMemberCreate[])` | — | Read revisions separately for each write, since creating a row changes the iteration. |
