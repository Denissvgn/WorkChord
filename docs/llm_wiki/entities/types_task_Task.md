# Task

**Location:** `frontend/src/types/task.ts:95`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `Task` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `iteration_revision` | `number` | No | — | — |
| `effective_is_deferred` | `boolean` | No | — | — |
| `effective_is_optional` | `boolean` | No | — | — |
| `metric_contract_version` | `number` | No | — | — |
| `is_late_start` | `boolean` | No | — | — |
| `is_iteration_overflow` | `boolean` | No | — | — |
| `is_project_target_overflow` | `boolean` | No | — | — |
| `is_implemented` | `boolean` | No | — | — |
| `is_accepted` | `boolean` | No | — | — |
| `acceptance_unknown` | `boolean` | No | — | — |
| `owner_profile_id` | `number \| null` | No | — | — |
| `owner` | `TaskAssignee \| null` | No | — | — |
| `ownership_provenance` | `string` | No | — | — |
| `nominal_day_hours` | `number` | No | — | — |
| `estimate_provenance` | `string` | No | — | — |
| `brief` | `TaskBrief \| null` | No | — | — |
| `brief_revision` | `number` | No | — | — |
| `brief_provenance` | `string` | No | — | — |
| `legacy_description` | `string \| null` | No | — | — |
| `brief_migration_notes` | `string[]` | No | — | — |
| `progress` | `TaskProgress \| null` | No | — | — |
| `artifact_revision` | `number` | No | — | — |
| `execution_mode` | `'manual' \| 'scheduled'` | No | — | — |
| `blocked_reason` | `string \| null` | No | — | — |
| `canceled_at` | `string \| null` | No | — | — |
| `canceled_reason` | `string \| null` | No | — | — |
| `detail_context` | `TaskDetail` | No | — | — |
| `baseline_start_date` | `string \| null` | No | — | — |
| `baseline_end_date` | `string \| null` | No | — | — |
| `baseline_revision` | `number` | No | — | — |
| `baseline_provenance` | `string` | No | — | — |
| `started_at` | `string \| null` | No | — | — |
| `resolved_at` | `string \| null` | No | — | — |
| `accepted_at` | `string \| null` | No | — | — |
| `id` | `number` | Yes | — | — |
| `iteration_id` | `number \| null` | Yes | — | — |
| `project_id` | `number \| null` | No | — | — |
| `milestone_id` | `number \| null` | No | — | — |
| `parent_id` | `number \| null` | No | — | — |
| `title` | `string` | Yes | — | — |
| `description` | `string` | No | — | — |
| `priority` | `number` | Yes | — | — |
| `effort_days` | `number \| null` | Yes | — | — |
| `effort_hours` | `number \| null` | Yes | — | — |
| `project` | `TaskProject \| null` | No | — | — |
| `milestone` | `TaskMilestone \| null` | No | — | — |
| `assignee` | `TaskAssignee \| null` | No | — | — |
| `status` | `TaskStatus` | Yes | — | — |
| `displayed_state` | `TaskDisplayedState` | No | — | — |
| `successor_task_id` | `number \| null` | No | — | — |
| `successor_kind` | `'replacement' \| 'supersession' \| null` | No | — | — |
| `start_date` | `string \| null` | No | — | — |
| `end_date` | `string \| null` | No | — | — |
| `actual_start_date` | `string \| null` | No | — | — |
| `actual_end_date` | `string \| null` | No | — | — |
| `min_start_date` | `string \| null` | No | — | — |
| `max_end_date` | `string \| null` | No | — | — |
| `is_overdue` | `boolean` | Yes | — | — |
| `is_delayed` | `boolean` | Yes | — | — |
| `is_composite` | `boolean` | Yes | — | — |
| `is_optional` | `boolean` | Yes | — | — |
| `is_deferred` | `boolean` | Yes | — | — |
| `is_outside_constraints` | `boolean` | No | — | — |
| `tags` | `string[]` | Yes | — | — |
| `sort_order` | `number` | Yes | — | — |
| `external_key` | `string \| null` | No | — | — |
| `source` | `string \| null` | No | — | — |
| `source_url` | `string \| null` | No | — | — |
| `external_links` | `ExternalLink[]` | Yes | — | — |
| `request_count` | `number` | Yes | — | — |
| `agent_readiness` | `TaskAgentReadiness` | Yes | — | — |
| `version` | `number` | Yes | — | — |
| `claimed_by` | `TaskClaimedBy \| null` | No | — | — |
| `agent_working` | `boolean \| null` | No | — | — |
| `claim_expires_at` | `string \| null` | No | — | — |
| `updated_at` | `string \| null` | No | — | — |
| `children` | `Task[]` | Yes | — | — |
| `dependencies` | `number[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Task (frontend/src/types/task.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["TaskRoutingPanel (frontend/src/components/agent/TaskRoutingPanel.tsx)"]
    n3["TaskEditDrawer (frontend/src/components/gantt/TaskEditDrawer.tsx)"]
    n4["frontend/src/components/planning/PlanBlockersSection.tsx"]
    n5["PlanScheduleSection (frontend/src/components/planning/PlanScheduleSection.tsx)"]
    n6["PlanWorkSection (frontend/src/components/planning/PlanWorkSection.tsx)"]
    n7["ProjectTasksTab (frontend/src/components/projects/ProjectTasksTab.tsx)"]
    n8["frontend/src/components/projects/ProjectTaskTree.test.tsx"]
    n9["ProjectTaskTree (frontend/src/components/projects/ProjectTaskTree.tsx)"]
    n10["frontend/src/components/releases/ReleaseForm.tsx"]
    n11["frontend/src/components/tasks/assigneeDisplay.test.tsx"]
    n12["frontend/src/components/tasks/AssigneePicker.test.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/TaskRoutingPanel.md"
    click n3 "../modules/TaskEditDrawer.md"
    click n4 "../modules/PlanBlockersSection.md"
    click n5 "../modules/PlanScheduleSection.md"
    click n6 "../modules/PlanWorkSection.md"
    click n7 "../modules/ProjectTasksTab.md"
    click n8 "../modules/ProjectTaskTree.test.md"
    click n9 "../modules/ProjectTaskTree.md"
    click n10 "../modules/ReleaseForm.md"
    click n11 "../modules/assigneeDisplay.test.md"
    click n12 "../modules/AssigneePicker.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `acceptance_unknown`, `accepted_at`, `actual_end_date`, `actual_start_date`, `agent_readiness`, `agent_working`, `artifact_revision`, `assignee`, `baseline_end_date`, `baseline_provenance`, `baseline_revision`, `baseline_start_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `TaskRoutingPanel` | type_reference | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
| `TaskEditDrawer` | type_reference | [TaskEditDrawer](../modules/TaskEditDrawer.md) | — |
| `PlanBlockersSection` | import | [PlanBlockersSection](../modules/PlanBlockersSection.md) | — |
| `PlanScheduleSection` | type_reference | [PlanScheduleSection](../modules/PlanScheduleSection.md) | — |
| `PlanWorkSection` | type_reference | [PlanWorkSection](../modules/PlanWorkSection.md) | — |
| `ProjectTasksTab` | type_reference | [ProjectTasksTab](../modules/ProjectTasksTab.md) | — |
| `ProjectTaskTree.test` | import | [ProjectTaskTree.test](../modules/ProjectTaskTree.test.md) | — |
| `ProjectTaskTree` | type_reference | [ProjectTaskTree](../modules/ProjectTaskTree.md) | — |
| `ReleaseForm` | import | [ReleaseForm](../modules/ReleaseForm.md) | — |
| `assigneeDisplay.test` | import | [assigneeDisplay.test](../modules/assigneeDisplay.test.md) | — |
| `AssigneePicker.test` | import | [AssigneePicker.test](../modules/AssigneePicker.test.md) | — |

> References: showing 12 of 117 logical references; 105 omitted by the 12-row generated summary limit.
