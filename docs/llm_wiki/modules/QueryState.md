# QueryState Module

**Path:** `frontend/src/components/feedback/QueryState.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/QueryState.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Inbox`, `LoaderCircle`, `RefreshCw` | — | compiler-dependent |
| `react` | `Ref` | Declaration | erased |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState`, `QueryStaleState` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/QueryState.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (66) |
| Outbound | `frontend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 68 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SharedStateProps](../entities/SharedStateProps.md) | Interface | 7 | — | — |
| [QueryLoadingStateProps](../entities/QueryLoadingStateProps.md) | Interface | 11 | `SharedStateProps` | — |
| [QueryErrorStateProps](../entities/QueryErrorStateProps.md) | Interface | 15 | `SharedStateProps` | — |
| [QueryEmptyStateProps](../entities/QueryEmptyStateProps.md) | Interface | 27 | `SharedStateProps` | — |
| [QueryStaleStateProps](../entities/QueryStaleStateProps.md) | Interface | 32 | `SharedStateProps` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `QueryLoadingState` | `({ message, className = '' }: QueryLoadingStateProps)` | — | — |
| `QueryErrorState` | <pre><code>&#40;&#123;&#10;    error&#44;&#10;    fallback&#44;&#10;    headingLevel&#44;&#10;    isRetrying &#61; false&#44;&#10;    message&#44;&#10;    onRetry&#44;&#10;    retryButtonRef&#44;&#10;    retryLabel&#44;&#10;    title&#44;&#10;    className &#61; &#39;&#39;&#44;&#10;&#125;&#58; QueryErrorStateProps&#41;</code></pre> | — | — |
| `QueryEmptyState` | `({ title, description, className = '' }: QueryEmptyStateProps)` | — | — |
| `QueryStaleState` | `({ message, onRetry, className = '' }: QueryStaleStateProps)` | — | — |
