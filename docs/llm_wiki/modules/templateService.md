# templateService Module

**Path:** `frontend/src/services/templateService.ts`

## Description

_Auto-generated from `frontend/src/services/templateService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/template` | `TemplateListParams`, `WorkTemplate`, `WorkTemplateCreate`, `WorkTemplateUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendTemplateService`, `templateService` |
| Constants | `templateService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/pages/TriagePage.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/services/templateService.ts"]
    n6["frontend/src/types/template.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n1 --> n6
    n2 --> n5
    n2 --> n6
    n3 --> n5
    n3 --> n6
    n5 --> n4
    n5 --> n6
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/TriagePage.md"
    click n4 "../modules/api.md"
    click n5 "../modules/templateService.md"
    click n6 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_template](../modules/types_template.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendTemplateService](../entities/FrontendTemplateService.md) | Class | 23 | — | — |
