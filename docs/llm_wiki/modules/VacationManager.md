# VacationManager Module

**Path:** `frontend/src/components/team/VacationManager.tsx`

## Description

_Auto-generated from `frontend/src/components/team/VacationManager.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/teamService` | `teamService` |
| `../../types/team` | `Vacation`, `TeamMember` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `../common/Modal` | `Modal` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` |
| `lucide-react` | `Plane`, `Trash2`, `Plus`, `Calendar`, `Upload` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `VacationManager` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/common/useConfirmDialog.tsx"]
    n4["frontend/src/components/team/TeamList.tsx"]
    n5["frontend/src/components/team/VacationManager.tsx"]
    n6["frontend/src/services/teamService.ts"]
    n7["frontend/src/types/team.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n9["frontend/src/utils/formatDate.ts"]
    n4 --> n0
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/useConfirmDialog.md"
    click n4 "../modules/TeamList.md"
    click n5 "../modules/VacationManager.md"
    click n6 "../modules/teamService.md"
    click n7 "../modules/types_team.md"
    click n8 "../modules/apiError.md"
    click n9 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamList](../modules/TeamList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [useConfirmDialog](../modules/useConfirmDialog.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [VacationManagerProps](../entities/VacationManagerProps.md) | Class | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `VacationManager` | `({ member, onClose }: VacationManagerProps)` | — | — |
