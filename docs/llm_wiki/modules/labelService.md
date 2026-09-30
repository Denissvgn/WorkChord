# labelService Module

**Path:** `frontend/src/services/labelService.ts`

## Description

_Auto-generated from `frontend/src/services/labelService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/label` | `Label`, `LabelCreate`, `LabelGroup`, `LabelGroupCreate`, `LabelGroupListParams`, `LabelGroupUpdate`, `LabelListParams`, `LabelUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FrontendLabelService`, `labelService` |
| Constants | `labelService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/labels/LabelSelector.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n3["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n4["frontend/src/components/tasks/TaskList.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/services/labelService.ts"]
    n7["frontend/src/types/label.ts"]
    n0 --> n6
    n0 --> n7
    n1 --> n0
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n2 --> n6
    n3 --> n6
    n4 --> n3
    n4 --> n6
    n4 --> n7
    n6 --> n5
    n6 --> n7
    click n0 "../modules/LabelSelector.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/KanbanBoard.md"
    click n3 "../modules/TaskFiltersBar.md"
    click n4 "../modules/TaskList.md"
    click n5 "../modules/api.md"
    click n6 "../modules/labelService.md"
    click n7 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [LabelSelector](../modules/LabelSelector.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_label](../modules/types_label.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FrontendLabelService](../entities/FrontendLabelService.md) | Class | 41 | — | — |
