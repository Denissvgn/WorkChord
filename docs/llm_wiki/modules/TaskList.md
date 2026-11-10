# TaskList Module

**Path:** `frontend/src/components/tasks/TaskList.tsx`

## Description

Merge drafts capture the aggregate revision when their confirmation editor opens. Live list updates do not replace it at submission; conflicts retain title/selection and expose explicit current-input review.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/labelService` | `labelService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/label` | `Label` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/graphLimitError` | `isGraphLimitError` | — | compiler-dependent |
| `../../utils/taskFilters` | `filterTaskWithChildren` | — | compiler-dependent |
| `../../utils/visibleWork` | `selectVisibleWork` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/ConfirmDialog` | `ConfirmDialog` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/WorkFreshness` | `WorkFreshness` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `../ui` | `OverflowMenu` | — | compiler-dependent |
| `../ui/tone` | `statusTextClassName` | — | compiler-dependent |
| `./GuardedTaskModal` | `GuardedTaskModal` | — | compiler-dependent |
| `./PagedTaskBrowser` | `PagedTaskBrowser` | — | compiler-dependent |
| `./TaskAgentReadinessBadge` | `TaskAgentReadinessBadge` | — | compiler-dependent |
| `./TaskBulkOperationsPanel` | `TaskBulkOperationsPanel` | — | compiler-dependent |
| `./TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `@dnd-kit/core` | `DragEndEvent` | Declaration | erased |
| `@dnd-kit/core` | `DndContext`, `closestCenter`, `KeyboardSensor`, `PointerSensor`, `useSensor`, `useSensors` | — | compiler-dependent |
| `@dnd-kit/sortable` | `arrayMove`, `SortableContext`, `sortableKeyboardCoordinates`, `useSortable`, `verticalListSortingStrategy` | — | compiler-dependent |
| `@dnd-kit/utilities` | `CSS` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery`, `useMutation`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `ChevronRight`, `ChevronDown`, `CheckCircle2`, `Circle`, `Trash2`, `Plus`, `Edit`, `CornerDownRight`, `AlertTriangle`, `ArrowUpDown`, `GripVertical`, `Layers`, `Unlink`, `Bot`, `ClipboardCheck` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useId`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SortKey`, `TaskList`, `TaskMode` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/TaskList.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskList.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (4) |
| Outbound | `frontend` (21) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 8 | 0 |

> All 25 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskListProps](../entities/TaskListProps.md) | Interface | 70 | — | — |
| [TaskItemProps](../entities/TaskItemProps.md) | Interface | 740 | — | — |
| [TaskItemContentProps](../entities/TaskItemContentProps.md) | Interface | 792 | `TaskItemProps` | — |
| [SortKey](../entities/SortKey.md) | Type alias | 48 | `'priority' \| 'sort_order' \| 'status' \| 'title'` | — |
| [TaskMode](../entities/TaskMode.md) | Type alias | 49 | `'bulk' \| 'merge'` | — |
| [TaskOrderRequest](../entities/TaskOrderRequest.md) | Type alias | 50 | `Parameters<typeof taskService.reorder>[0]` | — |
| [ReorderVariables](../entities/ReorderVariables.md) | Type alias | 51 | <pre><code>&#123;&#10;    order&#58; TaskOrderRequest&#59;&#10;    undoOrder&#58; TaskOrderRequest&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskList` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    filters&#44;&#10;    sortKey&#44;&#10;    onSortKeyChange&#44;&#10;    hasActiveFilters &#61; false&#44;&#10;    activeViewName&#44;&#10;    onClearFilters&#44;&#10;    onCreateTask&#44;&#10;    requestedMode&#44;&#10;    onModeChange&#44;&#10;&#125;&#58; TaskListProps&#41;</code></pre> | — | — |