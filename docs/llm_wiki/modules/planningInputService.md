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
| Exports | `MemberPlanningIntent`, `ObservedPlanningInput`, `ObservedRevisions`, `PlanningInputKind`, `planningInputService`, `revisionHeaders` |
| Constants | `planningInputService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/services/planningInputService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/planningInputService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (20) |
| Outbound | `frontend` (1) |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ObservedPlanningInput](../entities/ObservedPlanningInput.md) | Class | 4 | — | — |
| [PlanningInputKind](../entities/PlanningInputKind.md) | Type alias | 3 | — | — |
| [MemberPlanningIntent](../entities/planningInputService_MemberPlanningIntent.md) | Type alias | 12 | — | — |
| [ObservedRevisions](../entities/ObservedRevisions.md) | Type alias | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `revisionHeaders` | `(revisions: ObservedRevisions)` | — | — |