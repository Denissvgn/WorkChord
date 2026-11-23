# buttonStyles Module

**Path:** `frontend/src/components/common/buttonStyles.ts`

## Description

_Auto-generated from `frontend/src/components/common/buttonStyles.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `clsx` | `clsx` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ButtonSize`, `ButtonVariant`, `buttonClassName` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/ButtonLink.tsx"]
    n2["frontend/src/components/common/buttonStyles.ts"]
    n3["frontend/src/components/planning/PlanShareSection.tsx"]
    n4["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n5["frontend/src/components/team/VacationCsvImport.tsx"]
    n6["frontend/src/components/ui/OverflowMenu.tsx"]
    n0 --> n2
    n1 --> n2
    n3 --> n0
    n3 --> n2
    n4 --> n0
    n4 --> n2
    n5 --> n0
    n5 --> n2
    n6 --> n0
    n6 --> n2
    click n0 "../modules/Button.md"
    click n1 "../modules/ButtonLink.md"
    click n2 "../modules/buttonStyles.md"
    click n3 "../modules/PlanShareSection.md"
    click n4 "../modules/WorkCalendarSettings.md"
    click n5 "../modules/VacationCsvImport.md"
    click n6 "../modules/OverflowMenu.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [Button](../modules/Button.md) |
| Inbound | [ButtonLink](../modules/ButtonLink.md) |
| Inbound | [PlanShareSection](../modules/PlanShareSection.md) |
| Inbound | [WorkCalendarSettings](../modules/WorkCalendarSettings.md) |
| Inbound | [VacationCsvImport](../modules/VacationCsvImport.md) |
| Inbound | [OverflowMenu](../modules/OverflowMenu.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ButtonVariant](../entities/ButtonVariant.md) | Type alias | 3 | `'primary' \| 'secondary' \| 'danger' \| 'warning' \| 'ghost' \| 'outline' \| 'plain'` | — |
| [ButtonSize](../entities/ButtonSize.md) | Type alias | 4 | `'sm' \| 'md' \| 'lg'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `buttonClassName` | `(variant: ButtonVariant = 'primary', size: ButtonSize = 'md', className?: string, iconOnly = false)` | — | — |
