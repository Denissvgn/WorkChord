"""Secret-free agent-team topology and deterministic reconciliation contract."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
LOGICAL_KEY_PATTERN = r"^[a-z][a-z0-9-]{2,99}$"
OPAQUE_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/@+-]{2,1023}$"


PM_SCOPES = (
    "assignments:read",
    "assignments:write",
    "planning:read",
    "planning:write",
    "recovery:read",
    "recovery:write",
    "reports:write",
    "skills:read",
    "tasks:read",
    "team:read",
)
WORKER_SCOPES = (
    "assignments:read",
    "events:write",
    "runs:write",
    "skills:read",
    "triage:write",
    "work:execute",
)
VERIFIER_SCOPES = (
    "assignments:read",
    "skills:read",
    "verification:read",
    "verification:write",
)
ROLE_SCOPE_PRESETS = {
    "postgresql-pm-v1": PM_SCOPES,
    "postgresql-worker-v1": WORKER_SCOPES,
    "postgresql-verifier-v1": VERIFIER_SCOPES,
}

POSTGRESQL_DISPATCHABLE_KEYS = (
    "pg-program-controller",
    "pg-code-executor",
    "pg-platform-executor",
    "pg-load-executor",
    "pg-database-executor",
    "pg-application-executor",
    "pg-security-executor",
    "pg-cleanroom-executor",
    "pg-snapshot-sanitizer",
    "pg-retention-executor",
    "pg-cutover-orchestrator",
    "pg-security-verifier",
    "pg-qualification-verifier",
    "pg-documentation-verifier",
    "pg-release-verifier",
    "pg-closure-verifier",
    "pg-availability-verifier",
    "pg-adversarial-verifier-a",
    "pg-adversarial-verifier-b",
)


class TopologyLifecycleState(StrEnum):
    DESIRED = "desired"
    CONFIGURED = "configured"
    CREDENTIAL_DELIVERED = "credential_delivered"
    ONBOARDING = "onboarding"
    CONNECTED = "connected"
    RUNTIME_READY = "runtime_ready"
    DISABLED = "disabled"


class ReconciliationClass(StrEnum):
    CREATE = "create"
    SAFE_UPDATE = "safe_update"
    NO_CHANGE = "no_change"
    BLOCKED_CONFLICT = "blocked_conflict"
    REQUIRES_REPLACEMENT = "requires_replacement"
    PROPOSE_DISABLE = "propose_disable"
    UNMANAGED = "unmanaged"


class ModelBindingContract(StrictContractModel):
    binding_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    catalog_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    minimum_reasoning_tier: int = Field(ge=1, le=3)
    minimum_context_tier: Literal["small", "medium", "large"]
    tool_tags: tuple[str, ...] = Field(default=(), max_length=128)
    data_policy_tags: tuple[str, ...] = Field(default=(), max_length=128)
    is_default: bool

    @field_validator("tool_tags", "data_policy_tags")
    @classmethod
    def normalized_tags(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(sorted(value))
        if len(set(normalized)) != len(normalized):
            raise ValueError("Binding tags must be unique")
        if any(not item or item != item.strip() for item in normalized):
            raise ValueError("Binding tags must be canonical and nonblank")
        return normalized


class RolePackageContract(StrictContractModel):
    package_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    version: str = Field(min_length=1, max_length=128)
    checksum_sha256: str = Field(pattern=SHA256_PATTERN)


class RuntimeContract(StrictContractModel):
    runtime_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    image_digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    sandbox_profile: str = Field(pattern=LOGICAL_KEY_PATTERN)
    attestation_policy_digest: str = Field(pattern=SHA256_PATTERN)


class TopologyMemberContract(StrictContractModel):
    logical_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    actor_name: str = Field(pattern=LOGICAL_KEY_PATTERN)
    role: Literal["pm", "worker", "verifier"]
    primary_controller: bool = False
    scope_preset: Literal[
        "postgresql-pm-v1",
        "postgresql-worker-v1",
        "postgresql-verifier-v1",
    ]
    scopes: tuple[str, ...] = Field(min_length=1, max_length=64)
    profile_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    profile_revision: int = Field(ge=1)
    skill_requirements: dict[str, int] = Field(default_factory=dict, max_length=128)
    model_bindings: tuple[ModelBindingContract, ...] = Field(
        min_length=1, max_length=32
    )
    role_package: RolePackageContract
    runtime: RuntimeContract
    independence_group: str = Field(pattern=LOGICAL_KEY_PATTERN)
    workload_identity_subject: str = Field(min_length=1, max_length=512)
    kms_key_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    external_lease_classes: tuple[str, ...] = Field(default=(), max_length=128)
    work_policy: Literal["assigned_only"] = "assigned_only"
    max_parallel_work: Literal[1] = 1

    @field_validator("scopes", "external_lease_classes")
    @classmethod
    def unique_sequence(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("Scope and lease-class values must be unique")
        if any(not item or item != item.strip() or item == "*" for item in value):
            raise ValueError("Scope and lease-class values must be exact")
        return tuple(sorted(value))

    @field_validator("skill_requirements")
    @classmethod
    def valid_skills(cls, value: dict[str, int]) -> dict[str, int]:
        if any(not key or level < 1 or level > 3 for key, level in value.items()):
            raise ValueError("Skill requirements must use levels 1-3")
        return dict(sorted(value.items()))

    @model_validator(mode="after")
    def compatible_role(self) -> "TopologyMemberContract":
        expected_preset = {
            "pm": "postgresql-pm-v1",
            "worker": "postgresql-worker-v1",
            "verifier": "postgresql-verifier-v1",
        }[self.role]
        if self.scope_preset != expected_preset:
            raise ValueError("Role and scope preset are incompatible")
        if self.scopes != tuple(sorted(ROLE_SCOPE_PRESETS[self.scope_preset])):
            raise ValueError("Member scopes do not exactly match the frozen preset")
        if self.primary_controller != (self.role == "pm"):
            raise ValueError("Only the single PM may be the primary controller")
        default_bindings = [item for item in self.model_bindings if item.is_default]
        if len(default_bindings) != 1:
            raise ValueError("Every member requires exactly one default model binding")
        binding_keys = [item.binding_key for item in self.model_bindings]
        if len(set(binding_keys)) != len(binding_keys):
            raise ValueError("Model binding keys must be unique per member")
        ensure_secret_free(self.model_dump(mode="json"))
        return self


class AgentTeamMasterContract(StrictContractModel):
    """Portable desired state for the PostgreSQL PM/worker/verifier topology."""

    schema_version: Literal["agent-team-master-v1"] = "agent-team-master-v1"
    topology_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    revision: int = Field(ge=1)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    model_catalog_revision: int = Field(ge=1)
    credential_sink_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=1024)
    members: tuple[TopologyMemberContract, ...] = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def complete_topology(self) -> "AgentTeamMasterContract":
        keys = [member.logical_key for member in self.members]
        actors = [member.actor_name for member in self.members]
        groups = [member.independence_group for member in self.members]
        if len(set(keys)) != len(keys) or len(set(actors)) != len(actors):
            raise ValueError("Topology logical keys and actor names must be unique")
        controllers = [member for member in self.members if member.primary_controller]
        if len(controllers) != 1:
            raise ValueError("Topology requires exactly one primary PM")
        if not any(member.role == "worker" for member in self.members):
            raise ValueError("Topology requires at least one execution-capable worker")
        if set(keys) == set(POSTGRESQL_DISPATCHABLE_KEYS):
            if len(set(groups)) != len(groups):
                raise ValueError(
                    "The PostgreSQL autonomy topology requires distinct independence groups"
                )
        elif self.topology_key == "postgresql-autonomous-migration":
            missing = sorted(set(POSTGRESQL_DISPATCHABLE_KEYS) - set(keys))
            extra = sorted(set(keys) - set(POSTGRESQL_DISPATCHABLE_KEYS))
            raise ValueError(
                f"PostgreSQL topology membership mismatch; missing={missing}, extra={extra}"
            )
        ensure_secret_free(self.model_dump(mode="json"))
        return self

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def digest(self) -> str:
        return sha256_hex(self.canonical_bytes())


class CurrentTopologyMember(StrictContractModel):
    logical_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    actor_name: str = Field(pattern=LOGICAL_KEY_PATTERN)
    topology_key: str | None = Field(default=None, pattern=LOGICAL_KEY_PATTERN)
    object_revision: int = Field(ge=1)
    lifecycle_state: TopologyLifecycleState
    desired_contract: TopologyMemberContract


class CurrentTopologySnapshot(StrictContractModel):
    topology_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    revision: int = Field(ge=0)
    applied_manifest_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    members: tuple[CurrentTopologyMember, ...] = Field(default=(), max_length=512)


class TopologyPlanAction(StrictContractModel):
    action_id: str = Field(pattern=LOGICAL_KEY_PATTERN)
    action_digest: str = Field(pattern=SHA256_PATTERN)
    reconciliation_class: ReconciliationClass
    logical_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    target_revision: int | None = Field(default=None, ge=1)
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    blocker_code: str | None = Field(default=None, pattern=LOGICAL_KEY_PATTERN)
    requires_explicit_confirmation: bool = False


class AgentTeamReconciliationPlan(StrictContractModel):
    schema_version: Literal["agent-team-reconciliation-plan-v1"] = (
        "agent-team-reconciliation-plan-v1"
    )
    topology_key: str = Field(pattern=LOGICAL_KEY_PATTERN)
    expected_topology_revision: int = Field(ge=0)
    manifest_digest: str = Field(pattern=SHA256_PATTERN)
    actions: tuple[TopologyPlanAction, ...] = Field(max_length=1024)
    plan_digest: str = Field(pattern=SHA256_PATTERN)


def reconcile_agent_team(
    desired: AgentTeamMasterContract,
    current: CurrentTopologySnapshot,
) -> AgentTeamReconciliationPlan:
    """Derive a stable, redacted plan without mutating topology or credentials."""

    if current.topology_key != desired.topology_key:
        raise ValueError("Current snapshot belongs to another topology")
    by_key = {item.logical_key: item for item in current.members}
    actions: list[TopologyPlanAction] = []
    desired_by_key = {item.logical_key: item for item in desired.members}

    for member in sorted(desired.members, key=lambda item: item.logical_key):
        existing = by_key.get(member.logical_key)
        before = _redacted_member(existing.desired_contract) if existing else None
        after = _redacted_member(member)
        blocker_code: str | None = None
        requires_confirmation = False
        if existing is None:
            classification = ReconciliationClass.CREATE
        elif existing.topology_key not in (None, desired.topology_key):
            classification = ReconciliationClass.BLOCKED_CONFLICT
            blocker_code = "cross-topology-owner"
        elif existing.actor_name != member.actor_name or existing.desired_contract.role != member.role:
            classification = ReconciliationClass.REQUIRES_REPLACEMENT
            blocker_code = "stable-identity-drift"
            requires_confirmation = True
        elif existing.desired_contract == member:
            classification = ReconciliationClass.NO_CHANGE
        else:
            authority_fields = (
                existing.desired_contract.scopes != member.scopes
                or existing.desired_contract.kms_key_ref != member.kms_key_ref
                or existing.desired_contract.independence_group
                != member.independence_group
                or existing.desired_contract.workload_identity_subject
                != member.workload_identity_subject
            )
            classification = (
                ReconciliationClass.REQUIRES_REPLACEMENT
                if authority_fields
                else ReconciliationClass.SAFE_UPDATE
            )
            requires_confirmation = authority_fields
            if authority_fields:
                blocker_code = "authority-boundary-drift"
        actions.append(
            _action(
                desired=desired,
                logical_key=member.logical_key,
                classification=classification,
                target_revision=existing.object_revision if existing else None,
                before=before,
                after=after,
                blocker_code=blocker_code,
                requires_confirmation=requires_confirmation,
            )
        )

    for existing in sorted(current.members, key=lambda item: item.logical_key):
        if existing.logical_key in desired_by_key:
            continue
        if existing.topology_key == desired.topology_key:
            classification = ReconciliationClass.PROPOSE_DISABLE
            requires_confirmation = True
        else:
            classification = ReconciliationClass.UNMANAGED
            requires_confirmation = False
        actions.append(
            _action(
                desired=desired,
                logical_key=existing.logical_key,
                classification=classification,
                target_revision=existing.object_revision,
                before=_redacted_member(existing.desired_contract),
                after=None,
                blocker_code=None,
                requires_confirmation=requires_confirmation,
            )
        )

    core = {
        "schema_version": "agent-team-reconciliation-plan-v1",
        "topology_key": desired.topology_key,
        "expected_topology_revision": current.revision,
        "manifest_digest": desired.digest(),
        "actions": [item.model_dump(mode="json") for item in actions],
    }
    return AgentTeamReconciliationPlan(
        **core,
        plan_digest=sha256_hex(core),
    )


def _redacted_member(member: TopologyMemberContract) -> dict[str, Any]:
    value = member.model_dump(mode="json")
    ensure_secret_free(value)
    return value


def _action(
    *,
    desired: AgentTeamMasterContract,
    logical_key: str,
    classification: ReconciliationClass,
    target_revision: int | None,
    before: dict[str, Any] | None,
    after: dict[str, Any] | None,
    blocker_code: str | None,
    requires_confirmation: bool,
) -> TopologyPlanAction:
    action_id = f"{classification.value.replace('_', '-')}-{logical_key}"
    digest_input = {
        "action_id": action_id,
        "reconciliation_class": classification.value,
        "logical_key": logical_key,
        "target_revision": target_revision,
        "before": before,
        "after": after,
        "blocker_code": blocker_code,
        "requires_explicit_confirmation": requires_confirmation,
        "manifest_digest": desired.digest(),
        "topology_revision": desired.revision,
    }
    return TopologyPlanAction(
        action_id=action_id,
        action_digest=sha256_hex(digest_input),
        reconciliation_class=classification,
        logical_key=logical_key,
        target_revision=target_revision,
        before=before,
        after=after,
        blocker_code=blocker_code,
        requires_explicit_confirmation=requires_confirmation,
    )
