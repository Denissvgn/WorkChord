# _CalibrationModel

**Location:** `backend/app/schemas/routing_calibration.py:31`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_routing_calibration](../modules/schemas_routing_calibration.md)

## Description

_Auto-generated from `_CalibrationModel` in `backend/app/schemas/routing_calibration.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |
| `from_attributes` | `True` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["_CalibrationModel (backend/app/schemas/routing_calibration.py)"]
    n1["BaseModel"]
    n2["CalibrationBiasReview (backend/app/schemas/routing_calibration.py)"]
    n3["CalibrationContractActor (backend/app/schemas/routing_calibration.py)"]
    n4["CalibrationDecay (backend/app/schemas/routing_calibration.py)"]
    n5["CalibrationSampleBounds (backend/app/schemas/routing_calibration.py)"]
    n6["RoutingCalibrationContractApprove (backend/app/schemas/routing_calibration.py)"]
    n7["RoutingCalibrationContractListResponse (backend/app/schemas/routing_calibration.py)"]
    n8["RoutingCalibrationContractResponse (backend/app/schemas/routing_calibration.py)"]
    n9["RoutingCalibrationContractRevisionResponse (backend/app/schemas/routing_calibration.py)"]
    n10["RoutingCalibrationContractTerms (backend/app/schemas/routing_calibration.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/schemas_routing_calibration.md"
    click n2 "../modules/schemas_routing_calibration.md"
    click n3 "../modules/schemas_routing_calibration.md"
    click n4 "../modules/schemas_routing_calibration.md"
    click n5 "../modules/schemas_routing_calibration.md"
    click n6 "../modules/schemas_routing_calibration.md"
    click n7 "../modules/schemas_routing_calibration.md"
    click n8 "../modules/schemas_routing_calibration.md"
    click n9 "../modules/schemas_routing_calibration.md"
    click n10 "../modules/schemas_routing_calibration.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_calibration](../modules/schemas_routing_calibration.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `CalibrationBiasReview` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `CalibrationContractActor` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `CalibrationDecay` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `CalibrationSampleBounds` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `RoutingCalibrationContractApprove` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `RoutingCalibrationContractListResponse` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `RoutingCalibrationContractResponse` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `RoutingCalibrationContractRevisionResponse` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
| Subclass | `RoutingCalibrationContractTerms` | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) |
