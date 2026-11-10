# projectService Module

**Path:** `frontend/src/services/projectService.ts`

## Description

_Auto-generated from `frontend/src/services/projectService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/iteration` | `Iteration` | Declaration | erased |
| `../types/project` | `Initiative`, `InitiativeCreate`, `InitiativeUpdate`, `Project`, `ProjectCreate`, `ProjectMilestone`, `ProjectMilestoneCreateRequest`, `ProjectMilestoneDeleteResponse`, `ProjectMilestoneUpdateRequest`, `ProjectPortfolioSummary`, `ProjectSummary`, `ProjectUpdate`, `ProjectUpdateEntry`, `ProjectUpdateEntryCreate`, `RoadmapMilestonePage` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |
| `./planningInputService` | `ObservedRevisions` | Specifier | compiler-dependent |
| `./planningInputService` | `revisionHeaders` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `projectService` |
| Constants | `projectService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/services/projectService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/projectService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (16) |
| Outbound | `frontend` (5) |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
