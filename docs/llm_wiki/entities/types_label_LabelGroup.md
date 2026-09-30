# LabelGroup

**Location:** `frontend/src/types/label.ts:24`
**Kind:** Class
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

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LabelGroup (frontend/src/types/label.ts)"]
    n1["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n2["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n3["labelGroupDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n4["frontend/src/services/labelService.ts"]
    n5["filterTaskWithChildren (frontend/src/utils/taskFilters.ts)"]
    n6["taskMatchesFilters (frontend/src/utils/taskFilters.ts)"]
    n7["selectVisibleWork (frontend/src/utils/visibleWork.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_label.md"
    click n1 "../modules/TemplateLabelSettings.test.md"
    click n2 "../modules/TemplateLabelSettings.md"
    click n3 "../modules/seedDisplay.md"
    click n4 "../modules/labelService.md"
    click n5 "../modules/taskFilters.md"
    click n6 "../modules/taskFilters.md"
    click n7 "../modules/visibleWork.md"
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
| `labelGroupDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `labelService` | import | [labelService](../modules/labelService.md) | — |
| `filterTaskWithChildren` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
| `taskMatchesFilters` | type_reference | [taskFilters](../modules/taskFilters.md) | — |
| `selectVisibleWork` | type_reference | [visibleWork](../modules/visibleWork.md) | — |
