# RoutingCalibrationContractDetail

**Location:** `backend/app/schemas/routing_calibration.py:267`
**Kind:** Pydantic model
**Bases:** `RoutingCalibrationContractResponse`
**Module:** [schemas_routing_calibration](../modules/schemas_routing_calibration.md)

## Description

One contract with every revision it has had.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `revisions` | `list[RoutingCalibrationContractRevisionResponse]` | `revisions` | No | No | factory: `list` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingCalibrationContractDetail (backend/app/schemas/routing_calibration.py)"]
    n1["RoutingCalibrationContractResponse (backend/app/schemas/routing_calibration.py)"]
    n2["get_routing_calibration_contract (backend/app/routers/agent_catalog.py)"]
    n3["RoutingCalibrationContractService.get_contract (backend/app/services/routing_calibration_contract_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_routing_calibration.md"
    click n1 "../modules/schemas_routing_calibration.md"
    click n2 "../modules/agent_catalog.md"
    click n3 "../modules/routing_calibration_contract_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_calibration](../modules/schemas_routing_calibration.md) | 0 | `revisions` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingCalibrationContractResponse` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_routing_calibration_contract` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `RoutingCalibrationContractService.get_contract` | call | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | 1 |
| `RoutingCalibrationContractService.get_contract` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
