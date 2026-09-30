# SignedActionLease

**Location:** `backend/app/autonomy/leases.py:127`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [leases](../modules/leases.md)

## Description

_Auto-generated from `SignedActionLease` in `backend/app/autonomy/leases.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `lease` | `ActionLease` | `lease` | Yes | No | — | — | — | — |
| `signature` | `DetachedSignatureEnvelope` | `signature` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SignedActionLease (backend/app/autonomy/leases.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["ActionLeasePolicy.issue (backend/app/autonomy/leases.py)"]
    n3["verify_action_lease (backend/app/autonomy/leases.py)"]
    n4["backend/app/autonomy/providers.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/leases.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/leases.md"
    click n3 "../modules/leases.md"
    click n4 "../modules/providers.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [leases](../modules/leases.md) | 0 | `lease`, `signature` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ActionLeasePolicy.issue` | call | [leases](../modules/leases.md) | 1 |
| `ActionLeasePolicy.issue` | type_reference | [leases](../modules/leases.md) | — |
| `verify_action_lease` | type_reference | [leases](../modules/leases.md) | — |
| `providers` | import | [providers](../modules/providers.md) | — |
