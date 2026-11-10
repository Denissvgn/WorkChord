# TriagePage Module

**Path:** `frontend/src/pages/TriagePage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TriagePage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/CollapsibleSection` | `CollapsibleSection` | — | compiler-dependent |
| `../components/common/Input` | `Input`, `RequiredIndicator` | — | compiler-dependent |
| `../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/labels/LabelSelector` | `LabelSelector` | — | compiler-dependent |
| `../components/requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` | — | compiler-dependent |
| `../components/tasks/TaskBriefEditor` | `TaskBriefEditor` | — | compiler-dependent |
| `../components/tasks/TaskDependencySelector` | `TaskDependencySelector` | — | compiler-dependent |
| `../components/tasks/taskEditorContract` | `emptyTaskBrief`, `newCriterion` | — | compiler-dependent |
| `../components/team/AssigneeRecommendationsPanel` | `AssigneeRecommendationsPanel` | — | compiler-dependent |
| `../components/ui` | `OverflowMenu`, `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../i18n/seedDisplay` | `templateDisplay` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../services/taskService` | `taskService` | — | compiler-dependent |
| `../services/teamService` | `teamService` | — | compiler-dependent |
| `../services/templateService` | `templateService` | — | compiler-dependent |
| `../services/triageService` | `triageService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `../types/project` | `Project` | Declaration | erased |
| `../types/savedView` | `SavedView` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `../types/team` | `TeamMember` | Declaration | erased |
| `../types/template` | `WorkTemplate` | Declaration | erased |
| `../types/triage` | `TriageActionRequest`, `TriageClassificationSuggestion`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestion`, `TriageDuplicateSuggestionsResponse`, `TriageItem`, `TriageItemCreate`, `TriageItemStatus`, `TriageListParams`, `TriageSnoozeRequest`, `TriageTaskDraftResponse` | Declaration | erased |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../utils/safeUrl` | `safeExternalHref` | — | compiler-dependent |
| `../utils/templateDefaults` | `appendChecklistToDescription`, `getPayloadString`, `mergeLabels` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `CheckCircle2`, `Clock3`, `CopyCheck`, `ExternalLink`, `Inbox`, `ListFilter`, `Loader2`, `MessageSquare`, `Plus`, `Search`, `Send`, `Sparkles`, `X`, `XCircle` | — | compiler-dependent |
| `react` | `FormEvent`, `ReactNode` | Declaration | erased |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `t`, `statusOptions`, `statusLabelKeys` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/TriagePage.tsx"]
    n1 --> n0
    click n1 "../modules/TriagePage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (33) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 33 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskListOption](../entities/TaskListOption.md) | Interface | 178 | — | — |
| [ModalFrameProps](../entities/ModalFrameProps.md) | Interface | 206 | — | — |
| [CreateTriageModalProps](../entities/CreateTriageModalProps.md) | Interface | 229 | — | — |
| [DuplicateActionDefaults](../entities/DuplicateActionDefaults.md) | Interface | 403 | — | — |
| [TriageActionModalProps](../entities/TriageActionModalProps.md) | Interface | 410 | — | — |
| [ConvertTriageModalProps](../entities/ConvertTriageModalProps.md) | Interface | 704 | — | — |
| [TriageDetailPanelProps](../entities/TriageDetailPanelProps.md) | Interface | 1263 | — | — |
| [DuplicateSuggestionsPanelProps](../entities/DuplicateSuggestionsPanelProps.md) | Interface | 1467 | — | — |
| [DuplicateSuggestionGroupProps](../entities/DuplicateSuggestionGroupProps.md) | Interface | 1531 | — | — |
| [ClassificationPanelProps](../entities/ClassificationPanelProps.md) | Interface | 1591 | — | — |
| [TriageRowProps](../entities/TriageRowProps.md) | Interface | 1716 | — | — |
| [ConvertMutationInput](../entities/ConvertMutationInput.md) | Interface | 1798 | — | — |
| [TriageLifecycleAction](../entities/TriageLifecycleAction.md) | Type alias | 401 | `'accept' \| 'decline' \| 'snooze' \| 'duplicate'` | — |
| [ActionMutationInput](../entities/ActionMutationInput.md) | Type alias | 1792 | <pre><code>&#124; &#123; type&#58; &#39;accept&#39;&#59; itemId&#58; number&#59; payload&#58; TriageActionRequest &#125;&#10;    &#124; &#123; type&#58; &#39;decline&#39;&#59; itemId&#58; number&#59; payload&#58; TriageActionRequest &#125;&#10;    &#124; &#123; type&#58; &#39;snooze&#39;&#59; itemId&#58; number&#59; payload&#58; TriageSnoozeRequest &#125;&#10;    &#124; &#123; type&#58; &#39;duplicate&#39;&#59; itemId&#58; number&#59; payload&#58; TriageDuplicateRequest &#125;</code></pre> | — |
