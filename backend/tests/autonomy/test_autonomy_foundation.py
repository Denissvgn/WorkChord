"""Fail-closed contract, evidence, lease, and orchestration coverage."""

from __future__ import annotations

import base64
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from pydantic import ValidationError

from app.autonomy.canonical import (
    SecretMaterialError,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.autonomy.contracts.charter import (
    AutonomyCharter,
    AutonomyState,
    BootstrapActionManifest,
    BootstrapActionSlot,
    CharterVerifier,
    ExactResourceBinding,
    ExecutionBudget,
    ExecutionWindow,
    ImmutableInputBinding,
    MigrationPolicy,
    RevocationObservation,
    SignedAutonomyCharter,
    SignedBootstrapActionManifest,
    TrustedKeyBinding,
    sign_charter_verification_receipt,
)
from app.autonomy.contracts.postgresql import (
    ContractBundleError,
    load_postgresql_contract_bundle,
)
from app.autonomy.contracts.topology import (
    AgentTeamMasterContract,
    CurrentTopologyMember,
    CurrentTopologySnapshot,
    ModelBindingContract,
    PM_SCOPES,
    ReconciliationClass,
    RolePackageContract,
    RuntimeContract,
    TopologyLifecycleState,
    TopologyMemberContract,
    VERIFIER_SCOPES,
    WORKER_SCOPES,
    reconcile_agent_team,
)
from app.autonomy.evidence import (
    AttemptEventType,
    AttemptLedger,
    AttemptLedgerRecord,
    AttemptLedgerSnapshot,
    AutonomousEvidence,
    EvidenceResolutionError,
    EvidenceResolver,
    RedactionClass,
    SignedAutonomousEvidence,
    ZERO_DIGEST,
    store_signed_evidence,
)
from app.autonomy.leases import (
    ActionLeasePolicy,
    ActionLeaseRequest,
    verify_action_lease,
)
from app.autonomy.handoff import (
    AvailabilityState,
    ResolvedHandoffFact,
    RetentionState,
    build_manual_publication_handoff,
    evaluate_closeout,
    sign_handoff_verification,
    store_manual_publication_handoff,
)
from app.autonomy.orchestration import (
    AutonomousDagContract,
    DagController,
    DagJournalSnapshot,
    DagNodeSpec,
    DagNodeState,
    VerificationRequirementContract,
    VerificationRequirementState,
    WorkPackageContract,
    aggregate_work_package,
)
from app.autonomy.preflight import evaluate_agent_preflight
from app.autonomy.providers import (
    CompleteMetricWindow,
    MetricSample,
    ProviderActionRequest,
    ProviderAuditObservation,
    ProviderMutationReceipt,
    ReplicaMembershipObservation,
    correlate_provider_action,
)
from app.autonomy.signing import (
    DetachedSignatureEnvelope,
    PublicTrustAnchor,
)
from app.autonomy.status import evaluate_status_amendment


NOW = datetime(2026, 7, 19, 12, 0, tzinfo=UTC)
DIGEST_A = "a" * 64
DIGEST_B = "b" * 64
DIGEST_C = "c" * 64


class FakeRemoteSigner:
    def __init__(self) -> None:
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.key_ref = "kms:test:autonomy-key"
        self.key_version = "1"
        self.issuer = "test-issuer"

    def sign_digest(
        self,
        *,
        payload_sha256: str,
        key_ref: str,
        subject: str,
    ) -> DetachedSignatureEnvelope:
        assert key_ref == self.key_ref
        signature = self.private_key.sign(bytes.fromhex(payload_sha256))
        return DetachedSignatureEnvelope(
            key_ref=key_ref,
            key_version=self.key_version,
            issuer=self.issuer,
            subject=subject,
            algorithm="ed25519",
            payload_sha256=payload_sha256,
            signature_base64=base64.b64encode(signature).decode("ascii"),
        )

    def trust_anchor(self, *subjects: str) -> PublicTrustAnchor:
        public_pem = self.private_key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")
        return PublicTrustAnchor(
            key_ref=self.key_ref,
            key_version=self.key_version,
            issuer=self.issuer,
            allowed_subjects=subjects,
            algorithm="ed25519",
            public_key_pem=public_pem,
            source_receipt_digest=DIGEST_C,
        )


class FakeTrustResolver:
    def __init__(self, anchor: PublicTrustAnchor) -> None:
        self.anchor = anchor

    def resolve(self, *, key_ref: str, key_version: str) -> PublicTrustAnchor:
        if (key_ref, key_version) != (self.anchor.key_ref, self.anchor.key_version):
            raise KeyError("unknown key")
        return self.anchor


class FakeRevocationResolver:
    def resolve(self, *, charter_id: str, source_ref: str) -> RevocationObservation:
        return RevocationObservation(
            charter_id=charter_id,
            state="active",
            observed_at=NOW,
            source_ref=source_ref,
            source_generation="revocations-9",
            source_receipt_digest=DIGEST_B,
        )


class MemoryAttemptBackend:
    def __init__(self) -> None:
        self.records: list[AttemptLedgerRecord] = []

    def read(self) -> AttemptLedgerSnapshot:
        return AttemptLedgerSnapshot(
            revision=len(self.records),
            head_digest=self.records[-1].digest() if self.records else ZERO_DIGEST,
            records=tuple(self.records),
        )

    def compare_and_append(
        self,
        *,
        expected_revision: int,
        expected_head_digest: str,
        record: AttemptLedgerRecord,
    ) -> bool:
        snapshot = self.read()
        if snapshot.revision != expected_revision or snapshot.head_digest != expected_head_digest:
            return False
        self.records.append(record)
        return True


class MemoryWormStore:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def put_if_absent(
        self, *, object_key: str, payload: bytes, redaction_class: RedactionClass
    ) -> None:
        del redaction_class
        existing = self.objects.get(object_key)
        if existing is not None and existing != payload:
            raise ValueError("immutable object already exists")
        self.objects.setdefault(object_key, payload)

    def get(self, *, object_key: str) -> bytes:
        return self.objects[object_key]

    def ordered_keys(self, *, prefix: str) -> tuple[str, ...]:
        return tuple(sorted(key for key in self.objects if key.startswith(prefix)))


class MemoryDagJournal:
    def __init__(self) -> None:
        self.entries = []

    def read(self, *, run_id: str) -> DagJournalSnapshot:
        del run_id
        return DagJournalSnapshot(
            revision=len(self.entries),
            head_digest=self.entries[-1].digest() if self.entries else ZERO_DIGEST,
            entries=tuple(self.entries),
        )

    def compare_and_append(
        self,
        *,
        run_id: str,
        expected_revision: int,
        expected_head_digest: str,
        entry,
    ) -> bool:
        del run_id
        snapshot = self.read(run_id="unused")
        if snapshot.revision != expected_revision or snapshot.head_digest != expected_head_digest:
            return False
        self.entries.append(entry)
        return True


def _resources() -> tuple[ExactResourceBinding, ...]:
    systems = (
        "source-database",
        "target-database",
        "git",
        "ci",
        "registry",
        "deployment",
        "scheduler",
        "gateway",
        "dns",
        "identity",
        "kms",
        "worm",
        "control-journal",
        "observability",
        "backup",
        "clock",
        "sanitizer",
    )
    return tuple(
        ExactResourceBinding(
            logical_key=f"resource-{index}",
            system=system,
            resource_ref=f"urn:test:resource:{index}",
            generation="generation-1",
            account_ref="urn:test:account:1",
            region="test-region-1",
            allowed_operations=("mutate", "read"),
        )
        for index, system in enumerate(systems, start=1)
    )


def _bootstrap_manifest() -> BootstrapActionManifest:
    return BootstrapActionManifest(
        manifest_id="bootstrap-manifest-1",
        charter_id="charter-1",
        journal_genesis_digest=DIGEST_A,
        journal_expected_head_digest=DIGEST_B,
        issued_at=NOW - timedelta(minutes=5),
        expires_at=NOW + timedelta(hours=1),
        slots=(
            BootstrapActionSlot(
                ordinal=1,
                slot_id="slot-1",
                subject="pg-bootstrap-builder",
                action="repo-write",
                target_ref="urn:test:repo:bootstrap-branch",
                target_generation="commit-1",
                precondition_digest=DIGEST_A,
                input_schema="bootstrap-input-v1",
                output_schema="bootstrap-output-v1",
                journal_parent_digest=DIGEST_A,
                timeout_seconds=300,
                maximum_calls=1,
                maximum_spend_minor_units=100,
                nonce="nonce-1",
                reset_effect="repeat from clean checkout",
            ),
        ),
    )


def _charter(bootstrap_digest: str) -> AutonomyCharter:
    return AutonomyCharter(
        charter_id="charter-1",
        issuer="test-issuer",
        subject="workchord-postgresql-autonomous-migration",
        repository="urn:test:git:workchord",
        candidate_branch="db-migration",
        push_policy="fast-forward-only",
        project_ref="urn:test:workchord:project:1",
        iteration_ref="urn:test:workchord:iteration:1",
        task_graph_digest=DIGEST_A,
        topology_manifest_digest=DIGEST_B,
        bootstrap_action_manifest_digest=bootstrap_digest,
        contract_manifest_digest=DIGEST_C,
        valid_from=NOW - timedelta(minutes=10),
        expires_at=NOW + timedelta(hours=2),
        revocation_source_ref="urn:test:revocations:1",
        revocation_max_age_seconds=300,
        production_mutation_allowed=False,
        resources=_resources(),
        immutable_inputs=(
            ImmutableInputBinding(
                logical_key="autonomous-plan",
                object_uri="urn:test:worm:autonomous-plan",
                sha256=DIGEST_A,
                byte_length=100,
                media_type="text/markdown",
                schema_version="zero-human-agent-v1",
            ),
        ),
        trusted_keys=(
            TrustedKeyBinding(
                logical_key="action-policy-key",
                key_ref="kms:test:autonomy-key",
                issuer="test-issuer",
                allowed_subject="pg-action-policy",
                intended_use="action-leases",
            ),
        ),
        execution_windows=(
            ExecutionWindow(
                logical_key="bootstrap-window",
                starts_at=NOW - timedelta(minutes=5),
                ends_at=NOW + timedelta(hours=1),
                permitted_stages=("bootstrap", "evidence-stage"),
            ),
        ),
        budget=ExecutionBudget(
            maximum_spend_minor_units=10_000,
            currency="USD",
            maximum_elapsed_seconds=7200,
            maximum_api_calls=10_000,
            maximum_mutations=1000,
            maximum_attempts_per_leaf=3,
        ),
        migration_policy=MigrationPolicy(
            downtime_seconds=600,
            rpo_seconds=60,
            rto_seconds=600,
            snapshot_max_age_hours=24,
            retention_days=30,
            availability_target_percent=99.9,
            allowed_remediation_classes=("bounded-retry",),
        ),
    )


def _signed_document(document, signer: FakeRemoteSigner, subject: str):
    return signer.sign_digest(
        payload_sha256=sha256_hex(canonical_json_bytes(document)),
        key_ref=signer.key_ref,
        subject=subject,
    )


def _binding(key: str) -> ModelBindingContract:
    return ModelBindingContract(
        binding_key=f"{key}-binding",
        catalog_key="reasoning-model",
        minimum_reasoning_tier=3,
        minimum_context_tier="large",
        tool_tags=("code-edit",),
        data_policy_tags=("workspace-source",),
        is_default=True,
    )


def _member(key: str, role: str, scopes: tuple[str, ...]) -> TopologyMemberContract:
    return TopologyMemberContract(
        logical_key=key,
        actor_name=key,
        role=role,
        primary_controller=role == "pm",
        scope_preset=f"postgresql-{role}-v1",
        scopes=scopes,
        profile_key=f"{key}-profile",
        profile_revision=1,
        skill_requirements={"postgresql": 3},
        model_bindings=(_binding(key),),
        role_package=RolePackageContract(
            package_key=f"{key}-package",
            version="1.0.0",
            checksum_sha256=DIGEST_A,
        ),
        runtime=RuntimeContract(
            runtime_ref=f"urn:test:runtime:{key}",
            image_digest=f"sha256:{DIGEST_B}",
            sandbox_profile="restricted-runtime",
            attestation_policy_digest=DIGEST_C,
        ),
        independence_group=f"{key}-group",
        workload_identity_subject=f"spiffe://test/{key}",
        kms_key_ref=f"kms:test:{key}",
        external_lease_classes=("read",),
    )


@pytest.mark.contract
def test_canonical_contracts_reject_secret_material_and_non_finite_values() -> None:
    assert canonical_json_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}'
    with pytest.raises(SecretMaterialError, match="api_key"):
        ensure_secret_free({"api_key": "not-even-a-real-key"})
    with pytest.raises(SecretMaterialError, match="Credential-shaped"):
        ensure_secret_free({"value": "postgresql://owner:password@db.example/test"})
    with pytest.raises(ValueError, match="Non-finite"):
        ensure_secret_free({"value": float("nan")})


