# EffortModifierCard Module

**Path:** `frontend/src/components/settings/EffortModifierCard.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/EffortModifierCard.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/schedulingDisplay` | `effortModifierDisplay` | — | compiler-dependent |
| `../../types/schedulingRules` | `EffortModifier` | Declaration | erased |
| `../../types/schedulingRules` | `MATH_OPERATIONS`, `FORMULA_TEMPLATES`, `FORMULA_ASSIGNEE_FIELDS` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `lucide-react` | `Trash2`, `ChevronDown`, `ChevronRight`, `Info` | — | compiler-dependent |
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
    n0["frontend/src/components/common/Checkbox.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/settings/EffortModifierCard.test.tsx"]
    n3["frontend/src/components/settings/EffortModifierCard.tsx"]
    n4["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n5["frontend/src/i18n/schedulingDisplay.ts"]
    n6["frontend/src/types/schedulingRules.ts"]
    n2 --> n3
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n4 --> n3
    n4 --> n6
    n5 --> n6
    click n0 "../modules/Checkbox.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/EffortModifierCard.test.md"
    click n3 "../modules/EffortModifierCard.md"
    click n4 "../modules/SchedulingRulesSettings.md"
    click n5 "../modules/schedulingDisplay.md"
    click n6 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EffortModifierCard.test](../modules/EffortModifierCard.test.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [schedulingDisplay](../modules/schedulingDisplay.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Props](../entities/EffortModifierCard_Props.md) | Interface | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `EffortModifierCard` | `({ modifier, onChange, onRemove }: Props)` | — | — |
