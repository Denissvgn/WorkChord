# label Module

**Path:** `frontend/src/types/label.ts`

## Description

_Auto-generated from `frontend/src/types/label.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Label`, `LabelCreate`, `LabelGroup`, `LabelGroupBrief`, `LabelGroupCreate`, `LabelGroupListParams`, `LabelGroupUpdate`, `LabelListParams`, `LabelUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/labels/LabelSelector.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n2["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/i18n/seedDisplay.ts"]
    n5["frontend/src/services/labelService.ts"]
    n6["frontend/src/types/label.ts"]
    n7["frontend/src/utils/taskFilters.ts"]
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n2
    n1 --> n6
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n4 --> n6
    n5 --> n6
    n7 --> n6
    click n0 "../modules/LabelSelector.md"
    click n1 "../modules/TemplateLabelSettings.test.md"
    click n2 "../modules/TemplateLabelSettings.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/seedDisplay.md"
    click n5 "../modules/labelService.md"
    click n6 "../modules/types_label.md"
    click n7 "../modules/taskFilters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [LabelSelector](../modules/LabelSelector.md) |
| Inbound | [TemplateLabelSettings.test](../modules/TemplateLabelSettings.test.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [seedDisplay](../modules/seedDisplay.md) |
| Inbound | [labelService](../modules/labelService.md) |
| Inbound | [taskFilters](../modules/taskFilters.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [LabelGroupBrief](../entities/types_label_LabelGroupBrief.md) | Class | 1 | — | — |
| [Label](../entities/types_label_Label.md) | Class | 9 | — | — |
| [LabelGroup](../entities/types_label_LabelGroup.md) | Class | 24 | — | — |
| [LabelGroupCreate](../entities/types_label_LabelGroupCreate.md) | Class | 38 | — | — |
| [LabelCreate](../entities/types_label_LabelCreate.md) | Class | 49 | — | — |
| [LabelGroupListParams](../entities/LabelGroupListParams.md) | Class | 61 | — | — |
| [LabelListParams](../entities/LabelListParams.md) | Class | 65 | — | — |
| [LabelGroupUpdate](../entities/types_label_LabelGroupUpdate.md) | Type alias | 47 | — | — |
| [LabelUpdate](../entities/types_label_LabelUpdate.md) | Type alias | 59 | — | — |