@pytest.mark.contract
def test_charter_and_finite_bootstrap_manifest_verify_from_external_trust() -> None:
    signer = FakeRemoteSigner()
    manifest = _bootstrap_manifest()
    charter = _charter(sha256_hex(canonical_json_bytes(manifest)))
    trust = FakeTrustResolver(
        signer.trust_anchor(
            charter.subject,
            "pg-bootstrap-controller",
            "pg-action-policy",
            "pg-source-collector",
        )
    )
    receipt = CharterVerifier(
        trust_resolver=trust,
        revocation_resolver=FakeRevocationResolver(),
        clock=lambda: NOW,
    ).verify(
        SignedAutonomyCharter(
            document=charter,
            signature=_signed_document(charter, signer, charter.subject),
        ),
        SignedBootstrapActionManifest(
            document=manifest,
            signature=_signed_document(manifest, signer, "pg-bootstrap-controller"),
        ),
    )
    assert receipt.charter_digest == sha256_hex(canonical_json_bytes(charter))
    assert receipt.autonomy_state == AutonomyState.NOT_READY
    assert receipt.blocker_codes == ("autonomy_implementation_not_qualified",)
    signed_receipt = sign_charter_verification_receipt(
        receipt,
        signer=signer,
        key_ref=signer.key_ref,
    )
    assert signed_receipt.signature.subject == "pg-charter-verifier"

    invalid = manifest.model_copy(update={"slots": (manifest.slots[0].model_copy(update={"target_ref": "urn:test:prefix:"}),)})
    with pytest.raises(ValidationError, match="wildcard or prefix"):
        BootstrapActionManifest.model_validate(invalid.model_dump(mode="json"))


