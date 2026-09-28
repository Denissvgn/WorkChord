# ImmutableInputBinding

**Location:** `backend/app/autonomy/contracts/charter.py:87`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [charter](../modules/charter.md)

## Description

_Auto-generated from `ImmutableInputBinding` in `backend/app/autonomy/contracts/charter.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `logical_key` | `str` | `logical_key` | Yes | No | — | max_length=255; pattern=unknown (IDENTIFIER_PATTERN) | — | — |
| `object_uri` | `str` | `object_uri` | Yes | No | — | max_length=1024; pattern=unknown (OPAQUE_REF_PATTERN) | — | — |
| `sha256` | `str` | `sha256` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `byte_length` | `int` | `byte_length` | Yes | No | — | ge=1; le=100000000 | — | — |
| `media_type` | `str` | `media_type` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `schema_version` | `str` | `schema_version` | Yes | No | — | max_length=255; min_length=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImmutableInputBinding (backend/app/autonomy/contracts/charter.py)"]
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
| [charter](../modules/charter.md) | 0 | `byte_length`, `logical_key`, `media_type`, `object_uri`, `schema_version`, `sha256` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_charter` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
