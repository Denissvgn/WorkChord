# release Module

**Path:** `frontend/src/types/release.ts`

## Description

_Auto-generated from `frontend/src/types/release.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./task` | `TaskDisplayedState`, `TaskStatus` | Declaration | erased |
| `./workMetrics` | `WorkMetrics` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Release`, `ReleaseCreateRequest`, `ReleaseStatus`, `ReleaseTaskSummary`, `ReleaseUpdateRequest` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/projectDetailShared.ts"]
    n1["frontend/src/components/projects/ProjectReleasesTab.tsx"]
    n2["frontend/src/components/releases/ReleaseForm.tsx"]
    n3["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n4["frontend/src/services/releaseService.ts"]
    n5["frontend/src/types/release.ts"]
    n6["frontend/src/types/task.ts"]
    n7["frontend/src/types/workMetrics.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n4 --> n5
    n5 --> n6
    n5 --> n7
    click n0 "../modules/projectDetailShared.md"
    click n1 "../modules/ProjectReleasesTab.md"
    click n2 "../modules/ReleaseForm.md"
    click n3 "../modules/ProjectReleaseDetailPage.md"
    click n4 "../modules/releaseService.md"
    click n5 "../modules/types_release.md"
    click n6 "../modules/types_task.md"
    click n7 "../modules/workMetrics.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [projectDetailShared](../modules/projectDetailShared.md) |
| Inbound | [ProjectReleasesTab](../modules/ProjectReleasesTab.md) |
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Inbound | [releaseService](../modules/releaseService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [workMetrics](../modules/workMetrics.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ReleaseTaskSummary](../entities/types_release_ReleaseTaskSummary.md) | Interface | 6 | — | — |
| [Release](../entities/types_release_Release.md) | Interface | 14 | `WorkMetrics` | — |
| [ReleaseCreateRequest](../entities/types_release_ReleaseCreateRequest.md) | Interface | 30 | — | — |
| [ReleaseUpdateRequest](../entities/types_release_ReleaseUpdateRequest.md) | Interface | 41 | — | — |
| [ReleaseStatus](../entities/types_release_ReleaseStatus.md) | Type alias | 4 | `'planned' \| 'building' \| 'shipped' \| 'canceled'` | — |
