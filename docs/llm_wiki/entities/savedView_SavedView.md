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
    n1["frontend/src/components/layout/CommandMenu.tsx"]
    n2["useSavedViewManager (frontend/src/components/tasks/useSavedViewManager.tsx)"]
    n3["triageFiltersFromSavedView (frontend/src/components/triage/triageUtils.ts)"]
    n4["filtersFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n5["sortKeyFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n6["savedViewDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n7["frontend/src/pages/ProjectsPage.tsx"]
    n8["frontend/src/pages/TasksPage.toolbar.test.tsx"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n10["frontend/src/services/savedViewService.ts"]
    n11["frontend/src/utils/savedViewState.test.ts"]
    n12["savedViewModified (frontend/src/utils/savedViewState.ts)"]
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
    click n1 "../modules/CommandMenu.md"
    click n2 "../modules/useSavedViewManager.md"
    click n3 "../modules/triageUtils.md"
    click n4 "../modules/taskViewState.md"
    click n5 "../modules/taskViewState.md"
    click n6 "../modules/seedDisplay.md"
    click n7 "../modules/ProjectsPage.md"
    click n8 "../modules/TasksPage.toolbar.test.md"
    click n9 "../modules/TasksPage.md"
    click n10 "../modules/savedViewService.md"
    click n11 "../modules/savedViewState.test.md"
    click n12 "../modules/savedViewState.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedView](../modules/savedView.md) | 0 | `columns_json`, `created_at`, `created_by_session_id`, `description`, `filters_json`, `id`, `invalid_reason`, `is_valid`, `metric_migration_note`, `name`, `owner_principal_id`, `schema_version` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CommandMenu` | import | [CommandMenu](../modules/CommandMenu.md) | — |
| `useSavedViewManager` | type_reference | [useSavedViewManager](../modules/useSavedViewManager.md) | — |
| `triageFiltersFromSavedView` | type_reference | [triageUtils](../modules/triageUtils.md) | — |
| `filtersFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `sortKeyFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `savedViewDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `TasksPage.toolbar.test` | import | [TasksPage.toolbar.test](../modules/TasksPage.toolbar.test.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
| `savedViewService` | import | [savedViewService](../modules/savedViewService.md) | — |
| `savedViewState.test` | import | [savedViewState.test](../modules/savedViewState.test.md) | — |
| `savedViewModified` | type_reference | [savedViewState](../modules/savedViewState.md) | — |
