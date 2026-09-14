# TeamPage Module

**Path:** `frontend/src/pages/TeamPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TeamPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` |
| `../components/team/ImportTeamModal` | `ImportTeamModal` |
| `../components/team/TeamForm` | `TeamForm` |
| `../components/team/TeamList` | `TeamList` |
| `../components/team/TeamProfileManager` | `TeamProfileManager` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../services/iterationService` | `iterationService` |
| `../services/teamService` | `teamService` |
| `../store/iterationStore` | `useIterationStore` |
| `../types/team` | `TeamMember`, `TeamMemberProfile` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useState`, `useEffect` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/planning/PlanReturnBar.tsx"]
    n2["frontend/src/components/team/ImportTeamModal.tsx"]
    n3["frontend/src/components/team/TeamForm.tsx"]
    n4["frontend/src/components/team/TeamList.tsx"]
    n5["frontend/src/components/team/TeamProfileManager.tsx"]
    n6["frontend/src/components/ui/index.ts"]
    n7["frontend/src/pages/TeamPage.tsx"]
    n8["frontend/src/services/iterationService.ts"]
    n9["frontend/src/services/teamService.ts"]
    n10["frontend/src/store/iterationStore.ts"]
    n11["frontend/src/types/team.ts"]
    n2 --> n9
    n3 --> n0
    n3 --> n9
    n3 --> n11
    n4 --> n0
    n4 --> n9
    n4 --> n11
    n5 --> n0
    n5 --> n9
    n5 --> n11
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n7 --> n11
    n9 --> n11
    click n0 "../modules/QueryState.md"
    click n1 "../modules/PlanReturnBar.md"
    click n2 "../modules/ImportTeamModal.md"
    click n3 "../modules/TeamForm.md"
    click n4 "../modules/TeamList.md"
    click n5 "../modules/TeamProfileManager.md"
    click n6 "../modules/index.md"
    click n7 "../modules/TeamPage.md"
    click n8 "../modules/iterationService.md"
    click n9 "../modules/teamService.md"
    click n10 "../modules/iterationStore.md"
    click n11 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [ImportTeamModal](../modules/ImportTeamModal.md) |
| Outbound | [TeamForm](../modules/TeamForm.md) |
| Outbound | [TeamList](../modules/TeamList.md) |
| Outbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamPageAction](../entities/TeamPageAction.md) | Type alias | 17 | — | — |
