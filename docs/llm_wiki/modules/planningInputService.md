# planningInputService Module

**Path:** `frontend/src/services/planningInputService.ts`

## Description

Reads one resource and its complete revision map before a planning draft opens. The caller retains this observation for the eventual write; this utility does not refresh revisions at save time or silently recover authorization and incomplete-scope failures.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `MemberPlanningIntent`, `ObservedPlanningInput`, `ObservedRevisions`, `PlanningInputKind`, `planningInputService`, `revisionHeaders` |
| Constants | `planningInputService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| Inbound | `frontend` (22) |
| Outbound | `frontend` (1) |

> All 23 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ObservedPlanningInput](../entities/ObservedPlanningInput.md) | Interface | 4 | — | — |
| [PlanningInputKind](../entities/PlanningInputKind.md) | Type alias | 3 | `'calendar' \| 'project' \| 'iteration' \| 'profile' \| 'member' \| 'vacation'` | — |
| [MemberPlanningIntent](../entities/planningInputService_MemberPlanningIntent.md) | Type alias | 12 | `{ profile_id?: number \| null; name?: string; email?: string \| null; text?: string; csv_text?: string }` | — |
| [ObservedRevisions](../entities/ObservedRevisions.md) | Type alias | 13 | `Record<number, number>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `revisionHeaders` | `(revisions: ObservedRevisions)` | — | — |