@pytest.mark.contract
def test_topology_manifest_and_reconciliation_are_stable_and_non_destructive() -> None:
    pm = _member("test-controller", "pm", PM_SCOPES)
    worker = _member("test-worker", "worker", WORKER_SCOPES)
    verifier = _member("test-verifier", "verifier", VERIFIER_SCOPES)
    desired = AgentTeamMasterContract(
        topology_key="test-topology",
        revision=2,
        charter_digest=DIGEST_A,
        model_catalog_revision=4,
        credential_sink_ref="urn:test:secure-sink:1",
        members=(pm, worker, verifier),
    )
    current = CurrentTopologySnapshot(
        topology_key="test-topology",
        revision=1,
        members=(
            CurrentTopologyMember(
                logical_key=pm.logical_key,
                actor_name=pm.actor_name,
                topology_key="test-topology",
                object_revision=1,
                lifecycle_state=TopologyLifecycleState.RUNTIME_READY,
                desired_contract=pm,
            ),
            CurrentTopologyMember(
                logical_key="old-worker",
                actor_name="old-worker",
                topology_key="test-topology",
                object_revision=3,
                lifecycle_state=TopologyLifecycleState.RUNTIME_READY,
                desired_contract=_member("old-worker", "worker", WORKER_SCOPES),
            ),
        ),
    )
    first = reconcile_agent_team(desired, current)
    second = reconcile_agent_team(desired, current)
    assert first == second
    assert first.plan_digest == second.plan_digest
    by_key = {item.logical_key: item for item in first.actions}
    assert by_key["test-controller"].reconciliation_class == ReconciliationClass.NO_CHANGE
    assert by_key["test-worker"].reconciliation_class == ReconciliationClass.CREATE
    assert by_key["old-worker"].reconciliation_class == ReconciliationClass.PROPOSE_DISABLE
    assert by_key["old-worker"].requires_explicit_confirmation is True

    with pytest.raises(ValidationError, match="exactly one default"):
        TopologyMemberContract.model_validate(
            worker.model_copy(
                update={"model_bindings": (worker.model_bindings[0].model_copy(update={"is_default": False}),)}
            ).model_dump(mode="json")
        )


