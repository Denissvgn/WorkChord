# GitHubSettingsPanel Module

**Path:** `frontend/src/components/settings/GitHubSettingsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/GitHubSettingsPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/seedDisplay` | `githubRuleDisplay` | — | compiler-dependent |
| `../../services/githubService` | `githubService` | — | compiler-dependent |
| `../../types/github` | `GitHubAutomationEventType`, `GitHubAutomationTargetStatus`, `GitHubStatusAutomationRule`, `GitHubStatusAutomationRuleCreate` | Declaration | erased |
| `../../types/task` | `TaskStatus` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage`, `getApiErrorStatus` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `./AdminAccessGate` | `AdminAccessGate` | — | compiler-dependent |
| `./SettingsUnsavedBar` | `SettingsUnsavedBar` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Edit2`, `Github`, `Loader2`, `Plus`, `Save`, `Trash2`, `X` | — | compiler-dependent |
| `react` | `useId`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GitHubSettingsPanel` |
| Constants | `eventOptions`, `statusOptions`, `targetStatusOptions` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/GitHubSettingsPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FormErrors](../entities/FormErrors.md) | Type alias | 47 | `Partial<Record<'name' \| 'sort_order', string>>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `GitHubSettingsPanel` | `()` | — | — |
