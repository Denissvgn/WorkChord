# RequestSourceLinksPanel Module

**Path:** `frontend/src/components/requestSources/RequestSourceLinksPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/requestSources/RequestSourceLinksPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/requestSourceService` | `requestSourceService` | — | compiler-dependent |
| `../../types/requestSource` | `RequestSource`, `RequestSourceLinkCreate`, `RequestSourceTargetType`, `RequestSourceType` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/safeUrl` | `safeExternalHref` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `Link2`, `Loader2`, `Plus`, `Search`, `Trash2`, `X` | — | compiler-dependent |
| `react` | `KeyboardEvent` | Specifier | compiler-dependent |
| `react` | `useMemo`, `useState` | — | compiler-dependent |

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
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.test.tsx"]
    n2["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n3["frontend/src/components/tasks/TaskTimelinePanel.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/pages/ProjectDetailPage.tsx"]
    n6["frontend/src/pages/TriagePage.tsx"]
    n7["frontend/src/services/requestSourceService.ts"]
    n8["frontend/src/types/requestSource.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n10["frontend/src/utils/safeUrl.ts"]
    n0 --> n9
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n9
    n3 --> n10
    n5 --> n0
    n5 --> n2
    n5 --> n4
    n5 --> n9
    n6 --> n0
    n6 --> n2
    n6 --> n4
    n6 --> n9
    n6 --> n10
    n7 --> n8
    click n0 "../modules/QueryState.md"
    click n1 "../modules/RequestSourceLinksPanel.test.md"
    click n2 "../modules/RequestSourceLinksPanel.md"
    click n3 "../modules/TaskTimelinePanel.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/ProjectDetailPage.md"
    click n6 "../modules/TriagePage.md"
    click n7 "../modules/requestSourceService.md"
    click n8 "../modules/requestSource.md"
    click n9 "../modules/apiError.md"
    click n10 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RequestSourceLinksPanel.test](../modules/RequestSourceLinksPanel.test.md) |
| Inbound | [TaskTimelinePanel](../modules/TaskTimelinePanel.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [requestSourceService](../modules/requestSourceService.md) |
| Outbound | [requestSource](../modules/requestSource.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [safeUrl](../modules/safeUrl.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequestSourceLinksPanelProps](../entities/RequestSourceLinksPanelProps.md) | Interface | 19 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `RequestSourceLinksPanel` | <pre><code>&#40;&#123;&#10;    targetType&#44;&#10;    targetId&#44;&#10;    initialCount &#61; 0&#44;&#10;    title&#44;&#10;    compact &#61; false&#44;&#10;    onChanged&#44;&#10;&#125;&#58; RequestSourceLinksPanelProps&#41;</code></pre> | — | — |