def _signed_evidence(signer: FakeRemoteSigner) -> SignedAutonomousEvidence:
    evidence = AutonomousEvidence(
        run_id="run-1",
        task_id="AUT-EVD-001",
        stage_id="evidence-stage",
        action_id="source-proof",
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=DIGEST_C,
        issuer_workload_identity="pg-source-collector",
        issuer_role="source-collector",
        source_system="provider-api",
        source_resource_ref="urn:test:provider:resource:1",
        source_resource_generation="generation-1",
        source_receipt_ref="urn:test:audit:event:1",
        request_digest=DIGEST_A,
        idempotency_digest=DIGEST_B,
        observed_started_at=NOW - timedelta(seconds=1),
        observed_ended_at=NOW,
        clock_source_ref="urn:test:clock:1",
        query_digest=DIGEST_C,
        exit_code=0,
        source_outcome="succeeded",
        raw_artifact_uri="urn:test:worm:raw:1",
        raw_artifact_sha256=DIGEST_A,
        parent_hashes=(),
        ledger_sequence=1,
        previous_hash=ZERO_DIGEST,
        redaction_class=RedactionClass.INTERNAL,
    )
    return SignedAutonomousEvidence(
        evidence=evidence,
        signature=_signed_document(evidence, signer, "pg-source-collector"),
    )


def _handoff_fact(
    signer: FakeRemoteSigner,
    *,
    fact_kind: str,
    issuer: str,
    contract_manifest_digest: str,
) -> ResolvedHandoffFact:
    evidence = AutonomousEvidence(
        run_id="production-run-1",
        task_id="DBC-HANDOFF-001",
        stage_id="handoff-stage",
        action_id=fact_kind,
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=contract_manifest_digest,
        issuer_workload_identity=issuer,
        issuer_role="source-collector",
        source_system="production-api",
        source_resource_ref="urn:test:production:resource:1",
        source_resource_generation="generation-1",
        source_receipt_ref=f"urn:test:production:event:{fact_kind}",
        request_digest=DIGEST_A,
        idempotency_digest=DIGEST_B,
        observed_started_at=NOW - timedelta(seconds=1),
        observed_ended_at=NOW,
        clock_source_ref="urn:test:clock:1",
        query_digest=DIGEST_C,
        exit_code=0,
        source_outcome="succeeded",
        raw_artifact_uri=f"urn:test:worm:raw:{fact_kind}",
        raw_artifact_sha256=DIGEST_A,
        parent_hashes=(),
        ledger_sequence=1,
        previous_hash=ZERO_DIGEST,
        redaction_class=RedactionClass.INTERNAL,
    )
    signed = SignedAutonomousEvidence(
        evidence=evidence,
        signature=_signed_document(evidence, signer, issuer),
    )
    digest = sha256_hex(canonical_json_bytes(signed))
    return ResolvedHandoffFact(
        fact_kind=fact_kind,
        object_digest=digest,
        object_uri=f"urn:test:worm:evidence:{digest}",
        evidence=signed,
    )


