"""Portable agent-team setup, reconciliation, and readiness contracts."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal, Mapping
from urllib.parse import parse_qsl, urlsplit

from pydantic import ConfigDict, Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)


AGENT_TEAM_MASTER_SCHEMA_VERSION = "agent-team-master-v1"
AGENT_TEAM_PLAN_SCHEMA_VERSION = "agent-team-reconciliation-plan-v1"
AGENT_TEAM_STATUS_SCHEMA_VERSION = "agent-team-status-v1"
AGENT_TEAM_REPORT_SCHEMA_VERSION = "agent-team-setup-report-v1"
AGENT_TEAM_ACK_SCHEMA_VERSION = "agent-team-runtime-ack-v1"
AGENT_TEAM_HANDOFF_SCHEMA_VERSION = "agent-team-runtime-handoff-v1"
MAX_AGENT_TEAM_MANIFEST_BYTES = 65_536
MAX_AGENT_TEAM_PLAN_BYTES = 131_072
MAX_AGENT_TEAM_REPORT_BYTES = 65_536
MAX_AGENT_TEAM_MEMBERS = 128
MAX_AGENT_TEAM_ACTIONS = 256
MAX_AGENT_TEAM_BLOCKERS = 64
SHA256_PATTERN = r"^[0-9a-f]{64}$"
STABLE_KEY_PATTERN = r"^[a-z0-9](?:[a-z0-9._-]{0,98}[a-z0-9])?$"
ACTION_ID_PATTERN = r"^[a-z0-9](?:[a-z0-9._:-]{0,126}[a-z0-9])?$"
FEATURE_PATTERN = r"^[a-z0-9](?:[a-z0-9._-]{0,126}[a-z0-9])?$"
SEMVER_PATTERN = r"^\d+\.\d+\.\d+$"


ROLE_SCOPE_PRESETS: dict[str, tuple[str, ...]] = {
    "pm-v1": (
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
        "team:write",
    ),
    "worker-v1": (
        "assignments:read",
        "events:write",
        "runs:write",
        "skills:read",
        "triage:write",
        "work:execute",
    ),
    "verifier-v1": (
        "assignments:read",
        "skills:read",
        "verification:read",
        "verification:write",
    ),
}
ROLE_SCOPE_PRESET_BY_ROLE = {
    "pm": "pm-v1",
    "worker": "worker-v1",
    "verifier": "verifier-v1",
}
ROLE_PACKAGE_COMPATIBILITY: dict[str, tuple[str, ...]] = {
    "pm": ("workchord-pm",),
    "worker": ("workchord-worker",),
    # Verification is a control operation in the PM bundle. The narrower
    # verifier-v1 scope preset prevents the runtime from exercising PM powers.
    "verifier": ("workchord-pm",),
}
ROLE_ASSIGNMENT_MODE = {
    "pm": "ownership",
    "worker": "execution",
    "verifier": "verification",
}
SECRET_QUERY_KEYS = frozenset(
    {
        "access_token",
        "api_key",
        "apikey",
        "auth",
        "authorization",
        "credential",
        "password",
        "secret",
        "token",
    }
)


class UnsupportedAgentTeamMasterVersion(ValueError):
    """Raised when a caller submits an unknown manifest schema version."""


class AgentTeamReconciliationClass(StrEnum):
    CREATE = "create"
    SAFE_UPDATE = "safe_update"
    NO_CHANGE = "no_change"
    BLOCKED_CONFLICT = "blocked_conflict"
    REQUIRES_REPLACEMENT = "requires_replacement"
    PROPOSE_DISABLE = "propose_disable"
    UNMANAGED = "unmanaged"


class AgentTeamMemberLifecycle(StrEnum):
    DESIRED = "desired"
    CONFIGURED = "configured"
    CREDENTIAL_DELIVERED = "credential_delivered"
    ONBOARDING = "onboarding"
    CONNECTED = "connected"
    RUNTIME_READY = "runtime_ready"
    DISABLED = "disabled"


class AgentTeamActionStatus(StrEnum):
    PENDING = "pending"
    APPLIED = "applied"
    NO_CHANGE = "no_change"
    BLOCKED = "blocked"


def _normalize_unique_keys(
    values: tuple[str, ...],
    *,
    label: str,
) -> tuple[str, ...]:
    normalized = tuple(sorted(value.strip().lower() for value in values))
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} must be unique")
    return normalized


def _validate_reference(value: str, *, label: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized.encode("utf-8")) > 1_024:
        raise ValueError(f"{label} must be a bounded nonblank reference")
    parsed = urlsplit(normalized)
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"{label} must not contain user information")
    if any(key.strip().lower() in SECRET_QUERY_KEYS for key, _ in parse_qsl(parsed.query)):
        raise ValueError(f"{label} must not contain secret-like query fields")
    ensure_secret_free(normalized)
    return normalized


class AgentTeamSetupModel(StrictContractModel):
    """Strict base with JSON-schema metadata shared by setup contracts."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_default=True,
        allow_inf_nan=False,
        json_schema_extra={"x-secret-free": True},
    )


