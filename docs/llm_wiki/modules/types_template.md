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
    n2["frontend/src/components/tasks/TaskForm.test.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/i18n/seedDisplay.ts"]
    n5["frontend/src/pages/TriagePage.tsx"]
    n6["frontend/src/services/templateService.ts"]
    n7["frontend/src/types/template.ts"]
    n0 --> n4
    n0 --> n6
    n0 --> n7
    n1 --> n4
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n2 --> n7
    n3 --> n4
    n3 --> n6
    n3 --> n7
    n4 --> n7
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n6 --> n7
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/TaskForm.test.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/seedDisplay.md"
    click n5 "../modules/TriagePage.md"
    click n6 "../modules/templateService.md"
    click n7 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm.test](../modules/TaskForm.test.md) |
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
