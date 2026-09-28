# TrustedKeyBinding

**Location:** `backend/app/autonomy/contracts/charter.py:146`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [charter](../modules/charter.md)

## Description

_Auto-generated from `TrustedKeyBinding` in `backend/app/autonomy/contracts/charter.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `logical_key` | `str` | `logical_key` | Yes | No | — | pattern=unknown (IDENTIFIER_PATTERN) | — | — |
| `key_ref` | `str` | `key_ref` | Yes | No | — | max_length=1024; pattern=unknown (OPAQUE_REF_PATTERN) | — | — |
| `issuer` | `str` | `issuer` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `allowed_subject` | `str` | `allowed_subject` | Yes | No | — | max_length=512; min_length=1 | — | — |
| `intended_use` | `str` | `intended_use` | Yes | No | — | max_length=255; min_length=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TrustedKeyBinding (backend/app/autonomy/contracts/charter.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["_charter (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/charter.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [charter](../modules/charter.md) | 0 | `allowed_subject`, `intended_use`, `issuer`, `key_ref`, `logical_key` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_charter` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
