# SettingsPage.test Module

**Path:** `frontend/src/pages/SettingsPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/SettingsPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/CommandMenu` | `CommandMenu` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../utils/adminAccess` | `ADMIN_API_KEY_STORAGE_KEY` | — | compiler-dependent |
| `../utils/singleKeyShortcutPreference` | `SINGLE_KEY_SHORTCUTS_STORAGE_KEY` | — | compiler-dependent |
| `./SettingsPage` | `SettingsPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `themeStoreMock` |
| Module calls | `themeStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/pages/SettingsPage.test.tsx"]
    n2["frontend/src/pages/SettingsPage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/utils/adminAccess.ts"]
    n5["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/SettingsPage.test.md"
    click n2 "../modules/SettingsPage.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/adminAccess.md"
    click n5 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |
| Outbound | [singleKeyShortcutPreference](../modules/singleKeyShortcutPreference.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
