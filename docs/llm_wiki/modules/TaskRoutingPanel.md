# TaskRoutingPanel Module

**Path:** `frontend/src/components/agent/TaskRoutingPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/agent/TaskRoutingPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAgentAccess` | `useAgentAccess` | — | compiler-dependent |
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `../../types/agent` | `AgentAssignmentPurpose`, `AgentRoutingCandidate`, `AgentTaskAssignment`, `AssessmentReasonCode`, `ModelContextTier`, `ModelReasoningTier`, `TaskDifficultyAxes`, `TaskDifficultyScore`, `TaskReviewMode`, `TaskRoutingAssessment`, `TaskRoutingAssessmentCommand`, `TaskSkillLevel` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/apiError` | `normalizeApiError` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../../utils/modelRouting` | `ASSESSMENT_REASON_CODES`, `createAgentCommandMetadata`, `deriveDifficultyBand`, `formatRoutingCode`, `minimumReviewMode`, `MODEL_AWARE_ROUTING_FEATURE`, `parseRoutingTags`, `reviewModeMeets` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input`, `RequiredIndicator` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `./RoutingCandidateComparison` | `RoutingCandidateComparison` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `CheckCircle2`, `Plus`, `RefreshCw`, `Route`, `Trash2` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |
| `react` | `useEffect`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskRoutingPanel` |
| Constants | `DEFAULT_DRAFT`, `AXIS_KEYS`, `REVIEW_MODES`, `SKILL_CATALOG_READ_SCOPES`, `TEAM_ASSIGNMENT_READ_SCOPES` |
| Module calls | `SKILL_CATALOG_READ_SCOPES = Set`, `TEAM_ASSIGNMENT_READ_SCOPES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskRoutingPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskRoutingPanelProps](../entities/TaskRoutingPanelProps.md) | Interface | 54 | — | — |
| [AssessmentDraft](../entities/AssessmentDraft.md) | Interface | 59 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskRoutingPanel` | `({ task, onAssigned }: TaskRoutingPanelProps)` | — | — |
