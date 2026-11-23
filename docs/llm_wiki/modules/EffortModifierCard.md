# EffortModifierCard Module

**Path:** `frontend/src/components/settings/EffortModifierCard.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/EffortModifierCard.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../i18n/schedulingDisplay` | `effortModifierDisplay` | — | compiler-dependent |
| `../../types/schedulingRules` | `EffortModifier` | Declaration | erased |
| `../../types/schedulingRules` | `MATH_OPERATIONS`, `FORMULA_TEMPLATES`, `FORMULA_ASSIGNEE_FIELDS` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` | — | compiler-dependent |
| `./ReadOnlyFieldset` | `ReadOnlyFieldset` | — | compiler-dependent |
| `lucide-react` | `Trash2`, `ChevronRight`, `Info` | — | compiler-dependent |
| `react` | `useState`, `useMemo`, `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `EffortModifierCard` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Checkbox.tsx"]
    n2["frontend/src/components/common/Input.tsx"]
    n3["frontend/src/components/common/Select.tsx"]
    n4["frontend/src/components/settings/EffortModifierCard.test.tsx"]
    n5["frontend/src/components/settings/EffortModifierCard.tsx"]
    n6["frontend/src/components/settings/ReadOnlyFieldset.tsx"]
    n7["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n8["frontend/src/components/settings/schedulingSearchLabels.test.tsx"]
    n9["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n10["frontend/src/i18n/schedulingDisplay.ts"]
    n11["frontend/src/types/schedulingRules.ts"]
    n3 --> n2
    n4 --> n5
    n4 --> n11
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n7 --> n0
    n7 --> n5
    n7 --> n6
    n7 --> n11
    n8 --> n5
    n10 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/Checkbox.md"
    click n2 "../modules/Input.md"
    click n3 "../modules/Select.md"
    click n4 "../modules/EffortModifierCard.test.md"
    click n5 "../modules/EffortModifierCard.md"
    click n6 "../modules/ReadOnlyFieldset.md"
    click n7 "../modules/SchedulingRulesSettings.md"
    click n8 "../modules/schedulingSearchLabels.test.md"
    click n9 "../modules/SlideOverDrawer.md"
    click n10 "../modules/schedulingDisplay.md"
    click n11 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EffortModifierCard.test](../modules/EffortModifierCard.test.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [schedulingSearchLabels.test](../modules/schedulingSearchLabels.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [ReadOnlyFieldset](../modules/ReadOnlyFieldset.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |
| Outbound | [schedulingDisplay](../modules/schedulingDisplay.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Props](../entities/EffortModifierCard_Props.md) | Interface | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `EffortModifierCard` | `({ modifier, onChange, onRemove }: Props)` | — | — |