class AgentTeamSkillPackage(AgentTeamSetupModel):
    """Exact immutable role-package identity expected by one runtime."""

    name: str = Field(pattern=STABLE_KEY_PATTERN)
    version: str = Field(pattern=SEMVER_PATTERN)
    sha256: str = Field(pattern=SHA256_PATTERN)


class AgentTeamMemberSpec(AgentTeamSetupModel):
    """Portable desired state for one logical actor/runtime membership."""

    actor_key: str = Field(pattern=STABLE_KEY_PATTERN, max_length=100)
    actor_name: str = Field(pattern=STABLE_KEY_PATTERN, max_length=100)
    display_name: str = Field(min_length=1, max_length=255)
    role: Literal["pm", "worker", "verifier"]
    scope_preset: Literal["pm-v1", "worker-v1", "verifier-v1"]
    profile_key: str = Field(pattern=STABLE_KEY_PATTERN, max_length=120)
    skill_package: AgentTeamSkillPackage
    assignment_modes: tuple[
        Literal["ownership", "execution", "verification", "design_handoff"], ...
    ] = Field(min_length=1, max_length=4)
    model_binding_keys: tuple[str, ...] = Field(min_length=1, max_length=16)
    default_model_binding_key: str = Field(
        pattern=STABLE_KEY_PATTERN,
        max_length=120,
    )
    runtime_ref: str = Field(min_length=1, max_length=1_024)
    credential_ref: str = Field(min_length=1, max_length=1_024)

    @field_validator("assignment_modes")
    @classmethod
    def normalize_assignment_modes(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        return _normalize_unique_keys(value, label="assignment_modes")

    @field_validator("model_binding_keys")
    @classmethod
    def normalize_model_binding_keys(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        normalized = _normalize_unique_keys(value, label="model_binding_keys")
        for key in normalized:
            if len(key) > 120:
                raise ValueError("model_binding_keys must be bounded")
            if not key[0].isalnum() or not key[-1].isalnum() or any(
                character not in "abcdefghijklmnopqrstuvwxyz0123456789._-"
                for character in key
            ):
                raise ValueError(
                    "model_binding_keys must use stable lowercase identifiers"
                )
        return normalized

    @field_validator("runtime_ref", "credential_ref")
    @classmethod
    def validate_external_references(cls, value: str, info: Any) -> str:
        return _validate_reference(value, label=info.field_name)

    @model_validator(mode="after")
    def validate_role_compatibility(self) -> "AgentTeamMemberSpec":
        expected_preset = ROLE_SCOPE_PRESET_BY_ROLE[self.role]
        if self.scope_preset != expected_preset:
            raise ValueError("Role and scope preset are incompatible")
        expected_mode = ROLE_ASSIGNMENT_MODE[self.role]
        if expected_mode not in self.assignment_modes:
            raise ValueError(
                f"{self.role} members require assignment mode {expected_mode}"
            )
        if self.skill_package.name not in ROLE_PACKAGE_COMPATIBILITY[self.role]:
            raise ValueError("Role and immutable skill package are incompatible")
        if self.default_model_binding_key not in self.model_binding_keys:
            raise ValueError(
                "default_model_binding_key must name one declared model binding"
            )
        ensure_agent_team_secret_free(self.model_dump(mode="json"))
        return self

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


class AgentTeamReadinessPolicy(AgentTeamSetupModel):
    """Backend-owned minimum topology needed before runtime readiness."""

    minimum_execution_workers: int = Field(default=1, ge=1, le=64)
    require_independent_verifier_when_assessed: bool = True
    maximum_runtime_staleness_seconds: int = Field(
        default=300,
        ge=30,
        le=86_400,
    )


class AgentTeamMaster(AgentTeamSetupModel):
    """Canonical portable desired-state document for one agent team."""

    schema_version: Literal["agent-team-master-v1"] = (
        AGENT_TEAM_MASTER_SCHEMA_VERSION
    )
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN, max_length=100)
    server_url: str = Field(min_length=1, max_length=2_000)
    credential_sink_ref: str = Field(min_length=1, max_length=1_024)
    required_server_features: tuple[str, ...] = Field(
        min_length=1,
        max_length=64,
    )
    controller: AgentTeamMemberSpec
    workers: tuple[AgentTeamMemberSpec, ...] = Field(
        min_length=1,
        max_length=MAX_AGENT_TEAM_MEMBERS - 1,
    )
    verifiers: tuple[AgentTeamMemberSpec, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_MEMBERS - 2,
    )
    readiness_policy: AgentTeamReadinessPolicy = Field(
        default_factory=AgentTeamReadinessPolicy
    )

    @field_validator("server_url")
    @classmethod
    def validate_server_url(cls, value: str) -> str:
        normalized = _validate_reference(value, label="server_url").rstrip("/")
        parsed = urlsplit(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("server_url must be an absolute HTTP(S) URL")
        return normalized

    @field_validator("credential_sink_ref")
    @classmethod
    def validate_credential_sink_ref(cls, value: str) -> str:
        return _validate_reference(value, label="credential_sink_ref")

    @field_validator("required_server_features")
    @classmethod
    def normalize_required_features(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        normalized = _normalize_unique_keys(
            value,
            label="required_server_features",
        )
        import re

        if any(re.fullmatch(FEATURE_PATTERN, item) is None for item in normalized):
            raise ValueError("required_server_features contains an invalid key")
        return normalized

    @model_validator(mode="after")
    def validate_complete_topology(self) -> "AgentTeamMaster":
        if self.controller.role != "pm":
            raise ValueError("controller must be the single primary PM")
        if any(member.role != "worker" for member in self.workers):
            raise ValueError("workers may contain only worker-role members")
        if any(member.role != "verifier" for member in self.verifiers):
            raise ValueError("verifiers may contain only verifier-role members")
        members = self.all_members
        if len(members) > MAX_AGENT_TEAM_MEMBERS:
            raise ValueError(
                f"Agent team may contain at most {MAX_AGENT_TEAM_MEMBERS} members"
            )
        for attribute in (
            "actor_key",
            "actor_name",
            "runtime_ref",
            "credential_ref",
        ):
            values = [getattr(member, attribute) for member in members]
            if len(values) != len(set(values)):
                raise ValueError(f"Agent-team {attribute} values must be unique")
        if self.readiness_policy.minimum_execution_workers > len(self.workers):
            raise ValueError(
                "minimum_execution_workers exceeds declared worker membership"
            )
        ensure_agent_team_secret_free(self.model_dump(mode="json"))
        encoded = canonical_json_bytes(self)
        if len(encoded) > MAX_AGENT_TEAM_MANIFEST_BYTES:
            raise ValueError(
                "Agent-team manifest exceeds "
                f"{MAX_AGENT_TEAM_MANIFEST_BYTES} canonical bytes"
            )
        return self

    @property
    def all_members(self) -> tuple[AgentTeamMemberSpec, ...]:
        return (self.controller, *self.workers, *self.verifiers)

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def digest(self) -> str:
        return sha256_hex(self.canonical_bytes())


def ensure_agent_team_secret_free(value: Any) -> None:
    """Enforce setup-specific secret, prompt, environment, and log exclusions."""

    forbidden_fields = {
        "api_key",
        "api_token",
        "authorization",
        "client_secret",
        "credential",
        "credentials",
        "database_url",
        "environment",
        "environment_value",
        "password",
        "private_endpoint_token",
        "private_key",
        "prompt",
        "raw_log",
        "secret",
        "secret_key",
        "token",
    }

    def visit(item: Any, path: str = "") -> None:
        if isinstance(item, Mapping):
            for raw_key, nested in item.items():
                key = str(raw_key).strip().lower()
                child = f"{path}.{key}" if path else key
                if key in forbidden_fields:
                    raise ValueError(f"Secret-bearing setup field is forbidden at {child}")
                visit(nested, child)
        elif isinstance(item, (list, tuple)):
            for index, nested in enumerate(item):
                visit(nested, f"{path}[{index}]")

    visit(value)
    ensure_secret_free(value)


def parse_agent_team_master(value: Any) -> AgentTeamMaster:
    """Validate one supported manifest and return its canonical model."""

    if isinstance(value, AgentTeamMaster):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("Agent-team manifest must be a JSON object")
    version = value.get("schema_version")
    if version != AGENT_TEAM_MASTER_SCHEMA_VERSION:
        raise UnsupportedAgentTeamMasterVersion(
            "Unsupported agent-team master schema version"
        )
    return AgentTeamMaster.model_validate(value)


class AgentTeamCurrentMember(AgentTeamSetupModel):
    """Redacted authoritative member projection used by reconciliation."""

    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    actor_id: int | None = Field(default=None, ge=1)
    actor_name: str = Field(pattern=STABLE_KEY_PATTERN)
    topology_key: str | None = Field(default=None, pattern=STABLE_KEY_PATTERN)
    object_revision: int = Field(ge=1)
    lifecycle_state: AgentTeamMemberLifecycle
    desired_spec: AgentTeamMemberSpec


class AgentTeamCurrentSnapshot(AgentTeamSetupModel):
    """Current topology state with installation-local IDs kept separate."""

    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    revision: int = Field(ge=0)
    manifest_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    members: tuple[AgentTeamCurrentMember, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_MEMBERS * 2,
    )


class AgentTeamPlanAction(AgentTeamSetupModel):
    """One stable, redacted reconciliation decision."""

    action_id: str = Field(pattern=ACTION_ID_PATTERN, max_length=128)
    action_digest: str = Field(pattern=SHA256_PATTERN)
    reconciliation_class: AgentTeamReconciliationClass
    operation: Literal[
        "create_member",
        "adopt_member",
        "update_member",
        "no_change",
        "disable_member",
        "replace_member",
        "blocked",
        "unmanaged",
    ]
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    target_actor_id: int | None = Field(default=None, ge=1)
    expected_object_revision: int | None = Field(default=None, ge=1)
    expected_actor_revision: int | None = Field(default=None, ge=1)
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    preconditions: dict[str, Any] = Field(default_factory=dict, max_length=32)
    blocker_code: str | None = Field(
        default=None,
        pattern=FEATURE_PATTERN,
        max_length=128,
    )
    requires_explicit_confirmation: bool = False
    authority_change: bool = False

    @model_validator(mode="after")
    def validate_redacted_action(self) -> "AgentTeamPlanAction":
        ensure_agent_team_secret_free(self.model_dump(mode="json"))
        return self


class AgentTeamReconciliationPlan(AgentTeamSetupModel):
    """Digest-bound dry-run output applied only by exact action ID."""

    schema_version: Literal["agent-team-reconciliation-plan-v1"] = (
        AGENT_TEAM_PLAN_SCHEMA_VERSION
    )
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    expected_topology_revision: int = Field(ge=0)
    manifest_digest: str = Field(pattern=SHA256_PATTERN)
    actions: tuple[AgentTeamPlanAction, ...] = Field(
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )
    plan_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("blocker_codes")
    @classmethod
    def normalize_blocker_codes(
        cls,
        value: tuple[str, ...],
    ) -> tuple[str, ...]:
        return _normalize_unique_keys(value, label="blocker_codes")

    @model_validator(mode="after")
    def validate_plan_size(self) -> "AgentTeamReconciliationPlan":
        if len(canonical_json_bytes(self)) > MAX_AGENT_TEAM_PLAN_BYTES:
            raise ValueError(
                f"Agent-team plan exceeds {MAX_AGENT_TEAM_PLAN_BYTES} canonical bytes"
            )
        return self


def _member_projection(member: AgentTeamMemberSpec) -> dict[str, Any]:
    projection = member.model_dump(mode="json")
    ensure_agent_team_secret_free(projection)
    return projection


def _build_action(
    *,
    desired: AgentTeamMaster,
    actor_key: str,
    classification: AgentTeamReconciliationClass,
    operation: str,
    target_actor_id: int | None,
    expected_object_revision: int | None,
    expected_actor_revision: int | None,
    before: dict[str, Any] | None,
    after: dict[str, Any] | None,
    blocker_code: str | None = None,
    requires_confirmation: bool = False,
    authority_change: bool = False,
) -> AgentTeamPlanAction:
    action_id = f"{classification.value.replace('_', '-')}-{actor_key}"
    core = {
        "action_id": action_id,
        "reconciliation_class": classification.value,
        "operation": operation,
        "actor_key": actor_key,
        "target_actor_id": target_actor_id,
        "expected_object_revision": expected_object_revision,
        "expected_actor_revision": expected_actor_revision,
        "before": before,
        "after": after,
        "preconditions": {
            "manifest_digest": desired.digest(),
            "topology_key": desired.topology_key,
        },
        "blocker_code": blocker_code,
        "requires_explicit_confirmation": requires_confirmation,
        "authority_change": authority_change,
    }
    return AgentTeamPlanAction(
        **core,
        action_digest=sha256_hex(core),
    )


def reconcile_agent_team_master(
    desired: AgentTeamMaster,
    current: AgentTeamCurrentSnapshot,
) -> AgentTeamReconciliationPlan:
    """Derive a deterministic, non-destructive baseline reconciliation plan."""

    if current.topology_key != desired.topology_key:
        raise ValueError("Current snapshot belongs to another topology")
    by_key = {member.actor_key: member for member in current.members}
    desired_by_key = {member.actor_key: member for member in desired.all_members}
    actions: list[AgentTeamPlanAction] = []

    for member in sorted(desired.all_members, key=lambda item: item.actor_key):
        existing = by_key.get(member.actor_key)
        before = _member_projection(existing.desired_spec) if existing else None
        after = _member_projection(member)
        if existing is None:
            actions.append(
                _build_action(
                    desired=desired,
                    actor_key=member.actor_key,
                    classification=AgentTeamReconciliationClass.CREATE,
                    operation="create_member",
                    target_actor_id=None,
                    expected_object_revision=None,
                    expected_actor_revision=None,
                    before=None,
                    after=after,
                )
            )
            continue
        if existing.topology_key not in (None, desired.topology_key):
            actions.append(
                _build_action(
                    desired=desired,
                    actor_key=member.actor_key,
                    classification=AgentTeamReconciliationClass.BLOCKED_CONFLICT,
                    operation="blocked",
                    target_actor_id=existing.actor_id,
                    expected_object_revision=existing.object_revision,
                    expected_actor_revision=None,
                    before=before,
                    after=after,
                    blocker_code="cross_topology_owner",
                )
            )
            continue
        if (
            existing.actor_name != member.actor_name
            or existing.desired_spec.role != member.role
        ):
            actions.append(
                _build_action(
                    desired=desired,
                    actor_key=member.actor_key,
                    classification=AgentTeamReconciliationClass.REQUIRES_REPLACEMENT,
                    operation="replace_member",
                    target_actor_id=existing.actor_id,
                    expected_object_revision=existing.object_revision,
                    expected_actor_revision=None,
                    before=before,
                    after=after,
                    blocker_code="stable_identity_drift",
                    requires_confirmation=True,
                    authority_change=True,
                )
            )
            continue
        if existing.desired_spec == member:
            actions.append(
                _build_action(
                    desired=desired,
                    actor_key=member.actor_key,
                    classification=AgentTeamReconciliationClass.NO_CHANGE,
                    operation="no_change",
                    target_actor_id=existing.actor_id,
                    expected_object_revision=existing.object_revision,
                    expected_actor_revision=None,
                    before=before,
                    after=after,
                )
            )
            continue
        authority_change = (
            existing.desired_spec.scope_preset != member.scope_preset
            or existing.desired_spec.profile_key != member.profile_key
            or existing.desired_spec.role != member.role
        )
        actions.append(
            _build_action(
                desired=desired,
                actor_key=member.actor_key,
                classification=AgentTeamReconciliationClass.SAFE_UPDATE,
                operation="update_member",
                target_actor_id=existing.actor_id,
                expected_object_revision=existing.object_revision,
                expected_actor_revision=None,
                before=before,
                after=after,
                requires_confirmation=authority_change,
                authority_change=authority_change,
            )
        )

    for existing in sorted(current.members, key=lambda item: item.actor_key):
        if existing.actor_key in desired_by_key:
            continue
        managed = existing.topology_key == desired.topology_key
        actions.append(
            _build_action(
                desired=desired,
                actor_key=existing.actor_key,
                classification=(
                    AgentTeamReconciliationClass.PROPOSE_DISABLE
                    if managed
                    else AgentTeamReconciliationClass.UNMANAGED
                ),
                operation="disable_member" if managed else "unmanaged",
                target_actor_id=existing.actor_id,
                expected_object_revision=existing.object_revision,
                expected_actor_revision=None,
                before=_member_projection(existing.desired_spec),
                after=None,
                requires_confirmation=managed,
                authority_change=managed,
            )
        )

    blocker_codes = tuple(
        sorted(
            {
                action.blocker_code
                for action in actions
                if action.blocker_code is not None
            }
        )
    )
    core = {
        "schema_version": AGENT_TEAM_PLAN_SCHEMA_VERSION,
        "topology_key": desired.topology_key,
        "expected_topology_revision": current.revision,
        "manifest_digest": desired.digest(),
        "actions": [action.model_dump(mode="json") for action in actions],
        "blocker_codes": list(blocker_codes),
    }
    return AgentTeamReconciliationPlan(
        **core,
        plan_digest=sha256_hex(core),
    )


class AgentTeamManifestRequest(AgentTeamSetupModel):
    manifest: AgentTeamMaster


class AgentTeamValidateResponse(AgentTeamSetupModel):
    schema_version: Literal["agent-team-validation-v1"] = "agent-team-validation-v1"
    valid: bool
    manifest_digest: str = Field(pattern=SHA256_PATTERN)
    normalized_manifest: AgentTeamMaster
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )


class AgentTeamPlanRequest(AgentTeamSetupModel):
    manifest: AgentTeamMaster
    expected_topology_revision: int = Field(ge=0)


class AgentTeamApplyRequest(AgentTeamSetupModel):
    manifest: AgentTeamMaster
    expected_topology_revision: int = Field(ge=0)
    plan_digest: str = Field(pattern=SHA256_PATTERN)
    approved_action_ids: tuple[str, ...] = Field(
        min_length=1,
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )
    confirmed_action_ids: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )

    @field_validator("approved_action_ids", "confirmed_action_ids")
    @classmethod
    def normalize_action_ids(
        cls,
        value: tuple[str, ...],
        info: Any,
    ) -> tuple[str, ...]:
        return _normalize_unique_keys(value, label=info.field_name)

    @model_validator(mode="after")
    def confirmations_are_approved(self) -> "AgentTeamApplyRequest":
        if not set(self.confirmed_action_ids).issubset(self.approved_action_ids):
            raise ValueError("confirmed_action_ids must also be approved")
        return self


class AgentTeamActionReceipt(AgentTeamSetupModel):
    action_id: str = Field(pattern=ACTION_ID_PATTERN)
    action_digest: str = Field(pattern=SHA256_PATTERN)
    reconciliation_class: AgentTeamReconciliationClass
    operation: str = Field(pattern=FEATURE_PATTERN)
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    status: AgentTeamActionStatus
    target_actor_id: int | None = Field(default=None, ge=1)
    before_revision: int | None = Field(default=None, ge=1)
    after_revision: int | None = Field(default=None, ge=1)
    blocker_code: str | None = Field(default=None, pattern=FEATURE_PATTERN)
    next_action: str | None = Field(default=None, max_length=255)


class AgentTeamApplyResponse(AgentTeamSetupModel):
    schema_version: Literal["agent-team-apply-receipt-v1"] = (
        "agent-team-apply-receipt-v1"
    )
    apply_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    manifest_digest: str = Field(pattern=SHA256_PATTERN)
    plan_digest: str = Field(pattern=SHA256_PATTERN)
    expected_topology_revision: int = Field(ge=0)
    resulting_topology_revision: int = Field(ge=0)
    status: Literal["completed", "partial", "blocked"]
    replayed: bool = False
    receipts: tuple[AgentTeamActionReceipt, ...] = Field(
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )
    pending_action_ids: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )


