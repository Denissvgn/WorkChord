# templateService Module

**Path:** `frontend/src/services/templateService.ts`

## Description

_Auto-generated from `frontend/src/services/templateService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/template` | `TemplateListParams`, `WorkTemplate`, `WorkTemplateCreate`, `WorkTemplateUpdate` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendTemplateService`, `templateService` |
| Constants | `templateService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n4["frontend/src/components/triage/CreateTriageDrawer.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/services/templateService.ts"]
    n7["frontend/src/types/template.ts"]
    n0 --> n6
    n0 --> n7
    n1 --> n6
    n1 --> n7
    n2 --> n6
    n2 --> n7
    n3 --> n6
    n4 --> n6
    n4 --> n7
    n6 --> n5
    n6 --> n7
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/ConvertTriageDrawer.md"
    click n4 "../modules/CreateTriageDrawer.md"
    click n5 "../modules/api.md"
    click n6 "../modules/templateService.md"
    click n7 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |
| Inbound | [CreateTriageDrawer](../modules/CreateTriageDrawer.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_template](../modules/types_template.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendTemplateService](../entities/FrontendTemplateService.md) | Interface | 23 | — | — |
