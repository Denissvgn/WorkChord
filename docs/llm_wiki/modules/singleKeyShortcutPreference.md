# singleKeyShortcutPreference Module

**Path:** `frontend/src/utils/singleKeyShortcutPreference.ts`

## Description

_Auto-generated from `frontend/src/utils/singleKeyShortcutPreference.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SINGLE_KEY_SHORTCUTS_CHANGED_EVENT`, `SINGLE_KEY_SHORTCUTS_STORAGE_KEY`, `readSingleKeyShortcutsEnabled`, `writeSingleKeyShortcutsEnabled` |
| Constants | `SINGLE_KEY_SHORTCUTS_STORAGE_KEY`, `SINGLE_KEY_SHORTCUTS_CHANGED_EVENT` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.test.tsx"]
    n1["frontend/src/components/layout/ContextHelp.test.tsx"]
    n2["frontend/src/hooks/useSingleKeyShortcutPreference.test.tsx"]
    n3["frontend/src/hooks/useSingleKeyShortcutPreference.ts"]
    n4["frontend/src/pages/SettingsPage.test.tsx"]
    n5["frontend/src/utils/singleKeyShortcutPreference.ts"]
    n0 --> n5
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n3 --> n5
    n4 --> n5
    click n0 "../modules/CommandMenu.test.md"
    click n1 "../modules/ContextHelp.test.md"
    click n2 "../modules/useSingleKeyShortcutPreference.test.md"
    click n3 "../modules/useSingleKeyShortcutPreference.md"
    click n4 "../modules/SettingsPage.test.md"
    click n5 "../modules/singleKeyShortcutPreference.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CommandMenu.test](../modules/CommandMenu.test.md) |
| Inbound | [ContextHelp.test](../modules/ContextHelp.test.md) |
| Inbound | [useSingleKeyShortcutPreference.test](../modules/useSingleKeyShortcutPreference.test.md) |
| Inbound | [useSingleKeyShortcutPreference](../modules/useSingleKeyShortcutPreference.md) |
| Inbound | [SettingsPage.test](../modules/SettingsPage.test.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `readSingleKeyShortcutsEnabled` | `()` | — | — |
| `writeSingleKeyShortcutsEnabled` | `(enabled: boolean)` | — | — |
