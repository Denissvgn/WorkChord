# TriagePage Module

**Path:** `frontend/src/pages/TriagePage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TriagePage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/triage/ConvertTriageDrawer` | `ConvertTriageDrawer` | — | compiler-dependent |
| `../components/triage/CreateTriageDrawer` | `CreateTriageDrawer` | — | compiler-dependent |
| `../components/triage/TriageActionModal` | `TriageActionModal` | — | compiler-dependent |
| `../components/triage/TriageDetailPanel` | `TriageDetailPanel` | — | compiler-dependent |
| `../components/triage/TriageList` | `TriageList` | — | compiler-dependent |
| `../components/triage/TriageToolbar` | `TriageToolbar` | — | compiler-dependent |
| `../components/triage/triageUtils` | `DuplicateActionDefaults`, `TriageLifecycleAction` | Specifier | compiler-dependent |
| `../components/triage/triageUtils` | `AGENT_SOURCE_LABEL_KEYS`, `getErrorMessage`, `isDueSnoozed`, `makeLookup`, `toLocalDateTimeInputValue`, `triageFiltersFromSavedView` | — | compiler-dependent |
| `../components/ui` | `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../features/firstRun/firstRunSteps` | `firstRunPlanHref` | — | compiler-dependent |
| `../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../features/mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../services/triageService` | `triageService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../types/triage` | `TriageActionRequest`, `TriageConvertToTaskRequest`, `TriageConvertToTaskResponse`, `TriageDuplicateRequest`, `TriageDuplicateSuggestion`, `TriageItem`, `TriageItemCreate`, `TriageItemStatus`, `TriageListParams`, `TriageSnoozeRequest` | Declaration | erased |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `CheckCircle2`, `ExternalLink`, `Plus`, `X` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

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
    n1["frontend/src/pages/TriagePage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TriagePage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ConvertMutationInput](../entities/ConvertMutationInput.md) | Interface | 51 | — | — |
| [ActionMutationInput](../entities/ActionMutationInput.md) | Type alias | 45 | <pre><code>&#124; &#123; type&#58; &#39;accept&#39;&#59; itemId&#58; number&#59; payload&#58; TriageActionRequest &#125;&#10;    &#124; &#123; type&#58; &#39;decline&#39;&#59; itemId&#58; number&#59; payload&#58; TriageActionRequest &#125;&#10;    &#124; &#123; type&#58; &#39;snooze&#39;&#59; itemId&#58; number&#59; payload&#58; TriageSnoozeRequest &#125;&#10;    &#124; &#123; type&#58; &#39;duplicate&#39;&#59; itemId&#58; number&#59; payload&#58; TriageDuplicateRequest &#125;</code></pre> | — |
