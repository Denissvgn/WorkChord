# TeamList Module

**Path:** `frontend/src/components/team/TeamList.tsx`

## Description

_Auto-generated from `frontend/src/components/team/TeamList.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/planningInputService` | `planningInputService`, `ObservedRevisions` |
| `../../services/teamService` | `teamService` |
| `../../types/team` | `MemberCapacity`, `MemberWorkload`, `TeamMember` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../feedback/toast` | `useToast` |
| `./VacationManager` | `VacationManager` |
| `@tanstack/react-query` | `useQuery`, `useMutation`, `useQueryClient` |
| `lucide-react` | `ChevronDown`, `ChevronUp`, `Loader2`, `Trash2`, `User`, `Plane`, `Calendar` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TeamList` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/useConfirmDialog.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/feedback/toast.ts"]
    n4["frontend/src/components/team/TeamList.tsx"]
    n5["frontend/src/components/team/VacationManager.tsx"]
    n6["frontend/src/pages/TeamPage.tsx"]
    n7["frontend/src/services/planningInputService.ts"]
    n8["frontend/src/services/teamService.ts"]
    n9["frontend/src/types/team.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n10
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n5 --> n1
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n6 --> n2
    n6 --> n4
    n6 --> n8
    n6 --> n9
    n8 --> n7
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/useConfirmDialog.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/toast.md"
    click n4 "../modules/TeamList.md"
    click n5 "../modules/VacationManager.md"
    click n6 "../modules/TeamPage.md"
    click n7 "../modules/planningInputService.md"
    click n8 "../modules/teamService.md"
    click n9 "../modules/types_team.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [useConfirmDialog](../modules/useConfirmDialog.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [toast](../modules/toast.md) |
| Outbound | [VacationManager](../modules/VacationManager.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamListProps](../entities/TeamListProps.md) | Class | 15 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TeamList` | `({ iterationId, onEdit }: TeamListProps)` | — | — |
