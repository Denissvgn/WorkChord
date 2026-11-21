# usePlanScheduleWorkloads Module

**Path:** `frontend/src/features/planningMasters/usePlanScheduleWorkloads.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanScheduleWorkloads.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `usePlanScheduleWorkloads` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanReviewSection.tsx"]
    n1["frontend/src/components/planning/PlanScheduleSection.tsx"]
    n2["frontend/src/features/planningMasters/usePlanScheduleWorkloads.ts"]
    n3["frontend/src/services/teamService.ts"]
    n4["frontend/src/types/team.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n2
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n3 --> n4
    click n0 "../modules/PlanReviewSection.md"
    click n1 "../modules/PlanScheduleSection.md"
    click n2 "../modules/usePlanScheduleWorkloads.md"
    click n3 "../modules/teamService.md"
    click n4 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanReviewSection](../modules/PlanReviewSection.md) |
| Inbound | [PlanScheduleSection](../modules/PlanScheduleSection.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `usePlanScheduleWorkloads` | `(iterationId: number, members: TeamMember[])` | — | — |