class AgentTeamRuntimeAcknowledgement(AgentTeamSetupModel):
    schema_version: Literal["agent-team-runtime-ack-v1"] = (
        AGENT_TEAM_ACK_SCHEMA_VERSION
    )
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    topology_revision: int = Field(ge=1)
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    role: Literal["pm", "worker", "verifier"]
    skill_package: AgentTeamSkillPackage
    profile_revision: str = Field(min_length=1, max_length=128)
    model_binding_revisions: dict[str, int] = Field(
        min_length=1,
        max_length=16,
    )
    server_features: tuple[str, ...] = Field(min_length=1, max_length=64)
    supported_assignment_modes: tuple[str, ...] = Field(
        min_length=1,
        max_length=4,
    )

    @field_validator("server_features", "supported_assignment_modes")
    @classmethod
    def normalize_ack_sequences(
        cls,
        value: tuple[str, ...],
        info: Any,
    ) -> tuple[str, ...]:
        return _normalize_unique_keys(value, label=info.field_name)

    @field_validator("model_binding_revisions")
    @classmethod
    def validate_binding_revisions(
        cls,
        value: dict[str, int],
    ) -> dict[str, int]:
        if any(
            not isinstance(revision, int)
            or isinstance(revision, bool)
            or revision < 1
            for revision in value.values()
        ):
            raise ValueError("model_binding_revisions must be positive integers")
        return dict(sorted(value.items()))


