# labelService Module

**Path:** `frontend/src/services/labelService.ts`

## Description

_Auto-generated from `frontend/src/services/labelService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/label` | `Label`, `LabelCreate`, `LabelGroup`, `LabelGroupCreate`, `LabelGroupListParams`, `LabelGroupUpdate`, `LabelListParams`, `LabelUpdate` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendLabelService`, `labelService` |
| Constants | `labelService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/labels/LabelSelector.tsx"]
    n1["frontend/src/components/planning/PlanBlockersSection.tsx"]
    n2["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n4["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n5["frontend/src/components/tasks/TaskList.tsx"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/services/api.ts"]
    n8["frontend/src/services/labelService.ts"]
    n9["frontend/src/types/label.ts"]
    n0 --> n8
    n0 --> n9
    n1 --> n8
    n2 --> n0
    n2 --> n8
    n2 --> n9
    n3 --> n4
    n3 --> n8
    n4 --> n8
    n5 --> n4
    n5 --> n8
    n5 --> n9
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n8
    n8 --> n7
    n8 --> n9
    click n0 "../modules/LabelSelector.md"
    click n1 "../modules/PlanBlockersSection.md"
    click n2 "../modules/TemplateLabelSettings.md"
    click n3 "../modules/KanbanBoard.md"
    click n4 "../modules/TaskFiltersBar.md"
    click n5 "../modules/TaskList.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/api.md"
    click n8 "../modules/labelService.md"
    click n9 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [LabelSelector](../modules/LabelSelector.md) |
| Inbound | [PlanBlockersSection](../modules/PlanBlockersSection.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_label](../modules/types_label.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendLabelService](../entities/FrontendLabelService.md) | Interface | 41 | — | — |
