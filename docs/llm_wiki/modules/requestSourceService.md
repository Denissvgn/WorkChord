# requestSourceService Module

**Path:** `frontend/src/services/requestSourceService.ts`

## Description

_Auto-generated from `frontend/src/services/requestSourceService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/requestSource` | `RequestSource`, `RequestSourceLinkCreate`, `RequestSourceLinkWithSource`, `RequestSourceTargetType`, `RequestSourceType` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `requestSourceService` |
| Constants | `requestSourceService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/requestSourceService.ts"]
    n3["frontend/src/types/requestSource.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/RequestSourceLinksPanel.md"
    click n1 "../modules/api.md"
    click n2 "../modules/requestSourceService.md"
    click n3 "../modules/requestSource.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [requestSource](../modules/requestSource.md) |