class AgentTeamRuntimeAcknowledgementResponse(AgentTeamSetupModel):
    schema_version: Literal["agent-team-runtime-ack-receipt-v1"] = (
        "agent-team-runtime-ack-receipt-v1"
    )
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    topology_revision: int = Field(ge=1)
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    actor_id: int = Field(ge=1)
    lifecycle_state: AgentTeamMemberLifecycle
    acknowledgement_digest: str = Field(pattern=SHA256_PATTERN)
    topology_runtime_ready: bool
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )


class AgentTeamRuntimeHandoff(AgentTeamSetupModel):
    schema_version: Literal["agent-team-runtime-handoff-v1"] = (
        AGENT_TEAM_HANDOFF_SCHEMA_VERSION
    )
    topology_key: str = Field(pattern=STABLE_KEY_PATTERN)
    topology_revision: int = Field(ge=1)
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    actor_id: int = Field(ge=1)
    role: Literal["pm", "worker", "verifier"]
    server_url: str
    required_server_features: tuple[str, ...]
    skill_package: AgentTeamSkillPackage
    profile_key: str = Field(pattern=STABLE_KEY_PATTERN)
    profile_revision: str
    model_binding_revisions: dict[str, int]
    supported_assignment_modes: tuple[str, ...]
    startup_instructions: tuple[str, ...] = Field(min_length=1, max_length=16)
    credential_ref: str = Field(min_length=1, max_length=1_024)

    @model_validator(mode="after")
    def validate_handoff(self) -> "AgentTeamRuntimeHandoff":
        _validate_reference(self.server_url, label="server_url")
        _validate_reference(self.credential_ref, label="credential_ref")
        ensure_agent_team_secret_free(self.model_dump(mode="json"))
        return self