@pytest.mark.contract
def test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission() -> None:
    backend = MemoryAttemptBackend()
    ledger = AttemptLedger(backend=backend, clock=lambda: NOW)
    allocation = ledger.allocate(
        run_id="run-1",
        task_id="AUT-EVD-001",
        stage_id="evidence-stage",
        action_id="source-proof",
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=DIGEST_C,
    )
    start = ledger.start(attempt_id=allocation.attempt_id)
    checkpoint = ledger.append(
        attempt_id=allocation.attempt_id,
        event_type=AttemptEventType.CHECKPOINT,
        evidence_digest=DIGEST_A,
    )
    ledger.append(
        attempt_id=allocation.attempt_id,
        event_type=AttemptEventType.EVALUATED,
        evidence_digest=DIGEST_B,
    )
    ledger.append(attempt_id=allocation.attempt_id, event_type=AttemptEventType.FINAL)
    assert [item.event_type for item in backend.records] == [
        AttemptEventType.ALLOCATED,
        AttemptEventType.STARTED,
        AttemptEventType.CHECKPOINT,
        AttemptEventType.EVALUATED,
        AttemptEventType.FINAL,
    ]
    assert start.previous_hash == allocation.digest()
    assert checkpoint.previous_hash == start.digest()
    with pytest.raises(ValueError, match="immutable"):
        ledger.append(attempt_id=allocation.attempt_id, event_type=AttemptEventType.CHECKPOINT)

    stopped = ledger.allocate(
        run_id="run-1",
        task_id="AUT-EVD-001",
        stage_id="evidence-stage",
        action_id="unstarted-action",
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=DIGEST_C,
    )
    ledger.append(
        attempt_id=stopped.attempt_id,
        event_type=AttemptEventType.STOPPED,
        normalized_reason_code="lease-unavailable",
    )
    ledger.append(
        attempt_id=stopped.attempt_id,
        event_type=AttemptEventType.EVALUATED,
        evidence_digest=DIGEST_C,
    )
    ledger.append(attempt_id=stopped.attempt_id, event_type=AttemptEventType.FINAL)

    signer = FakeRemoteSigner()
    store = MemoryWormStore()
    signed = _signed_evidence(signer)
    digest = store_signed_evidence(store, signed)
    resolved = EvidenceResolver(
        store=store,
        trust_resolver=FakeTrustResolver(signer.trust_anchor("pg-source-collector")),
        clock=lambda: NOW,
    ).resolve(
        digest,
        expected_release_fingerprint=DIGEST_A,
        expected_charter_digest=DIGEST_B,
        expected_contract_manifest_digest=DIGEST_C,
        expected_issuer_roles={"source-collector"},
        expected_source_system="provider-api",
        maximum_age=timedelta(minutes=1),
    )
    assert resolved == signed
    child_evidence = AutonomousEvidence.model_validate(
        {
            **signed.evidence.model_dump(mode="python"),
            "ledger_sequence": 2,
            "previous_hash": digest,
            "raw_artifact_uri": "urn:test:worm:raw:child",
        }
    )
    child = SignedAutonomousEvidence(
        evidence=child_evidence,
        signature=_signed_document(
            child_evidence, signer, "pg-source-collector"
        ),
    )
    child_digest = store_signed_evidence(store, child)
    assert EvidenceResolver(
        store=store,
        trust_resolver=FakeTrustResolver(
            signer.trust_anchor("pg-source-collector")
        ),
        clock=lambda: NOW,
    ).resolve(
        child_digest,
        expected_release_fingerprint=DIGEST_A,
        expected_charter_digest=DIGEST_B,
        expected_contract_manifest_digest=DIGEST_C,
        expected_issuer_roles={"source-collector"},
        expected_source_system="provider-api",
        maximum_age=timedelta(minutes=1),
    ) == child
    store.objects[digest] = store.objects[digest] + b" "
    with pytest.raises(EvidenceResolutionError, match="digest mismatch"):
        EvidenceResolver(
            store=store,
            trust_resolver=FakeTrustResolver(signer.trust_anchor("pg-source-collector")),
            clock=lambda: NOW,
        ).resolve(
            digest,
            expected_release_fingerprint=DIGEST_A,
            expected_charter_digest=DIGEST_B,
            expected_contract_manifest_digest=DIGEST_C,
            expected_issuer_roles={"source-collector"},
            expected_source_system="provider-api",
            maximum_age=timedelta(minutes=1),
        )


