# TriagePage Module

**Path:** `frontend/src/pages/TriagePage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TriagePage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/common/CollapsibleSection` | `CollapsibleSection` |
| `../components/common/Input` | `Input`, `RequiredIndicator` |
| `../components/common/Modal` | `Modal` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/labels/LabelSelector` | `LabelSelector` |
| `../components/requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` |
| `../components/tasks/TaskBriefEditor` | `TaskBriefEditor` |
| `../components/tasks/TaskDependencySelector` | `TaskDependencySelector` |
| `../components/tasks/taskEditorContract` | `emptyTaskBrief`, `newCriterion` |
| `../components/team/AssigneeRecommendationsPanel` | `AssigneeRecommendationsPanel` |
| `../components/ui` | `OverflowMenu`, `PageHeader`, `PageLayout` |
| `../i18n/i18n` | `i18n` |
| `../i18n/seedDisplay` | `templateDisplay` |
| `../services/iterationService` | `iterationService` |
| `../services/projectService` | `projectService` |
| `../services/savedViewService` | `savedViewService` |
| `../services/taskService` | `taskService` |
| `../services/teamService` | `teamService` |
| `../services/templateService` | `templateService` |
| `../services/triageService` | `triageService` |
| `../store/iterationStore` | `useIterationStore` |
| `../types/iteration` | `Iteration` |
| `../types/project` | `Project` |
| `../types/savedView` | `SavedView` |
| `../types/task` | `Task` |
| `../types/team` | `TeamMember` |
| `../types/template` | `WorkTemplate` |
| `../types/triage` | `TriageActionRequest`, `TriageClassificationSuggestion`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestion`, `TriageDuplicateSuggestionsResponse`, `TriageItem`, `TriageItemCreate`, `TriageItemStatus`, `TriageListParams`, `TriageSnoozeRequest`, `TriageTaskDraftResponse` |
| `../utils/apiError` | `getApiErrorMessage` |
| `../utils/formatDate` | `formatDateTime` |
| `../utils/safeUrl` | `safeExternalHref` |
| `../utils/templateDefaults` | `appendChecklistToDescription`, `getPayloadString`, `mergeLabels` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `clsx` | `clsx` |
| `lucide-react` | `AlertCircle`, `CheckCircle2`, `Clock3`, `CopyCheck`, `ExternalLink`, `Inbox`, `ListFilter`, `Loader2`, `MessageSquare`, `Plus`, `Search`, `Send`, `Sparkles`, `X`, `XCircle` |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState`, `FormEvent`, `ReactNode` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `t`, `statusOptions`, `statusLabelKeys` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
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
| [TaskListOption](../entities/TaskListOption.md) | Class | 178 | — | — |
| [ModalFrameProps](../entities/ModalFrameProps.md) | Class | 206 | — | — |
| [CreateTriageModalProps](../entities/CreateTriageModalProps.md) | Class | 229 | — | — |
| [DuplicateActionDefaults](../entities/DuplicateActionDefaults.md) | Class | 403 | — | — |
| [TriageActionModalProps](../entities/TriageActionModalProps.md) | Class | 410 | — | — |
| [ConvertTriageModalProps](../entities/ConvertTriageModalProps.md) | Class | 704 | — | — |
| [TriageDetailPanelProps](../entities/TriageDetailPanelProps.md) | Class | 1263 | — | — |
| [DuplicateSuggestionsPanelProps](../entities/DuplicateSuggestionsPanelProps.md) | Class | 1467 | — | — |
| [DuplicateSuggestionGroupProps](../entities/DuplicateSuggestionGroupProps.md) | Class | 1531 | — | — |
| [ClassificationPanelProps](../entities/ClassificationPanelProps.md) | Class | 1591 | — | — |
| [TriageRowProps](../entities/TriageRowProps.md) | Class | 1716 | — | — |
| [ConvertMutationInput](../entities/ConvertMutationInput.md) | Class | 1798 | — | — |
| [TriageLifecycleAction](../entities/TriageLifecycleAction.md) | Type alias | 401 | — | — |
| [ActionMutationInput](../entities/ActionMutationInput.md) | Type alias | 1792 | — | — |
