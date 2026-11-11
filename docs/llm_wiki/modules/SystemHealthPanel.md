# SystemHealthPanel Module

**Path:** `frontend/src/components/settings/SystemHealthPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/SystemHealthPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/healthService` | `healthService` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `CircleHelp`, `RefreshCw` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SystemHealthPanel` |
| Constants | `appVersion`, `stateClasses`, `stateIcons` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/settings/SettingsAccessAndAbout.test.tsx"]
    n2["frontend/src/components/settings/SystemHealthPanel.tsx"]
    n3["frontend/src/pages/SettingsPage.tsx"]
    n4["frontend/src/services/healthService.ts"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    click n0 "../modules/Button.md"
    click n1 "../modules/SettingsAccessAndAbout.test.md"
    click n2 "../modules/SystemHealthPanel.md"
    click n3 "../modules/SettingsPage.md"
    click n4 "../modules/healthService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SettingsAccessAndAbout.test](../modules/SettingsAccessAndAbout.test.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [healthService](../modules/healthService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [VisibleHealthState](../entities/VisibleHealthState.md) | Type alias | 9 | `'notChecked' \| 'checking' \| 'healthy' \| 'unhealthy' \| 'unavailable'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SystemHealthPanel` | `()` | — | — |
