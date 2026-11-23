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
    n2["frontend/src/components/triage/TriageConvertSource.tsx"]
    n3["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n4["frontend/src/utils/safeUrl.ts"]
    n0 --> n4
    n1 --> n0
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n3 --> n0
    n3 --> n4
    click n0 "../modules/RequestSourceLinksPanel.md"
    click n1 "../modules/TaskTimelinePanel.md"
    click n2 "../modules/TriageConvertSource.md"
    click n3 "../modules/TriageDetailPanel.md"
    click n4 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Inbound | [TaskTimelinePanel](../modules/TaskTimelinePanel.md) |
| Inbound | [TriageConvertSource](../modules/TriageConvertSource.md) |
| Inbound | [TriageDetailPanel](../modules/TriageDetailPanel.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `safeExternalHref` | `(value?: string \| null) -> string \| undefined` | — | — |
