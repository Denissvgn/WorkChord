# emailSettings Module

**Path:** `frontend/src/types/emailSettings.ts`

## Description

_Auto-generated from `frontend/src/types/emailSettings.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./systemSettings` | `RuntimeSettingSource` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `EmailSettings`, `EmailSettingsUpdate`, `TestEmailRequest`, `TestEmailResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/EmailSettingsPanel.test.tsx"]
    n1["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n2["frontend/src/services/emailSettingsService.ts"]
    n3["frontend/src/types/emailSettings.ts"]
    n4["frontend/src/types/systemSettings.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n3 --> n4
    click n0 "../modules/EmailSettingsPanel.test.md"
    click n1 "../modules/EmailSettingsPanel.md"
    click n2 "../modules/emailSettingsService.md"
    click n3 "../modules/emailSettings.md"
    click n4 "../modules/systemSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EmailSettingsPanel.test](../modules/EmailSettingsPanel.test.md) |
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [emailSettingsService](../modules/emailSettingsService.md) |
| Outbound | [systemSettings](../modules/systemSettings.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [EmailSettings](../entities/emailSettings_EmailSettings.md) | Class | 3 | — | — |
| [EmailSettingsUpdate](../entities/emailSettings_EmailSettingsUpdate.md) | Class | 16 | — | — |
| [TestEmailRequest](../entities/emailSettings_TestEmailRequest.md) | Class | 28 | — | — |
| [TestEmailResponse](../entities/emailSettings_TestEmailResponse.md) | Class | 32 | — | — |
