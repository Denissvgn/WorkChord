# BackendBuildIdentity

**Location:** `backend/app/build_identity.py:32`
**Kind:** Pydantic model
**Bases:** `BuildIdentity`
**Module:** [build_identity](../modules/build_identity.md)

## Description

Backend package identity plus its independently built gateway digest.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `component` | `Literal['backend']` | `component` | No | No | `'backend'` | — | — | — |
| `expected_frontend_artifact_digest` | `str` | `expected_frontend_artifact_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["BackendBuildIdentity (backend/app/build_identity.py)"]
    n1["BuildIdentity (backend/app/build_identity.py)"]
    n2["verify_receipt_current_build (backend/app/autonomy/server_acceptance.py)"]
    n3["load_backend_build_identity (backend/app/build_identity.py)"]
    n4["main (backend/app/build_identity.py)"]
    n5["_build_identity (backend/tests/autonomy/test_server_acceptance.py)"]
    n6["test_baked_build_identity_hashes_stable_package_members (backend/tests/autonomy/test_server_acceptance.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/build_identity.md"
    click n1 "../modules/build_identity.md"
    click n2 "../modules/autonomy_server_acceptance.md"
    click n3 "../modules/build_identity.md"
    click n4 "../modules/build_identity.md"
    click n5 "../modules/test_server_acceptance.md"
    click n6 "../modules/test_server_acceptance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [build_identity](../modules/build_identity.md) | 0 | `component`, `expected_frontend_artifact_digest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BuildIdentity` | [build_identity](../modules/build_identity.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `verify_receipt_current_build` | type_reference | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | — |
| `load_backend_build_identity` | type_reference | [build_identity](../modules/build_identity.md) | — |
| `main` | call | [build_identity](../modules/build_identity.md) | 1 |
| `_build_identity` | call | [test_server_acceptance](../modules/test_server_acceptance.md) | 1 |
| `_build_identity` | type_reference | [test_server_acceptance](../modules/test_server_acceptance.md) | — |
| `test_baked_build_identity_hashes_stable_package_members` | call | [test_server_acceptance](../modules/test_server_acceptance.md) | 1 |
