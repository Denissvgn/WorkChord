# AutonomySchema

**Location:** `backend/app/schemas/autonomy.py:15`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_autonomy](../modules/schemas_autonomy.md)

## Description

_Auto-generated from `AutonomySchema` in `backend/app/schemas/autonomy.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |
| `str_strip_whitespace` | `True` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AutonomySchema (backend/app/schemas/autonomy.py)"]
    n1["BaseModel"]
    n2["AgentWorkPackageCreate (backend/app/schemas/autonomy.py)"]
    n3["AgentWorkPackageResponse (backend/app/schemas/autonomy.py)"]
    n4["ResolvedVerifierLease (backend/app/schemas/autonomy.py)"]
    n5["VerificationBeginRequest (backend/app/schemas/autonomy.py)"]
    n6["VerificationClaimRequest (backend/app/schemas/autonomy.py)"]
    n7["VerificationCriterionResult (backend/app/schemas/autonomy.py)"]
    n8["VerificationRenewRequest (backend/app/schemas/autonomy.py)"]
    n9["VerificationRequirementCreate (backend/app/schemas/autonomy.py)"]
    n10["VerificationRequirementResponse (backend/app/schemas/autonomy.py)"]
    n11["VerificationSubmitRequest (backend/app/schemas/autonomy.py)"]
    n12["VerificationTransitionResponse (backend/app/schemas/autonomy.py)"]
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
    n11 --> n0
    n12 --> n0
    click n0 "../modules/schemas_autonomy.md"
    click n2 "../modules/schemas_autonomy.md"
    click n3 "../modules/schemas_autonomy.md"
    click n4 "../modules/schemas_autonomy.md"
    click n5 "../modules/schemas_autonomy.md"
    click n6 "../modules/schemas_autonomy.md"
    click n7 "../modules/schemas_autonomy.md"
    click n8 "../modules/schemas_autonomy.md"
    click n9 "../modules/schemas_autonomy.md"
    click n10 "../modules/schemas_autonomy.md"
    click n11 "../modules/schemas_autonomy.md"
    click n12 "../modules/schemas_autonomy.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_autonomy](../modules/schemas_autonomy.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentWorkPackageCreate` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `AgentWorkPackageResponse` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `ResolvedVerifierLease` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationBeginRequest` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationClaimRequest` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationCriterionResult` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationRenewRequest` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationRequirementCreate` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationRequirementResponse` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationSubmitRequest` | [schemas_autonomy](../modules/schemas_autonomy.md) |
| Subclass | `VerificationTransitionResponse` | [schemas_autonomy](../modules/schemas_autonomy.md) |
