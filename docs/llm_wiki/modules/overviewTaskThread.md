# overviewTaskThread Module

**Path:** `frontend/src/features/overview/overviewTaskThread.ts`

## Description

_Auto-generated from `frontend/src/features/overview/overviewTaskThread.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OVERVIEW_TASK_ORIGIN`, `OVERVIEW_TASK_ORIGIN_PARAM`, `OVERVIEW_TASK_PARAM`, `OVERVIEW_TASK_RETURN_PARAM`, `OVERVIEW_TASK_THREAD_PARAM`, `OVERVIEW_TASK_THREAD_SOURCES`, `OverviewTaskThreadSource`, `overviewTaskDrawerHref`, `overviewTaskReturnFocusId`, `overviewTaskThreadSource`, `positiveTaskId` |
| Constants | `OVERVIEW_TASK_PARAM`, `OVERVIEW_TASK_ORIGIN_PARAM`, `OVERVIEW_TASK_ORIGIN`, `OVERVIEW_TASK_RETURN_PARAM`, `OVERVIEW_TASK_THREAD_PARAM`, `OVERVIEW_TASK_THREAD_SOURCES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/overview/OverviewTaskReturnBar.tsx"]
    n1["frontend/src/features/overview/overviewTaskThread.ts"]
    n2["frontend/src/pages/OverviewPage.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n0 --> n1
    n2 --> n1
    n3 --> n0
    n3 --> n1
    click n0 "../modules/OverviewTaskReturnBar.md"
    click n1 "../modules/overviewTaskThread.md"
    click n2 "../modules/OverviewPage.md"
    click n3 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OverviewTaskReturnBar](../modules/OverviewTaskReturnBar.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OverviewTaskThreadSource](../entities/OverviewTaskThreadSource.md) | Type alias | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `positiveTaskId` | `(value: string \| null) -> number \| null` | — | — |
| `overviewTaskThreadSource` | `(value: string \| null) -> OverviewTaskThreadSource \| null` | — | — |
| `overviewTaskReturnFocusId` | `(taskId: number)` | — | — |
| `overviewTaskDrawerHref` | `(taskId: number, source: OverviewTaskThreadSource)` | — | — |
