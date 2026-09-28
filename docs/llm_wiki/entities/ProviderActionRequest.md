# ProviderActionRequest

**Location:** `backend/app/autonomy/providers.py:24`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [providers](../modules/providers.md)

## Description

Exact mutation request; adapter selection remains charter-owned.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `bounded_action` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `domain` | `Literal['platform', 'database', 'application', 'security', 'sanitization', 'retention']` | `domain` | Yes | No | — | — | — | — |
| `operation` | `str` | `operation` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `resource_ref` | `str` | `resource_ref` | Yes | No | — | max_length=2048; pattern=unknown (OPAQUE_REF_PATTERN) | — | — |
| `resource_generation` | `str` | `resource_generation` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `environment` | `Literal['ephemeral', 'rehearsal', 'production']` | `environment` | Yes | No | — | — | — | — |
| `destructive` | `bool` | `destructive` | No | No | `False` | — | — | — |
| `exact_object_digest` | `str \| None` | `exact_object_digest` | No | Yes | `None` | pattern=unknown (SHA256_PATTERN) | — | — |
| `lease` | `SignedActionLease` | `lease` | Yes | No | — | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `bounded_action` | `() -> 'ProviderActionRequest'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProviderActionRequest (backend/app/autonomy/providers.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["correlate_provider_action (backend/app/autonomy/providers.py)"]
    n3["ProviderActionRequest.bounded_action (backend/app/autonomy/providers.py)"]
    n4["ProviderMutationAdapter.execute (backend/app/autonomy/providers.py)"]
    n5["test_action_lease_binds_exact_attempt_target_generation_and_remote_key (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/providers.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/providers.md"
    click n3 "../modules/providers.md"
    click n4 "../modules/providers.md"
    click n5 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [providers](../modules/providers.md) | 1 | `destructive`, `domain`, `environment`, `exact_object_digest`, `lease`, `operation`, `resource_generation`, `resource_ref` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `correlate_provider_action` | type_reference | [providers](../modules/providers.md) | — |
| `ProviderActionRequest.bounded_action` | type_reference | [providers](../modules/providers.md) | — |
| `ProviderMutationAdapter.execute` | type_reference | [providers](../modules/providers.md) | — |
| `test_action_lease_binds_exact_attempt_target_generation_and_remote_key` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
