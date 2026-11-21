# SettingsPage.test Module

**Path:** `frontend/src/pages/SettingsPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/SettingsPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/CommandMenu` | `CommandMenu` | — | compiler-dependent |
| `../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../utils/singleKeyShortcutPreference` | `SINGLE_KEY_SHORTCUTS_STORAGE_KEY` | — | compiler-dependent |
| `./SettingsPage` | `SettingsPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `themeStoreMock`, `GROUPS` |
| Module calls | `themeStoreMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/i18n/i18n.ts"]
    n2["frontend/src/pages/SettingsPage.test.tsx"]
    n3["frontend/src/pages/SettingsPage.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n4 --> n1
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/i18n.md"
    click n2 "../modules/SettingsPage.test.md"
    click n3 "../modules/SettingsPage.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [singleKeyShortcutPreference](../modules/singleKeyShortcutPreference.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
