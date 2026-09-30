# FakeRemoteSigner

**Location:** `backend/tests/autonomy/test_autonomy_foundation.py:117`
**Kind:** Class
**Bases:** —
**Module:** [test_autonomy_foundation](../modules/test_autonomy_foundation.md)

## Description

_Auto-generated from `FakeRemoteSigner` in `backend/tests/autonomy/test_autonomy_foundation.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `() -> None` | — | — |
| `sign_digest` | `(*, payload_sha256: str, key_ref: str, subject: str) -> DetachedSignatureEnvelope` | — | — |
| `trust_anchor` | `(*subjects: str) -> PublicTrustAnchor` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FakeRemoteSigner (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n1["_handoff_fact (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n2["_signed_document (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n3["_signed_evidence (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n4["test_action_lease_binds_exact_attempt_target_generation_and_remote_key (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n5["test_charter_and_finite_bootstrap_manifest_verify_from_external_trust (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n6["test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n7["test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/test_autonomy_foundation.md"
    click n1 "../modules/test_autonomy_foundation.md"
    click n2 "../modules/test_autonomy_foundation.md"
    click n3 "../modules/test_autonomy_foundation.md"
    click n4 "../modules/test_autonomy_foundation.md"
    click n5 "../modules/test_autonomy_foundation.md"
    click n6 "../modules/test_autonomy_foundation.md"
    click n7 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 3 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_handoff_fact` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
| `_signed_document` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
| `_signed_evidence` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
| `test_action_lease_binds_exact_attempt_target_generation_and_remote_key` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `test_charter_and_finite_bootstrap_manifest_verify_from_external_trust` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
