# TeamForm Module

**Path:** `frontend/src/components/team/TeamForm.tsx`

## Description

_Auto-generated from `frontend/src/components/team/TeamForm.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/teamService` | `teamService` |
| `../../types/team` | `TeamMember`, `TeamMemberCreate`, `TeamMemberProfile` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/CollapsibleSection` | `CollapsibleSection` |
| `../common/Input` | `Input` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useMutation`, `useQueryClient`, `useQuery` |
| `lucide-react` | `Save` |
| `react` | `useEffect`, `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TeamForm` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/CollapsibleSection.tsx"]
    n2["frontend/src/components/common/Input.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/team/TeamForm.test.tsx"]
    n5["frontend/src/components/team/TeamForm.tsx"]
    n6["frontend/src/pages/TeamPage.tsx"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/types/team.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n9
    n4 --> n5
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n6 --> n3
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/CollapsibleSection.md"
    click n2 "../modules/Input.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/TeamForm.test.md"
    click n5 "../modules/TeamForm.md"
    click n6 "../modules/TeamPage.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/types_team.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamForm.test](../modules/TeamForm.test.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [CollapsibleSection](../modules/CollapsibleSection.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
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
| [TeamFormProps](../entities/TeamFormProps.md) | Class | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TeamForm` | `({     iterationId,     initialData,     initialProfile,     onSuccess,     onCancel,     onStateChange, }: TeamFormProps)` | — | — |
