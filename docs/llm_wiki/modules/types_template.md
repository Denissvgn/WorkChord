# template Module

**Path:** `frontend/src/types/template.ts`

## Description

_Auto-generated from `frontend/src/types/template.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TemplateListParams`, `TemplateType`, `WorkTemplate`, `WorkTemplateCreate`, `WorkTemplateUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/i18n/seedDisplay.ts"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/templateService.ts"]
    n6["frontend/src/types/template.ts"]
    n0 --> n3
    n0 --> n5
    n0 --> n6
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n3 --> n6
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n5 --> n6
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/seedDisplay.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/templateService.md"
    click n6 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [seedDisplay](../modules/seedDisplay.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Inbound | [templateService](../modules/templateService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkTemplate](../entities/types_template_WorkTemplate.md) | Class | 3 | — | — |
| [WorkTemplateCreate](../entities/types_template_WorkTemplateCreate.md) | Class | 22 | — | — |
| [TemplateListParams](../entities/TemplateListParams.md) | Class | 39 | — | — |
| [TemplateType](../entities/types_template_TemplateType.md) | Type alias | 1 | — | — |
| [WorkTemplateUpdate](../entities/types_template_WorkTemplateUpdate.md) | Type alias | 37 | — | — |
