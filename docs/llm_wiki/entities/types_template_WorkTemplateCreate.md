# WorkTemplateCreate

**Location:** `frontend/src/types/template.ts:22`
**Kind:** Class
**Bases:** —
**Module:** [types_template](../modules/types_template.md)

## Description

_Auto-generated from `WorkTemplateCreate` in `frontend/src/types/template.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `template_type` | `TemplateType` | Yes | — | — |
| `default_title` | `string \| null` | No | — | — |
| `default_description` | `string \| null` | No | — | — |
| `default_priority` | `number \| null` | No | — | — |
| `default_effort_days` | `number \| null` | No | — | — |
| `default_labels` | `string[]` | No | — | — |
| `default_checklist` | `string[]` | No | — | — |
| `default_payload` | `Record<string, unknown>` | No | — | — |
| `is_active` | `boolean` | No | — | — |
| `sort_order` | `number` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkTemplateCreate (frontend/src/types/template.ts)"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/services/templateService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_template.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/templateService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_template](../modules/types_template.md) | 0 | `default_checklist`, `default_description`, `default_effort_days`, `default_labels`, `default_payload`, `default_priority`, `default_title`, `description`, `is_active`, `name`, `sort_order`, `template_type` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TemplateLabelSettings` | import | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) | — |
| `templateService` | import | [templateService](../modules/templateService.md) | — |
