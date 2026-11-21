# RequestSourceLinksPanel Module

**Path:** `frontend/src/components/requestSources/RequestSourceLinksPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/requestSources/RequestSourceLinksPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/requestSourceService` | `requestSourceService` | — | compiler-dependent |
| `../../types/requestSource` | `RequestSource`, `RequestSourceLinkCreate`, `RequestSourceTargetType`, `RequestSourceType` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/safeUrl` | `safeExternalHref` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../ui` | `SlideOverDrawer` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `Link2`, `Loader2`, `Plus`, `Search`, `Trash2`, `X` | — | compiler-dependent |
| `react` | `KeyboardEvent` | Specifier | compiler-dependent |
| `react` | `useId`, `useMemo`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RequestSourceLinksPanel` |
| Constants | `t`, `sourceTypeOptions` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/RequestSourceLinksPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (4) |
| Outbound | `frontend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequestSourceLinksPanelProps](../entities/RequestSourceLinksPanelProps.md) | Interface | 22 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `RequestSourceLinksPanel` | <pre><code>&#40;&#123;&#10;    targetType&#44;&#10;    targetId&#44;&#10;    initialCount &#61; 0&#44;&#10;    title&#44;&#10;    compact &#61; false&#44;&#10;    onChanged&#44;&#10;&#125;&#58; RequestSourceLinksPanelProps&#41;</code></pre> | — | — |
