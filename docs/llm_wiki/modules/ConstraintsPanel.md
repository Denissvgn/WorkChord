# ConstraintsPanel Module

**Path:** `frontend/src/components/settings/ConstraintsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/ConstraintsPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/schedulingRules` | `Constraints` |
| `../common/Checkbox` | `Checkbox` |
| `../common/Input` | `Input` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ConstraintsPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Checkbox.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/settings/ConstraintsPanel.tsx"]
    n3["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n4["frontend/src/types/schedulingRules.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n3 --> n2
    n3 --> n4
    click n0 "../modules/Checkbox.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/ConstraintsPanel.md"
    click n3 "../modules/SchedulingRulesSettings.md"
    click n4 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Outbound | [Checkbox](../modules/Checkbox.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Props](../entities/ConstraintsPanel_Props.md) | Class | 6 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ConstraintsPanel` | `({ constraints, onChange }: Props)` | — | — |
