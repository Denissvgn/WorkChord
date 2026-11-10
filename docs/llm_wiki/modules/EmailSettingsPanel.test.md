# EmailSettingsPanel.test Module

**Path:** `frontend/src/components/settings/EmailSettingsPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/EmailSettingsPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/emailSettings` | `EmailSettings` | Declaration | erased |
| `./EmailSettingsPanel` | `EmailSettingsPanel` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `adminAccessMock`, `emailSettingsServiceMock` |
| Module calls | `adminAccessMock = hoisted`, `emailSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/EmailSettingsPanel.test.tsx"]
    n1["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/emailSettings.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/EmailSettingsPanel.test.md"
    click n1 "../modules/EmailSettingsPanel.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/emailSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [emailSettings](../modules/emailSettings.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
