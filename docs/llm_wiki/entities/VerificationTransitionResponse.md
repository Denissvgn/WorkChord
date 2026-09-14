# VerificationTransitionResponse

**Location:** `backend/app/schemas/autonomy.py:185`
**Kind:** Pydantic model
**Bases:** `AutonomySchema`
**Module:** [schemas_autonomy](../modules/schemas_autonomy.md)

## Description

_Auto-generated from `VerificationTransitionResponse` in `backend/app/schemas/autonomy.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `requirement` | `VerificationRequirementResponse` | `requirement` | Yes | No | — | — | — | — |
| `package_state` | `Literal['planned', 'evaluating', 'passed', 'rework_required']` | `package_state` | Yes | No | — | — | — | — |
| `verdict` | `Literal['passed', 'rejected'] \| None` | `verdict` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VerificationTransitionResponse (backend/app/schemas/autonomy.py)"]
    n1["AutonomySchema (backend/app/schemas/autonomy.py)"]
    n2["AutonomyWorkPackageService._lease_transition (backend/app/services/autonomy_work_package_service.py)"]
    n3["AutonomyWorkPackageService.begin_requirement (backend/app/services/autonomy_work_package_service.py)"]
    n4["AutonomyWorkPackageService.claim_requirement (backend/app/services/autonomy_work_package_service.py)"]
    n5["AutonomyWorkPackageService.renew_requirement (backend/app/services/autonomy_work_package_service.py)"]
    n6["AutonomyWorkPackageService.submit_requirement (backend/app/services/autonomy_work_package_service.py)"]
    n7["AutonomyWorkPackageService.transition_response (backend/app/services/autonomy_work_package_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_autonomy.md"
    click n1 "../modules/schemas_autonomy.md"
    click n2 "../modules/autonomy_work_package_service.md"
    click n3 "../modules/autonomy_work_package_service.md"
    click n4 "../modules/autonomy_work_package_service.md"
    click n5 "../modules/autonomy_work_package_service.md"
    click n6 "../modules/autonomy_work_package_service.md"
    click n7 "../modules/autonomy_work_package_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_autonomy](../modules/schemas_autonomy.md) | 0 | `package_state`, `requirement`, `verdict` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AutonomySchema` | [schemas_autonomy](../modules/schemas_autonomy.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AutonomyWorkPackageService._lease_transition` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.begin_requirement` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.claim_requirement` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.renew_requirement` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.submit_requirement` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.transition_response` | call | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | 1 |
| `AutonomyWorkPackageService.transition_response` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
