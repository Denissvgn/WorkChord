# CapacityAdjustmentCommand

**Location:** `backend/app/schemas/team.py:422`
**Kind:** Class
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Record and withdraw dated adjustments on one capacity row in one command.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_change` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `adjustments` | `list[CapacityAdjustmentItem]` | `adjustments` | No | No | factory: `list` | max_length=50 | — | — |
| `withdraw_adjustment_ids` | `list[int]` | `withdraw_adjustment_ids` | No | No | factory: `list` | max_length=50 | — | — |
| `reason` | `str` | `reason` | Yes | No | — | max_length=1000; min_length=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_change` | `() -> 'CapacityAdjustmentCommand'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CapacityAdjustmentCommand (backend/app/schemas/team.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["apply_capacity_adjustment (backend/app/routers/team.py)"]
    n4["preview_capacity_adjustment (backend/app/routers/team.py)"]
    n5["CapacityAdjustmentCommand.validate_change (backend/app/schemas/team.py)"]
    n6["AgentPlanningService.apply_capacity_adjustment (backend/app/services/agent_planning_service.py)"]
    n7["CapacityAdjustmentService.apply (backend/app/services/capacity_adjustments.py)"]
    n8["CapacityAdjustmentService.preview (backend/app/services/capacity_adjustments.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_team.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_team.md"
    click n4 "../modules/routers_team.md"
    click n5 "../modules/schemas_team.md"
    click n6 "../modules/agent_planning_service.md"
    click n7 "../modules/capacity_adjustments.md"
    click n8 "../modules/capacity_adjustments.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 1 | `adjustments`, `reason`, `withdraw_adjustment_ids` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `apply_capacity_adjustment` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `preview_capacity_adjustment` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `CapacityAdjustmentCommand.validate_change` | type_reference | [schemas_team](../modules/schemas_team.md) | — |
| `AgentPlanningService.apply_capacity_adjustment` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `CapacityAdjustmentService.apply` | type_reference | [capacity_adjustments](../modules/capacity_adjustments.md) | — |
| `CapacityAdjustmentService.preview` | type_reference | [capacity_adjustments](../modules/capacity_adjustments.md) | — |
