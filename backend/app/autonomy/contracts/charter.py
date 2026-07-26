"""Standing delegation and finite bootstrap-action contracts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import StrEnum
from collections.abc import Callable
from typing import Literal, Protocol, runtime_checkable

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.autonomy.signing import (
    DetachedSignatureEnvelope,
    PublicTrustResolver,
    RemoteSigner,
    SignatureVerificationError,
    verify_detached_signature,
)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-z0-9][a-z0-9._:-]{0,254}$"
OPAQUE_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/@+-]{2,1023}$"


class ProgramDecision(StrEnum):
    NO_SHIP = "NO-SHIP"
    READY_FOR_MANUAL_PUBLICATION = "READY-FOR-MANUAL-PUBLICATION"


class AutonomyState(StrEnum):
    NOT_READY = "AUTONOMY-NOT-READY"
    BLOCKED_EXTERNAL = "BLOCKED_EXTERNAL"
    QUALIFIED = "AUTONOMY-QUALIFIED"


class ExactResourceBinding(StrictContractModel):
    """One charter-pinned external system/resource generation."""

    logical_key: str = Field(pattern=IDENTIFIER_PATTERN, max_length=255)
    system: Literal[
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
    ]
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    generation: str = Field(min_length=1, max_length=255)
    account_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    region: str = Field(min_length=1, max_length=128)
    allowed_operations: tuple[str, ...] = Field(min_length=1, max_length=256)
    compatibility_rule: str | None = Field(default=None, max_length=512)

    @field_validator("allowed_operations")
    @classmethod
    def exact_operations(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(sorted(value))
        if len(set(normalized)) != len(normalized):
            raise ValueError("allowed_operations must be unique")
        for operation in normalized:
            if not operation or operation != operation.strip():
                raise ValueError("allowed_operations must be nonblank canonical strings")
            if operation == "*" or operation.endswith(".*") or "publication" in operation:
                raise ValueError("Wildcard and release-publication operations are forbidden")
        return normalized


class ImmutableInputBinding(StrictContractModel):
    logical_key: str = Field(pattern=IDENTIFIER_PATTERN, max_length=255)
    object_uri: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    sha256: str = Field(pattern=SHA256_PATTERN)
    byte_length: int = Field(ge=1, le=100_000_000)
    media_type: str = Field(min_length=1, max_length=255)
    schema_version: str = Field(min_length=1, max_length=255)


class ExecutionBudget(StrictContractModel):
    maximum_spend_minor_units: int = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    maximum_elapsed_seconds: int = Field(ge=1, le=31_536_000)
    maximum_api_calls: int = Field(ge=1, le=100_000_000)
    maximum_mutations: int = Field(ge=1, le=1_000_000)
    maximum_attempts_per_leaf: int = Field(ge=1, le=100)


class MigrationPolicy(StrictContractModel):
    downtime_seconds: int = Field(ge=0, le=86_400)
    rpo_seconds: int = Field(ge=0, le=86_400)
    rto_seconds: int = Field(ge=1, le=604_800)
    snapshot_max_age_hours: int = Field(ge=1, le=24)
    retention_days: int = Field(ge=1, le=3_650)
    availability_observation_days: Literal[30] = 30
    availability_target_percent: float = Field(gt=0, le=100)
    allowed_remediation_classes: tuple[str, ...] = Field(max_length=128)
    pre_write_recovery: Literal["sqlite-rollback"] = "sqlite-rollback"
    post_write_recovery: Literal["postgresql-forward-only"] = (
        "postgresql-forward-only"
    )

    @field_validator("allowed_remediation_classes")
    @classmethod
    def remediation_allowlist(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("allowed_remediation_classes must be unique")
        if any(not item or item == "*" for item in value):
            raise ValueError("Remediation classes must be exact and nonblank")
        return tuple(sorted(value))


class ExecutionWindow(StrictContractModel):
    logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    starts_at: datetime
    ends_at: datetime
    permitted_stages: tuple[str, ...] = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def valid_window(self) -> "ExecutionWindow":
        _require_aware(self.starts_at, "starts_at")
        _require_aware(self.ends_at, "ends_at")
        if self.ends_at <= self.starts_at:
            raise ValueError("Execution window must end after it starts")
        if len(set(self.permitted_stages)) != len(self.permitted_stages):
            raise ValueError("permitted_stages must be unique")
        return self


class TrustedKeyBinding(StrictContractModel):
    logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    key_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    issuer: str = Field(min_length=1, max_length=255)
    allowed_subject: str = Field(min_length=1, max_length=512)
    intended_use: str = Field(min_length=1, max_length=255)


class AutonomyCharter(StrictContractModel):
    """Externally established authority consumed by the autonomous program."""

    schema_version: Literal["workchord-postgresql-autonomy-charter-v1"] = (
        "workchord-postgresql-autonomy-charter-v1"
    )
    charter_id: str = Field(pattern=IDENTIFIER_PATTERN)
    issuer: str = Field(min_length=1, max_length=255)
    subject: Literal["workchord-postgresql-autonomous-migration"]
    repository: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    candidate_branch: str = Field(min_length=1, max_length=255)
    push_policy: str = Field(min_length=1, max_length=512)
    project_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    iteration_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    task_graph_digest: str = Field(pattern=SHA256_PATTERN)
    topology_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    bootstrap_action_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    valid_from: datetime
    expires_at: datetime
    revocation_source_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    revocation_max_age_seconds: int = Field(ge=1, le=3600)
    production_mutation_allowed: bool
    resources: tuple[ExactResourceBinding, ...] = Field(min_length=1, max_length=256)
    immutable_inputs: tuple[ImmutableInputBinding, ...] = Field(
        min_length=1, max_length=256
    )
    trusted_keys: tuple[TrustedKeyBinding, ...] = Field(min_length=1, max_length=64)
    execution_windows: tuple[ExecutionWindow, ...] = Field(
        min_length=1, max_length=256
    )
    budget: ExecutionBudget
    migration_policy: MigrationPolicy

    @model_validator(mode="after")
    def semantic_boundary(self) -> "AutonomyCharter":
        _require_aware(self.valid_from, "valid_from")
        _require_aware(self.expires_at, "expires_at")
        if self.expires_at <= self.valid_from:
            raise ValueError("Charter expiry must follow valid_from")
        logical_keys = [item.logical_key for item in self.resources]
        if len(set(logical_keys)) != len(logical_keys):
            raise ValueError("Resource logical keys must be unique")
        input_keys = [item.logical_key for item in self.immutable_inputs]
        if len(set(input_keys)) != len(input_keys):
            raise ValueError("Immutable input logical keys must be unique")
        required_systems = {
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
        }
        present_systems = {item.system for item in self.resources}
        missing = sorted(required_systems - present_systems)
        if missing:
            raise ValueError(f"Charter is missing required systems: {missing}")
        key_names = [item.logical_key for item in self.trusted_keys]
        if len(set(key_names)) != len(key_names):
            raise ValueError("Trusted key logical keys must be unique")
        window_names = [item.logical_key for item in self.execution_windows]
        if len(set(window_names)) != len(window_names):
            raise ValueError("Execution-window logical keys must be unique")
        if any(
            item.starts_at < self.valid_from or item.ends_at > self.expires_at
            for item in self.execution_windows
        ):
            raise ValueError("Execution windows must be contained by charter validity")
        ensure_secret_free(self.model_dump(mode="json"))
        return self


class BootstrapActionSlot(StrictContractModel):
    """One finite externally preissued bootstrap mutation slot."""

    ordinal: int = Field(ge=1, le=100_000)
    slot_id: str = Field(pattern=IDENTIFIER_PATTERN)
    subject: Literal[
        "pg-bootstrap-controller",
        "pg-bootstrap-builder",
        "pg-bootstrap-verifier",
    ]
    action: str = Field(min_length=1, max_length=255)
    target_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    target_generation: str = Field(min_length=1, max_length=255)
    precondition_digest: str = Field(pattern=SHA256_PATTERN)
    input_schema: str = Field(pattern=IDENTIFIER_PATTERN)
    output_schema: str = Field(pattern=IDENTIFIER_PATTERN)
    journal_parent_digest: str = Field(pattern=SHA256_PATTERN)
    timeout_seconds: int = Field(ge=1, le=86_400)
    maximum_calls: int = Field(ge=1, le=100)
    maximum_spend_minor_units: int = Field(ge=0)
    nonce: str = Field(pattern=IDENTIFIER_PATTERN)
    reset_effect: str = Field(min_length=1, max_length=512)

    @model_validator(mode="after")
    def exact_slot(self) -> "BootstrapActionSlot":
        if self.action == "*" or self.action.endswith(".*"):
            raise ValueError("Bootstrap slot action must be exact")
        if "*" in self.target_ref or self.target_ref.endswith(("/", ":")):
            raise ValueError("Bootstrap slot target cannot be a wildcard or prefix")
        ensure_secret_free(self.model_dump(mode="json"))
        return self


class BootstrapActionManifest(StrictContractModel):
    schema_version: Literal["bootstrap-action-manifest-v1"] = (
        "bootstrap-action-manifest-v1"
    )
    manifest_id: str = Field(pattern=IDENTIFIER_PATTERN)
    charter_id: str = Field(pattern=IDENTIFIER_PATTERN)
    journal_genesis_digest: str = Field(pattern=SHA256_PATTERN)
    journal_expected_head_digest: str = Field(pattern=SHA256_PATTERN)
    issued_at: datetime
    expires_at: datetime
    slots: tuple[BootstrapActionSlot, ...] = Field(min_length=1, max_length=100_000)

    @model_validator(mode="after")
    def finite_ordered_slots(self) -> "BootstrapActionManifest":
        _require_aware(self.issued_at, "issued_at")
        _require_aware(self.expires_at, "expires_at")
        if self.expires_at <= self.issued_at:
            raise ValueError("Bootstrap action manifest expiry is invalid")
        ordinals = [slot.ordinal for slot in self.slots]
        if ordinals != list(range(1, len(self.slots) + 1)):
            raise ValueError("Bootstrap slots must have contiguous ordered ordinals")
        slot_ids = [slot.slot_id for slot in self.slots]
        nonces = [slot.nonce for slot in self.slots]
        if len(set(slot_ids)) != len(slot_ids) or len(set(nonces)) != len(nonces):
            raise ValueError("Bootstrap slot IDs and nonces must be unique")
        return self


class SignedAutonomyCharter(StrictContractModel):
    document: AutonomyCharter
    signature: DetachedSignatureEnvelope


class SignedBootstrapActionManifest(StrictContractModel):
    document: BootstrapActionManifest
    signature: DetachedSignatureEnvelope


class RevocationObservation(StrictContractModel):
    """Source-derived revocation result; never a caller-authored bare Boolean."""

    charter_id: str = Field(pattern=IDENTIFIER_PATTERN)
    state: Literal["active", "revoked", "unknown"]
    observed_at: datetime
    source_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    source_generation: str = Field(min_length=1, max_length=255)
    source_receipt_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("observed_at")
    @classmethod
    def aware_observation(cls, value: datetime) -> datetime:
        _require_aware(value, "observed_at")
        return value


@runtime_checkable
class RevocationResolver(Protocol):
    def resolve(
        self, *, charter_id: str, source_ref: str
    ) -> RevocationObservation: ...


class CharterVerificationReceipt(StrictContractModel):
    schema_version: Literal["workchord-charter-verification-v1"] = (
        "workchord-charter-verification-v1"
    )
    verified_at: datetime
    autonomy_state: AutonomyState
    program_decision: ProgramDecision
    charter_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    bootstrap_manifest_digest: str | None = Field(
        default=None, pattern=SHA256_PATTERN
    )
    trust_source_receipts: tuple[str, ...] = Field(default=(), max_length=16)
    blocker_codes: tuple[str, ...] = Field(default=(), max_length=64)

    @model_validator(mode="after")
    def valid_receipt(self) -> "CharterVerificationReceipt":
        _require_aware(self.verified_at, "verified_at")
        if len(set(self.blocker_codes)) != len(self.blocker_codes):
            raise ValueError("Charter blocker codes must be unique")
        if self.autonomy_state == AutonomyState.BLOCKED_EXTERNAL and not self.blocker_codes:
            raise ValueError("Blocked charter verification requires a blocker")
        return self


class SignedCharterVerificationReceipt(StrictContractModel):
    receipt: CharterVerificationReceipt
    signature: DetachedSignatureEnvelope


class CharterVerificationError(ValueError):
    pass


class CharterVerifier:
    """Verify external authority without creating or broadening it."""

    def __init__(
        self,
        *,
        trust_resolver: PublicTrustResolver,
        revocation_resolver: RevocationResolver,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._trust_resolver = trust_resolver
        self._revocation_resolver = revocation_resolver
        self._clock = clock

    def verify(
        self,
        charter: SignedAutonomyCharter,
        bootstrap_manifest: SignedBootstrapActionManifest,
    ) -> CharterVerificationReceipt:
        now = self._clock()
        _require_aware(now, "clock")
        charter_bytes = canonical_json_bytes(charter.document)
        manifest_bytes = canonical_json_bytes(bootstrap_manifest.document)
        try:
            charter_anchor = verify_detached_signature(
                charter_bytes, charter.signature, self._trust_resolver
            )
            manifest_anchor = verify_detached_signature(
                manifest_bytes, bootstrap_manifest.signature, self._trust_resolver
            )
        except SignatureVerificationError as exc:
            raise CharterVerificationError(str(exc)) from exc
        charter_digest = sha256_hex(charter_bytes)
        manifest_digest = sha256_hex(manifest_bytes)
        if charter.document.bootstrap_action_manifest_digest != manifest_digest:
            raise CharterVerificationError(
                "Bootstrap action manifest does not match the charter"
            )
        if bootstrap_manifest.document.charter_id != charter.document.charter_id:
            raise CharterVerificationError("Bootstrap manifest binds another charter")
        if bootstrap_manifest.document.expires_at > charter.document.expires_at:
            raise CharterVerificationError("Bootstrap authority outlives the charter")
        if not (charter.document.valid_from <= now < charter.document.expires_at):
            raise CharterVerificationError("Charter is not currently valid")
        if not (
            bootstrap_manifest.document.issued_at
            <= now
            < bootstrap_manifest.document.expires_at
        ):
            raise CharterVerificationError(
                "Bootstrap action manifest is not currently valid"
            )
        try:
            revocation = self._revocation_resolver.resolve(
                charter_id=charter.document.charter_id,
                source_ref=charter.document.revocation_source_ref,
            )
        except Exception as exc:
            raise CharterVerificationError("Revocation source is unavailable") from exc
        if revocation.charter_id != charter.document.charter_id:
            raise CharterVerificationError("Revocation source returned another charter")
        if revocation.source_ref != charter.document.revocation_source_ref:
            raise CharterVerificationError("Revocation source reference mismatch")
        age = now - revocation.observed_at.astimezone(UTC)
        if age < timedelta(0) or age > timedelta(
            seconds=charter.document.revocation_max_age_seconds
        ):
            raise CharterVerificationError("Revocation observation is stale")
        if revocation.state != "active":
            raise CharterVerificationError(
                f"Charter revocation state is {revocation.state}"
            )
        if charter.signature.issuer != charter.document.issuer:
            raise CharterVerificationError("Charter issuer metadata mismatch")
        return CharterVerificationReceipt(
            verified_at=now,
            autonomy_state=AutonomyState.NOT_READY,
            program_decision=ProgramDecision.NO_SHIP,
            charter_digest=charter_digest,
            bootstrap_manifest_digest=manifest_digest,
            trust_source_receipts=(
                charter_anchor.source_receipt_digest,
                manifest_anchor.source_receipt_digest,
                revocation.source_receipt_digest,
            ),
            blocker_codes=("autonomy_implementation_not_qualified",),
        )

    def verify_or_block(
        self,
        charter: SignedAutonomyCharter | None,
        bootstrap_manifest: SignedBootstrapActionManifest | None,
    ) -> CharterVerificationReceipt:
        now = self._clock()
        if charter is None or bootstrap_manifest is None:
            return CharterVerificationReceipt(
                verified_at=now,
                autonomy_state=AutonomyState.BLOCKED_EXTERNAL,
                program_decision=ProgramDecision.NO_SHIP,
                blocker_codes=("standing_delegation_missing",),
            )
        try:
            return self.verify(charter, bootstrap_manifest)
        except (CharterVerificationError, ValueError) as exc:
            normalized = str(exc).lower()
            if "revocation" in normalized:
                code = "standing_delegation_revocation_invalid"
            elif "signature" in normalized or "trust" in normalized:
                code = "standing_delegation_trust_invalid"
            elif "bootstrap" in normalized:
                code = "bootstrap_authority_invalid"
            else:
                code = "standing_delegation_invalid"
            return CharterVerificationReceipt(
                verified_at=now,
                autonomy_state=AutonomyState.BLOCKED_EXTERNAL,
                program_decision=ProgramDecision.NO_SHIP,
                blocker_codes=(code,),
            )


def sign_charter_verification_receipt(
    receipt: CharterVerificationReceipt,
    *,
    signer: RemoteSigner,
    key_ref: str,
) -> SignedCharterVerificationReceipt:
    """Sign a deterministic receipt through the external charter-verifier key."""

    subject = "pg-charter-verifier"
    signature = signer.sign_digest(
        payload_sha256=sha256_hex(canonical_json_bytes(receipt)),
        key_ref=key_ref,
        subject=subject,
    )
    if signature.subject != subject:
        raise ValueError("Remote signer returned another charter-verifier subject")
    return SignedCharterVerificationReceipt(receipt=receipt, signature=signature)


def _require_aware(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
