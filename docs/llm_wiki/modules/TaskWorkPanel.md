# TaskWorkPanel Module

**Path:** `frontend/src/components/tasks/TaskWorkPanel.tsx`

## Description

Commit and uncommit commands retain original source and selected-target aggregate maps with command input. Scope conflicts preserve the reason and map until explicit current comparison. Obsolete request callbacks cannot clear replacement drafts or pending state.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../features/identity/identityContext` | `useIdentity` | — | compiler-dependent |
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedRevisions` | Declaration | erased |
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/task` | `CriterionProgress`, `Task` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `./TaskOwnerAcceptance` | `TaskOwnerAcceptance`, `VERIFIED_PUBLISHER_CODE` | — | compiler-dependent |
| `./TaskPostponeForm` | `TaskPostponeForm` | — | compiler-dependent |
| `./TaskPostponementPanel` | `TaskPostponementPanel` | — | compiler-dependent |
| `./TaskReviewHistory` | `TaskReviewHistory` | — | compiler-dependent |
| `./TaskReviewer` | `TaskReviewer` | — | compiler-dependent |
| `./useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `./useTaskReviewer` | `useTaskReviewer` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery` | — | compiler-dependent |
| `react` | `useEffect`, `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskWorkPanel` |
| Constants | `DRAFT_TTL_MS`, `PROGRESS_STATES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskWorkPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (5) |
| Outbound | `frontend` (21) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 26 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskWorkPanel` | <pre><code>&#40;&#123; task&#44; disabled&#44; draftKey&#44; onDirty&#44; onPending&#44; onUpdated&#44; onReload&#44; onEditBrief&#44; offerDispatch &#61; false &#125;&#58; &#123;&#10;    task&#58; Task&#59; disabled&#58; boolean&#59; draftKey&#58; string &#124; null&#59; onDirty&#58; &#40;dirty&#58; boolean&#41; &#61;&#62; void&#59;&#10;    onPending&#58; &#40;pending&#58; boolean&#41; &#61;&#62; void&#59; onUpdated&#58; &#40;task&#58; Task&#41; &#61;&#62; void&#59; onReload&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    &#47;&#42;&#42; Opens the brief for editing&#44; so a missing acceptance criterion can be added&#46; &#42;&#47;&#10;    onEditBrief&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    &#47;&#42;&#42;&#10;     &#42; A connected agent has not been sent the task&#58; it gets the task through dispatch&#44; which the&#10;     &#42; task view&#39;s header offers&#44; so manual Start work is not offered here&#46;&#10;     &#42;&#47;&#10;    offerDispatch&#63;&#58; boolean&#59;&#10;&#125;&#41;</code></pre> | — | — |
