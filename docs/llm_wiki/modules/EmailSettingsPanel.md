# EmailSettingsPanel Module

**Path:** `frontend/src/components/settings/EmailSettingsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/EmailSettingsPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../../services/emailSettingsService` | `emailSettingsService` | — | compiler-dependent |
| `../../types/emailSettings` | `EmailSettings` | Declaration | erased |
| `../../types/systemSettings` | `RuntimeSettingSource` | Declaration | erased |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery`, `useMutation`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Save`, `Mail`, `Server`, `Shield`, `Eye`, `EyeOff`, `Send` | — | compiler-dependent |
| `react` | `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `EmailSettingsPanel` |
| Constants | `sourceLabelKey`, `sourceClass` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/EmailSettingsPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [EmailValidationErrors](../entities/EmailValidationErrors.md) | Type alias | 47 | <pre><code>Partial&#60;Record&#60;&#10;    &#39;smtp&#95;host&#39; &#124; &#39;smtp&#95;port&#39; &#124; &#39;smtp&#95;from&#95;email&#39; &#124; &#39;test&#95;email&#39;&#44;&#10;    string&#10;&#62;&#62;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `EmailSettingsPanel` | `()` | — | — |
