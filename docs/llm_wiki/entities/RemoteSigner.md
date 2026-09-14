# RemoteSigner

**Location:** `backend/app/autonomy/signing.py:77`
**Kind:** Class
**Bases:** `Protocol`
**Module:** [signing](../modules/signing.md)

**Decorators:** `@runtime_checkable`

## Description

Sign a digest through a non-exportable external key service.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `sign_digest` | `(*, payload_sha256: str, key_ref: str, subject: str) -> DetachedSignatureEnvelope` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RemoteSigner (backend/app/autonomy/signing.py)"]
    n1["Protocol"]
    n2["sign_charter_verification_receipt (backend/app/autonomy/contracts/charter.py)"]
    n3["sign_closeout_decision (backend/app/autonomy/handoff.py)"]
    n4["sign_handoff_verification (backend/app/autonomy/handoff.py)"]
    n5["ActionLeasePolicy.__init__ (backend/app/autonomy/leases.py)"]
    n6["sign_agent_preflight (backend/app/autonomy/preflight.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/signing.md"
    click n2 "../modules/charter.md"
    click n3 "../modules/handoff.md"
    click n4 "../modules/handoff.md"
    click n5 "../modules/leases.md"
    click n6 "../modules/preflight.md"
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
| `sign_charter_verification_receipt` | type_reference | [charter](../modules/charter.md) | — |
| `sign_closeout_decision` | type_reference | [handoff](../modules/handoff.md) | — |
| `sign_handoff_verification` | type_reference | [handoff](../modules/handoff.md) | — |
| `ActionLeasePolicy.__init__` | type_reference | [leases](../modules/leases.md) | — |
| `sign_agent_preflight` | type_reference | [preflight](../modules/preflight.md) | — |