@pytest.mark.contract
def test_action_lease_binds_exact_attempt_target_generation_and_remote_key() -> None:
    signer = FakeRemoteSigner()
    manifest = _bootstrap_manifest()
    charter = _charter(sha256_hex(canonical_json_bytes(manifest)))
    backend = MemoryAttemptBackend()
    ledger = AttemptLedger(backend=backend, clock=lambda: NOW)
    allocation = ledger.allocate(
        run_id="run-1",
        task_id="AUT-EVD-001",
        stage_id="evidence-stage",
        action_id="mutate",
        release_fingerprint=DIGEST_A,
        charter_digest=sha256_hex(canonical_json_bytes(charter)),
        contract_manifest_digest=DIGEST_C,
    )
    start = ledger.start(attempt_id=allocation.attempt_id)
    snapshot = backend.read()
    target = charter.resources[0]
    request = ActionLeaseRequest(
        run_id="run-1",
        task_id="AUT-EVD-001",
        stage_id="evidence-stage",
        action="mutate",
        environment="rehearsal",
        resource_logical_key=target.logical_key,
        resource_ref=target.resource_ref,
        resource_generation=target.generation,
        topology_revision=1,
        attempt_id=allocation.attempt_id,
        attempt_start_digest=start.digest(),
        attempt_start_sequence=start.sequence,
        ledger_head_at_request=snapshot.head_digest,
        requested_ttl_seconds=60,
        maximum_calls=1,
        budget_minor_units=5,
        nonce="lease-nonce-1",
        lease_mode="bootstrap-revalidation",
    )
    policy = ActionLeasePolicy(
        charter=charter,
        charter_digest=sha256_hex(canonical_json_bytes(charter)),
        contract_manifest_digest=DIGEST_C,
        release_fingerprint=DIGEST_A,
        ledger_backend=backend,
        signer=signer,
        signing_key_ref=signer.key_ref,
        clock=lambda: NOW,
    )
    signed_lease = policy.issue(request)
    production_request = ActionLeaseRequest(
        **{
            **request.model_dump(mode="python"),
            "environment": "production",
            "lease_mode": "autonomous",
            "autonomy_qualified_report_digest": DIGEST_A,
        }
    )
    with pytest.raises(ValueError, match="does not permit production"):
        policy.issue(production_request)
    verified = verify_action_lease(
        signed_lease,
        trust_resolver=FakeTrustResolver(signer.trust_anchor("pg-action-policy")),
        ledger_backend=backend,
        expected_action="mutate",
        expected_environment="rehearsal",
        expected_destructive=False,
        expected_resource_ref=target.resource_ref,
        expected_resource_generation=target.generation,
        now=NOW + timedelta(seconds=1),
    )
    assert verified.attempt_start_digest == start.digest()
    provider_request = ProviderActionRequest(
        domain="platform",
        operation="mutate",
        resource_ref=target.resource_ref,
        resource_generation=target.generation,
        environment="rehearsal",
        lease=signed_lease,
    )
    mutation = ProviderMutationReceipt(
        lease_digest=signed_lease.lease.lease_id,
        domain="platform",
        operation="mutate",
        resource_ref=target.resource_ref,
        resource_generation_before=target.generation,
        resource_generation_after="generation-2",
        provider_request_id="provider-request-1",
        response_received_at=NOW,
        raw_response_uri="urn:test:worm:provider-response:1",
        raw_response_sha256=DIGEST_A,
        tls_peer_identity_digest=DIGEST_B,
    )
    audit = ProviderAuditObservation(
        provider_request_id="provider-request-1",
        provider_event_id="provider-event-1",
        operation="mutate",
        resource_ref=target.resource_ref,
        resource_generation_before=target.generation,
        resource_generation_after="generation-2",
        observed_at=NOW + timedelta(seconds=1),
        source_query_digest=DIGEST_C,
        raw_audit_uri="urn:test:worm:provider-audit:1",
        raw_audit_sha256=DIGEST_A,
        source_generation="audit-generation-1",
    )
    correlated = correlate_provider_action(
        request=provider_request,
        mutation=mutation,
        audit=audit,
    )
    assert correlated.provider_event_id == "provider-event-1"
    with pytest.raises(ValueError, match="output generation"):
        correlate_provider_action(
            request=provider_request,
            mutation=mutation,
            audit=audit.model_copy(update={"resource_generation_after": "wrong"}),
        )
    with pytest.raises(ValueError, match="generation mismatch"):
        verify_action_lease(
            signed_lease,
            trust_resolver=FakeTrustResolver(signer.trust_anchor("pg-action-policy")),
            ledger_backend=backend,
            expected_action="mutate",
            expected_environment="rehearsal",
            expected_destructive=False,
            expected_resource_ref=target.resource_ref,
            expected_resource_generation="stale-generation",
            now=NOW + timedelta(seconds=1),
        )
    ledger.append(
        attempt_id=allocation.attempt_id,
        event_type=AttemptEventType.STOPPED,
        normalized_reason_code="provider-action-complete",
    )
    with pytest.raises(ValueError, match="already closed"):
        verify_action_lease(
            signed_lease,
            trust_resolver=FakeTrustResolver(
                signer.trust_anchor("pg-action-policy")
            ),
            ledger_backend=backend,
            expected_action="mutate",
            expected_environment="rehearsal",
            expected_destructive=False,
            expected_resource_ref=target.resource_ref,
            expected_resource_generation=target.generation,
            now=NOW + timedelta(seconds=1),
        )


