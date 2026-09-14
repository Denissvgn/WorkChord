# SchedulingPass

**Location:** `backend/app/services/scheduling_rules_service.py:43`
**Kind:** Class
**Bases:** —
**Module:** [scheduling_rules_service](../modules/scheduling_rules_service.md)

**Decorators:** `@dataclass`

## Description

A scheduling pass with filter and sort rules.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `str` | *required* | — |
| `description` | `str` | *required* | — |
| `filter_conditions` | `list[str]` | *required* | — |
| `sort_criteria` | `list[SortCriterion]` | *required* | — |
| `enabled` | `bool` | `True` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SchedulingPass (backend/app/services/scheduling_rules_service.py)"]
    n1["SchedulingRulesService._parse_rules (backend/app/services/scheduling_rules_service.py)"]
    n2["SchedulingRulesService.get_scheduling_passes (backend/app/services/scheduling_rules_service.py)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/scheduling_rules_service.md"
    click n1 "../modules/scheduling_rules_service.md"
    click n2 "../modules/scheduling_rules_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [scheduling_rules_service](../modules/scheduling_rules_service.md) | 0 | `description`, `enabled`, `filter_conditions`, `id`, `sort_criteria` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulingRulesService._parse_rules` | call | [scheduling_rules_service](../modules/scheduling_rules_service.md) | 1 |
| `SchedulingRulesService.get_scheduling_passes` | type_reference | [scheduling_rules_service](../modules/scheduling_rules_service.md) | — |