class AgentTeamMemberStatus(AgentTeamSetupModel):
    actor_key: str = Field(pattern=STABLE_KEY_PATTERN)
    actor_id: int | None = Field(default=None, ge=1)
    actor_name: str = Field(pattern=STABLE_KEY_PATTERN)
    display_name: str
    role: Literal["pm", "worker", "verifier"]
    desired: bool
    configured: bool
    lifecycle_state: AgentTeamMemberLifecycle
    enabled: bool
    profile_key: str = Field(pattern=STABLE_KEY_PATTERN)
    profile_revision: str | None = None
    binding_revisions: dict[str, int] = Field(default_factory=dict)
    skill_package: AgentTeamSkillPackage
    package_acknowledged: bool
    credential_delivery_state: Literal[
        "pending",
        "delivered",
        "uncertain",
        "not_required",
    ]
    connection_state: Literal[
        "unobserved",
        "observed",
        "stale",
    ]
    last_seen_at: datetime | None = None
    queued_assignments: int | None = Field(default=None, ge=0)
    accepted_assignments: int | None = Field(default=None, ge=0)
    running_runs: int | None = Field(default=None, ge=0)
    runtime_ready: bool
    availability: Literal["availability_unknown"] = "availability_unknown"
    blocker_codes: tuple[str, ...] = Field(default=(), max_length=32)
    handoff: AgentTeamRuntimeHandoff | None = None


