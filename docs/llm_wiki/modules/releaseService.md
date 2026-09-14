# releaseService Module

**Path:** `frontend/src/services/releaseService.ts`

## Description

_Auto-generated from `frontend/src/services/releaseService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/release` | `Release`, `ReleaseCreateRequest`, `ReleaseUpdateRequest` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `releaseService` |
| Constants | `releaseService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/releases/ReleaseForm.tsx"]
    n1["frontend/src/pages/ProjectDetailPage.tsx"]
    n2["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/releaseService.ts"]
    n5["frontend/src/types/release.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n4 --> n3
    n4 --> n5
    click n0 "../modules/ReleaseForm.md"
    click n1 "../modules/ProjectDetailPage.md"
    click n2 "../modules/ProjectReleaseDetailPage.md"
    click n3 "../modules/api.md"
    click n4 "../modules/releaseService.md"
    click n5 "../modules/types_release.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_release](../modules/types_release.md) |
