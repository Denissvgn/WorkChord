# SortCriterion

**Location:** `backend/app/services/scheduling_rules_service.py:36`
**Kind:** Class
**Bases:** —
**Module:** [scheduling_rules_service](../modules/scheduling_rules_service.md)

**Decorators:** `@dataclass`

## Description

A single sort criterion.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `field` | `str` | *required* | — |
| `order` | `str` | `'asc'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SortCriterion (backend/app/services/scheduling_rules_service.py)"]
    n1["SchedulingRulesService._parse_rules (backend/app/services/scheduling_rules_service.py)"]
    n1 --> n0
    click n0 "../modules/scheduling_rules_service.md"
    click n1 "../modules/scheduling_rules_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [scheduling_rules_service](../modules/scheduling_rules_service.md) | 0 | `field`, `order` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulingRulesService._parse_rules` | call | [scheduling_rules_service](../modules/scheduling_rules_service.md) | 1 |
