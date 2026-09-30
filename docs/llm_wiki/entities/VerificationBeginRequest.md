# VerificationBeginRequest

**Location:** `backend/app/schemas/autonomy.py:94`
**Kind:** Pydantic model
**Bases:** `AutonomySchema`
**Module:** [schemas_autonomy](../modules/schemas_autonomy.md)

## Description

_Auto-generated from `VerificationBeginRequest` in `backend/app/schemas/autonomy.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `requirement_id` | `int` | `requirement_id` | Yes | No | — | ge=1 | — | — |
| `expected_lease_generation` | `int` | `expected_lease_generation` | Yes | No | — | ge=1 | — | — |
| `expected_lease_digest` | `str` | `expected_lease_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `runtime_attestation_digest` | `str` | `runtime_attestation_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `external_journal_revision` | `int` | `external_journal_revision` | Yes | No | — | ge=1 | — | — |
| `external_journal_head_digest` | `str` | `external_journal_head_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VerificationBeginRequest (backend/app/schemas/autonomy.py)"]
    n1["AutonomySchema (backend/app/schemas/autonomy.py)"]
    n2["AutonomyWorkPackageService._lease_transition (backend/app/services/autonomy_work_package_service.py)"]
    n3["AutonomyWorkPackageService.begin_requirement (backend/app/services/autonomy_work_package_service.py)"]
    n4["test_multi_slot_verification_is_fenced_and_rejection_invalidates_sibling (backend/tests/autonomy/test_work_package_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_autonomy.md"
    click n1 "../modules/schemas_autonomy.md"
    click n2 "../modules/autonomy_work_package_service.md"
    click n3 "../modules/autonomy_work_package_service.md"
    click n4 "../modules/test_work_package_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_autonomy](../modules/schemas_autonomy.md) | 0 | `expected_lease_digest`, `expected_lease_generation`, `external_journal_head_digest`, `external_journal_revision`, `requirement_id`, `runtime_attestation_digest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AutonomySchema` | [schemas_autonomy](../modules/schemas_autonomy.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AutonomyWorkPackageService._lease_transition` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `AutonomyWorkPackageService.begin_requirement` | type_reference | [autonomy_work_package_service](../modules/autonomy_work_package_service.md) | — |
| `test_multi_slot_verification_is_fenced_and_rejection_invalidates_sibling` | call | [test_work_package_service](../modules/test_work_package_service.md) | 3 |
