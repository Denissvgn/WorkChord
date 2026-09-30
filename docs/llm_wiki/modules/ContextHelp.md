# ContextHelp Module

**Path:** `frontend/src/components/layout/ContextHelp.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/ContextHelp.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useSingleKeyShortcutPreference` | `useSingleKeyShortcutPreference` |
| `../../navigation/helpContexts` | `getHelpContext`, `HelpContentProvider` |
| `../common/Checkbox` | `Checkbox` |
| `../planning/PlanningWorkflowGuide` | `PlanningWorkflowHelpContent` |
| `../settings/SettingsGoalHelpContent` | `SettingsGoalHelpContent` |
| `../tasks/TaskWorkflowGuide` | `TaskWorkflowHelpContent` |
| `../ui` | `SlideOverDrawer` |
| `./commandMenuEvents` | `openCommandMenu` |
| `lucide-react` | `ArrowDownUp`, `ChevronRight`, `CircleHelp`, `Command`, `CornerDownLeft`, `Keyboard` |
| `react` | `useId`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useLocation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ContextHelp` |
| Constants | `PROVIDER_COPY_KEYS`, `TASK_SHORTCUTS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Checkbox.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/commandMenuEvents.ts"]
    n3["frontend/src/components/layout/ContextHelp.test.tsx"]
    n4["frontend/src/components/layout/ContextHelp.tsx"]
    n5["frontend/src/components/planning/PlanningWorkflowGuide.tsx"]
    n6["frontend/src/components/settings/SettingsGoalHelpContent.tsx"]
    n7["frontend/src/components/tasks/TaskWorkflowGuide.tsx"]
    n8["frontend/src/components/ui/index.ts"]
    n9["frontend/src/hooks/useSingleKeyShortcutPreference.ts"]
    n10["frontend/src/navigation/helpContexts.ts"]
    n1 --> n2
    n1 --> n4
    n3 --> n4
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    click n0 "../modules/Checkbox.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/commandMenuEvents.md"
    click n3 "../modules/ContextHelp.test.md"
    click n4 "../modules/ContextHelp.md"
    click n5 "../modules/PlanningWorkflowGuide.md"
    click n6 "../modules/SettingsGoalHelpContent.md"
    click n7 "../modules/TaskWorkflowGuide.md"
    click n8 "../modules/index.md"
    click n9 "../modules/useSingleKeyShortcutPreference.md"
    click n10 "../modules/helpContexts.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [ContextHelp.test](../modules/ContextHelp.test.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [commandMenuEvents](../modules/commandMenuEvents.md) |
| Outbound | [PlanningWorkflowGuide](../modules/PlanningWorkflowGuide.md) |
| Outbound | [SettingsGoalHelpContent](../modules/SettingsGoalHelpContent.md) |
| Outbound | [TaskWorkflowGuide](../modules/TaskWorkflowGuide.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [useSingleKeyShortcutPreference](../modules/useSingleKeyShortcutPreference.md) |
| Outbound | [helpContexts](../modules/helpContexts.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ContextHelp` | `()` | — | — |
