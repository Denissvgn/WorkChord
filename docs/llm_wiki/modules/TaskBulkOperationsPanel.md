# TaskBulkOperationsPanel Module

**Path:** `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskBulkAction`, `TaskBulkOperationResponse`, `TaskStatus` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/routingCheck` | `RoutingChangeItem` | Specifier | compiler-dependent |
| `../../utils/routingCheck` | `resultsNeedingRouting`, `routingChangeItems`, `routingNeedsResolution` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../ui/OverflowMenu` | `OverflowMenu` | — | compiler-dependent |
| `./RoutingCheckNotice` | `RoutingResultsList` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Trash2` | — | compiler-dependent |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BulkSelectedTask`, `TaskBulkOperationsPanel` |
| Constants | `STATUS_OPTIONS`, `AUTO`, `NONE`, `selectClassName` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskBulkOperationsPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (3) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [BulkRejected](../entities/BulkRejected.md) | Class | 59 | `Error` | — |
| [TaskBulkOperationsPanelProps](../entities/TaskBulkOperationsPanelProps.md) | Interface | 24 | — | — |
| [RoutingDecision](../entities/RoutingDecision.md) | Interface | 49 | — | A dry run that found tasks whose reviewer would no longer fit; nothing was written. It keeps the |
| [BulkKind](../entities/BulkKind.md) | Type alias | 19 | `'assign' \| 'status' \| 'priority' \| 'iteration' \| 'project' \| 'clearProject' \| 'milestone' \| 'clearMilestone' \| 'addLabels' \| 'removeLabels' \| 'flags' \| 'delete'` | — |
| [BulkSelectedTask](../entities/BulkSelectedTask.md) | Type alias | 22 | `Pick<Task, 'id' \| 'title' \| 'version'>` | What the bar needs of a selected task. |
| [RoutingChoice](../entities/RoutingChoice.md) | Type alias | 43 | `'apply_suggestion' \| 'keep'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskBulkOperationsPanel` | <pre><code>&#40;&#123;&#10;    iterationId&#44; selectedTasks&#44; matchingCount&#44; onSelectAll&#44; onClearSelection&#44; onMerge&#44; openAssign &#61; false&#44;&#10;&#125;&#58; TaskBulkOperationsPanelProps&#41;</code></pre> | — | The bar shown while tasks are selected. Each change is one choice and one Apply: the server |
