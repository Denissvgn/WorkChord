# leases Module

**Path:** `backend/app/autonomy/leases.py`

## Description

Short-lived exact-target action leases parented to durable attempt starts.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `StrictContractModel`, `canonical_json_bytes`, `sha256_hex` |
| `app.autonomy.contracts.charter` | `AutonomyCharter`, `ExactResourceBinding` |
| `app.autonomy.evidence` | `AttemptEventType`, `AttemptLedgerBackend`, `AttemptLedgerRecord`, `ZERO_DIGEST`, `validate_attempt_ledger_snapshot` |
| `app.autonomy.signing` | `DetachedSignatureEnvelope`, `PublicTrustResolver`, `RemoteSigner`, `verify_detached_signature` |
| `collections.abc` | `Callable` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `pydantic` | `Field`, `model_validator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/canonical.py"]
    n1["backend/app/autonomy/contracts/charter.py"]
    n2["backend/app/autonomy/evidence.py"]
    n3["backend/app/autonomy/leases.py"]
    n4["backend/app/autonomy/providers.py"]
    n5["backend/app/autonomy/signing.py"]
    n6["backend/tests/autonomy/test_autonomy_foundation.py"]
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n2 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n4 --> n0
    n4 --> n3
    n5 --> n0
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/autonomy_canonical.md"
    click n1 "../modules/charter.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/leases.md"
    click n4 "../modules/providers.md"
    click n5 "../modules/signing.md"
    click n6 "../modules/test_autonomy_foundation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [providers](../modules/providers.md) |
| Inbound | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) |
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |
| Outbound | [charter](../modules/charter.md) |
| Outbound | [evidence](../modules/evidence.md) |
| Outbound | [signing](../modules/signing.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ActionLeaseRequest](../entities/ActionLeaseRequest.md) | 33 | `StrictContractModel` | — |
| [ActionLease](../entities/ActionLease.md) | 76 | `StrictContractModel` | — |
| [SignedActionLease](../entities/SignedActionLease.md) | 127 | `StrictContractModel` | — |
| [ActionLeasePolicy](../entities/ActionLeasePolicy.md) | 132 | — | Non-generative issuer that cannot invent authority or attempt ancestry. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `verify_action_lease` | `(signed: SignedActionLease, *, trust_resolver: PublicTrustResolver, ledger_backend: AttemptLedgerBackend, expected_action: str, expected_environment: Literal['ephemeral', 'rehearsal', 'production'], expected_destructive: bool, expected_resource_ref: str, expected_resource_generation: str, now: datetime) -> ActionLease` | — | Adapter-side verification before any provider mutation. |
