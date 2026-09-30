# SavedView

**Location:** `frontend/src/types/savedView.ts:4`
**Kind:** Class
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

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedView (frontend/src/types/savedView.ts)"]
    n1["frontend/src/components/layout/AppSidebar.test.tsx"]
    n2["frontend/src/components/layout/AppSidebar.tsx"]
    n3["SavedViewsControl (frontend/src/components/tasks/SavedViewsControl.tsx)"]
    n4["savedViewDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n5["frontend/src/pages/ProjectsPage.tsx"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/pages/TriagePage.tsx"]
    n8["frontend/src/services/savedViewService.ts"]
    n9["frontend/src/utils/savedViewState.test.ts"]
    n10["savedViewModified (frontend/src/utils/savedViewState.ts)"]
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
    click n0 "../modules/savedView.md"
    click n1 "../modules/AppSidebar.test.md"
    click n2 "../modules/AppSidebar.md"
    click n3 "../modules/SavedViewsControl.md"
    click n4 "../modules/seedDisplay.md"
    click n5 "../modules/ProjectsPage.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/TriagePage.md"
    click n8 "../modules/savedViewService.md"
    click n9 "../modules/savedViewState.test.md"
    click n10 "../modules/savedViewState.md"
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
| `SavedViewsControl` | type_reference | [SavedViewsControl](../modules/SavedViewsControl.md) | — |
| `savedViewDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `ProjectsPage` | import | [ProjectsPage](../modules/ProjectsPage.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `savedViewService` | import | [savedViewService](../modules/savedViewService.md) | — |
| `savedViewState.test` | import | [savedViewState.test](../modules/savedViewState.test.md) | — |
| `savedViewModified` | type_reference | [savedViewState](../modules/savedViewState.md) | — |
