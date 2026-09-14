# test_autonomy_foundation Module

**Path:** `backend/tests/autonomy/test_autonomy_foundation.py`

## Description

Fail-closed contract, evidence, lease, and orchestration coverage.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.canonical` | `SecretMaterialError`, `canonical_json_bytes`, `ensure_secret_free`, `sha256_hex` |
| `app.autonomy.contracts.charter` | `AutonomyCharter`, `AutonomyState`, `BootstrapActionManifest`, `BootstrapActionSlot`, `CharterVerifier`, `ExactResourceBinding`, `ExecutionBudget`, `ExecutionWindow`, `ImmutableInputBinding`, `MigrationPolicy`, `RevocationObservation`, `SignedAutonomyCharter`, `SignedBootstrapActionManifest`, `TrustedKeyBinding`, `sign_charter_verification_receipt` |
| `app.autonomy.contracts.postgresql` | `ContractBundleError`, `load_postgresql_contract_bundle` |
| `app.autonomy.contracts.topology` | `AgentTeamMasterContract`, `CurrentTopologyMember`, `CurrentTopologySnapshot`, `ModelBindingContract`, `PM_SCOPES`, `ReconciliationClass`, `RolePackageContract`, `RuntimeContract`, `TopologyLifecycleState`, `TopologyMemberContract`, `VERIFIER_SCOPES`, `WORKER_SCOPES`, `reconcile_agent_team` |
| `app.autonomy.evidence` | `AttemptEventType`, `AttemptLedger`, `AttemptLedgerRecord`, `AttemptLedgerSnapshot`, `AutonomousEvidence`, `EvidenceResolutionError`, `EvidenceResolver`, `RedactionClass`, `SignedAutonomousEvidence`, `ZERO_DIGEST`, `store_signed_evidence` |
| `app.autonomy.handoff` | `AvailabilityState`, `ResolvedHandoffFact`, `RetentionState`, `build_manual_publication_handoff`, `evaluate_closeout`, `sign_handoff_verification`, `store_manual_publication_handoff` |
| `app.autonomy.leases` | `ActionLeasePolicy`, `ActionLeaseRequest`, `verify_action_lease` |
| `app.autonomy.orchestration` | `AutonomousDagContract`, `DagController`, `DagJournalSnapshot`, `DagNodeSpec`, `DagNodeState`, `VerificationRequirementContract`, `VerificationRequirementState`, `WorkPackageContract`, `aggregate_work_package` |
| `app.autonomy.preflight` | `evaluate_agent_preflight` |
| `app.autonomy.providers` | `CompleteMetricWindow`, `MetricSample`, `ProviderActionRequest`, `ProviderAuditObservation`, `ProviderMutationReceipt`, `ReplicaMembershipObservation`, `correlate_provider_action` |
| `app.autonomy.signing` | `DetachedSignatureEnvelope`, `PublicTrustAnchor` |
| `app.autonomy.status` | `evaluate_status_amendment` |
| `base64` | `base64` |
| `cryptography.hazmat.primitives` | `serialization` |
| `cryptography.hazmat.primitives.asymmetric` | `ed25519` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `pathlib` | `Path` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/autonomy/test_autonomy_foundation.py"]
    n1 --> n0
    click n1 "../modules/test_autonomy_foundation.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [FakeRemoteSigner](../entities/FakeRemoteSigner.md) | 117 | — | — |
| [FakeTrustResolver](../entities/FakeTrustResolver.md) | 159 | — | — |
| [FakeRevocationResolver](../entities/FakeRevocationResolver.md) | 169 | — | — |
| [MemoryAttemptBackend](../entities/MemoryAttemptBackend.md) | 181 | — | — |
| [MemoryWormStore](../entities/MemoryWormStore.md) | 206 | — | — |
| [MemoryDagJournal](../entities/MemoryDagJournal.md) | 226 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_resources` | `() -> tuple[ExactResourceBinding, ...]` | — | — |
| `_bootstrap_manifest` | `() -> BootstrapActionManifest` | — | — |
| `_charter` | `(bootstrap_digest: str) -> AutonomyCharter` | — | — |
| `_signed_document` | `(document, signer: FakeRemoteSigner, subject: str)` | — | — |
| `_binding` | `(key: str) -> ModelBindingContract` | — | — |
| `_member` | `(key: str, role: str, scopes: tuple[str, ...]) -> TopologyMemberContract` | — | — |
| `test_canonical_contracts_reject_secret_material_and_non_finite_values` | `() -> None` | `@pytest.mark.contract` | — |
| `test_charter_and_finite_bootstrap_manifest_verify_from_external_trust` | `() -> None` | `@pytest.mark.contract` | — |
| `test_topology_manifest_and_reconciliation_are_stable_and_non_destructive` | `() -> None` | `@pytest.mark.contract` | — |
| `_signed_evidence` | `(signer: FakeRemoteSigner) -> SignedAutonomousEvidence` | — | — |
| `_handoff_fact` | `(signer: FakeRemoteSigner, *, fact_kind: str, issuer: str, contract_manifest_digest: str) -> ResolvedHandoffFact` | — | — |
| `test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission` | `() -> None` | `@pytest.mark.contract` | — |
| `test_action_lease_binds_exact_attempt_target_generation_and_remote_key` | `() -> None` | `@pytest.mark.contract` | — |
| `test_collector_windows_reject_metric_gaps_counter_resets_and_missing_replicas` | `() -> None` | `@pytest.mark.contract` | — |
| `test_external_dag_and_multi_slot_package_are_fenced_and_append_only` | `() -> None` | `@pytest.mark.contract` | — |
| `test_packaged_contract_status_and_preflight_remain_truthfully_blocked` | `(tmp_path: Path) -> None` | `@pytest.mark.contract` | — |
| `test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship` | `() -> None` | `@pytest.mark.contract` | — |
