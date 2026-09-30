# FakeTrustResolver

**Location:** `backend/tests/autonomy/test_autonomy_foundation.py:159`
**Kind:** Class
**Bases:** —
**Module:** [test_autonomy_foundation](../modules/test_autonomy_foundation.md)

## Description

_Auto-generated from `FakeTrustResolver` in `backend/tests/autonomy/test_autonomy_foundation.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(anchor: PublicTrustAnchor) -> None` | — | — |
| `resolve` | `(*, key_ref: str, key_version: str) -> PublicTrustAnchor` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FakeTrustResolver (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n1["test_action_lease_binds_exact_attempt_target_generation_and_remote_key (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n2["test_charter_and_finite_bootstrap_manifest_verify_from_external_trust (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n3["test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n4["test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/test_autonomy_foundation.md"
    click n1 "../modules/test_autonomy_foundation.md"
    click n2 "../modules/test_autonomy_foundation.md"
    click n3 "../modules/test_autonomy_foundation.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_action_lease_binds_exact_attempt_target_generation_and_remote_key` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 3 |
| `test_charter_and_finite_bootstrap_manifest_verify_from_external_trust` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 3 |
| `test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
