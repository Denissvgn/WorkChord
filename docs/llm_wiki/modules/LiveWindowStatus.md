# LiveWindowStatus Module

**Path:** `frontend/src/components/feedback/LiveWindowStatus.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/LiveWindowStatus.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../common/Button` | `Button` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `LiveWindowStatus` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/LiveWindowStatus.tsx"]
    n2["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n3["frontend/src/components/tasks/BacklogPanel.tsx"]
    n4["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n5["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n6["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n7["frontend/src/pages/MyWorkPage.tsx"]
    n8["frontend/src/pages/RoadmapPage.tsx"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n4 --> n0
    n4 --> n1
    n5 --> n0
    n5 --> n1
    n6 --> n0
    n6 --> n1
    n7 --> n0
    n7 --> n1
    n8 --> n0
    n8 --> n1
    click n0 "../modules/Button.md"
    click n1 "../modules/LiveWindowStatus.md"
    click n2 "../modules/TimeEntriesReport.md"
    click n3 "../modules/BacklogPanel.md"
    click n4 "../modules/PagedTaskBrowser.md"
    click n5 "../modules/TaskDiscussion.md"
    click n6 "../modules/TimeEntriesPanel.md"
    click n7 "../modules/MyWorkPage.md"
    click n8 "../modules/RoadmapPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [BacklogPanel](../modules/BacklogPanel.md) |
| Inbound | [PagedTaskBrowser](../modules/PagedTaskBrowser.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
| Outbound | [Button](../modules/Button.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LiveWindowStatus` | `({ window }: { window: {     outsideWindow: boolean; headError: boolean; isFetching: boolean; restart: () => Promise<void>; } })` | — | — |