class AgentTeamSetupStep(AgentTeamSetupModel):
    id: Literal[
        "authority",
        "master",
        "controller",
        "workers",
        "bindings",
        "verifier",
        "review",
    ]
    state: Literal["done", "warn", "blocked", "todo"]
    blocker_codes: tuple[str, ...] = Field(default=(), max_length=32)
    next_action: str | None = Field(default=None, max_length=255)


class AgentTeamStatusResponse(AgentTeamSetupModel):
    schema_version: Literal["agent-team-status-v1"] = (
        AGENT_TEAM_STATUS_SCHEMA_VERSION
    )
    topology_key: str | None = Field(default=None, pattern=STABLE_KEY_PATTERN)
    topology_revision: int | None = Field(default=None, ge=1)
    manifest_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    topology_state: Literal[
        "absent",
        "configured",
        "onboarding",
        "runtime_ready",
        "blocked",
        "disabled",
    ]
    runtime_ready: bool
    availability: Literal["availability_unknown"] = "availability_unknown"
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )
    steps: tuple[AgentTeamSetupStep, ...] = Field(max_length=7)
    members: tuple[AgentTeamMemberStatus, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_MEMBERS,
    )
    pending_action_ids: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_ACTIONS,
    )
    can_mutate: bool
    next_action: str | None = Field(default=None, max_length=255)


