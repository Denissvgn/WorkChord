# TeamProfileManager Module

**Path:** `frontend/src/components/team/TeamProfileManager.tsx`

## Description

Profile and skill writes send the original complete observed revisions. Deletion confirmations capture independent immutable observations, and conflicts preserve input for explicit reapply. Skill drafts prevent selection from moving their owning profile.

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/usePlanningObservation` | `usePlanningObservation` |
| `../../services/planningInputService` | `planningInputService` |
| `../../services/teamService` | `teamService` |
| `../../types/team` | `TeamMemberAssignmentMode`, `TeamMemberProfile`, `TeamMemberProfileCreate`, `TeamMemberProfileKind`, `TeamMemberProfileSkill`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileUpdate` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `Plus`, `Trash2` |
| `react` | `useEffect`, `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TeamProfileManager` |
| Constants | `PROFILE_KINDS`, `ASSIGNMENT_MODES`, `emptyProfileForm`, `emptySkillForm` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/common/useConfirmDialog.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n5["frontend/src/components/team/TeamProfileManager.tsx"]
    n6["frontend/src/features/usePlanningObservation.ts"]
    n7["frontend/src/pages/TeamPage.tsx"]
    n8["frontend/src/services/planningInputService.ts"]
    n9["frontend/src/services/teamService.ts"]
    n10["frontend/src/types/team.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n11
    n4 --> n5
    n4 --> n10
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n6 --> n8
    n6 --> n11
    n7 --> n3
    n7 --> n5
    n7 --> n9
    n7 --> n10
    n9 --> n8
    n9 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/useConfirmDialog.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/TeamProfileManager.test.md"
    click n5 "../modules/TeamProfileManager.md"
    click n6 "../modules/usePlanningObservation.md"
    click n7 "../modules/TeamPage.md"
    click n8 "../modules/planningInputService.md"
    click n9 "../modules/teamService.md"
    click n10 "../modules/types_team.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [useConfirmDialog](../modules/useConfirmDialog.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [usePlanningObservation](../modules/usePlanningObservation.md) |
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
| [TeamProfileManagerProps](../entities/TeamProfileManagerProps.md) | Class | 66 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TeamProfileManager` | `({     currentIterationId = null,     currentIterationName = null,     assignedProfileIds = [],     onAssignProfile, }: TeamProfileManagerProps)` | — | — |