# overviewSignals Module

**Path:** `frontend/src/features/overview/overviewSignals.ts`

## Description

_Auto-generated from `frontend/src/features/overview/overviewSignals.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `../../types/agent` | `AgentPipeline` | Declaration | erased |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/task` | `Task`, `TaskReference` | Declaration | erased |
| `../../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `../../utils/visibleWork` | `selectVisibleWork` | — | compiler-dependent |
| `../savedViews/taskViewParams` | `writeFiltersToSearchParams` | — | compiler-dependent |
| `../scope/workScope` | `ScopeIteration`, `ScopeProject` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ATTENTION_KINDS`, `AttentionCandidate`, `AttentionKind`, `DeliveryRisk`, `OVERVIEW_COUNT_LIST_PARAM`, `OVERVIEW_TASK_LISTS`, `OverviewCountList`, `OverviewTaskList`, `PIPELINE_STAGES`, `PipelineStage`, `backlogRoots`, `calendarDaysLeft`, `daysLeftToLatestEnd`, `deliveryRisk`, `isOpenIteration`, `iterationsInView`, `listTasks`, `overviewCountListHref`, `overviewListFilters`, `parseOverviewCountList`, `pickAttention`, `pipelineStageHref`, `pipelineTasksInScope`, `selectWorkNow`, `taskListHref` |
| Constants | `OVERVIEW_TASK_LISTS`, `PIPELINE_STAGES`, `DONE_STATUSES`, `OVERVIEW_COUNT_LIST_PARAM`, `MS_PER_DAY`, `RISK_RANK`, `ATTENTION_KINDS` |
| Module calls | `DONE_STATUSES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/PipelineView.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/features/overview/overviewSignals.test.ts"]
    n3["frontend/src/features/overview/overviewSignals.ts"]
    n4["frontend/src/features/savedViews/taskViewParams.ts"]
    n5["frontend/src/features/scope/workScope.ts"]
    n6["frontend/src/pages/OverviewPage.tsx"]
    n7["frontend/src/types/agent.ts"]
    n8["frontend/src/types/iteration.ts"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/taskFilterDefaults.ts"]
    n11["frontend/src/utils/visibleWork.ts"]
    n0 --> n1
    n0 --> n3
    n0 --> n5
    n0 --> n9
    n1 --> n10
    n2 --> n3
    n2 --> n4
    n2 --> n8
    n2 --> n9
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n1
    n4 --> n10
    n6 --> n3
    n6 --> n5
    n6 --> n8
    n6 --> n9
    n7 --> n9
    n8 --> n9
    n10 --> n1
    n11 --> n1
    n11 --> n9
    click n0 "../modules/PipelineView.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/overviewSignals.test.md"
    click n3 "../modules/overviewSignals.md"
    click n4 "../modules/taskViewParams.md"
    click n5 "../modules/workScope.md"
    click n6 "../modules/OverviewPage.md"
    click n7 "../modules/types_agent.md"
    click n8 "../modules/types_iteration.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/taskFilterDefaults.md"
    click n11 "../modules/visibleWork.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PipelineView](../modules/PipelineView.md) |
| Inbound | [overviewSignals.test](../modules/overviewSignals.test.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [taskViewParams](../modules/taskViewParams.md) |
| Outbound | [workScope](../modules/workScope.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |
| Outbound | [visibleWork](../modules/visibleWork.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AttentionCandidate](../entities/AttentionCandidate.md) | Interface | 227 | — | — |
| [OverviewTaskList](../entities/OverviewTaskList.md) | Type alias | 23 | `keyof typeof OVERVIEW_TASK_LISTS` | — |
| [PipelineStage](../entities/PipelineStage.md) | Type alias | 55 | `typeof PIPELINE_STAGES[number]` | — |
| [OverviewCountList](../entities/OverviewCountList.md) | Type alias | 78 | `OverviewTaskList` | A list Overview can show itself, for task counts that no single Tasks list holds: a sum |
| [DeliveryRisk](../entities/DeliveryRisk.md) | Type alias | 185 | `'overdue' \| 'late-start' \| 'outside-limits' \| 'blocked' \| null` | — |
| [AttentionKind](../entities/AttentionKind.md) | Type alias | 225 | `typeof ATTENTION_KINDS[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `overviewListFilters` | `(list: OverviewTaskList) -> TaskFilters` | — | — |
| `listTasks` | `(roots: Task[], list: OverviewTaskList)` | — | The tasks the Tasks list shows for this list: the leaves of the filtered tree. |
| `taskListHref` | `(list: OverviewTaskList, extra: Record<string, string> = {})` | — | The Tasks link that shows `list`; `extra` adds parameters such as a selection mode. |
| `pipelineStageHref` | `(stage: PipelineStage)` | — | The Tasks link that opens the pipeline view on one stage. |
| `pipelineTasksInScope` | `(tasks: Task[], project: ScopeProject \| undefined, iteration: ScopeIteration \| undefined)` | — | The pipeline tasks that belong to one scope, by the rule the pipeline view applies. |
| `parseOverviewCountList` | `(value: string \| null) -> OverviewCountList \| null` | — | — |
| `overviewCountListHref` | `(list: OverviewCountList)` | — | The Overview link that opens one of its own lists; the scope is added by the caller. |
| `backlogRoots` | `(references: TaskReference[]) -> Task[]` | — | Backlog work as Overview reads it. The backlog lookup returns task references, which carry |
| `isOpenIteration` | `(iteration: Pick<Iteration, 'start_date' \| 'end_date'>, today: string)` | — | True when today falls within the iteration's dates. |
| `iterationsInView` | `(iterations: Iteration[], project: ScopeProject \| undefined, iteration: ScopeIteration \| undefined, today: string) -> Iteration[]` | — | The iterations Overview counts: the one in scope. With All projects and no iteration chosen, |
| `calendarDaysLeft` | `(iteration: Pick<Iteration, 'end_date'>, today: string) -> number \| null` | — | Calendar days from today to the iteration's end date; 0 once it has ended. |
| `daysLeftToLatestEnd` | `(iterations: Pick<Iteration, 'id' \| 'end_date'>[], today: string) -> number \| null` | — | Calendar days from today to the latest end among the iterations: with All projects the |
| `deliveryRisk` | `(task: Task) -> DeliveryRisk` | — | Why an open task threatens delivery, most severe reason first. |
| `selectWorkNow` | `(roots: Task[], limit = 5)` | — | The next open tasks to work on, highest delivery risk first, then by due date and priority. |
| `pickAttention` | `(candidates: AttentionCandidate[]) -> AttentionCandidate \| null` | — | The most severe candidate: kinds in severity order, then the larger count, then the earlier iteration. |
