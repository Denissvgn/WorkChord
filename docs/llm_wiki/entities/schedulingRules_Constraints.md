# Constraints

**Location:** `frontend/src/types/schedulingRules.ts:37`
**Kind:** Class
**Bases:** —
**Module:** [schedulingRules](../modules/schedulingRules.md)

## Description

_Auto-generated from `Constraints` in `frontend/src/types/schedulingRules.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `sequential_per_assignee` | `boolean` | *required* | — |
| `respect_dependencies` | `boolean` | *required* | — |
| `min_start_date` | `boolean` | *required* | — |
| `max_finish_date` | `boolean` | *required* | — |
| `prefer_uninterrupted` | `boolean` | *required* | — |
| `balance_workload` | `BalanceWorkload \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Constraints (frontend/src/types/schedulingRules.ts)"]
    n1["frontend/src/components/settings/ConstraintsPanel.tsx"]
    n2["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/schedulingRules.md"
    click n1 "../modules/ConstraintsPanel.md"
    click n2 "../modules/SchedulingRulesSettings.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schedulingRules](../modules/schedulingRules.md) | 0 | `balance_workload`, `max_finish_date`, `min_start_date`, `prefer_uninterrupted`, `respect_dependencies`, `sequential_per_assignee` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ConstraintsPanel` | import | [ConstraintsPanel](../modules/ConstraintsPanel.md) | — |
| `SchedulingRulesSettings` | import | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) | — |
