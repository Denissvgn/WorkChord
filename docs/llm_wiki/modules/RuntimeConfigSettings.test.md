# RuntimeConfigSettings.test Module

**Path:** `frontend/src/components/settings/RuntimeConfigSettings.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/RuntimeConfigSettings.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/systemSettings` | `SystemSettings` | Declaration | erased |
| `./RuntimeConfigSettings` | `RuntimeConfigSettings` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `adminAccessMock`, `systemSettingsServiceMock` |
| Module calls | `adminAccessMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/RuntimeConfigSettings.test.tsx"]
    n1["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/systemSettings.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/RuntimeConfigSettings.test.md"
    click n1 "../modules/RuntimeConfigSettings.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/systemSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [systemSettings](../modules/systemSettings.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
