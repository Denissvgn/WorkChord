# sessionService Module

**Path:** `frontend/src/services/sessionService.ts`

## Description

_Auto-generated from `frontend/src/services/sessionService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `UserSession`, `sessionService` |
| Constants | `sessionService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n1["frontend/src/components/UserSessionBadge.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/sessionService.ts"]
    n0 --> n3
    n1 --> n3
    n3 --> n2
    click n0 "../modules/SavedViewsControl.md"
    click n1 "../modules/UserSessionBadge.md"
    click n2 "../modules/api.md"
    click n3 "../modules/sessionService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SavedViewsControl](../modules/SavedViewsControl.md) |
| Inbound | [UserSessionBadge](../modules/UserSessionBadge.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [UserSession](../entities/sessionService_UserSession.md) | Class | 3 | — | — |
