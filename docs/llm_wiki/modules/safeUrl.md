# safeUrl Module

**Path:** `frontend/src/utils/safeUrl.ts`

## Description

_Auto-generated from `frontend/src/utils/safeUrl.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `safeExternalHref`, `sourceLinkHref` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n1["frontend/src/components/tasks/TaskTimelinePanel.tsx"]
    n2["frontend/src/components/triage/TriageConvertSource.tsx"]
    n3["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n4["frontend/src/pages/TriagePage.test.tsx"]
    n5["frontend/src/utils/safeUrl.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n3 --> n0
    n3 --> n5
    n4 --> n5
    click n0 "../modules/RequestSourceLinksPanel.md"
    click n1 "../modules/TaskTimelinePanel.md"
    click n2 "../modules/TriageConvertSource.md"
    click n3 "../modules/TriageDetailPanel.md"
    click n4 "../modules/TriagePage.test.md"
    click n5 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Inbound | [TaskTimelinePanel](../modules/TaskTimelinePanel.md) |
| Inbound | [TriageConvertSource](../modules/TriageConvertSource.md) |
| Inbound | [TriageDetailPanel](../modules/TriageDetailPanel.md) |
| Inbound | [TriagePage.test](../modules/TriagePage.test.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `safeExternalHref` | `(value?: string \| null) -> string \| undefined` | — | — |
| `sourceLinkHref` | `(value?: string \| null) -> string \| undefined` | — | An intake or task source link: a path inside this instance, or a safe http(s) address. |
