# PublicTrustResolver

**Location:** `backend/app/autonomy/signing.py:70`
**Kind:** Class
**Bases:** `Protocol`
**Module:** [signing](../modules/signing.md)

**Decorators:** `@runtime_checkable`

## Description

Resolve a current public key from an external trust source.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `resolve` | `(*, key_ref: str, key_version: str) -> PublicTrustAnchor` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PublicTrustResolver (backend/app/autonomy/signing.py)"]
    n1["Protocol"]
    n2["CharterVerifier.__init__ (backend/app/autonomy/contracts/charter.py)"]
    n3["EvidenceResolver.__init__ (backend/app/autonomy/evidence.py)"]
    n4["evaluate_closeout (backend/app/autonomy/handoff.py)"]
    n5["verify_action_lease (backend/app/autonomy/leases.py)"]
    n6["verify_detached_signature (backend/app/autonomy/signing.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/signing.md"
    click n2 "../modules/charter.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/handoff.md"
    click n5 "../modules/leases.md"
    click n6 "../modules/signing.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [signing](../modules/signing.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Protocol` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CharterVerifier.__init__` | type_reference | [charter](../modules/charter.md) | — |
| `EvidenceResolver.__init__` | type_reference | [evidence](../modules/evidence.md) | — |
| `evaluate_closeout` | type_reference | [handoff](../modules/handoff.md) | — |
| `verify_action_lease` | type_reference | [leases](../modules/leases.md) | — |
| `verify_detached_signature` | type_reference | [signing](../modules/signing.md) | — |
