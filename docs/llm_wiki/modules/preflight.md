# preflight Module

**Path:** `backend/app/autonomy/preflight.py`

## Description

Deterministic autonomous-start gate evaluation.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `StrictContractModel`, `canonical_json_bytes`, `sha256_hex` |
| `app.autonomy.contracts.charter` | `AutonomyState`, `CharterVerificationReceipt`, `ProgramDecision` |
| `app.autonomy.contracts.postgresql.loader` | `PostgreSQLContractBundle` |
| `app.autonomy.evidence` | `SignedAutonomousEvidence` |
| `app.autonomy.signing` | `DetachedSignatureEnvelope`, `RemoteSigner` |
| `datetime` | `UTC`, `datetime` |
| `pydantic` | `Field`, `model_validator` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/canonical.py"]
    n1["backend/app/autonomy/contracts/charter.py"]
    n2["backend/app/autonomy/contracts/postgresql/loader.py"]
    n3["backend/app/autonomy/evidence.py"]
    n4["backend/app/autonomy/preflight.py"]
    n5["backend/app/autonomy/signing.py"]
    n6["backend/app/cli/agent_preflight.py"]
    n7["backend/tests/autonomy/test_autonomy_foundation.py"]
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n3 --> n0
    n3 --> n5
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n5 --> n0
    n6 --> n0
    n6 --> n4
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/autonomy_canonical.md"
    click n1 "../modules/charter.md"
    click n2 "../modules/loader.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/preflight.md"
    click n5 "../modules/signing.md"
    click n6 "../modules/agent_preflight.md"
    click n7 "../modules/test_autonomy_foundation.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [agent_preflight](../modules/agent_preflight.md) |
| Inbound | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) |
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |
| Outbound | [charter](../modules/charter.md) |
| Outbound | [loader](../modules/loader.md) |
| Outbound | [evidence](../modules/evidence.md) |
| Outbound | [signing](../modules/signing.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [VerifiedPreflightArtifact](../entities/VerifiedPreflightArtifact.md) | 65 | `StrictContractModel` | — |
| [PreflightPredicateResult](../entities/PreflightPredicateResult.md) | 85 | `StrictContractModel` | — |
| [AgentPreflightReport](../entities/AgentPreflightReport.md) | 93 | `StrictContractModel` | — |
| [SignedAgentPreflightReport](../entities/SignedAgentPreflightReport.md) | 118 | `StrictContractModel` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `evaluate_agent_preflight` | `(*, release_fingerprint: str, bundle: PostgreSQLContractBundle, charter_receipt: CharterVerificationReceipt \| None, artifacts: tuple[VerifiedPreflightArtifact, ...] = (), advertised_features: set[str] \| frozenset[str] = frozenset(), evaluated_at: datetime \| None = None) -> AgentPreflightReport` | — | Evaluate every start row; missing facts are explicit blockers, never skips. |
| `sign_agent_preflight` | `(report: AgentPreflightReport, *, signer: RemoteSigner, key_ref: str, subject: str = 'pg-program-controller') -> SignedAgentPreflightReport` | — | — |
