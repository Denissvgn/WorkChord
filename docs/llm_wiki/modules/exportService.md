# exportService Module

**Path:** `frontend/src/services/exportService.ts`

## Description

_Auto-generated from `frontend/src/services/exportService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `exportService` |
| Constants | `exportService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/iteration/IterationList.tsx"]
    n1["frontend/src/pages/IterationsPage.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/exportService.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n3
    n3 --> n2
    click n0 "../modules/IterationList.md"
    click n1 "../modules/IterationsPage.md"
    click n2 "../modules/api.md"
    click n3 "../modules/exportService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationList](../modules/IterationList.md) |
| Inbound | [IterationsPage](../modules/IterationsPage.md) |
| Outbound | [api](../modules/api.md) |
