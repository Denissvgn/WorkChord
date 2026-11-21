# CommandMenu.test Module

**Path:** `frontend/src/components/layout/CommandMenu.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/CommandMenu.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../../features/scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../navigation/destinations` | `DESTINATIONS`, `DESTINATION_VIEWS` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../utils/singleKeyShortcutPreference` | `SINGLE_KEY_SHORTCUTS_STORAGE_KEY` | — | compiler-dependent |
| `./CommandMenu` | `CommandMenu`, `RECENT_COMMANDS_STORAGE_KEY` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `lookup`, `projects`, `savedViews`, `iterations` |
| Module calls | `lookup = hoisted`, `mock`, `projects = hoisted`, `mock`, `savedViews = hoisted`, `mock`, `iterations = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/layout/CommandMenu.test.tsx"]
    n2["frontend/src/components/layout/CommandMenu.tsx"]
    n3["frontend/src/features/scope/scopeStore.ts"]
    n4["frontend/src/features/scope/useWorkScope.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/navigation/destinations.ts"]
    n7["frontend/src/test/renderWithProviders.tsx"]
    n8["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n2 --> n0
    n2 --> n4
    n2 --> n6
    n4 --> n3
    n7 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/CommandMenu.test.md"
    click n2 "../modules/CommandMenu.md"
    click n3 "../modules/scopeStore.md"
    click n4 "../modules/useWorkScope.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/destinations.md"
    click n7 "../modules/renderWithProviders.md"
    click n8 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [singleKeyShortcutPreference](../modules/singleKeyShortcutPreference.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
