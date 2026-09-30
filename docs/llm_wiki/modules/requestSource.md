# requestSource Module

**Path:** `frontend/src/types/requestSource.ts`

## Description

_Auto-generated from `frontend/src/types/requestSource.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RequestSource`, `RequestSourceCreate`, `RequestSourceLink`, `RequestSourceLinkCreate`, `RequestSourceLinkWithSource`, `RequestSourceTargetType`, `RequestSourceType` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n1["frontend/src/services/requestSourceService.ts"]
    n2["frontend/src/types/requestSource.ts"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    click n0 "../modules/RequestSourceLinksPanel.md"
    click n1 "../modules/requestSourceService.md"
    click n2 "../modules/requestSource.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Inbound | [requestSourceService](../modules/requestSourceService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequestSource](../entities/requestSource_RequestSource.md) | Class | 4 | — | — |
| [RequestSourceCreate](../entities/requestSource_RequestSourceCreate.md) | Class | 16 | — | — |
| [RequestSourceLink](../entities/requestSource_RequestSourceLink.md) | Class | 26 | — | — |
| [RequestSourceLinkWithSource](../entities/RequestSourceLinkWithSource.md) | Class | 35 | `RequestSourceLink` | — |
| [RequestSourceType](../entities/requestSource_RequestSourceType.md) | Type alias | 1 | — | — |
| [RequestSourceTargetType](../entities/requestSource_RequestSourceTargetType.md) | Type alias | 2 | — | — |
| [RequestSourceLinkCreate](../entities/requestSource_RequestSourceLinkCreate.md) | Type alias | 39 | — | — |
