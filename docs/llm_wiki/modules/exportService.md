# exportService Module

**Path:** `frontend/src/services/exportService.ts`

## Description

_Auto-generated from `frontend/src/services/exportService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |
| `./planningInputService` | `revisionHeaders`, `ObservedRevisions` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `exportService` |
| Constants | `exportService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/iteration/IterationImportDialog.tsx"]
    n1["frontend/src/components/iteration/IterationList.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/exportService.ts"]
    n4["frontend/src/services/planningInputService.ts"]
    n0 --> n3
    n0 --> n4
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    n4 --> n2
    click n0 "../modules/IterationImportDialog.md"
    click n1 "../modules/IterationList.md"
    click n2 "../modules/api.md"
    click n3 "../modules/exportService.md"
    click n4 "../modules/planningInputService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationImportDialog](../modules/IterationImportDialog.md) |
| Inbound | [IterationList](../modules/IterationList.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
