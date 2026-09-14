# SchedulingPassCard Module

**Path:** `frontend/src/components/settings/SchedulingPassCard.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/SchedulingPassCard.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/schedulingDisplay` | `schedulingPassDisplay` |
| `../../types/schedulingRules` | `SchedulingPass`, `SortCriterion`, `TASK_FIELDS`, `FILTER_FIELDS`, `OPERATORS`, `FILTER_VALUES` |
| `../common/Checkbox` | `Checkbox` |
| `../common/Input` | `Input` |
| `@dnd-kit/sortable` | `useSortable` |
| `@dnd-kit/utilities` | `CSS` |
| `lucide-react` | `Trash2`, `ChevronDown`, `ChevronRight`, `GripVertical`, `Plus`, `X`, `ArrowUp`, `ArrowDown`, `Info` |
| `react` | `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SchedulingPassCard` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Checkbox.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/settings/SchedulingPassCard.tsx"]
    n3["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n4["frontend/src/i18n/schedulingDisplay.ts"]
    n5["frontend/src/types/schedulingRules.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n3 --> n2
    n3 --> n5
    n4 --> n5
    click n0 "../modules/Checkbox.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/SchedulingPassCard.md"
    click n3 "../modules/SchedulingRulesSettings.md"
    click n4 "../modules/schedulingDisplay.md"
    click n5 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [schedulingDisplay](../modules/schedulingDisplay.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Props](../entities/SchedulingPassCard_Props.md) | Class | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SchedulingPassCard` | `({ pass, sortableId, onChange, onRemove }: Props)` | — | — |
