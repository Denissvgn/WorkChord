# EffortModifier

**Location:** `frontend/src/types/schedulingRules.ts:23`
**Kind:** Class
**Bases:** —
**Module:** [schedulingRules](../modules/schedulingRules.md)

## Description

_Auto-generated from `EffortModifier` in `frontend/src/types/schedulingRules.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `string` | *required* | — |
| `enabled` | `boolean` | *required* | — |
| `formula` | `string \| null` | *required* | — |
| `operation` | `'ceil' \| 'floor' \| 'round' \| null` | *required* | — |
| `fallback` | `string` | *required* | — |
| `min_value` | `number \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["EffortModifier (frontend/src/types/schedulingRules.ts)"]
    n1["frontend/src/components/settings/EffortModifierCard.test.tsx"]
    n2["frontend/src/components/settings/EffortModifierCard.tsx"]
    n3["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n4["effortModifierDisplay (frontend/src/i18n/schedulingDisplay.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schedulingRules.md"
    click n1 "../modules/EffortModifierCard.test.md"
    click n2 "../modules/EffortModifierCard.md"
    click n3 "../modules/SchedulingRulesSettings.md"
    click n4 "../modules/schedulingDisplay.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schedulingRules](../modules/schedulingRules.md) | 0 | `enabled`, `fallback`, `formula`, `id`, `min_value`, `operation` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `EffortModifierCard.test` | import | [EffortModifierCard.test](../modules/EffortModifierCard.test.md) | — |
| `EffortModifierCard` | import | [EffortModifierCard](../modules/EffortModifierCard.md) | — |
| `SchedulingRulesSettings` | import | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) | — |
| `effortModifierDisplay` | type_reference | [schedulingDisplay](../modules/schedulingDisplay.md) | — |
