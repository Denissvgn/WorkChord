# TeamPage Module

**Path:** `frontend/src/pages/TeamPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TeamPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../components/iteration/IterationSelector` | `IterationSelector` | — | compiler-dependent |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` | — | compiler-dependent |
| `../components/team/ImportTeamModal` | `ImportTeamModal` | — | compiler-dependent |
| `../components/team/TeamForm` | `TeamForm` | — | compiler-dependent |
| `../components/team/TeamList` | `TeamList` | — | compiler-dependent |
| `../components/team/TeamProfileManager` | `TeamProfileManager` | — | compiler-dependent |
| `../components/ui` | `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/teamService` | `teamService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore`, `pickDefaultIteration` | — | compiler-dependent |
| `../types/team` | `TeamMember`, `TeamMemberProfile` | Declaration | erased |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useState`, `useEffect` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/TeamPage.tsx"]
    n1 --> n0
    click n1 "../modules/TeamPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamPageAction](../entities/TeamPageAction.md) | Type alias | 18 | `'assign' \| 'import'` | — |
