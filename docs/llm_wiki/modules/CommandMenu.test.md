# CommandMenu.test Module

**Path:** `frontend/src/components/layout/CommandMenu.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/CommandMenu.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../navigation/workspaces` | `PRIMARY_NAV_ITEMS` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../utils/singleKeyShortcutPreference` | `SINGLE_KEY_SHORTCUTS_STORAGE_KEY` | — | compiler-dependent |
| `./CommandMenu` | `CommandMenu`, `RECENT_COMMANDS_STORAGE_KEY` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `lookup`, `projects`, `savedViews` |
| Module calls | `lookup = hoisted`, `mock`, `projects = hoisted`, `mock`, `savedViews = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.test.tsx"]
    n1["frontend/src/components/layout/CommandMenu.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/navigation/workspaces.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n3
    n4 --> n2
    click n0 "../modules/CommandMenu.test.md"
    click n1 "../modules/CommandMenu.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/workspaces.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [workspaces](../modules/workspaces.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [singleKeyShortcutPreference](../modules/singleKeyShortcutPreference.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
