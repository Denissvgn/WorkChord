# planShareService Module

**Path:** `frontend/src/services/planShareService.ts`

## Description

_Auto-generated from `frontend/src/services/planShareService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanShare`, `PlanShareSnapshot`, `PlanShareTask`, `PlanShareTeamMember`, `planShareService` |
| Constants | `planShareService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanShareSection.test.tsx"]
    n1["frontend/src/components/planning/PlanShareSection.tsx"]
    n2["frontend/src/pages/PlanSharePage.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/planShareService.ts"]
    n0 --> n1
    n0 --> n4
    n1 --> n4
    n2 --> n4
    n4 --> n3
    click n0 "../modules/PlanShareSection.test.md"
    click n1 "../modules/PlanShareSection.md"
    click n2 "../modules/PlanSharePage.md"
    click n3 "../modules/api.md"
    click n4 "../modules/planShareService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanShareSection.test](../modules/PlanShareSection.test.md) |
| Inbound | [PlanShareSection](../modules/PlanShareSection.md) |
| Inbound | [PlanSharePage](../modules/PlanSharePage.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanShareTask](../entities/PlanShareTask.md) | Interface | 3 | — | — |
| [PlanShareTeamMember](../entities/PlanShareTeamMember.md) | Interface | 20 | — | — |
| [PlanShareSnapshot](../entities/PlanShareSnapshot.md) | Interface | 26 | — | — |
| [PlanShare](../entities/planShareService_PlanShare.md) | Interface | 41 | — | — |
