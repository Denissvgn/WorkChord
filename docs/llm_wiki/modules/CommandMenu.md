# CommandMenu Module

**Path:** `frontend/src/components/layout/CommandMenu.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/CommandMenu.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useSingleKeyShortcutPreference` | `useSingleKeyShortcutPreference` |
| `../../navigation/workspaces` | `getWorkspaceForPath` |
| `../common/Checkbox` | `Checkbox` |
| `../common/Modal` | `Modal` |
| `./commandMenuEvents` | `OPEN_COMMAND_MENU_EVENT` |
| `lucide-react` | `ArrowUpDown`, `ClipboardCheck`, `Command`, `GanttChartSquare`, `Layers`, `List`, `LayoutGrid`, `ListFilter`, `ListTodo`, `MapPin`, `Maximize2`, `Minimize2`, `Plus`, `Search`, `Settings`, `Users`, `LucideIcon` |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState`, `KeyboardEvent` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useLocation`, `useNavigate` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CommandMenu`, `RECENT_COMMANDS_STORAGE_KEY` |
| Constants | `TASKS_FIRST_GROUPS`, `CURRENT_FIRST_GROUPS`, `COMPACT_GROUPS`, `MAX_COMPACT_SUGGESTIONS`, `MAX_RECENT_COMMANDS`, `RECENT_COMMANDS_STORAGE_KEY`, `WORKSPACE_SUGGESTION_IDS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Checkbox.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/layout/AppShell.tsx"]
    n3["frontend/src/components/layout/CommandMenu.test.tsx"]
    n4["frontend/src/components/layout/CommandMenu.tsx"]
    n5["frontend/src/components/layout/commandMenuEvents.ts"]
    n6["frontend/src/hooks/useSingleKeyShortcutPreference.ts"]
    n7["frontend/src/navigation/workspaces.ts"]
    n8["frontend/src/pages/SettingsPage.test.tsx"]
    n2 --> n4
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n8 --> n4
    click n0 "../modules/Checkbox.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/AppShell.md"
    click n3 "../modules/CommandMenu.test.md"
    click n4 "../modules/CommandMenu.md"
    click n5 "../modules/commandMenuEvents.md"
    click n6 "../modules/useSingleKeyShortcutPreference.md"
    click n7 "../modules/workspaces.md"
    click n8 "../modules/SettingsPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [CommandMenu.test](../modules/CommandMenu.test.md) |
| Inbound | [SettingsPage.test](../modules/SettingsPage.test.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [commandMenuEvents](../modules/commandMenuEvents.md) |
| Outbound | [useSingleKeyShortcutPreference](../modules/useSingleKeyShortcutPreference.md) |
| Outbound | [workspaces](../modules/workspaces.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CommandAction](../entities/CommandAction.md) | Class | 32 | — | — |
| [CommandGroup](../entities/CommandGroup.md) | Type alias | 30 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `CommandMenu` | `()` | — | — |
