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
| Exports | `ObservedPlanningInput`, `PlanningInputKind`, `planningInputService` |
| Constants | `planningInputService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/services/api.ts"]
    n1["frontend/src/services/planningInputService.test.ts"]
    n2["frontend/src/services/planningInputService.ts"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/api.md"
    click n1 "../modules/planningInputService.test.md"
    click n2 "../modules/planningInputService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [planningInputService.test](../modules/planningInputService.test.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ObservedPlanningInput](../entities/ObservedPlanningInput.md) | Class | 4 | — | — |
| [PlanningInputKind](../entities/PlanningInputKind.md) | Type alias | 3 | — | — |
