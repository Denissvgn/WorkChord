# snapshotService Module

**Path:** `frontend/src/services/snapshotService.ts`

## Description

_Auto-generated from `frontend/src/services/snapshotService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationSnapshot`, `SnapshotRestoreResponse`, `snapshotService` |
| Constants | `snapshotService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/pages/GanttPage.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/snapshotService.ts"]
    n3["frontend/src/services/snapshotVersions.test.ts"]
    n0 --> n2
    n2 --> n1
    n3 --> n1
    n3 --> n2
    click n0 "../modules/GanttPage.md"
    click n1 "../modules/api.md"
    click n2 "../modules/snapshotService.md"
    click n3 "../modules/snapshotVersions.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [snapshotVersions.test](../modules/snapshotVersions.test.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationSnapshot](../entities/IterationSnapshot.md) | Class | 3 | — | — |
| [SnapshotRestoreResponse](../entities/snapshotService_SnapshotRestoreResponse.md) | Class | 10 | — | — |
