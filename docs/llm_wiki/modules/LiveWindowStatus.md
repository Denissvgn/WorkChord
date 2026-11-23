# LiveWindowStatus Module

**Path:** `frontend/src/components/feedback/LiveWindowStatus.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/LiveWindowStatus.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

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
    n2["frontend/src/components/projects/RoadmapView.tsx"]
    n3["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n4["frontend/src/components/tasks/BacklogPanel.tsx"]
    n5["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n6["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n7["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n7
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
    click n2 "../modules/RoadmapView.md"
    click n3 "../modules/TimeEntriesReport.md"
    click n4 "../modules/BacklogPanel.md"
    click n5 "../modules/PagedTaskBrowser.md"
    click n6 "../modules/TaskDiscussion.md"
    click n7 "../modules/TimeEntriesPanel.md"
    click n8 "../modules/MyWorkPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [BacklogPanel](../modules/BacklogPanel.md) |
| Inbound | [PagedTaskBrowser](../modules/PagedTaskBrowser.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [Button](../modules/Button.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LiveWindowStatus` | <pre><code>&#40;&#123; window &#125;&#58; &#123; window&#58; &#123;&#10;    outsideWindow&#58; boolean&#59; headError&#58; boolean&#59; isFetching&#58; boolean&#59; restart&#58; &#40;&#41; &#61;&#62; Promise&#60;void&#62;&#59;&#10;&#125; &#125;&#41;</code></pre> | — | — |
