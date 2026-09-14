# schedulingRules Module

**Path:** `frontend/src/types/schedulingRules.ts`

## Description

/**
 * Scheduling Rules Types
 * Mirrors backend SchedulingRulesSchema structure
 */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ASSIGNEE_FIELDS`, `BalanceWorkload`, `Constraints`, `EffortModifier`, `FILTER_FIELDS`, `FILTER_VALUES`, `FORMULA_ASSIGNEE_FIELDS`, `FORMULA_TEMPLATES`, `FilterConfig`, `MATH_OPERATIONS`, `OPERATORS`, `SchedulingPass`, `SchedulingRules`, `SchedulingRulesResponse`, `SortCriterion`, `TASK_FIELDS` |
| Constants | `TASK_FIELDS`, `ASSIGNEE_FIELDS`, `OPERATORS`, `MATH_OPERATIONS`, `FILTER_FIELDS`, `FILTER_VALUES`, `FORMULA_TEMPLATES`, `FORMULA_ASSIGNEE_FIELDS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/ConstraintsPanel.tsx"]
    n1["frontend/src/components/settings/EffortModifierCard.test.tsx"]
    n2["frontend/src/components/settings/EffortModifierCard.tsx"]
    n3["frontend/src/components/settings/SchedulingPassCard.tsx"]
    n4["frontend/src/components/settings/SchedulingRulesSettings.test.tsx"]
    n5["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n6["frontend/src/i18n/schedulingDisplay.ts"]
    n7["frontend/src/services/schedulingRulesService.ts"]
    n8["frontend/src/types/schedulingRules.ts"]
    n0 --> n8
    n1 --> n2
    n1 --> n8
    n2 --> n6
    n2 --> n8
    n3 --> n6
    n3 --> n8
    n4 --> n5
    n4 --> n8
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n7
    n5 --> n8
    n6 --> n8
    n7 --> n8
    click n0 "../modules/ConstraintsPanel.md"
    click n1 "../modules/EffortModifierCard.test.md"
    click n2 "../modules/EffortModifierCard.md"
    click n3 "../modules/SchedulingPassCard.md"
    click n4 "../modules/SchedulingRulesSettings.test.md"
    click n5 "../modules/SchedulingRulesSettings.md"
    click n6 "../modules/schedulingDisplay.md"
    click n7 "../modules/schedulingRulesService.md"
    click n8 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ConstraintsPanel](../modules/ConstraintsPanel.md) |
| Inbound | [EffortModifierCard.test](../modules/EffortModifierCard.test.md) |
| Inbound | [EffortModifierCard](../modules/EffortModifierCard.md) |
| Inbound | [SchedulingPassCard](../modules/SchedulingPassCard.md) |
| Inbound | [SchedulingRulesSettings.test](../modules/SchedulingRulesSettings.test.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [schedulingDisplay](../modules/schedulingDisplay.md) |
| Inbound | [schedulingRulesService](../modules/schedulingRulesService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SortCriterion](../entities/schedulingRules_SortCriterion.md) | Class | 6 | — | Scheduling Rules Types |
| [FilterConfig](../entities/FilterConfig.md) | Class | 11 | — | — |
| [SchedulingPass](../entities/schedulingRules_SchedulingPass.md) | Class | 15 | — | — |
| [EffortModifier](../entities/schedulingRules_EffortModifier.md) | Class | 23 | — | — |
| [BalanceWorkload](../entities/BalanceWorkload.md) | Class | 32 | — | — |
| [Constraints](../entities/schedulingRules_Constraints.md) | Class | 37 | — | — |
| [SchedulingRules](../entities/schedulingRules_SchedulingRules.md) | Class | 46 | — | — |
| [SchedulingRulesResponse](../entities/schedulingRules_SchedulingRulesResponse.md) | Class | 53 | — | — |
