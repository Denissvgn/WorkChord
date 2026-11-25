# CapacityTransferWithdrawal

**Location:** `backend/app/schemas/team.py:541`
**Kind:** Class
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Return the lent capacity of every row of one transfer together.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_reason` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `reason` | `str` | `reason` | Yes | No | — | min_length=1; max_length=1000 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_reason` | `() -> 'CapacityTransferWithdrawal'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CapacityTransferWithdrawal (backend/app/schemas/team.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["preview_capacity_transfer_withdrawal (backend/app/routers/team.py)"]
    n4["withdraw_capacity_transfer (backend/app/routers/team.py)"]
    n5["CapacityTransferWithdrawal.validate_reason (backend/app/schemas/team.py)"]
    n6["AgentPlanningService.withdraw_capacity_transfer (backend/app/services/agent_planning_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_team.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_team.md"
    click n4 "../modules/routers_team.md"
    click n5 "../modules/schemas_team.md"
    click n6 "../modules/agent_planning_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 1 | `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `preview_capacity_transfer_withdrawal` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `withdraw_capacity_transfer` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `CapacityTransferWithdrawal.validate_reason` | type_reference | [schemas_team](../modules/schemas_team.md) | — |
| `AgentPlanningService.withdraw_capacity_transfer` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
