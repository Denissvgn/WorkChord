# SavedView

**Location:** `frontend/src/types/savedView.ts:4`
**Kind:** Interface
**Bases:** —
**Module:** [savedView](../modules/savedView.md)

## Description

_Auto-generated from `SavedView` in `frontend/src/types/savedView.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `seed_key` | `string \| null` | No | — | — |
| `view_type` | `SavedViewType` | Yes | — | — |
| `scope` | `SavedViewScope` | Yes | — | — |
| `filters_json` | `Record<string, unknown>` | Yes | — | — |
| `sort_json` | `Record<string, unknown>` | Yes | — | — |
| `columns_json` | `Record<string, unknown>` | Yes | — | — |
| `created_by_session_id` | `number \| null` | No | — | — |
| `schema_version` | `number` | Yes | — | — |
| `metric_migration_note` | `string \| null` | No | — | — |
| `owner_principal_id` | `number \| null` | No | — | — |
| `is_valid` | `boolean` | Yes | — | — |
| `invalid_reason` | `string \| null` | No | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedView (frontend/src/types/savedView.ts)"]
    n1["frontend/src/components/layout/AppSidebar.test.tsx"]
    n2["frontend/src/components/layout/AppSidebar.tsx"]
    n3["frontend/src/components/layout/CommandMenu.tsx"]
    n4["SavedViewsControl (frontend/src/components/tasks/SavedViewsControl.tsx)"]
    n5["filtersFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n6["sortKeyFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n7["savedViewDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n8["frontend/src/pages/ProjectsPage.tsx"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n10["frontend/src/pages/TriagePage.tsx"]
    n11["frontend/src/services/savedViewService.ts"]
    n12["frontend/src/utils/savedViewState.test.ts"]
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
    click n0 "../modules/savedView.md"
    click n1 "../modules/AppSidebar.test.md"
    click n2 "../modules/AppSidebar.md"
    click n3 "../modules/CommandMenu.md"
    click n4 "../modules/SavedViewsControl.md"
    click n5 "../modules/taskViewState.md"
    click n6 "../modules/taskViewState.md"
    click n7 "../modules/seedDisplay.md"
    click n8 "../modules/ProjectsPage.md"
    click n9 "../modules/TasksPage.md"
    click n10 "../modules/TriagePage.md"
    click n11 "../modules/savedViewService.md"
    click n12 "../modules/savedViewState.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedView](../modules/savedView.md) | 0 | `columns_json`, `created_at`, `created_by_session_id`, `description`, `filters_json`, `id`, `invalid_reason`, `is_valid`, `metric_migration_note`, `name`, `owner_principal_id`, `schema_version` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AppSidebar.test` | import | [AppSidebar.test](../modules/AppSidebar.test.md) | — |
| `AppSidebar` | import | [AppSidebar](../modules/AppSidebar.md) | — |
| `CommandMenu` | import | [CommandMenu](../modules/CommandMenu.md) | — |
| `SavedViewsControl` | type_reference | [SavedViewsControl](../modules/SavedViewsControl.md) | — |
| `filtersFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `sortKeyFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `savedViewDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `savedViewService` | import | [savedViewService](../modules/savedViewService.md) | — |
| `savedViewState.test` | import | [savedViewState.test](../modules/savedViewState.test.md) | — |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
