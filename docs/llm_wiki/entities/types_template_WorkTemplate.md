# WorkTemplate

**Location:** `frontend/src/types/template.ts:3`
**Kind:** Class
**Bases:** —
**Module:** [types_template](../modules/types_template.md)

## Description

_Auto-generated from `WorkTemplate` in `frontend/src/types/template.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `seed_key` | `string \| null` | *required* | — |
| `template_type` | `TemplateType` | *required* | — |
| `default_title` | `string \| null` | *required* | — |
| `default_description` | `string \| null` | *required* | — |
| `default_priority` | `number \| null` | *required* | — |
| `default_effort_days` | `number \| null` | *required* | — |
| `default_labels` | `string[]` | *required* | — |
| `default_checklist` | `string[]` | *required* | — |
| `default_payload` | `Record<string, unknown>` | *required* | — |
| `is_active` | `boolean` | *required* | — |
| `sort_order` | `number` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkTemplate (frontend/src/types/template.ts)"]
    n1["frontend/src/components/projects/ProjectForm.tsx"]
    n2["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["templateDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n5["frontend/src/pages/TriagePage.tsx"]
    n6["frontend/src/services/templateService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/types_template.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/TemplateLabelSettings.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/seedDisplay.md"
    click n5 "../modules/TriagePage.md"
    click n6 "../modules/templateService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_template](../modules/types_template.md) | 0 | `created_at`, `default_checklist`, `default_description`, `default_effort_days`, `default_labels`, `default_payload`, `default_priority`, `default_title`, `description`, `id`, `is_active`, `name` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ProjectForm` | import | [ProjectForm](../modules/ProjectForm.md) | — |
| `TemplateLabelSettings` | import | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `templateDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `TriagePage` | import | [TriagePage](../modules/TriagePage.md) | — |
| `templateService` | import | [templateService](../modules/templateService.md) | — |