@pytest.mark.contract
def test_collector_windows_reject_metric_gaps_counter_resets_and_missing_replicas() -> None:
    samples = (
        MetricSample(sampled_at=NOW, value=1, counter_generation="counter-1"),
        MetricSample(
            sampled_at=NOW + timedelta(seconds=30),
            value=2,
            counter_generation="counter-1",
        ),
        MetricSample(
            sampled_at=NOW + timedelta(seconds=60),
            value=3,
            counter_generation="counter-1",
        ),
    )
    window = CompleteMetricWindow(
        metric_key="gateway-requests",
        starts_at=NOW,
        ends_at=NOW + timedelta(seconds=60),
        expected_interval_seconds=30,
        maximum_gap_seconds=35,
        samples=samples,
    )
    assert len(window.samples) == 3
    with pytest.raises(ValidationError, match="counter reset"):
        CompleteMetricWindow(
            metric_key="gateway-requests",
            starts_at=NOW,
            ends_at=NOW + timedelta(seconds=60),
            expected_interval_seconds=30,
            maximum_gap_seconds=35,
            samples=(
                samples[0],
                samples[1].model_copy(update={"counter_generation": "counter-2"}),
                samples[2],
            ),
        )
    with pytest.raises(ValidationError, match="membership mismatch"):
        ReplicaMembershipObservation(
            expected_members=("web-1", "web-2"),
            observed_members=("web-1",),
            scheduler_membership_digest=DIGEST_A,
            connection_ownership_digest=DIGEST_B,
        )


@pytest.mark.contract
def test_external_dag_and_multi_slot_package_are_fenced_and_append_only() -> None:
    contract = AutonomousDagContract(
        run_id="run-1",
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=DIGEST_C,
        nodes=(
            DagNodeSpec(
                node_id="node-a",
                node_version=1,
                dependencies=(),
                reset_targets=("node-b",),
                timeout_seconds=60,
                maximum_attempts=3,
                retry_classes=("transient",),
                maximum_cost_minor_units=10,
                evaluator_version="eval-1",
                source_contract_digest=DIGEST_C,
            ),
            DagNodeSpec(
                node_id="node-b",
                node_version=1,
                dependencies=("node-a",),
                timeout_seconds=60,
                maximum_attempts=3,
                retry_classes=(),
                maximum_cost_minor_units=10,
                evaluator_version="eval-1",
                source_contract_digest=DIGEST_C,
            ),
        ),
    )
    journal = MemoryDagJournal()
    controller = DagController(
        contract=contract,
        journal=journal,
        controller_subject="pg-program-controller",
        clock=lambda: NOW,
    )
    controller.initialize()
    with pytest.raises(ValueError, match="dependencies"):
        controller.transition(node_id="node-b", to_state=DagNodeState.READY, transition="ready")
    controller.transition(node_id="node-a", to_state=DagNodeState.READY, transition="ready")
    with pytest.raises(ValueError, match="lease and attempt"):
        controller.transition(node_id="node-a", to_state=DagNodeState.LEASED, transition="lease")
    controller.transition(
        node_id="node-a",
        to_state=DagNodeState.LEASED,
        transition="lease",
        lease_digest=DIGEST_A,
        attempt_start_digest=DIGEST_B,
    )
    controller.transition(node_id="node-a", to_state=DagNodeState.RUNNING, transition="begin")
    controller.transition(
        node_id="node-a",
        to_state=DagNodeState.EVIDENCE_PENDING,
        transition="submit",
        evidence_digest=DIGEST_C,
    )
    controller.transition(node_id="node-a", to_state=DagNodeState.EVALUATING, transition="evaluate")
    controller.transition(node_id="node-a", to_state=DagNodeState.PASSED, transition="pass")
    controller.transition(node_id="node-b", to_state=DagNodeState.READY, transition="ready")
    reset = controller.transition(
        node_id="node-a",
        to_state=DagNodeState.RESET_REQUIRED,
        transition="material-change",
        reason_code="contract-drift",
    )
    dependents = controller.reset_dependents(
        failed_node_id="node-a", reason_code="upstream-reset"
    )
    assert reset.to_state == DagNodeState.RESET_REQUIRED
    assert [item.node_id for item in dependents] == ["node-b"]

    requirements = (
        VerificationRequirementContract(
            slot_id="slot-a",
            verifier_logical_key="verifier-a",
            criterion_schema="criteria-v1",
            artifact_set_digest=DIGEST_A,
            evaluator_version="eval-1",
            executor_independence_group="executor-group",
            required_verifier_independence_group="verifier-a-group",
            maximum_lease_seconds=60,
        ),
        VerificationRequirementContract(
            slot_id="slot-b",
            verifier_logical_key="verifier-b",
            criterion_schema="criteria-v1",
            artifact_set_digest=DIGEST_A,
            evaluator_version="eval-1",
            executor_independence_group="executor-group",
            required_verifier_independence_group="verifier-b-group",
            maximum_lease_seconds=60,
        ),
    )
    package = WorkPackageContract(
        package_id="package-1",
        package_version=1,
        execution_task_id="task-1",
        artifact_set_digest=DIGEST_A,
        requirements=requirements,
    )
    assert aggregate_work_package(
        package,
        {
            "slot-a": VerificationRequirementState.PASSED,
            "slot-b": VerificationRequirementState.RUNNING,
        },
    ) == "evaluating"
    assert aggregate_work_package(
        package,
        {
            "slot-a": VerificationRequirementState.PASSED,
            "slot-b": VerificationRequirementState.REJECTED,
        },
    ) == "rework_required"


