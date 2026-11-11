# TeamProfileManager Module

**Path:** `frontend/src/components/team/TeamProfileManager.tsx`

## Description

Profile and skill writes send the original complete observed revisions. Deletion confirmations capture independent immutable observations, and conflicts preserve input for explicit reapply. Skill drafts prevent selection from moving their owning profile. The create-profile and add-capability forms open on request, and the selected profile's detail leads the rail.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../features/mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/team` | `TeamMemberAssignmentMode`, `TeamMemberProfile`, `TeamMemberProfileCreate`, `TeamMemberProfileKind`, `TeamMemberProfileSkill`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileUpdate` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Plus`, `Trash2` | — | compiler-dependent |
| `react` | `useEffect`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TeamProfileManager` |
| Constants | `PROFILE_KINDS`, `ASSIGNMENT_MODES`, `emptyProfileForm`, `emptySkillForm` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/team/TeamProfileManager.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TeamProfileManager.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (10) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamProfileManagerProps](../entities/TeamProfileManagerProps.md) | Interface | 68 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TeamProfileManager` | <pre><code>&#40;&#123;&#10;    currentIterationId &#61; null&#44;&#10;    currentIterationName &#61; null&#44;&#10;    assignedProfileIds &#61; &#91;&#93;&#44;&#10;    onAssignProfile&#44;&#10;&#125;&#58; TeamProfileManagerProps&#41;</code></pre> | — | — |