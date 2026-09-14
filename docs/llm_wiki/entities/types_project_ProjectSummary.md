# ProjectSummary

**Location:** `frontend/src/types/project.ts:198`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectSummary` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `status` | `ProjectStatus` | *required* | — |
| `health` | `ProjectHealth` | *required* | — |
| `owner_id` | `number \| null` | *required* | — |
| `owner` | `ProjectOwner \| null` | *required* | — |
| `owner_profile_id` | `number \| null` | *required* | — |
| `owner_profile` | `ProjectProfileOwner \| null` | *required* | — |
| `initiative_id` | `number \| null` | *required* | — |
| `start_date` | `string \| null` | *required* | — |
| `target_date` | `string \| null` | *required* | — |
| `completed_at` | `string \| null` | *required* | — |
| `total_tasks` | `number` | *required* | — |
| `completed_tasks` | `number` | *required* | — |
| `completion_percent` | `number` | *required* | — |
| `active_tasks` | `number` | *required* | — |
| `blocked_tasks` | `number` | *required* | — |
| `overdue_tasks` | `number` | *required* | — |
| `target_date_risk` | `ProjectTargetDateRisk` | *required* | — |
| `target_date_risk_reason` | `string \| null` | *required* | — |
| `target_date_slip_days` | `number` | *required* | — |
| `days_until_target` | `number \| null` | *required* | — |
| `status_counts` | `Record<string, number>` | *required* | — |
| `total_effort_days` | `number` | *required* | — |
| `remaining_effort_days` | `number` | *required* | — |
| `milestone_groups` | `ProjectMilestoneTaskGroup[]` | *required* | — |
| `request_count` | `number` | *required* | — |
| `task_start_date` | `string \| null` | *required* | — |
| `task_end_date` | `string \| null` | *required* | — |
| `latest_update` | `ProjectUpdateEntry \| null` | *required* | — |
| `latest_update_at` | `string \| null` | *required* | — |
| `days_since_latest_update` | `number \| null` | *required* | — |
| `update_freshness` | `ProjectUpdateFreshness` | *required* | — |
| `is_update_stale` | `boolean` | *required* | — |
| `stale_update_threshold_days` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectSummary (frontend/src/types/project.ts)"]
    n1["frontend/src/pages/OverviewPage.tsx"]
    n2["frontend/src/services/projectService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/OverviewPage.md"
    click n2 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `active_tasks`, `blocked_tasks`, `completed_at`, `completed_tasks`, `completion_percent`, `days_since_latest_update`, `days_until_target`, `health`, `id`, `initiative_id`, `is_update_stale`, `latest_update` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `OverviewPage` | import | [OverviewPage](../modules/OverviewPage.md) | — |
| `projectService` | import | [projectService](../modules/projectService.md) | — |
