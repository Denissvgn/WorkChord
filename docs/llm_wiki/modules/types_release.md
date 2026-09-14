# release Module

**Path:** `frontend/src/types/release.ts`

## Description

_Auto-generated from `frontend/src/types/release.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./task` | `TaskStatus` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Release`, `ReleaseCreateRequest`, `ReleaseStatus`, `ReleaseTaskSummary`, `ReleaseUpdateRequest` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/releases/ReleaseForm.tsx"]
    n1["frontend/src/pages/ProjectDetailPage.tsx"]
    n2["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n3["frontend/src/services/releaseService.ts"]
    n4["frontend/src/types/release.ts"]
    n5["frontend/src/types/task.ts"]
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n3 --> n4
    n4 --> n5
    click n0 "../modules/ReleaseForm.md"
    click n1 "../modules/ProjectDetailPage.md"
    click n2 "../modules/ProjectReleaseDetailPage.md"
    click n3 "../modules/releaseService.md"
    click n4 "../modules/types_release.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Inbound | [releaseService](../modules/releaseService.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ReleaseTaskSummary](../entities/types_release_ReleaseTaskSummary.md) | Class | 5 | — | — |
| [Release](../entities/types_release_Release.md) | Class | 12 | — | — |
| [ReleaseCreateRequest](../entities/types_release_ReleaseCreateRequest.md) | Class | 28 | — | — |
| [ReleaseUpdateRequest](../entities/types_release_ReleaseUpdateRequest.md) | Class | 39 | — | — |
| [ReleaseStatus](../entities/types_release_ReleaseStatus.md) | Type alias | 3 | — | — |
