# planningInputService Module

**Path:** `frontend/src/services/planningInputService.ts`

## Description

Reads one resource and its complete revision map before a planning draft opens. The caller retains this observation for the eventual write; this utility does not refresh revisions at save time or silently recover authorization and incomplete-scope failures.

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ObservedPlanningInput`, `ObservedRevisions`, `PlanningInputKind`, `planningInputService`, `revisionHeaders` |
| Constants | `planningInputService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/team/TeamProfileManager.tsx"]
    n1["frontend/src/features/usePlanningObservation.ts"]
    n2["frontend/src/pages/CalendarPage.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/calendarService.ts"]
    n5["frontend/src/services/planningInputService.test.ts"]
    n6["frontend/src/services/planningInputService.ts"]
    n7["frontend/src/services/teamService.ts"]
    n0 --> n1
    n0 --> n6
    n0 --> n7
    n1 --> n6
    n2 --> n1
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n4 --> n3
    n4 --> n6
    n5 --> n3
    n5 --> n6
    n6 --> n3
    n7 --> n3
    n7 --> n6
    click n0 "../modules/TeamProfileManager.md"
    click n1 "../modules/usePlanningObservation.md"
    click n2 "../modules/CalendarPage.md"
    click n3 "../modules/api.md"
    click n4 "../modules/calendarService.md"
    click n5 "../modules/planningInputService.test.md"
    click n6 "../modules/planningInputService.md"
    click n7 "../modules/teamService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Inbound | [usePlanningObservation](../modules/usePlanningObservation.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Inbound | [calendarService](../modules/calendarService.md) |
| Inbound | [planningInputService.test](../modules/planningInputService.test.md) |
| Inbound | [teamService](../modules/teamService.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ObservedPlanningInput](../entities/ObservedPlanningInput.md) | Class | 4 | — | — |
| [PlanningInputKind](../entities/PlanningInputKind.md) | Type alias | 3 | — | — |
| [ObservedRevisions](../entities/ObservedRevisions.md) | Type alias | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `revisionHeaders` | `(revisions: ObservedRevisions)` | — | — |