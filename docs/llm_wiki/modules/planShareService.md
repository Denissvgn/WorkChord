# planShareService Module

**Path:** `frontend/src/services/planShareService.ts`

## Description

_Auto-generated from `frontend/src/services/planShareService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanShare`, `PlanShareSnapshot`, `PlanShareTask`, `PlanShareTeamMember`, `planShareService` |
| Constants | `planShareService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/pages/PlanMasterPage.tsx"]
    n1["frontend/src/pages/PlanSharePage.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/planShareService.ts"]
    n0 --> n3
    n1 --> n3
    n3 --> n2
    click n0 "../modules/PlanMasterPage.md"
    click n1 "../modules/PlanSharePage.md"
    click n2 "../modules/api.md"
    click n3 "../modules/planShareService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Inbound | [PlanSharePage](../modules/PlanSharePage.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanShareTask](../entities/PlanShareTask.md) | Class | 3 | — | — |
| [PlanShareTeamMember](../entities/PlanShareTeamMember.md) | Class | 20 | — | — |
| [PlanShareSnapshot](../entities/PlanShareSnapshot.md) | Class | 26 | — | — |
| [PlanShare](../entities/planShareService_PlanShare.md) | Class | 41 | — | — |
