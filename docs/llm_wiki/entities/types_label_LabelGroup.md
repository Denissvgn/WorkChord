# LabelGroup

**Location:** `frontend/src/types/label.ts:24`
**Kind:** Interface
**Bases:** —
**Module:** [types_label](../modules/types_label.md)

## Description

_Auto-generated from `LabelGroup` in `frontend/src/types/label.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `key` | `string` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `color` | `string` | Yes | — | — |
| `is_active` | `boolean` | Yes | — | — |
| `sort_order` | `number` | Yes | — | — |
| `seed_key` | `string \| null` | No | — | — |
| `labels` | `Label[]` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LabelGroup (frontend/src/types/label.ts)"]
    n1["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n2["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n3["PipelineView (frontend/src/components/tasks/PipelineView.tsx)"]
    n4["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n5["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n6["frontend/src/services/labelService.ts"]
    n7["filterTaskWithChildren (frontend/src/utils/taskFilters.ts)"]
    n8["taskMatchesFilters (frontend/src/utils/taskFilters.ts)"]
    n9["selectVisibleWork (frontend/src/utils/visibleWork.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/types_label.md"
    click n1 "../modules/TemplateLabelSettings.test.md"
    click n2 "../modules/TemplateLabelSettings.md"
    click n3 "../modules/PipelineView.md"
    click n4 "../modules/SettingsPage.labels.test.md"
    click n5 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n6 "../modules/labelService.md"
    click n7 "../modules/taskFilters.md"
    click n8 "../modules/taskFilters.md"
    click n9 "../modules/visibleWork.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_label](../modules/types_label.md) | 0 | `color`, `created_at`, `description`, `id`, `is_active`, `key`, `labels`, `name`, `seed_key`, `sort_order`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TemplateLabelSettings.test` | import | [TemplateLabelSettings.test](../modules/TemplateLabelSettings.test.md) | — |
| `TemplateLabelSettings` | import | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) | — |
| `PipelineView` | type_reference | [PipelineView](../modules/PipelineView.md) | — |
| `SettingsPage.labels.test` | import | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) | — |
| `SettingsPage.readOnlyPanels.test` | import | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) | — |
| `labelService` | import | [labelService](../modules/labelService.md) | — |
| `filterTaskWithChildren` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
| `taskMatchesFilters` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
| `selectVisibleWork` | type_reference | [visibleWork](../modules/visibleWork.md) | — |