class AgentTeamSetupReportCounts(AgentTeamSetupModel):
    """Bounded lifecycle and current-work counts without member internals."""

    desired: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    configured: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    credential_delivered: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    onboarding: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    connected: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    runtime_ready: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    blocked: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    disabled: int = Field(ge=0, le=MAX_AGENT_TEAM_MEMBERS)
    queued_assignments: int = Field(ge=0)
    accepted_assignments: int = Field(ge=0)
    running_runs: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_member_counts(self) -> "AgentTeamSetupReportCounts":
        for field_name in (
            "configured",
            "credential_delivered",
            "onboarding",
            "connected",
            "runtime_ready",
            "blocked",
            "disabled",
        ):
            if getattr(self, field_name) > self.desired:
                raise ValueError(
                    f"{field_name} cannot exceed the desired member count"
                )
        if self.runtime_ready + self.blocked != self.desired:
            raise ValueError(
                "runtime_ready and blocked must partition desired members"
            )
        return self


class AgentTeamSetupReportEvidence(AgentTeamSetupModel):
    """Durable reconciliation evidence summarized without action payloads."""

    apply_runs: int = Field(ge=0)
    action_receipts: int = Field(ge=0)
    latest_apply_id: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{32}$",
    )
    latest_apply_status: Literal[
        "running",
        "completed",
        "partial",
        "blocked",
    ] | None = None
    pending_actions: int = Field(ge=0, le=MAX_AGENT_TEAM_ACTIONS)


