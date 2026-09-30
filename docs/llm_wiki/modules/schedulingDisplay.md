# schedulingDisplay Module

**Path:** `frontend/src/i18n/schedulingDisplay.ts`

## Description

_Auto-generated from `frontend/src/i18n/schedulingDisplay.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/schedulingRules` | `EffortModifier`, `SchedulingPass`, `SortCriterion` |
| `./i18n` | `i18n` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `effortModifierDisplay`, `schedulingPassDisplay` |
| Constants | `defaultEffortModifiers`, `defaultSchedulingPasses` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/EffortModifierCard.tsx"]
    n1["frontend/src/components/settings/SchedulingPassCard.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/i18n/schedulingDisplay.ts"]
    n4["frontend/src/types/schedulingRules.ts"]
    n0 --> n3
    n0 --> n4
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    click n0 "../modules/EffortModifierCard.md"
    click n1 "../modules/SchedulingPassCard.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/schedulingDisplay.md"
    click n4 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EffortModifierCard](../modules/EffortModifierCard.md) |
| Inbound | [SchedulingPassCard](../modules/SchedulingPassCard.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `effortModifierDisplay` | `(modifier: EffortModifier)` | — | — |
| `schedulingPassDisplay` | `(pass: SchedulingPass)` | — | — |
