# SavedViewDashboardCards Module

**Path:** `frontend/src/components/dashboard/SavedViewDashboardCards.tsx`

## Description

_Auto-generated from `frontend/src/components/dashboard/SavedViewDashboardCards.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/seedDisplay` | `savedViewDisplay` | — | compiler-dependent |
| `../../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../../types/savedView` | `SavedViewDashboardCard`, `SavedViewType` | Declaration | erased |
| `../feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `ArrowRight`, `Bookmark`, `FolderOpen`, `Inbox`, `ListTodo` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SavedViewDashboardCards` |
| Constants | `viewTypeLabelKeys`, `viewTypeIcons`, `viewTypeChip` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/dashboard/SavedViewDashboardCards.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/i18n/seedDisplay.ts"]
    n3["frontend/src/pages/AnalyticsPage.tsx"]
    n4["frontend/src/services/savedViewService.ts"]
    n5["frontend/src/types/savedView.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n4
    n0 --> n5
    n2 --> n5
    n3 --> n0
    n3 --> n1
    n4 --> n5
    click n0 "../modules/SavedViewDashboardCards.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/seedDisplay.md"
    click n3 "../modules/AnalyticsPage.md"
    click n4 "../modules/savedViewService.md"
    click n5 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AnalyticsPage](../modules/AnalyticsPage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [seedDisplay](../modules/seedDisplay.md) |
| Outbound | [savedViewService](../modules/savedViewService.md) |
| Outbound | [savedView](../modules/savedView.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SavedViewDashboardCardsProps](../entities/SavedViewDashboardCardsProps.md) | Interface | 11 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SavedViewDashboardCards` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    title&#44;&#10;    className&#44;&#10;&#125;&#58; SavedViewDashboardCardsProps&#41;</code></pre> | — | — |
