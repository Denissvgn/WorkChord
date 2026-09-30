# emailSettingsService Module

**Path:** `frontend/src/services/emailSettingsService.ts`

## Description

_Auto-generated from `frontend/src/services/emailSettingsService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/emailSettings` | `EmailSettings`, `EmailSettingsUpdate`, `TestEmailResponse` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `emailSettingsService` |
| Constants | `emailSettingsService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/emailSettingsService.ts"]
    n3["frontend/src/types/emailSettings.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/EmailSettingsPanel.md"
    click n1 "../modules/api.md"
    click n2 "../modules/emailSettingsService.md"
    click n3 "../modules/emailSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [emailSettings](../modules/emailSettings.md) |
