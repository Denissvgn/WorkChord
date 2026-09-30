# safeUrl Module

**Path:** `frontend/src/utils/safeUrl.ts`

## Description

_Auto-generated from `frontend/src/utils/safeUrl.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `safeExternalHref` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n1["frontend/src/components/tasks/TaskTimelinePanel.tsx"]
    n2["frontend/src/pages/TriagePage.tsx"]
    n3["frontend/src/utils/safeUrl.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/RequestSourceLinksPanel.md"
    click n1 "../modules/TaskTimelinePanel.md"
    click n2 "../modules/TriagePage.md"
    click n3 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Inbound | [TaskTimelinePanel](../modules/TaskTimelinePanel.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `safeExternalHref` | `(value: string \| null) -> string \| undefined` | — | — |
