# DetachedSignatureEnvelope

**Location:** `backend/app/autonomy/signing.py:24`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [signing](../modules/signing.md)

## Description

Provider-neutral signature metadata without an embedded trust key.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `valid_base64` | field | signature_base64 | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `schema_version` | `Literal['workchord-remote-signature-v1']` | `schema_version` | No | No | `'workchord-remote-signature-v1'` | — | — | — |
| `key_ref` | `str` | `key_ref` | Yes | No | — | max_length=512; pattern=unknown (KEY_REF_PATTERN) | — | — |
| `key_version` | `str` | `key_version` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `issuer` | `str` | `issuer` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `subject` | `str` | `subject` | Yes | No | — | max_length=512; min_length=1 | — | — |
| `algorithm` | `Literal['ed25519', 'ecdsa-p256-sha256', 'rsa-pss-sha256']` | `algorithm` | Yes | No | — | — | — | — |
| `payload_sha256` | `str` | `payload_sha256` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `signature_base64` | `str` | `signature_base64` | Yes | No | — | max_length=16384; min_length=4 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `valid_base64` | `(value: str) -> str` | `@field_validator('signature_base64')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DetachedSignatureEnvelope (backend/app/autonomy/signing.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["backend/app/autonomy/contracts/charter.py"]
    n3["backend/app/autonomy/evidence.py"]
    n4["backend/app/autonomy/handoff.py"]
    n5["backend/app/autonomy/leases.py"]
    n6["backend/app/autonomy/preflight.py"]
    n7["RemoteSigner.sign_digest (backend/app/autonomy/signing.py)"]
    n8["verify_detached_signature (backend/app/autonomy/signing.py)"]
    n9["FakeRemoteSigner.sign_digest (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/signing.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/charter.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/handoff.md"
    click n5 "../modules/leases.md"
    click n6 "../modules/preflight.md"
    click n7 "../modules/signing.md"
    click n8 "../modules/signing.md"
    click n9 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [signing](../modules/signing.md) | 1 | `algorithm`, `issuer`, `key_ref`, `key_version`, `payload_sha256`, `schema_version`, `signature_base64`, `subject` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `charter` | import | [charter](../modules/charter.md) | — |
| `evidence` | import | [evidence](../modules/evidence.md) | — |
| `handoff` | import | [handoff](../modules/handoff.md) | — |
| `leases` | import | [leases](../modules/leases.md) | — |
| `preflight` | import | [preflight](../modules/preflight.md) | — |
| `RemoteSigner.sign_digest` | type_reference | [signing](../modules/signing.md) | — |
| `verify_detached_signature` | type_reference | [signing](../modules/signing.md) | — |
| `FakeRemoteSigner.sign_digest` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `FakeRemoteSigner.sign_digest` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
