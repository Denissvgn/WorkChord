# Project

**Location:** `frontend/src/types/project.ts:56`
**Kind:** Interface
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `Project` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `status` | `ProjectStatus` | Yes | — | — |
| `health` | `ProjectHealth` | Yes | — | — |
| `owner_id` | `number \| null` | Yes | — | — |
| `owner` | `ProjectOwner \| null` | Yes | — | — |
| `owner_profile_id` | `number \| null` | Yes | — | — |
| `owner_profile` | `ProjectProfileOwner \| null` | Yes | — | — |
| `initiative_id` | `number \| null` | No | — | — |
| `initiative` | `ProjectInitiativeSummary \| null` | No | — | — |
| `start_date` | `string \| null` | No | — | — |
| `target_date` | `string \| null` | No | — | — |
| `completed_at` | `string \| null` | No | — | — |
| `sort_order` | `number` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Project (frontend/src/types/project.ts)"]
    n1["frontend/src/components/layout/ScopeBar.tsx"]
    n2["AddMilestoneModal (frontend/src/components/projects/AddMilestoneModal.tsx)"]
    n3["frontend/src/components/projects/ProjectForm.test.tsx"]
    n4["ProjectForm (frontend/src/components/projects/ProjectForm.tsx)"]
    n5["ProjectHeaderFields (frontend/src/components/projects/ProjectHeaderFields.tsx)"]
    n6["groupByInitiative (frontend/src/components/projects/projectPortfolio.ts)"]
    n7["matchesPortfolioFilters (frontend/src/components/projects/projectPortfolio.ts)"]
    n8["ownerKeyForProject (frontend/src/components/projects/projectPortfolio.ts)"]
    n9["ProjectSummaryTab (frontend/src/components/projects/ProjectSummaryTab.tsx)"]
    n10["frontend/src/components/projects/RoadmapView.test.tsx"]
    n11["RoadmapView (frontend/src/components/projects/RoadmapView.tsx)"]
    n12["SetDatesPopover (frontend/src/components/projects/SetDatesPopover.tsx)"]
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
    click n0 "../modules/types_project.md"
    click n1 "../modules/ScopeBar.md"
    click n2 "../modules/AddMilestoneModal.md"
    click n3 "../modules/ProjectForm.test.md"
    click n4 "../modules/ProjectForm.md"
    click n5 "../modules/ProjectHeaderFields.md"
    click n6 "../modules/projectPortfolio.md"
    click n7 "../modules/projectPortfolio.md"
    click n8 "../modules/projectPortfolio.md"
    click n9 "../modules/ProjectSummaryTab.md"
    click n10 "../modules/RoadmapView.test.md"
    click n11 "../modules/RoadmapView.md"
    click n12 "../modules/SetDatesPopover.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `completed_at`, `created_at`, `description`, `health`, `id`, `initiative`, `initiative_id`, `name`, `owner`, `owner_id`, `owner_profile`, `owner_profile_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ScopeBar` | import | [ScopeBar](../modules/ScopeBar.md) | — |
| `AddMilestoneModal` | type_reference | [AddMilestoneModal](../modules/AddMilestoneModal.md) | — |
| `ProjectForm.test` | import | [ProjectForm.test](../modules/ProjectForm.test.md) | — |
| `ProjectForm` | type_reference | [ProjectForm](../modules/ProjectForm.md) | — |
| `ProjectHeaderFields` | type_reference | [ProjectHeaderFields](../modules/ProjectHeaderFields.md) | — |
| `groupByInitiative` | type_reference | [projectPortfolio](../modules/projectPortfolio.md) | — |
| `matchesPortfolioFilters` | type_reference | [projectPortfolio](../modules/projectPortfolio.md) | — |
| `ownerKeyForProject` | type_reference | [projectPortfolio](../modules/projectPortfolio.md) | — |
| `ProjectSummaryTab` | type_reference | [ProjectSummaryTab](../modules/ProjectSummaryTab.md) | — |
| `RoadmapView.test` | import | [RoadmapView.test](../modules/RoadmapView.test.md) | — |
| `RoadmapView` | type_reference | [RoadmapView](../modules/RoadmapView.md) | — |
| `SetDatesPopover` | type_reference | [SetDatesPopover](../modules/SetDatesPopover.md) | — |

> References: showing 12 of 23 logical references; 11 omitted by the 12-row generated summary limit.
