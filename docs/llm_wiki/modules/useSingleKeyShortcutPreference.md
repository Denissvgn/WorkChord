# useSingleKeyShortcutPreference Module

**Path:** `frontend/src/hooks/useSingleKeyShortcutPreference.ts`

## Description

_Auto-generated from `frontend/src/hooks/useSingleKeyShortcutPreference.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../utils/singleKeyShortcutPreference` | `readSingleKeyShortcutsEnabled`, `SINGLE_KEY_SHORTCUTS_CHANGED_EVENT`, `SINGLE_KEY_SHORTCUTS_STORAGE_KEY`, `writeSingleKeyShortcutsEnabled` |
| `react` | `useCallback`, `useEffect`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useSingleKeyShortcutPreference` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/components/layout/ContextHelp.tsx"]
    n2["frontend/src/hooks/useSingleKeyShortcutPreference.test.tsx"]
    n3["frontend/src/hooks/useSingleKeyShortcutPreference.ts"]
    n4["frontend/src/pages/SettingsPage.tsx"]
    n5["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n0 --> n3
    n1 --> n3
    n2 --> n3
    n2 --> n5
    n3 --> n5
    n4 --> n3
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/ContextHelp.md"
    click n2 "../modules/useSingleKeyShortcutPreference.test.md"
    click n3 "../modules/useSingleKeyShortcutPreference.md"
    click n4 "../modules/SettingsPage.md"
    click n5 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CommandMenu](../modules/CommandMenu.md) |
| Inbound | [ContextHelp](../modules/ContextHelp.md) |
| Inbound | [useSingleKeyShortcutPreference.test](../modules/useSingleKeyShortcutPreference.test.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [singleKeyShortcutPreference](../modules/singleKeyShortcutPreference.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useSingleKeyShortcutPreference` | `()` | — | — |
