# SchedulingPassCard Module

**Path:** `frontend/src/components/settings/SchedulingPassCard.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/SchedulingPassCard.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/schedulingDisplay` | `schedulingPassDisplay` | — | compiler-dependent |
| `../../types/schedulingRules` | `SchedulingPass`, `SortCriterion` | Declaration | erased |
| `../../types/schedulingRules` | `TASK_FIELDS`, `FILTER_FIELDS`, `OPERATORS`, `FILTER_VALUES` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `@dnd-kit/sortable` | `useSortable` | — | compiler-dependent |
| `@dnd-kit/utilities` | `CSS` | — | compiler-dependent |
| `lucide-react` | `Trash2`, `ChevronDown`, `ChevronRight`, `GripVertical`, `Plus`, `X`, `ArrowUp`, `ArrowDown`, `Info` | — | compiler-dependent |
| `react` | `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SchedulingPassCard` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [Props](../entities/SchedulingPassCard_Props.md) | Interface | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SchedulingPassCard` | `({ pass, sortableId, onChange, onRemove }: Props)` | — | — |