class AgentTeamDispatchAvailability(AgentTeamSetupModel):
    """Explicitly withhold availability claims without task-bound evidence."""

    state: Literal["availability_unknown"] = "availability_unknown"
    task_id: int | None = Field(default=None, ge=1)
    assessment_id: int | None = Field(default=None, ge=1)
    planning_boundary: str | None = Field(default=None, max_length=255)
    dispatch_eligible: int | None = Field(default=None, ge=0)
    currently_available: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_unknown_availability(
        self,
    ) -> "AgentTeamDispatchAvailability":
        if any(
            value is not None
            for value in (
                self.task_id,
                self.assessment_id,
                self.planning_boundary,
                self.dispatch_eligible,
                self.currently_available,
            )
        ):
            raise ValueError(
                "availability_unknown cannot carry contextual eligibility claims"
            )
        return self


class AgentTeamSetupReport(AgentTeamSetupModel):
    """Portable redacted topology report derived only from current server state."""

    schema_version: Literal["agent-team-setup-report-v1"] = (
        AGENT_TEAM_REPORT_SCHEMA_VERSION
    )
    generated_at: datetime
    topology_key: str | None = Field(default=None, pattern=STABLE_KEY_PATTERN)
    topology_revision: int | None = Field(default=None, ge=1)
    manifest_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    topology_state: Literal[
        "absent",
        "configured",
        "onboarding",
        "runtime_ready",
        "blocked",
        "disabled",
    ]
    runtime_ready: bool
    availability: Literal["availability_unknown"] = "availability_unknown"
    status_digest: str = Field(pattern=SHA256_PATTERN)
    counts: AgentTeamSetupReportCounts
    evidence: AgentTeamSetupReportEvidence
    dispatch_context: AgentTeamDispatchAvailability = Field(
        default_factory=AgentTeamDispatchAvailability
    )
    blocker_codes: tuple[str, ...] = Field(
        default=(),
        max_length=MAX_AGENT_TEAM_BLOCKERS,
    )

    @model_validator(mode="after")
    def validate_bounded_secret_free_report(self) -> "AgentTeamSetupReport":
        value = self.model_dump(mode="json")
        ensure_agent_team_secret_free(value)
        if len(canonical_json_bytes(value)) > MAX_AGENT_TEAM_REPORT_BYTES:
            raise ValueError(
                "Agent-team setup report exceeds "
                f"{MAX_AGENT_TEAM_REPORT_BYTES} canonical bytes"
            )
        if self.runtime_ready != (
            self.topology_state == "runtime_ready"
            and self.counts.blocked == 0
        ):
            raise ValueError(
                "Report runtime readiness must agree with state and counts"
            )
        return self