@pytest.mark.contract
def test_packaged_contract_status_and_preflight_remain_truthfully_blocked(tmp_path: Path) -> None:
    bundle = load_postgresql_contract_bundle()
    assert bundle.archive_verified is False
    assert bundle.blocker_codes == ("immutable-contract-archive-unavailable",)
    assert len(bundle.manifest.trace.dbm_tasks) == 32
    assert set(bundle.manifest.trace.gates) == {f"G{index}" for index in range(1, 16)}
    ledger = evaluate_status_amendment(
        bundle=bundle,
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        source_status_snapshot_digest=DIGEST_A,
        generated_at=NOW,
    )
    assert ledger.overall_state == "acceptance_pending"
    perf = next(item for item in ledger.tasks if item.task_id == "DBM-PERF-001")
    assert perf.acceptance_state == "acceptance_pending"
    assert "reference-latency-memory-proof" in perf.missing_evidence_kinds
    docs = next(item for item in ledger.tasks if item.task_id == "DBM-DOC-002")
    assert docs.terminal_boundary == "manual_external"
    assert all(item.gate_state == "gate_pending" for item in ledger.gates)

    preflight = evaluate_agent_preflight(
        release_fingerprint=DIGEST_A,
        bundle=bundle,
        charter_receipt=None,
        evaluated_at=NOW,
    )
    assert preflight.autonomy_state == AutonomyState.BLOCKED_EXTERNAL
    assert preflight.program_decision.value == "NO-SHIP"
    assert all(item.state != "passed" for item in preflight.predicates)

    class MissingArchive:
        def get_exact(self, *, logical_key: str, expected_sha256: str) -> bytes:
            del logical_key, expected_sha256
            raise KeyError("missing")

    with pytest.raises(ContractBundleError, match="archive unavailable"):
        load_postgresql_contract_bundle(archive=MissingArchive(), require_archive=True)


@pytest.mark.contract
def test_manual_handoff_is_deterministic_unpublished_and_closeout_stays_no_ship() -> None:
    signer = FakeRemoteSigner()
    bundle = load_postgresql_contract_bundle()
    facts = tuple(
        _handoff_fact(
            signer,
            fact_kind=kind,
            issuer=(
                "pg-production-recorder"
                if kind == "production-cutover-record"
                else "pg-source-collector"
            ),
            contract_manifest_digest=bundle.manifest_digest,
        )
        for kind in (
            "production-cutover-record",
            "release-freeze-proof",
            "postcutover-runtime-proof",
            "handoff-input-integrity-proof",
        )
    )
    handoff = build_manual_publication_handoff(
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=bundle.manifest_digest,
        facts=facts,
        built_at=NOW,
        valid_until=NOW + timedelta(hours=1),
        availability_state=AvailabilityState.PENDING,
        retention_state=RetentionState.RETAINED_NOT_DUE,
        availability_observation_ends_at=NOW + timedelta(days=30),
        retention_due_at=NOW + timedelta(days=30),
    )
    repeated = build_manual_publication_handoff(
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        contract_manifest_digest=bundle.manifest_digest,
        facts=facts,
        built_at=NOW,
        valid_until=NOW + timedelta(hours=1),
        availability_state=AvailabilityState.PENDING,
        retention_state=RetentionState.RETAINED_NOT_DUE,
        availability_observation_ends_at=NOW + timedelta(days=30),
        retention_due_at=NOW + timedelta(days=30),
    )
    assert repeated == handoff
    assert handoff.publication_state == "NOT-PUBLISHED"
    assert handoff.availability_claim_allowed is False
    assert "no 99.9% availability claim" in handoff.candidate_notes
    store = MemoryWormStore()
    assert store_manual_publication_handoff(store, handoff) == sha256_hex(
        canonical_json_bytes(handoff)
    )
    verification = sign_handoff_verification(
        handoff,
        signer=signer,
        key_ref=signer.key_ref,
        verified_at=NOW,
    )
    status_ledger = evaluate_status_amendment(
        bundle=bundle,
        release_fingerprint=DIGEST_A,
        charter_digest=DIGEST_B,
        source_status_snapshot_digest=DIGEST_A,
        generated_at=NOW,
    )
    closeout = evaluate_closeout(
        handoff=handoff,
        handoff_verification=verification,
        status_ledger=status_ledger,
        trust_resolver=FakeTrustResolver(
            signer.trust_anchor("pg-release-verifier")
        ),
        evaluated_at=NOW + timedelta(minutes=1),
    )
    assert closeout.decision.value == "NO-SHIP"
    assert closeout.blocker_codes
    assert closeout.manual_external_items == ("DBM-DOC-002", "G15")

    with pytest.raises(ValueError, match="availability verifier proof"):
        build_manual_publication_handoff(
            release_fingerprint=DIGEST_A,
            charter_digest=DIGEST_B,
            contract_manifest_digest=bundle.manifest_digest,
            facts=facts,
            built_at=NOW,
            valid_until=NOW + timedelta(hours=1),
            availability_state=AvailabilityState.MET,
            retention_state=RetentionState.RETAINED_NOT_DUE,
            availability_observation_ends_at=NOW,
            retention_due_at=NOW + timedelta(days=30),
        )
