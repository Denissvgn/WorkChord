# signing Module

**Path:** `backend/app/autonomy/signing.py`

## Description

Detached remote-signing envelopes and pinned public-key verification.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `StrictContractModel`, `sha256_hex` |
| `base64` | `base64` |
| `binascii` | `binascii` |
| `collections.abc` | `Callable` |
| `cryptography.exceptions` | `InvalidSignature` |
| `cryptography.hazmat.primitives` | `hashes`, `serialization` |
| `cryptography.hazmat.primitives.asymmetric` | `ec`, `ed25519`, `padding`, `rsa` |
| `dataclasses` | `dataclass` |
| `pydantic` | `Field`, `field_validator` |
| `re` | `re` |
| `typing` | `Literal`, `Protocol`, `runtime_checkable` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/canonical.py"]
    n1["backend/app/autonomy/contracts/charter.py"]
    n2["backend/app/autonomy/evidence.py"]
    n3["backend/app/autonomy/handoff.py"]
    n4["backend/app/autonomy/leases.py"]
    n5["backend/app/autonomy/preflight.py"]
    n6["backend/app/autonomy/signing.py"]
    n7["backend/tests/autonomy/test_autonomy_foundation.py"]
    n1 --> n0
    n1 --> n6
    n2 --> n0
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n6
    n6 --> n0
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    click n0 "../modules/autonomy_canonical.md"
    click n1 "../modules/charter.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/handoff.md"
    click n4 "../modules/leases.md"
    click n5 "../modules/preflight.md"
    click n6 "../modules/signing.md"
    click n7 "../modules/test_autonomy_foundation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [charter](../modules/charter.md) |
| Inbound | [evidence](../modules/evidence.md) |
| Inbound | [handoff](../modules/handoff.md) |
| Inbound | [leases](../modules/leases.md) |
| Inbound | [preflight](../modules/preflight.md) |
| Inbound | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) |
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DetachedSignatureEnvelope](../entities/DetachedSignatureEnvelope.md) | 24 | `StrictContractModel` | Provider-neutral signature metadata without an embedded trust key. |
| [PublicTrustAnchor](../entities/PublicTrustAnchor.md) | 48 | `StrictContractModel` | A public key returned by a separately trusted resolver. |
| [PublicTrustResolver](../entities/PublicTrustResolver.md) | 70 | `Protocol` | Resolve a current public key from an external trust source. |
| [RemoteSigner](../entities/RemoteSigner.md) | 77 | `Protocol` | Sign a digest through a non-exportable external key service. |
| [SignatureVerificationError](../entities/SignatureVerificationError.md) | 89 | `ValueError` | Raised when a detached remote signature fails closed. |
| [CallableTrustResolver](../entities/CallableTrustResolver.md) | 154 | — | Small adapter for provider SDK integrations and deterministic tests. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `verify_detached_signature` | `(payload: bytes, envelope: DetachedSignatureEnvelope, resolver: PublicTrustResolver) -> PublicTrustAnchor` | — | Verify digest, trust metadata, key type, and detached signature. |
| `validate_sha256` | `(value: str, *, field_name: str = 'digest') -> str` | — | Validate a lowercase SHA-256 string at non-Pydantic boundaries. |
