# RuntimeConfigSettings Module

**Path:** `frontend/src/components/settings/RuntimeConfigSettings.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/RuntimeConfigSettings.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAdminAccess` | `useCanReadSettings` | — | compiler-dependent |
| `../../services/systemSettingsService` | `systemSettingsService` | — | compiler-dependent |
| `../../types/systemSettings` | `AILanguageMode`, `AppRuntimeSettingsUpdate`, `GitHubRuntimeSettingsUpdate`, `LLMProvider`, `LLMRuntimeSettingsUpdate`, `RuntimeSettingSource`, `SystemSettings`, `WebIntakeRuntimeSettingsUpdate` | Declaration | erased |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `./SettingsUnsavedBar` | `SettingsUnsavedBar` | — | compiler-dependent |
| `./WithheldValuesNote` | `WithheldValuesNote` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Globe2`, `KeyRound`, `RefreshCcw`, `Save`, `ServerCog`, `ShieldAlert` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RuntimeConfigSettings` |
| Constants | `DEFAULT_LLM_ENDPOINTS`, `sourceClass` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/RuntimeConfigSettings.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [LLMForm](../entities/LLMForm.md) | Interface | 27 | — | — |
| [AppForm](../entities/AppForm.md) | Interface | 37 | — | — |
| [GitHubForm](../entities/GitHubForm.md) | Interface | 41 | — | — |
| [WebIntakeForm](../entities/WebIntakeForm.md) | Interface | 51 | — | — |
| [RuntimeSection](../entities/RuntimeSection.md) | Type alias | 57 | `'llm' \| 'github' \| 'webIntake'` | — |
| [RuntimeErrors](../entities/RuntimeErrors.md) | Type alias | 58 | `Record<string, string>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `RuntimeConfigSettings` | `()` | — | — |
