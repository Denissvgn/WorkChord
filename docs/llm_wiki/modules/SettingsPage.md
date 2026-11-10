# SettingsPage Module

**Path:** `frontend/src/pages/SettingsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/SettingsPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../components/settings/AdminAccessGate` | `AdminAccessGate` | — | compiler-dependent |
| `../components/settings/AdminAccessPanel` | `AdminAccessPanel` | — | compiler-dependent |
| `../components/settings/AgentAccessPanel` | `AgentAccessPanel` | — | compiler-dependent |
| `../components/settings/AgentModelAdministration` | `AgentModelAdministration` | — | compiler-dependent |
| `../components/settings/EmailSettingsPanel` | `EmailSettingsPanel` | — | compiler-dependent |
| `../components/settings/GitHubSettingsPanel` | `GitHubSettingsPanel` | — | compiler-dependent |
| `../components/settings/InterfaceLanguageSettings` | `InterfaceLanguageSettings` | — | compiler-dependent |
| `../components/settings/OutboundWebhooksPanel` | `OutboundWebhooksPanel` | — | compiler-dependent |
| `../components/settings/RuntimeConfigSettings` | `RuntimeConfigSettings` | — | compiler-dependent |
| `../components/settings/SchedulingRulesSettings` | `SchedulingRulesSettings` | — | compiler-dependent |
| `../components/settings/SystemHealthPanel` | `SystemHealthPanel` | — | compiler-dependent |
| `../components/settings/TemplateLabelSettings` | `TemplateLabelSettings` | — | compiler-dependent |
| `../components/ui` | `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../hooks/useSingleKeyShortcutPreference` | `useSingleKeyShortcutPreference` | — | compiler-dependent |
| `../store/themeStore` | `useThemeStore` | — | compiler-dependent |
| `lucide-react` | `LucideIcon` | Declaration | erased |
| `lucide-react` | `Activity`, `AlertTriangle`, `ArrowRight`, `Bell`, `Bot`, `CalendarClock`, `Check`, `ChevronDown`, `Github`, `KeyRound`, `Keyboard`, `Palette`, `Search`, `ServerCog`, `Settings2`, `Tags`, `Webhook` | — | compiler-dependent |
| `react` | `KeyboardEvent` | Declaration | erased |
| `react` | `useEffect`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RECENT_SETTINGS_STORAGE_KEY`, `default` |
| Constants | `SETTINGS_GROUPS`, `SETTINGS_DESTINATIONS`, `MAX_RECENT_SETTINGS`, `RECENT_SETTINGS_STORAGE_KEY` |
| Module calls | `SETTINGS_DESTINATIONS = flatMap` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/SettingsPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/SettingsPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SettingsDestination](../entities/SettingsDestination.md) | Interface | 47 | — | — |
| [SettingsGroup](../entities/SettingsGroup.md) | Interface | 59 | — | — |
| [SettingsTab](../entities/SettingsTab.md) | Type alias | 43 | `'appearance' \| 'scheduling' \| 'templates_labels' \| 'models_agents' \| 'github' \| 'webhooks' \| 'notifications' \| 'admin_access' \| 'runtime' \| 'about'` | — |
| [SettingsPageTab](../entities/SettingsPageTab.md) | Type alias | 44 | `'overview' \| SettingsTab` | — |
| [SettingsGroupId](../entities/SettingsGroupId.md) | Type alias | 45 | `'personal' \| 'planning' \| 'agents' \| 'integrations' \| 'system'` | — |
| [SettingsDestinationHeader](../entities/SettingsDestinationHeader.md) | Type alias | 54 | <pre><code>Pick&#60;&#10;    SettingsDestination&#44;&#10;    &#39;labelKey&#39; &#124; &#39;descriptionKey&#39; &#124; &#39;icon&#39;&#10;&#62;</code></pre> | — |
