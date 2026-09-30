# scheduling_rules Module

**Path:** `backend/app/schemas/scheduling_rules.py`

## Description

Scheduling rules schemas for API.

## Imports

| Source | Symbols |
|--------|---------|
| `pydantic` | `BaseModel`, `Field` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/scheduling_rules.py"]
    n1["backend/app/schemas/scheduling_rules.py"]
    n0 --> n1
    click n0 "../modules/routers_scheduling_rules.md"
    click n1 "../modules/schemas_scheduling_rules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_scheduling_rules](../modules/routers_scheduling_rules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SortCriterionSchema](../entities/SortCriterionSchema.md) | 7 | `BaseModel` | A single sort criterion. |
| [FilterConfigSchema](../entities/FilterConfigSchema.md) | 13 | `BaseModel` | Filter configuration with conditions. |
| [SchedulingPassSchema](../entities/SchedulingPassSchema.md) | 18 | `BaseModel` | A scheduling pass with filter and sort rules. |
| [EffortModifierSchema](../entities/EffortModifierSchema.md) | 27 | `BaseModel` | An effort modifier rule. |
| [BalanceWorkloadSchema](../entities/BalanceWorkloadSchema.md) | 37 | `BaseModel` | Workload balancing configuration. |
| [ConstraintsSchema](../entities/ConstraintsSchema.md) | 43 | `BaseModel` | Scheduling constraints configuration. |
| [SchedulingRulesSchema](../entities/SchedulingRulesSchema.md) | 53 | `BaseModel` | Complete scheduling rules configuration. |
| [SchedulingRulesResponse](../entities/schemas_scheduling_rules_SchedulingRulesResponse.md) | 64 | `BaseModel` | Response wrapper for scheduling rules. |
