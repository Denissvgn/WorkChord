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
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/components/tasks/TaskForm.test.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/triage/CreateTriageDrawer.tsx"]
    n5["frontend/src/i18n/seedDisplay.ts"]
    n6["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n7["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n8["frontend/src/services/templateService.ts"]
    n9["frontend/src/types/template.ts"]
    n0 --> n5
    n0 --> n8
    n0 --> n9
    n1 --> n5
    n1 --> n8
    n1 --> n9
    n2 --> n3
    n2 --> n9
    n3 --> n5
    n3 --> n8
    n3 --> n9
    n4 --> n5
    n4 --> n8
    n4 --> n9
    n5 --> n9
    n6 --> n9
    n7 --> n9
    n8 --> n9
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/TaskForm.test.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/CreateTriageDrawer.md"
    click n5 "../modules/seedDisplay.md"
    click n6 "../modules/SettingsPage.labels.test.md"
    click n7 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n8 "../modules/templateService.md"
    click n9 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm.test](../modules/TaskForm.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [CreateTriageDrawer](../modules/CreateTriageDrawer.md) |
| Inbound | [seedDisplay](../modules/seedDisplay.md) |
| Inbound | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) |
| Inbound | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) |
| Inbound | [templateService](../modules/templateService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkTemplate](../entities/types_template_WorkTemplate.md) | Interface | 3 | — | — |
| [WorkTemplateCreate](../entities/types_template_WorkTemplateCreate.md) | Interface | 22 | — | — |
| [TemplateListParams](../entities/TemplateListParams.md) | Interface | 39 | — | — |
| [TemplateType](../entities/types_template_TemplateType.md) | Type alias | 1 | `'task' \| 'project' \| 'triage'` | — |
| [WorkTemplateUpdate](../entities/types_template_WorkTemplateUpdate.md) | Type alias | 37 | `Partial<WorkTemplateCreate>` | — |
