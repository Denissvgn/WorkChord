"""Operator-only agent-team validation, reconciliation, setup, and readiness."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any, Protocol

from sqlalchemy import func, or_, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agent_contract import (
    AGENT_CONTRACT_FEATURES,
    AGENT_TEAM_MASTER_FEATURE,
    MODEL_AWARE_ROUTING_FEATURE,
)
from app.config import get_settings
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTeamActionReceipt as AgentTeamActionReceiptRecord,
    AgentTeamApplyRun,
    AgentTeamManagedObject,
    AgentTeamTopology,
    AgentTeamTopologyMember,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.team_member import TeamMemberProfile
from app.schemas.agent_skill_bundle import SkillBundleCatalogResponse
from app.schemas.agent_team_setup import (
    AGENT_TEAM_PLAN_SCHEMA_VERSION,
    MAX_AGENT_TEAM_ACTIONS,
    ROLE_SCOPE_PRESETS,
    AgentTeamActionReceipt,
    AgentTeamActionStatus,
    AgentTeamApplyRequest,
    AgentTeamApplyResponse,
    AgentTeamCurrentMember,
    AgentTeamCurrentSnapshot,
    AgentTeamManifestRequest,
    AgentTeamMaster,
    AgentTeamMemberLifecycle,
    AgentTeamMemberSpec,
    AgentTeamMemberStatus,
    AgentTeamPlanAction,
    AgentTeamPlanRequest,
    AgentTeamReconciliationClass,
    AgentTeamReconciliationPlan,
    AgentTeamRuntimeAcknowledgement,
    AgentTeamRuntimeAcknowledgementResponse,
    AgentTeamRuntimeHandoff,
    AgentTeamDispatchAvailability,
    AgentTeamSetupReport,
    AgentTeamSetupReportCounts,
    AgentTeamSetupReportEvidence,
    AgentTeamSetupStep,
    AgentTeamSkillPackage,
    AgentTeamStatusResponse,
    AgentTeamValidateResponse,
    ensure_agent_team_secret_free,
    parse_agent_team_master,
    reconcile_agent_team_master,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.services.agent_profile_catalog_service import (
    ALL_PROFILE_PRESETS,
    AgentProfileCatalogService,
)
from app.services.agent_routing_rollout import AgentRoutingTopologyReadiness
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    AgentService,
    actor_scopes,
    hash_api_key,
    require_scope,
    validate_idempotency_key,
)
from app.utils.time import as_utc, utc_now


ACK_WINDOW_SECONDS = 60
ACK_ATTEMPT_LIMIT = 5
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class AgentTeamSetupConflictError(AgentConflictError):
    """Stable conflict envelope shared by setup REST and MCP reads."""

    def __init__(self, code: str, message: str, **context: Any):
        self.code = code
        self.message = message
        self.context = context
        super().__init__(message)

    def detail(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, **self.context}


class CredentialDeliveryError(RuntimeError):
    """Raised when a one-time actor key did not reach the approved sink."""


class AgentTeamCredentialSink(Protocol):
    """One-way sink boundary; implementations never return credential material."""

    reference: str

    @property
    def available(self) -> bool:
        ...

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        """Deliver once and return a non-secret receipt digest."""


class FilesystemAgentTeamCredentialSink:
    """Write one-time credentials to an operator-owned mode-0700 directory."""

    def __init__(self, *, directory: str, reference: str):
        self.directory = Path(directory).expanduser() if directory else None
        self.reference = reference.strip()

    @property
    def available(self) -> bool:
        if self.directory is None or not self.reference:
            return False
        try:
            metadata = self.directory.stat()
        except OSError:
            return False
        return (
            stat.S_ISDIR(metadata.st_mode)
            and stat.S_IMODE(metadata.st_mode) & 0o077 == 0
        )

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        if not self.available or self.directory is None:
            raise CredentialDeliveryError(
                "The configured agent-team credential sink is unavailable"
            )
        if not (
            credential_ref == self.reference
            or credential_ref.startswith(f"{self.reference}/")
        ):
            raise CredentialDeliveryError(
                "Manifest credential reference does not use the approved sink"
            )
        filename = (
            hashlib.sha256(credential_ref.encode("utf-8")).hexdigest()[:24]
            + "-"
            + actor_key
            + ".json"
        )
        path = self.directory / filename
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        payload = json.dumps(
            {
                "actor_key": actor_key,
                "actor_name": actor_name,
                "api_key": api_key,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        descriptor: int | None = None
        try:
            descriptor = os.open(path, flags, 0o600)
            if os.fstat(descriptor).st_mode & 0o077:
                raise CredentialDeliveryError(
                    "Credential sink did not create a private file"
                )
            written = 0
            while written < len(payload):
                written += os.write(descriptor, payload[written:])
            os.fsync(descriptor)
        except FileExistsError as exc:
            raise CredentialDeliveryError(
                "Credential reference already has a delivered value"
            ) from exc
        except OSError as exc:
            raise CredentialDeliveryError(
                "Credential sink delivery failed"
            ) from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)
        receipt = {
            "schema_version": "agent-team-credential-delivery-receipt-v1",
            "credential_ref": credential_ref,
            "actor_key": actor_key,
            "sink_reference": self.reference,
            "delivered": True,
        }
        return hashlib.sha256(
            json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest()


@dataclass(frozen=True)
class AgentTeamMembershipBoundary:
    """Current topology/revision and active member set for exact-actor routing."""

    topology_id: int
    topology_key: str
    topology_revision: int
    primary_actor_id: int | None
    member_actor_ids: frozenset[int]
    runtime_ready_actor_ids: frozenset[int]


def _json_loads(value: str | None, fallback: Any) -> Any:
    try:
        parsed = json.loads(value) if value else fallback
    except (json.JSONDecodeError, TypeError):
        return fallback
    return parsed


def _canonical_json(value: Any) -> str:
    ensure_agent_team_secret_free(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


class AgentTeamSetupService:
    """Reconcile one portable topology without making the UI a control plane."""

    def __init__(
        self,
        db: AsyncSession,
        *,
        credential_sink: AgentTeamCredentialSink | None = None,
        skill_catalog_path: Path | None = None,
    ):
        self.db = db
        settings = get_settings()
        self.credential_sink = credential_sink or FilesystemAgentTeamCredentialSink(
            directory=getattr(settings, "agent_team_credential_sink_dir", ""),
            reference=getattr(
                settings,
                "agent_team_credential_sink_ref",
                "agent-team-secure-sink",
            ),
        )
        self.skill_catalog_path = (
            skill_catalog_path
            or REPOSITORY_ROOT / "agent-skills" / "catalog.json"
        )

    @staticmethod
    def _require_operator(actor: AgentActor) -> None:
        require_scope(actor, "admin")
        if actor.name == "bootstrap-agent":
            raise AgentPermissionError(
                "The bootstrap provisioning identity cannot reconcile agent teams"
            )

    @staticmethod
    def _principal_key(actor: AgentActor) -> str:
        return f"actor:{actor.id}" if actor.id > 0 else actor.name

    @staticmethod
    def _supported_features() -> frozenset[str]:
        return frozenset(
            {
                *AGENT_CONTRACT_FEATURES,
                MODEL_AWARE_ROUTING_FEATURE,
                AGENT_TEAM_MASTER_FEATURE,
            }
        )

    def _skill_catalog(self) -> SkillBundleCatalogResponse:
        try:
            return SkillBundleCatalogResponse.model_validate_json(
                self.skill_catalog_path.read_bytes()
            )
        except (OSError, ValueError) as exc:
            raise AgentTeamSetupConflictError(
                "agent_team_skill_catalog_unavailable",
                "The immutable agent role-package catalog is unavailable",
            ) from exc

    async def _compatibility_blockers(
        self,
        manifest: AgentTeamMaster,
    ) -> tuple[str, ...]:
        blockers: set[str] = set()
        missing_features = set(manifest.required_server_features).difference(
            self._supported_features()
        )
        if missing_features:
            blockers.add("required_server_feature_missing")

        catalog = self._skill_catalog()
        packages = {
            (entry.name, entry.version): entry for entry in catalog.skills
        }
        profile_keys = {item["key"] for item in ALL_PROFILE_PRESETS}
        existing_profile_rows = (
            await self.db.execute(
                select(TeamMemberProfile.seed_key).where(
                    TeamMemberProfile.seed_key.in_(
                        [member.profile_key for member in manifest.all_members]
                    )
                )
            )
        ).scalars()
        profile_keys.update(key for key in existing_profile_rows if key)

        binding_keys = sorted(
            {
                key
                for member in manifest.all_members
                for key in member.model_binding_keys
            }
        )
        catalog_rows = (
            await self.db.execute(
                select(AgentModelCatalogEntry).where(
                    AgentModelCatalogEntry.key.in_(binding_keys)
                )
            )
        ).scalars()
        model_entries = {entry.key: entry for entry in catalog_rows}

        for member in manifest.all_members:
            if member.profile_key not in profile_keys:
                blockers.add("profile_reference_missing")
            package = packages.get(
                (member.skill_package.name, member.skill_package.version)
            )
            if package is None:
                blockers.add("role_package_missing")
            elif member.skill_package.sha256 not in {
                archive.sha256 for archive in package.archives
            }:
                blockers.add("role_package_checksum_mismatch")
            for key in member.model_binding_keys:
                entry = model_entries.get(key)
                if entry is None:
                    blockers.add("model_catalog_entry_missing")
                elif not entry.enabled:
                    blockers.add("model_catalog_entry_disabled")
            if not (
                member.credential_ref == manifest.credential_sink_ref
                or member.credential_ref.startswith(
                    f"{manifest.credential_sink_ref}/"
                )
            ):
                blockers.add("credential_sink_reference_mismatch")

        if (
            not self.credential_sink.available
            or self.credential_sink.reference != manifest.credential_sink_ref
        ):
            blockers.add("credential_sink_unavailable")
        return tuple(sorted(blockers))

    async def validate(
        self,
        actor: AgentActor,
        request: AgentTeamManifestRequest,
    ) -> AgentTeamValidateResponse:
        """Validate canonical bytes plus current server/package compatibility."""

        self._require_operator(actor)
        manifest = parse_agent_team_master(request.manifest)
        blockers = await self._compatibility_blockers(manifest)
        return AgentTeamValidateResponse(
            valid=not blockers,
            manifest_digest=manifest.digest(),
            normalized_manifest=manifest,
            blocker_codes=blockers,
        )

    async def _topology(
        self,
        topology_key: str,
        *,
        for_update: bool = False,
        load_members: bool = False,
    ) -> AgentTeamTopology | None:
        options: list[Any] = []
        if load_members:
            options.extend(
                [
                    selectinload(AgentTeamTopology.members)
                    .selectinload(AgentTeamTopologyMember.actor)
                    .selectinload(AgentActor.profile)
                    .selectinload(TeamMemberProfile.skills),
                    selectinload(AgentTeamTopology.members)
                    .selectinload(AgentTeamTopologyMember.actor)
                    .selectinload(AgentActor.model_bindings)
                    .selectinload(AgentModelBinding.model_catalog),
                    selectinload(AgentTeamTopology.apply_runs).selectinload(
                        AgentTeamApplyRun.action_receipts
                    ),
                ]
            )
        query = select(AgentTeamTopology).where(
            AgentTeamTopology.topology_key == topology_key
        )
        if options:
            query = query.options(*options).execution_options(
                populate_existing=True
            )
        if for_update:
            if self.db.get_bind().dialect.name == "sqlite":
                await self.db.execute(
                    text(
                        "UPDATE agent_team_topologies SET id = id "
                        "WHERE topology_key = :topology_key"
                    ),
                    {"topology_key": topology_key},
                )
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _current_snapshot(
        self,
        manifest: AgentTeamMaster,
    ) -> AgentTeamCurrentSnapshot:
        topology = await self._topology(
            manifest.topology_key,
            load_members=True,
        )
        if topology is None:
            return AgentTeamCurrentSnapshot(
                topology_key=manifest.topology_key,
                revision=0,
            )
        members: list[AgentTeamCurrentMember] = []
        for member in topology.members:
            try:
                desired = AgentTeamMemberSpec.model_validate_json(
                    member.desired_member_payload
                )
            except ValueError as exc:
                raise AgentTeamSetupConflictError(
                    "agent_team_stored_member_invalid",
                    "Stored agent-team member contract is invalid",
                    actor_key=member.actor_key,
                ) from exc
            members.append(
                AgentTeamCurrentMember(
                    actor_key=member.actor_key,
                    actor_id=member.actor_id,
                    actor_name=member.actor_name,
                    topology_key=topology.topology_key,
                    object_revision=member.object_revision,
                    lifecycle_state=member.lifecycle_state,
                    desired_spec=desired,
                )
            )
        return AgentTeamCurrentSnapshot(
            topology_key=topology.topology_key,
            revision=topology.revision,
            manifest_digest=topology.manifest_digest,
            members=tuple(members),
        )

    @staticmethod
    def _action_with(
        action: AgentTeamPlanAction,
        **updates: Any,
    ) -> AgentTeamPlanAction:
        values = action.model_dump(mode="json")
        values.update(updates)
        values.pop("action_digest", None)
        values["action_digest"] = _digest(values)
        return AgentTeamPlanAction.model_validate(values)

    async def _actor_by_name(self, name: str) -> AgentActor | None:
        result = await self.db.execute(
            select(AgentActor)
            .options(
                selectinload(AgentActor.profile).selectinload(
                    TeamMemberProfile.skills
                ),
                selectinload(AgentActor.model_bindings).selectinload(
                    AgentModelBinding.model_catalog
                ),
            )
            .where(AgentActor.name == name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _actual_member_drift(
        actor: AgentActor,
        desired: AgentTeamMemberSpec,
    ) -> tuple[tuple[str, ...], bool]:
        blockers: set[str] = set()
        authority_change = False
        if actor.role != desired.role:
            blockers.add("actor_role_mismatch")
            authority_change = True
        expected_scopes = set(ROLE_SCOPE_PRESETS[desired.scope_preset])
        if set(actor_scopes(actor)) != expected_scopes:
            blockers.add("actor_scope_mismatch")
            authority_change = True
        if actor.profile is None or actor.profile.seed_key != desired.profile_key:
            blockers.add("actor_profile_mismatch")
            authority_change = True
        elif (
            not actor.profile.automation_enabled
            or desired.assignment_modes
            and not set(desired.assignment_modes).issubset(
                set(actor.profile.assignment_modes or [])
            )
        ):
            blockers.add("profile_assignment_mode_mismatch")
        bindings = {
            binding.model_catalog.key: binding
            for binding in actor.model_bindings
            if binding.model_catalog is not None
        }
        for key in desired.model_binding_keys:
            binding = bindings.get(key)
            if binding is None or not binding.selectable:
                blockers.add("model_binding_missing_or_disabled")
            elif (
                key == desired.default_model_binding_key
                and not binding.is_default
            ):
                blockers.add("default_model_binding_mismatch")
        if actor.lifecycle_state == "disabled":
            blockers.add("actor_disabled")
        return tuple(sorted(blockers)), authority_change

    async def plan(
        self,
        actor: AgentActor,
        request: AgentTeamPlanRequest,
    ) -> AgentTeamReconciliationPlan:
        """Return the exact current redacted plan without mutating any object."""

        self._require_operator(actor)
        manifest = parse_agent_team_master(request.manifest)
        snapshot = await self._current_snapshot(manifest)
        if snapshot.revision != request.expected_topology_revision:
            raise AgentTeamSetupConflictError(
                "agent_team_topology_revision_conflict",
                "Topology revision changed; request a fresh setup plan",
                expected_topology_revision=request.expected_topology_revision,
                current_topology_revision=snapshot.revision,
            )
        baseline = reconcile_agent_team_master(manifest, snapshot)
        compatibility = set(await self._compatibility_blockers(manifest))
        desired_by_key = {
            member.actor_key: member for member in manifest.all_members
        }
        reference_rows = (
            await self.db.execute(
                select(
                    AgentTeamTopologyMember.runtime_ref,
                    AgentTeamTopologyMember.credential_ref,
                    AgentTeamTopologyMember.actor_key,
                    AgentTeamTopology.topology_key,
                )
                .join(
                    AgentTeamTopology,
                    AgentTeamTopology.id
                    == AgentTeamTopologyMember.topology_id,
                )
                .where(
                    or_(
                        AgentTeamTopologyMember.runtime_ref.in_(
                            [member.runtime_ref for member in manifest.all_members]
                        ),
                        AgentTeamTopologyMember.credential_ref.in_(
                            [
                                member.credential_ref
                                for member in manifest.all_members
                            ]
                        ),
                    )
                )
            )
        ).all()
        runtime_reference_owners = {
            runtime_ref: (owner_topology_key, owner_actor_key)
            for (
                runtime_ref,
                _,
                owner_actor_key,
                owner_topology_key,
            ) in reference_rows
        }
        credential_reference_owners = {
            credential_ref: (owner_topology_key, owner_actor_key)
            for (
                _,
                credential_ref,
                owner_actor_key,
                owner_topology_key,
            ) in reference_rows
        }
        actions: list[AgentTeamPlanAction] = []
        member_specific_blockers = {
            "required_server_feature_missing",
            "profile_reference_missing",
            "role_package_missing",
            "role_package_checksum_mismatch",
            "model_catalog_entry_missing",
            "model_catalog_entry_disabled",
            "credential_sink_reference_mismatch",
        }

        for action in baseline.actions:
            desired = desired_by_key.get(action.actor_key)
            current = next(
                (
                    item
                    for item in snapshot.members
                    if item.actor_key == action.actor_key
                ),
                None,
            )
            adjusted = action
            if desired is not None:
                expected_owner = (
                    manifest.topology_key,
                    desired.actor_key,
                )
                if (
                    runtime_reference_owners.get(desired.runtime_ref)
                    not in {None, expected_owner}
                ):
                    adjusted = self._action_with(
                        action,
                        reconciliation_class=(
                            AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                        ),
                        operation="blocked",
                        blocker_code="cross_topology_runtime_reference",
                    )
                    actions.append(adjusted)
                    continue
                if (
                    credential_reference_owners.get(desired.credential_ref)
                    not in {None, expected_owner}
                ):
                    adjusted = self._action_with(
                        action,
                        reconciliation_class=(
                            AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                        ),
                        operation="blocked",
                        blocker_code="cross_topology_credential_reference",
                    )
                    actions.append(adjusted)
                    continue
            if desired is not None and compatibility.intersection(
                member_specific_blockers
            ):
                code = sorted(compatibility.intersection(member_specific_blockers))[0]
                adjusted = self._action_with(
                    action,
                    reconciliation_class=(
                        AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                    ),
                    operation="blocked",
                    blocker_code=code,
                )
                actions.append(adjusted)
                continue

            if action.reconciliation_class == AgentTeamReconciliationClass.CREATE:
                assert desired is not None
                existing_actor = await self._actor_by_name(desired.actor_name)
                if existing_actor is None:
                    if "credential_sink_unavailable" in compatibility:
                        adjusted = self._action_with(
                            action,
                            reconciliation_class=(
                                AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                            ),
                            operation="blocked",
                            blocker_code="credential_sink_unavailable",
                        )
                else:
                    owner_result = await self.db.execute(
                        select(
                            AgentTeamTopologyMember,
                            AgentTeamTopology.topology_key,
                        )
                        .join(
                            AgentTeamTopology,
                            AgentTeamTopology.id
                            == AgentTeamTopologyMember.topology_id,
                        )
                        .where(
                            AgentTeamTopologyMember.actor_id == existing_actor.id
                        )
                    )
                    owner = owner_result.first()
                    drift, authority_change = self._actual_member_drift(
                        existing_actor,
                        desired,
                    )
                    if owner is not None:
                        adjusted = self._action_with(
                            action,
                            reconciliation_class=(
                                AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                            ),
                            operation="blocked",
                            target_actor_id=existing_actor.id,
                            expected_actor_revision=existing_actor.queue_revision,
                            blocker_code="cross_topology_owner",
                        )
                    elif any(
                        code in {"actor_role_mismatch", "actor_disabled"}
                        for code in drift
                    ):
                        adjusted = self._action_with(
                            action,
                            reconciliation_class=(
                                AgentTeamReconciliationClass.BLOCKED_CONFLICT.value
                            ),
                            operation="blocked",
                            target_actor_id=existing_actor.id,
                            expected_actor_revision=existing_actor.queue_revision,
                            blocker_code=drift[0],
                        )
                    else:
                        adjusted = self._action_with(
                            action,
                            reconciliation_class=(
                                AgentTeamReconciliationClass.SAFE_UPDATE.value
                            ),
                            operation="adopt_member",
                            target_actor_id=existing_actor.id,
                            expected_actor_revision=existing_actor.queue_revision,
                            requires_explicit_confirmation=True,
                            authority_change=authority_change or bool(drift),
                            blocker_code=None,
                        )
            elif current is not None and current.actor_id is not None:
                mapped_actor = await self._actor_by_name(current.actor_name)
                if mapped_actor is None or mapped_actor.id != current.actor_id:
                    adjusted = self._action_with(
                        action,
                        reconciliation_class=(
                            AgentTeamReconciliationClass.REQUIRES_REPLACEMENT.value
                        ),
                        operation="replace_member",
                        blocker_code="managed_actor_missing",
                        requires_explicit_confirmation=True,
                        authority_change=True,
                    )
                else:
                    member_record_result = await self.db.execute(
                        select(AgentTeamTopologyMember).where(
                            AgentTeamTopologyMember.topology_id
                            == (
                                select(AgentTeamTopology.id)
                                .where(
                                    AgentTeamTopology.topology_key
                                    == manifest.topology_key
                                )
                                .scalar_subquery()
                            ),
                            AgentTeamTopologyMember.actor_key
                            == current.actor_key,
                        )
                    )
                    member_record = member_record_result.scalar_one_or_none()
                    if (
                        member_record is not None
                        and member_record.credential_delivery_state
                        in {"pending", "uncertain"}
                    ):
                        adjusted = self._action_with(
                            action,
                            reconciliation_class=(
                                AgentTeamReconciliationClass.REQUIRES_REPLACEMENT.value
                            ),
                            operation="replace_member",
                            blocker_code="credential_delivery_uncertain",
                            requires_explicit_confirmation=True,
                            authority_change=True,
                            expected_actor_revision=mapped_actor.queue_revision,
                        )
                    else:
                        drift, authority_change = self._actual_member_drift(
                            mapped_actor,
                            desired or current.desired_spec,
                        )
                        if drift and action.operation == "no_change":
                            adjusted = self._action_with(
                                action,
                                reconciliation_class=(
                                    AgentTeamReconciliationClass.SAFE_UPDATE.value
                                ),
                                operation="update_member",
                                expected_actor_revision=(
                                    mapped_actor.queue_revision
                                ),
                                requires_explicit_confirmation=authority_change,
                                authority_change=authority_change,
                                blocker_code=None,
                            )
                        elif action.operation in {
                            "update_member",
                            "disable_member",
                            "replace_member",
                        }:
                            updates: dict[str, Any] = {
                                "expected_actor_revision": (
                                    mapped_actor.queue_revision
                                ),
                            }
                            if (
                                action.operation == "replace_member"
                                and desired is not None
                                and (
                                    desired.actor_name == current.actor_name
                                    or desired.runtime_ref
                                    == current.desired_spec.runtime_ref
                                    or desired.credential_ref
                                    == current.desired_spec.credential_ref
                                )
                            ):
                                updates["blocker_code"] = (
                                    "replacement_requires_new_identity_refs"
                                )
                            adjusted = self._action_with(
                                action,
                                **updates,
                            )
            actions.append(adjusted)

        blocker_codes = tuple(
            sorted(
                {
                    *(
                        code
                        for code in compatibility
                        if code != "credential_sink_unavailable"
                    ),
                    *(
                        action.blocker_code
                        for action in actions
                        if action.blocker_code is not None
                    ),
                }
            )
        )
        core = {
            "schema_version": AGENT_TEAM_PLAN_SCHEMA_VERSION,
            "topology_key": manifest.topology_key,
            "expected_topology_revision": snapshot.revision,
            "manifest_digest": manifest.digest(),
            "actions": [item.model_dump(mode="json") for item in actions],
            "blocker_codes": list(blocker_codes),
        }
        return AgentTeamReconciliationPlan(
            **core,
            plan_digest=_digest(core),
        )

    async def _find_apply_run(
        self,
        *,
        principal_key: str,
        idempotency_key: str,
    ) -> AgentTeamApplyRun | None:
        result = await self.db.execute(
            select(AgentTeamApplyRun)
            .options(selectinload(AgentTeamApplyRun.action_receipts))
            .where(
                AgentTeamApplyRun.principal_key == principal_key,
                AgentTeamApplyRun.idempotency_key == idempotency_key,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _apply_request_digest(
        request: AgentTeamApplyRequest,
        command: AgentPlanningCommandContext,
    ) -> str:
        return _digest(
            {
                "manifest": request.manifest.model_dump(mode="json"),
                "expected_topology_revision": request.expected_topology_revision,
                "plan_digest": request.plan_digest,
                "approved_action_ids": list(request.approved_action_ids),
                "confirmed_action_ids": list(request.confirmed_action_ids),
                "rationale": command.rationale,
                "correlation_id": command.correlation_id,
            }
        )

    @staticmethod
    def _receipt_from_record(
        record: AgentTeamActionReceiptRecord,
    ) -> AgentTeamActionReceipt:
        return AgentTeamActionReceipt(
            action_id=record.action_id,
            action_digest=record.action_digest,
            reconciliation_class=record.reconciliation_class,
            operation=record.operation,
            actor_key=record.actor_key,
            status=record.status,
            target_actor_id=record.target_actor_id,
            before_revision=record.before_revision,
            after_revision=record.after_revision,
            blocker_code=record.blocker_code,
            next_action=record.next_action,
        )

    async def _replay_apply(
        self,
        run: AgentTeamApplyRun,
        *,
        request_digest: str,
    ) -> AgentTeamApplyResponse | None:
        if not secrets.compare_digest(run.request_digest, request_digest):
            raise AgentTeamSetupConflictError(
                "agent_team_idempotency_conflict",
                "Idempotency key was already used for another setup request",
            )
        if run.response_payload is None:
            return None
        response = AgentTeamApplyResponse.model_validate_json(
            run.response_payload
        )
        return response.model_copy(update={"replayed": True})

    async def _ensure_topology_for_apply(
        self,
        manifest: AgentTeamMaster,
        run: AgentTeamApplyRun,
    ) -> tuple[AgentTeamTopology, bool]:
        topology = await self._topology(
            manifest.topology_key,
            for_update=True,
        )
        created = False
        if topology is None:
            if run.expected_topology_revision != 0:
                raise AgentTeamSetupConflictError(
                    "agent_team_topology_revision_conflict",
                    "Topology disappeared while applying the setup plan",
                )
            topology = AgentTeamTopology(
                topology_key=manifest.topology_key,
                revision=1,
                manifest_digest=manifest.digest(),
                manifest_payload=_canonical_json(
                    manifest.model_dump(mode="json")
                ),
                state="configured",
                blocker_codes="[]",
            )
            self.db.add(topology)
            await self.db.flush()
            created = True
        elif (
            topology.revision != run.expected_topology_revision
            and not (
                run.expected_topology_revision == 0
                and run.topology_id == topology.id
                and topology.revision == 1
            )
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_topology_revision_conflict",
                "Topology revision changed during setup apply",
                expected_topology_revision=run.expected_topology_revision,
                current_topology_revision=topology.revision,
            )
        run.topology_id = topology.id
        return topology, created

    async def _resolve_profile(
        self,
        member: AgentTeamMemberSpec,
    ) -> TeamMemberProfile:
        result = await self.db.execute(
            select(TeamMemberProfile)
            .options(selectinload(TeamMemberProfile.skills))
            .where(TeamMemberProfile.seed_key == member.profile_key)
        )
        profile = result.scalar_one_or_none()
        if profile is None:
            if member.profile_key not in {
                item["key"] for item in ALL_PROFILE_PRESETS
            }:
                raise AgentTeamSetupConflictError(
                    "agent_team_profile_missing",
                    "Referenced profile is not available",
                    profile_key=member.profile_key,
                )
            profile = await AgentProfileCatalogService(self.db).apply_preset(
                member.profile_key,
                commit=False,
            )
        if (
            not profile.automation_enabled
            or not set(member.assignment_modes).issubset(
                set(profile.assignment_modes or [])
            )
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_profile_incompatible",
                "Profile does not satisfy the declared runtime assignment modes",
                profile_key=member.profile_key,
            )
        return profile

    async def _catalog_entries(
        self,
        member: AgentTeamMemberSpec,
    ) -> dict[str, AgentModelCatalogEntry]:
        rows = (
            await self.db.execute(
                select(AgentModelCatalogEntry).where(
                    AgentModelCatalogEntry.key.in_(
                        list(member.model_binding_keys)
                    )
                )
            )
        ).scalars()
        entries = {row.key: row for row in rows}
        if set(entries) != set(member.model_binding_keys) or any(
            not entry.enabled for entry in entries.values()
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_model_catalog_incompatible",
                "Every declared model binding requires an enabled catalog entry",
                actor_key=member.actor_key,
            )
        return entries

    async def _reconcile_bindings(
        self,
        *,
        topology: AgentTeamTopology,
        actor: AgentActor,
        member: AgentTeamMemberSpec,
        entries: dict[str, AgentModelCatalogEntry],
        allow_binding_replacement: bool = False,
    ) -> dict[str, int]:
        result = await self.db.execute(
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .where(AgentModelBinding.actor_id == actor.id)
        )
        existing = {
            binding.model_catalog.key: binding
            for binding in result.scalars()
            if binding.model_catalog is not None
        }
        for key, binding in existing.items():
            if (
                key != member.default_model_binding_key
                and binding.is_default
            ):
                binding.is_default = False
                binding.revision += 1
        await self.db.flush()

        revisions: dict[str, int] = {}
        for key in member.model_binding_keys:
            binding = existing.get(key)
            desired_default = key == member.default_model_binding_key
            await self._upsert_managed_object(
                topology=topology,
                object_type="model_catalog",
                logical_key=key,
                object_id=entries[key].id,
                object_revision=entries[key].revision,
                desired_digest=_digest(
                    {
                        "catalog_key": key,
                        "catalog_revision": entries[key].revision,
                    }
                ),
            )
            if binding is None:
                binding = AgentModelBinding(
                    actor_id=actor.id,
                    model_catalog_id=entries[key].id,
                    is_default=desired_default,
                    enabled=True,
                    tool_tags=[],
                    data_policy_tags=[],
                    revision=1,
                )
                self.db.add(binding)
                await self.db.flush()
            else:
                changed = (
                    not binding.enabled
                    or binding.is_default != desired_default
                )
                binding.enabled = True
                binding.is_default = desired_default
                if changed:
                    binding.revision += 1
                await self.db.flush()
            revisions[key] = binding.revision
            await self._upsert_managed_object(
                topology=topology,
                object_type="model_binding",
                logical_key=f"{member.actor_key}:{key}",
                object_id=binding.id,
                object_revision=binding.revision,
                desired_digest=_digest(
                    {
                        "actor_key": member.actor_key,
                        "catalog_key": key,
                        "default": desired_default,
                    }
                ),
                allow_object_replacement=allow_binding_replacement,
            )
        return dict(sorted(revisions.items()))

    async def _upsert_managed_object(
        self,
        *,
        topology: AgentTeamTopology,
        object_type: str,
        logical_key: str,
        object_id: int,
        object_revision: int,
        desired_digest: str,
        allow_object_replacement: bool = False,
    ) -> None:
        owner_result = await self.db.execute(
            select(AgentTeamManagedObject).where(
                AgentTeamManagedObject.topology_id == topology.id,
                AgentTeamManagedObject.object_type == object_type,
                AgentTeamManagedObject.logical_key == logical_key,
            )
        )
        owner = owner_result.scalar_one_or_none()
        if (
            owner is not None
            and owner.object_id != object_id
            and not allow_object_replacement
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_managed_object_conflict",
                "A topology logical key now resolves to another object",
                object_type=object_type,
                logical_key=logical_key,
                expected_object_id=owner.object_id,
                object_id=object_id,
            )
        if owner is None:
            owner = AgentTeamManagedObject(
                topology_id=topology.id,
                object_type=object_type,
                logical_key=logical_key,
                object_id=object_id,
                object_revision=object_revision,
                desired_digest=desired_digest,
            )
            self.db.add(owner)
        else:
            owner.logical_key = logical_key
            owner.object_id = object_id
            owner.object_revision = object_revision
            owner.desired_digest = desired_digest

    @staticmethod
    def _set_member_contract(
        record: AgentTeamTopologyMember,
        member: AgentTeamMemberSpec,
    ) -> None:
        record.actor_key = member.actor_key
        record.actor_name = member.actor_name
        record.role = member.role
        record.desired_member_digest = member.digest()
        record.desired_member_payload = _canonical_json(
            member.model_dump(mode="json")
        )
        record.scope_preset = member.scope_preset
        record.profile_key = member.profile_key
        record.skill_package_name = member.skill_package.name
        record.skill_package_version = member.skill_package.version
        record.skill_package_checksum = member.skill_package.sha256
        record.model_binding_keys = _canonical_json(
            list(member.model_binding_keys)
        )
        record.default_model_binding_key = member.default_model_binding_key
        record.assignment_modes = _canonical_json(
            list(member.assignment_modes)
        )
        record.runtime_ref = member.runtime_ref
        record.credential_ref = member.credential_ref

    async def _member_record(
        self,
        topology_id: int,
        actor_key: str,
        *,
        for_update: bool = False,
    ) -> AgentTeamTopologyMember | None:
        query = (
            select(AgentTeamTopologyMember)
            .options(
                selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.profile)
                .selectinload(TeamMemberProfile.skills),
                selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.model_bindings)
                .selectinload(AgentModelBinding.model_catalog),
            )
            .where(
                AgentTeamTopologyMember.topology_id == topology_id,
                AgentTeamTopologyMember.actor_key == actor_key,
            )
        )
        if for_update:
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _stage_event(
        self,
        *,
        event_type: str,
        actor_id: int | None,
        correlation_id: str,
        idempotency_key: str | None,
        payload: dict[str, Any],
    ) -> None:
        ensure_agent_team_secret_free(payload)
        encoded = _canonical_json(payload)
        if len(encoded.encode("utf-8")) > 16_384:
            raise ValueError("Agent-team event payload is too large")
        self.db.add(
            TaskEvent(
                task_id=None,
                actor_type="agent" if actor_id else "operator",
                actor_id=actor_id,
                event_type=event_type,
                payload=encoded,
                correlation_id=correlation_id,
                idempotency_key=idempotency_key,
            )
        )

    async def _apply_create_or_update(
        self,
        *,
        topology: AgentTeamTopology,
        member: AgentTeamMemberSpec,
        action: AgentTeamPlanAction,
        run: AgentTeamApplyRun,
    ) -> tuple[AgentTeamActionReceipt, bool]:
        record = await self._member_record(
            topology.id,
            member.actor_key,
            for_update=True,
        )
        actor: AgentActor | None = record.actor if record is not None else None
        generated_api_key: str | None = None
        before_revision = record.object_revision if record else None

        if action.operation == "create_member":
            if record is not None or await self._actor_by_name(member.actor_name):
                raise AgentTeamSetupConflictError(
                    "agent_team_action_stale",
                    "Create action target now exists; request a fresh plan",
                    action_id=action.action_id,
                )
            if not self.credential_sink.available:
                raise CredentialDeliveryError(
                    "The approved credential sink is unavailable"
                )
            profile = await self._resolve_profile(member)
            entries = await self._catalog_entries(member)
            generated_api_key = f"pmag_{secrets.token_urlsafe(32)}"
            actor = AgentActor(
                name=member.actor_name,
                display_name=member.display_name,
                api_key_hash=hash_api_key(generated_api_key),
                scopes=_canonical_json(
                    list(ROLE_SCOPE_PRESETS[member.scope_preset])
                ),
                enabled=False,
                lifecycle_state="onboarding",
                role=member.role,
                profile_id=profile.id,
                work_policy="assigned_only",
                max_parallel_work=1,
                queue_revision=1,
            )
            self.db.add(actor)
            await self.db.flush()
            record = AgentTeamTopologyMember(
                topology_id=topology.id,
                actor_key=member.actor_key,
                actor_id=actor.id,
                actor_name=member.actor_name,
                role=member.role,
                object_revision=1,
                lifecycle_state="configured",
                desired_member_digest=member.digest(),
                desired_member_payload=_canonical_json(
                    member.model_dump(mode="json")
                ),
                scope_preset=member.scope_preset,
                profile_key=member.profile_key,
                skill_package_name=member.skill_package.name,
                skill_package_version=member.skill_package.version,
                skill_package_checksum=member.skill_package.sha256,
                model_binding_keys=_canonical_json(
                    list(member.model_binding_keys)
                ),
                default_model_binding_key=member.default_model_binding_key,
                assignment_modes=_canonical_json(
                    list(member.assignment_modes)
                ),
                runtime_ref=member.runtime_ref,
                credential_ref=member.credential_ref,
                credential_delivery_state="pending",
            )
            self.db.add(record)
            await self.db.flush()
            await self._reconcile_bindings(
                topology=topology,
                actor=actor,
                member=member,
                entries=entries,
            )
            await self._upsert_managed_object(
                topology=topology,
                object_type="profile",
                logical_key=member.profile_key,
                object_id=profile.id,
                object_revision=1,
                desired_digest=_digest(
                    {
                        "profile_key": member.profile_key,
                        "assignment_modes": list(member.assignment_modes),
                    }
                ),
            )
            if member.role == "pm":
                topology.primary_actor_id = actor.id
            await self.db.commit()
            try:
                delivery_digest = await self.credential_sink.deliver(
                    credential_ref=member.credential_ref,
                    actor_key=member.actor_key,
                    actor_name=member.actor_name,
                    api_key=generated_api_key,
                )
            except Exception as exc:
                record = await self._member_record(
                    topology.id,
                    member.actor_key,
                    for_update=True,
                )
                assert record is not None and record.actor is not None
                record.credential_delivery_state = "uncertain"
                record.lifecycle_state = "disabled"
                record.object_revision += 1
                record.actor.enabled = False
                record.actor.lifecycle_state = "disabled"
                record.actor.queue_revision += 1
                topology = await self._topology(
                    member_topology_key := topology.topology_key,
                    for_update=True,
                )
                assert topology is not None
                topology.state = "blocked"
                topology.blocker_codes = _canonical_json(
                    ["credential_delivery_uncertain"]
                )
                await self._stage_event(
                    event_type="agent.team_setup_action",
                    actor_id=(
                        run.principal_actor_id
                        if run.principal_actor_id
                        else None
                    ),
                    correlation_id=run.correlation_id,
                    idempotency_key=run.idempotency_key,
                    payload={
                        "action_id": action.action_id,
                        "actor_key": member.actor_key,
                        "status": "blocked",
                        "blocker_code": "credential_delivery_uncertain",
                        "topology_key": member_topology_key,
                    },
                )
                await self.db.commit()
                return (
                    AgentTeamActionReceipt(
                        action_id=action.action_id,
                        action_digest=action.action_digest,
                        reconciliation_class=action.reconciliation_class,
                        operation=action.operation,
                        actor_key=member.actor_key,
                        status=AgentTeamActionStatus.BLOCKED,
                        target_actor_id=record.actor_id,
                        before_revision=before_revision,
                        after_revision=record.object_revision,
                        blocker_code="credential_delivery_uncertain",
                        next_action=(
                            "Approve an explicit credential recovery or rotation"
                        ),
                    ),
                    True,
                )
            record = await self._member_record(
                topology.id,
                member.actor_key,
                for_update=True,
            )
            assert record is not None
            record.credential_delivery_state = "delivered"
            record.credential_delivery_receipt_digest = delivery_digest
            record.lifecycle_state = "onboarding"
            record.object_revision += 1
            topology = await self._topology(
                topology.topology_key,
                for_update=True,
            )
            assert topology is not None
            topology.state = "onboarding"
            await self.db.flush()
        else:
            if action.target_actor_id is not None:
                actor = await self.db.get(AgentActor, action.target_actor_id)
            if actor is None:
                actor = await self._actor_by_name(member.actor_name)
            if actor is None:
                raise AgentTeamSetupConflictError(
                    "agent_team_action_stale",
                    "Adopt/update target no longer exists",
                    action_id=action.action_id,
                )
            if (
                action.expected_actor_revision is not None
                and actor.queue_revision != action.expected_actor_revision
            ):
                raise AgentTeamSetupConflictError(
                    "agent_team_actor_revision_conflict",
                    "Actor revision changed; request a fresh setup plan",
                    actor_id=actor.id,
                    expected_actor_revision=action.expected_actor_revision,
                    current_actor_revision=actor.queue_revision,
                )
            profile = await self._resolve_profile(member)
            entries = await self._catalog_entries(member)
            if record is None:
                record = AgentTeamTopologyMember(
                    topology_id=topology.id,
                    actor_key=member.actor_key,
                    actor_id=actor.id,
                    actor_name=member.actor_name,
                    role=member.role,
                    object_revision=1,
                    lifecycle_state="connected",
                    desired_member_digest=member.digest(),
                    desired_member_payload=_canonical_json(
                        member.model_dump(mode="json")
                    ),
                    scope_preset=member.scope_preset,
                    profile_key=member.profile_key,
                    skill_package_name=member.skill_package.name,
                    skill_package_version=member.skill_package.version,
                    skill_package_checksum=member.skill_package.sha256,
                    model_binding_keys=_canonical_json(
                        list(member.model_binding_keys)
                    ),
                    default_model_binding_key=member.default_model_binding_key,
                    assignment_modes=_canonical_json(
                        list(member.assignment_modes)
                    ),
                    runtime_ref=member.runtime_ref,
                    credential_ref=member.credential_ref,
                    credential_delivery_state="not_required",
                )
                self.db.add(record)
            else:
                if (
                    action.expected_object_revision is not None
                    and record.object_revision
                    != action.expected_object_revision
                ):
                    raise AgentTeamSetupConflictError(
                        "agent_team_member_revision_conflict",
                        "Managed member revision changed; request a fresh plan",
                        actor_key=member.actor_key,
                    )
                record.object_revision += 1
                record.lifecycle_state = (
                    "connected"
                    if actor.lifecycle_state == "active"
                    else "onboarding"
                )
                record.runtime_acknowledgement_digest = None
                record.runtime_acknowledgement_payload = None
                record.runtime_acknowledged_at = None
            self._set_member_contract(record, member)
            actor.display_name = member.display_name
            actor.role = member.role
            actor.scopes = _canonical_json(
                list(ROLE_SCOPE_PRESETS[member.scope_preset])
            )
            actor.profile_id = profile.id
            actor.work_policy = "assigned_only"
            actor.max_parallel_work = 1
            actor.queue_revision += 1
            await self.db.flush()
            await self._reconcile_bindings(
                topology=topology,
                actor=actor,
                member=member,
                entries=entries,
            )
            await self._upsert_managed_object(
                topology=topology,
                object_type="profile",
                logical_key=member.profile_key,
                object_id=profile.id,
                object_revision=1,
                desired_digest=_digest(
                    {
                        "profile_key": member.profile_key,
                        "assignment_modes": list(member.assignment_modes),
                    }
                ),
            )
            if member.role == "pm":
                topology.primary_actor_id = actor.id

        await self._stage_event(
            event_type="agent.team_setup_action",
            actor_id=run.principal_actor_id if run.principal_actor_id else None,
            correlation_id=run.correlation_id,
            idempotency_key=run.idempotency_key,
            payload={
                "action_id": action.action_id,
                "actor_key": member.actor_key,
                "status": "applied",
                "operation": action.operation,
                "topology_key": topology.topology_key,
                "target_actor_id": actor.id if actor else None,
                "object_revision": record.object_revision,
            },
        )
        await self.db.commit()
        return (
            AgentTeamActionReceipt(
                action_id=action.action_id,
                action_digest=action.action_digest,
                reconciliation_class=action.reconciliation_class,
                operation=action.operation,
                actor_key=member.actor_key,
                status=AgentTeamActionStatus.APPLIED,
                target_actor_id=actor.id if actor else None,
                before_revision=before_revision,
                after_revision=record.object_revision,
                next_action="Start the runtime with its secret-free handoff",
            ),
            True,
        )

    async def _apply_identity_replacement(
        self,
        *,
        topology: AgentTeamTopology,
        member: AgentTeamMemberSpec,
        action: AgentTeamPlanAction,
        run: AgentTeamApplyRun,
    ) -> tuple[AgentTeamActionReceipt, bool]:
        record = await self._member_record(
            topology.id,
            member.actor_key,
            for_update=True,
        )
        if record is None:
            raise AgentTeamSetupConflictError(
                "agent_team_action_stale",
                "Managed member no longer exists for replacement",
                action_id=action.action_id,
            )
        if (
            action.expected_object_revision is not None
            and record.object_revision != action.expected_object_revision
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_member_revision_conflict",
                "Managed member changed before replacement",
                actor_key=member.actor_key,
            )
        old_actor = record.actor
        if (
            old_actor is not None
            and action.expected_actor_revision is not None
            and old_actor.queue_revision != action.expected_actor_revision
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_actor_revision_conflict",
                "Actor changed before replacement",
                actor_id=old_actor.id,
                expected_actor_revision=action.expected_actor_revision,
                current_actor_revision=old_actor.queue_revision,
            )
        if (
            member.actor_name == record.actor_name
            or member.runtime_ref == record.runtime_ref
            or member.credential_ref == record.credential_ref
        ):
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=member.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=record.actor_id,
                    before_revision=record.object_revision,
                    blocker_code="replacement_requires_new_identity_refs",
                    next_action=(
                        "Choose new actor_name, runtime_ref, and credential_ref "
                        "values, then request a fresh plan"
                    ),
                ),
                False,
            )

        name_owner = await self._actor_by_name(member.actor_name)
        if name_owner is not None:
            if old_actor is not None and name_owner.id == old_actor.id:
                return (
                    AgentTeamActionReceipt(
                        action_id=action.action_id,
                        action_digest=action.action_digest,
                        reconciliation_class=action.reconciliation_class,
                        operation=action.operation,
                        actor_key=member.actor_key,
                        status=AgentTeamActionStatus.BLOCKED,
                        target_actor_id=old_actor.id,
                        before_revision=record.object_revision,
                        blocker_code="replacement_requires_new_actor_name",
                        next_action=(
                            "Choose a new stable actor_name and request a fresh plan"
                        ),
                    ),
                    False,
                )
            raise AgentTeamSetupConflictError(
                "agent_team_replacement_name_conflict",
                "Replacement actor name is already owned by another identity",
                actor_name=member.actor_name,
                actor_id=name_owner.id,
            )
        if not self.credential_sink.available:
            raise CredentialDeliveryError(
                "The approved credential sink is unavailable"
            )

        profile = await self._resolve_profile(member)
        entries = await self._catalog_entries(member)
        api_key = f"pmag_{secrets.token_urlsafe(32)}"
        replacement = AgentActor(
            name=member.actor_name,
            display_name=member.display_name,
            api_key_hash=hash_api_key(api_key),
            scopes=_canonical_json(
                list(ROLE_SCOPE_PRESETS[member.scope_preset])
            ),
            enabled=False,
            lifecycle_state="onboarding",
            role=member.role,
            profile_id=profile.id,
            work_policy="assigned_only",
            max_parallel_work=1,
            queue_revision=1,
        )
        self.db.add(replacement)
        await self.db.flush()

        old_actor_id = old_actor.id if old_actor is not None else None
        if old_actor is not None:
            old_actor.enabled = False
            old_actor.lifecycle_state = "disabled"
            old_actor.queue_revision += 1

        before_revision = record.object_revision
        record.actor = replacement
        record.actor_id = replacement.id
        record.object_revision += 1
        record.lifecycle_state = "configured"
        record.credential_delivery_state = "pending"
        record.credential_delivery_receipt_digest = None
        record.handoff_digest = None
        record.runtime_acknowledgement_digest = None
        record.runtime_acknowledgement_payload = None
        record.runtime_acknowledged_at = None
        record.ack_attempt_count = 0
        record.ack_window_started_at = None
        self._set_member_contract(record, member)
        await self._reconcile_bindings(
            topology=topology,
            actor=replacement,
            member=member,
            entries=entries,
            allow_binding_replacement=True,
        )
        await self._upsert_managed_object(
            topology=topology,
            object_type="profile",
            logical_key=member.profile_key,
            object_id=profile.id,
            object_revision=1,
            desired_digest=_digest(
                {
                    "profile_key": member.profile_key,
                    "assignment_modes": list(member.assignment_modes),
                }
            ),
        )
        if member.role == "pm":
            topology.primary_actor_id = replacement.id
        elif topology.primary_actor_id == old_actor_id:
            topology.primary_actor_id = None
        topology.state = "onboarding"
        await self.db.commit()

        try:
            receipt_digest = await self.credential_sink.deliver(
                credential_ref=member.credential_ref,
                actor_key=member.actor_key,
                actor_name=member.actor_name,
                api_key=api_key,
            )
        except Exception:
            record = await self._member_record(
                topology.id,
                member.actor_key,
                for_update=True,
            )
            assert record is not None and record.actor is not None
            record.credential_delivery_state = "uncertain"
            record.lifecycle_state = "disabled"
            record.object_revision += 1
            record.actor.enabled = False
            record.actor.lifecycle_state = "disabled"
            record.actor.queue_revision += 1
            current_topology = await self._topology(
                topology.topology_key,
                for_update=True,
            )
            assert current_topology is not None
            current_topology.state = "blocked"
            current_topology.blocker_codes = _canonical_json(
                ["credential_delivery_uncertain"]
            )
            await self._stage_event(
                event_type="agent.team_setup_action",
                actor_id=(
                    run.principal_actor_id
                    if run.principal_actor_id
                    else None
                ),
                correlation_id=run.correlation_id,
                idempotency_key=run.idempotency_key,
                payload={
                    "action_id": action.action_id,
                    "actor_key": member.actor_key,
                    "operation": "replace_member",
                    "status": "blocked",
                    "blocker_code": "credential_delivery_uncertain",
                    "topology_key": current_topology.topology_key,
                    "replaced_actor_id": old_actor_id,
                    "target_actor_id": record.actor_id,
                },
            )
            await self.db.commit()
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=member.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=record.actor_id,
                    before_revision=before_revision,
                    after_revision=record.object_revision,
                    blocker_code="credential_delivery_uncertain",
                    next_action=(
                        "Approve an explicit credential recovery or rotation"
                    ),
                ),
                True,
            )

        record = await self._member_record(
            topology.id,
            member.actor_key,
            for_update=True,
        )
        assert record is not None
        record.credential_delivery_state = "delivered"
        record.credential_delivery_receipt_digest = receipt_digest
        record.lifecycle_state = "onboarding"
        record.object_revision += 1
        await self._stage_event(
            event_type="agent.team_setup_action",
            actor_id=run.principal_actor_id if run.principal_actor_id else None,
            correlation_id=run.correlation_id,
            idempotency_key=run.idempotency_key,
            payload={
                "action_id": action.action_id,
                "actor_key": member.actor_key,
                "operation": "replace_member",
                "status": "applied",
                "topology_key": topology.topology_key,
                "replaced_actor_id": old_actor_id,
                "target_actor_id": record.actor_id,
                "object_revision": record.object_revision,
            },
        )
        await self.db.commit()
        return (
            AgentTeamActionReceipt(
                action_id=action.action_id,
                action_digest=action.action_digest,
                reconciliation_class=action.reconciliation_class,
                operation=action.operation,
                actor_key=member.actor_key,
                status=AgentTeamActionStatus.APPLIED,
                target_actor_id=record.actor_id,
                before_revision=before_revision,
                after_revision=record.object_revision,
                next_action="Start the replacement runtime and acknowledge its handoff",
            ),
            True,
        )

    async def _apply_replace_recovery(
        self,
        *,
        topology: AgentTeamTopology,
        member: AgentTeamMemberSpec,
        action: AgentTeamPlanAction,
        run: AgentTeamApplyRun,
    ) -> tuple[AgentTeamActionReceipt, bool]:
        record = await self._member_record(
            topology.id,
            member.actor_key,
            for_update=True,
        )
        if (
            record is None
            or record.actor is None
            or record.credential_delivery_state
            not in {"pending", "uncertain"}
            or action.blocker_code != "credential_delivery_uncertain"
        ):
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=action.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=action.target_actor_id,
                    before_revision=action.expected_object_revision,
                    blocker_code=action.blocker_code or "replacement_requires_operator",
                    next_action="Resolve identity replacement outside setup apply",
                ),
                False,
            )
        try:
            stored_member = AgentTeamMemberSpec.model_validate_json(
                record.desired_member_payload
            )
        except ValueError as exc:
            raise AgentTeamSetupConflictError(
                "agent_team_stored_member_invalid",
                "Stored agent-team member contract is invalid",
                actor_key=member.actor_key,
            ) from exc
        if member.credential_ref == record.credential_ref:
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=member.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=record.actor_id,
                    before_revision=record.object_revision,
                    blocker_code="credential_recovery_requires_new_reference",
                    next_action=(
                        "Choose a new credential_ref and request a fresh plan"
                    ),
                ),
                False,
            )
        if stored_member.model_copy(
            update={"credential_ref": member.credential_ref}
        ) != member:
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=member.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=record.actor_id,
                    before_revision=record.object_revision,
                    blocker_code="credential_recovery_change_not_isolated",
                    next_action=(
                        "Change only credential_ref for recovery, then reconcile "
                        "other drift with a fresh plan"
                    ),
                ),
                False,
            )
        if not self.credential_sink.available:
            raise CredentialDeliveryError("Credential sink is unavailable")
        actor = record.actor
        if (
            action.expected_actor_revision is not None
            and actor.queue_revision != action.expected_actor_revision
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_actor_revision_conflict",
                "Actor changed before credential recovery",
            )
        api_key = f"pmag_{secrets.token_urlsafe(32)}"
        actor.api_key_hash = hash_api_key(api_key)
        actor.enabled = False
        actor.lifecycle_state = "onboarding"
        actor.queue_revision += 1
        record.credential_delivery_state = "pending"
        record.lifecycle_state = "configured"
        record.object_revision += 1
        self._set_member_contract(record, member)
        await self.db.commit()
        try:
            receipt_digest = await self.credential_sink.deliver(
                credential_ref=member.credential_ref,
                actor_key=member.actor_key,
                actor_name=member.actor_name,
                api_key=api_key,
            )
        except Exception as exc:
            record = await self._member_record(
                topology.id,
                member.actor_key,
                for_update=True,
            )
            assert record is not None and record.actor is not None
            record.credential_delivery_state = "uncertain"
            record.lifecycle_state = "disabled"
            record.actor.lifecycle_state = "disabled"
            record.object_revision += 1
            await self.db.commit()
            raise CredentialDeliveryError(
                "Credential recovery delivery remains uncertain"
            ) from exc
        record = await self._member_record(
            topology.id,
            member.actor_key,
            for_update=True,
        )
        assert record is not None
        record.credential_delivery_state = "delivered"
        record.credential_delivery_receipt_digest = receipt_digest
        record.lifecycle_state = "onboarding"
        record.object_revision += 1
        await self._stage_event(
            event_type="agent.team_setup_credential_recovered",
            actor_id=run.principal_actor_id if run.principal_actor_id else None,
            correlation_id=run.correlation_id,
            idempotency_key=run.idempotency_key,
            payload={
                "action_id": action.action_id,
                "actor_key": member.actor_key,
                "topology_key": topology.topology_key,
                "credential_delivery_state": "delivered",
            },
        )
        await self.db.commit()
        return (
            AgentTeamActionReceipt(
                action_id=action.action_id,
                action_digest=action.action_digest,
                reconciliation_class=action.reconciliation_class,
                operation=action.operation,
                actor_key=member.actor_key,
                status=AgentTeamActionStatus.APPLIED,
                target_actor_id=record.actor_id,
                before_revision=action.expected_object_revision,
                after_revision=record.object_revision,
                next_action="Restart the runtime and acknowledge the new handoff",
            ),
            True,
        )

    async def _apply_disable(
        self,
        *,
        topology: AgentTeamTopology,
        action: AgentTeamPlanAction,
        run: AgentTeamApplyRun,
    ) -> tuple[AgentTeamActionReceipt, bool]:
        record = await self._member_record(
            topology.id,
            action.actor_key,
            for_update=True,
        )
        if record is None:
            raise AgentTeamSetupConflictError(
                "agent_team_action_stale",
                "Managed member no longer exists",
                action_id=action.action_id,
            )
        if (
            action.expected_object_revision is not None
            and record.object_revision != action.expected_object_revision
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_member_revision_conflict",
                "Managed member changed before disable",
            )
        before_revision = record.object_revision
        record.lifecycle_state = "disabled"
        record.object_revision += 1
        if record.actor is not None:
            record.actor.enabled = False
            record.actor.lifecycle_state = "disabled"
            record.actor.queue_revision += 1
        if topology.primary_actor_id == record.actor_id:
            topology.primary_actor_id = None
        await self._stage_event(
            event_type="agent.team_setup_action",
            actor_id=run.principal_actor_id if run.principal_actor_id else None,
            correlation_id=run.correlation_id,
            idempotency_key=run.idempotency_key,
            payload={
                "action_id": action.action_id,
                "actor_key": action.actor_key,
                "operation": "disable_member",
                "status": "applied",
                "topology_key": topology.topology_key,
            },
        )
        await self.db.commit()
        return (
            AgentTeamActionReceipt(
                action_id=action.action_id,
                action_digest=action.action_digest,
                reconciliation_class=action.reconciliation_class,
                operation=action.operation,
                actor_key=action.actor_key,
                status=AgentTeamActionStatus.APPLIED,
                target_actor_id=record.actor_id,
                before_revision=before_revision,
                after_revision=record.object_revision,
                next_action="Review replacement or rollback before re-enabling",
            ),
            True,
        )

    async def _record_action_receipt(
        self,
        run: AgentTeamApplyRun,
        receipt: AgentTeamActionReceipt,
    ) -> None:
        self.db.add(
            AgentTeamActionReceiptRecord(
                apply_run_id=run.id,
                action_id=receipt.action_id,
                action_digest=receipt.action_digest,
                reconciliation_class=receipt.reconciliation_class.value,
                operation=receipt.operation,
                actor_key=receipt.actor_key,
                status=receipt.status.value,
                target_actor_id=receipt.target_actor_id,
                before_revision=receipt.before_revision,
                after_revision=receipt.after_revision,
                blocker_code=receipt.blocker_code,
                next_action=receipt.next_action,
                result_payload=_canonical_json(
                    receipt.model_dump(mode="json")
                ),
            )
        )
        await self.db.commit()

    async def _execute_action(
        self,
        *,
        manifest: AgentTeamMaster,
        action: AgentTeamPlanAction,
        run: AgentTeamApplyRun,
        confirmed_action_ids: set[str],
    ) -> tuple[AgentTeamActionReceipt, bool, bool]:
        if (
            action.requires_explicit_confirmation
            and action.action_id not in confirmed_action_ids
        ):
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=action.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=action.target_actor_id,
                    before_revision=action.expected_object_revision,
                    blocker_code="explicit_confirmation_required",
                    next_action="Confirm this exact current action ID",
                ),
                False,
                True,
            )
        if action.reconciliation_class in {
            AgentTeamReconciliationClass.BLOCKED_CONFLICT,
            AgentTeamReconciliationClass.UNMANAGED,
        }:
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=action.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=action.target_actor_id,
                    before_revision=action.expected_object_revision,
                    blocker_code=action.blocker_code or "action_blocked",
                    next_action="Resolve the conflict and request a fresh plan",
                ),
                False,
                True,
            )
        if action.reconciliation_class == AgentTeamReconciliationClass.NO_CHANGE:
            return (
                AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=action.actor_key,
                    status=AgentTeamActionStatus.NO_CHANGE,
                    target_actor_id=action.target_actor_id,
                    before_revision=action.expected_object_revision,
                    after_revision=action.expected_object_revision,
                    next_action="No operator action is required",
                ),
                False,
                False,
            )

        topology, created = await self._ensure_topology_for_apply(
            manifest,
            run,
        )
        desired = next(
            (
                member
                for member in manifest.all_members
                if member.actor_key == action.actor_key
            ),
            None,
        )
        if action.operation in {
            "create_member",
            "adopt_member",
            "update_member",
        }:
            if desired is None:
                raise AgentTeamSetupConflictError(
                    "agent_team_action_stale",
                    "Approved action is not present in the manifest",
                )
            receipt, mutated = await self._apply_create_or_update(
                topology=topology,
                member=desired,
                action=action,
                run=run,
            )
            return receipt, mutated or created, receipt.status == AgentTeamActionStatus.BLOCKED
        if action.operation == "replace_member":
            if desired is None:
                raise AgentTeamSetupConflictError(
                    "agent_team_action_stale",
                    "Replacement target is not present in the manifest",
                )
            if action.blocker_code == "credential_delivery_uncertain":
                receipt, mutated = await self._apply_replace_recovery(
                    topology=topology,
                    member=desired,
                    action=action,
                    run=run,
                )
            else:
                receipt, mutated = await self._apply_identity_replacement(
                    topology=topology,
                    member=desired,
                    action=action,
                    run=run,
                )
            return receipt, mutated or created, receipt.status == AgentTeamActionStatus.BLOCKED
        if action.operation == "disable_member":
            receipt, mutated = await self._apply_disable(
                topology=topology,
                action=action,
                run=run,
            )
            return receipt, mutated or created, False
        raise AgentTeamSetupConflictError(
            "agent_team_action_unsupported",
            "Approved setup action is not supported",
            action_id=action.action_id,
        )

    async def _profile_revision(
        self,
        actor: AgentActor,
    ) -> str:
        if actor.profile is None:
            return "missing"
        profile = actor.profile
        skills = sorted(
            profile.skills,
            key=lambda item: (item.skill_key, item.id),
        )
        revision_payload = {
            "profile_id": profile.id,
            "updated_at": profile.updated_at.isoformat(),
            "automation_enabled": profile.automation_enabled,
            "profile_kind": profile.profile_kind,
            "assignment_modes": sorted(profile.assignment_modes or []),
            "skills": [
                {
                    "id": skill.id,
                    "key": skill.skill_key,
                    "level": skill.level,
                    "interest": skill.interest,
                    "weakness": skill.is_weakness,
                    "updated_at": skill.updated_at.isoformat(),
                }
                for skill in skills
            ],
        }
        digest = hashlib.sha256(
            json.dumps(
                revision_payload,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()[:24]
        return f"p{profile.id}-{digest}"

    async def _binding_revisions(
        self,
        actor: AgentActor,
    ) -> dict[str, int]:
        result = await self.db.execute(
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .where(
                AgentModelBinding.actor_id == actor.id,
                AgentModelBinding.enabled.is_(True),
            )
        )
        return dict(
            sorted(
                (
                    binding.model_catalog.key,
                    binding.revision,
                )
                for binding in result.scalars()
                if binding.model_catalog is not None
                and binding.model_catalog.enabled
            )
        )

    async def _handoff(
        self,
        *,
        topology: AgentTeamTopology,
        manifest: AgentTeamMaster,
        member_record: AgentTeamTopologyMember,
        member: AgentTeamMemberSpec,
    ) -> AgentTeamRuntimeHandoff | None:
        actor = member_record.actor
        if actor is None:
            return None
        return AgentTeamRuntimeHandoff(
            topology_key=topology.topology_key,
            topology_revision=topology.revision,
            actor_key=member.actor_key,
            actor_id=actor.id,
            role=member.role,
            server_url=manifest.server_url,
            required_server_features=manifest.required_server_features,
            skill_package=member.skill_package,
            profile_key=member.profile_key,
            profile_revision=await self._profile_revision(actor),
            model_binding_revisions=await self._binding_revisions(actor),
            supported_assignment_modes=member.assignment_modes,
            startup_instructions=(
                "Load the exact immutable role package and verify its checksum.",
                "Resolve credential_ref through the runtime secret store.",
                "Send one restricted onboarding acknowledgement before normal work.",
                "Re-read capabilities and topology status after acknowledgement.",
            ),
            credential_ref=member.credential_ref,
        )

    async def _refresh_handoffs(
        self,
        topology: AgentTeamTopology,
        manifest: AgentTeamMaster,
    ) -> None:
        for member in manifest.all_members:
            record = await self._member_record(topology.id, member.actor_key)
            if record is None:
                continue
            handoff = await self._handoff(
                topology=topology,
                manifest=manifest,
                member_record=record,
                member=member,
            )
            record.handoff_digest = (
                _digest(handoff.model_dump(mode="json"))
                if handoff is not None
                else None
            )

    async def apply(
        self,
        actor: AgentActor,
        request: AgentTeamApplyRequest,
        *,
        command: AgentPlanningCommandContext,
    ) -> AgentTeamApplyResponse:
        """Apply only exact approved action IDs and persist resumable receipts."""

        self._require_operator(actor)
        idempotency_key = validate_idempotency_key(
            command.idempotency_key,
            required=True,
        )
        assert idempotency_key is not None
        manifest = parse_agent_team_master(request.manifest)
        principal_key = self._principal_key(actor)
        request_digest = self._apply_request_digest(request, command)
        existing_run = await self._find_apply_run(
            principal_key=principal_key,
            idempotency_key=idempotency_key,
        )
        if existing_run is not None:
            replay = await self._replay_apply(
                existing_run,
                request_digest=request_digest,
            )
            if replay is not None:
                return replay
            run = existing_run
            plan = AgentTeamReconciliationPlan.model_validate_json(
                run.plan_payload
            )
        else:
            plan = await self.plan(
                actor,
                AgentTeamPlanRequest(
                    manifest=manifest,
                    expected_topology_revision=(
                        request.expected_topology_revision
                    ),
                ),
            )
            if not secrets.compare_digest(plan.plan_digest, request.plan_digest):
                raise AgentTeamSetupConflictError(
                    "agent_team_plan_digest_conflict",
                    "Plan digest is stale or does not match current server actions",
                    current_plan_digest=plan.plan_digest,
                )
            action_ids = {action.action_id for action in plan.actions}
            unknown = sorted(set(request.approved_action_ids) - action_ids)
            if unknown:
                raise AgentTeamSetupConflictError(
                    "agent_team_unknown_action",
                    "Approved action IDs are not in the current plan",
                    unknown_action_ids=unknown,
                )
            run = AgentTeamApplyRun(
                apply_id=secrets.token_hex(16),
                topology_key=manifest.topology_key,
                principal_key=principal_key,
                principal_actor_id=actor.id if actor.id > 0 else None,
                idempotency_key=idempotency_key,
                request_digest=request_digest,
                manifest_digest=manifest.digest(),
                plan_digest=plan.plan_digest,
                expected_topology_revision=request.expected_topology_revision,
                resulting_topology_revision=request.expected_topology_revision,
                approved_action_ids=_canonical_json(
                    list(request.approved_action_ids)
                ),
                confirmed_action_ids=_canonical_json(
                    list(request.confirmed_action_ids)
                ),
                plan_payload=_canonical_json(plan.model_dump(mode="json")),
                rationale=command.rationale,
                correlation_id=command.correlation_id,
                status="running",
                blocker_codes="[]",
                action_receipts=[],
            )
            self.db.add(run)
            try:
                await self.db.commit()
            except IntegrityError:
                await self.db.rollback()
                concurrent = await self._find_apply_run(
                    principal_key=principal_key,
                    idempotency_key=idempotency_key,
                )
                if concurrent is None:
                    raise
                replay = await self._replay_apply(
                    concurrent,
                    request_digest=request_digest,
                )
                if replay is not None:
                    return replay
                run = concurrent
                plan = AgentTeamReconciliationPlan.model_validate_json(
                    run.plan_payload
                )

        approved = set(_json_loads(run.approved_action_ids, []))
        confirmed = set(_json_loads(run.confirmed_action_ids, []))
        completed_ids = {receipt.action_id for receipt in run.action_receipts}
        mutated = False
        blocked = False
        receipts = [
            self._receipt_from_record(record)
            for record in run.action_receipts
        ]
        actions_by_id = {action.action_id: action for action in plan.actions}
        for action_id in sorted(
            approved,
            key=lambda value: (
                {
                    "create_member": 0,
                    "adopt_member": 1,
                    "update_member": 2,
                    "replace_member": 3,
                    "disable_member": 4,
                    "no_change": 5,
                }.get(actions_by_id[value].operation, 9),
                value,
            ),
        ):
            if action_id in completed_ids:
                continue
            action = actions_by_id[action_id]
            try:
                receipt, action_mutated, action_blocked = (
                    await self._execute_action(
                        manifest=manifest,
                        action=action,
                        run=run,
                        confirmed_action_ids=confirmed,
                    )
                )
            except CredentialDeliveryError:
                receipt = AgentTeamActionReceipt(
                    action_id=action.action_id,
                    action_digest=action.action_digest,
                    reconciliation_class=action.reconciliation_class,
                    operation=action.operation,
                    actor_key=action.actor_key,
                    status=AgentTeamActionStatus.BLOCKED,
                    target_actor_id=action.target_actor_id,
                    before_revision=action.expected_object_revision,
                    blocker_code="credential_delivery_uncertain",
                    next_action="Approve explicit credential recovery or rotation",
                )
                action_mutated = True
                action_blocked = True
            await self._record_action_receipt(run, receipt)
            receipts.append(receipt)
            mutated = mutated or action_mutated
            blocked = blocked or action_blocked

        topology = await self._topology(
            manifest.topology_key,
            for_update=True,
            load_members=True,
        )
        resulting_revision = request.expected_topology_revision
        if topology is not None:
            if (
                mutated
                and request.expected_topology_revision > 0
                and topology.revision == request.expected_topology_revision
            ):
                topology.revision += 1
            topology.manifest_digest = manifest.digest()
            topology.manifest_payload = _canonical_json(
                manifest.model_dump(mode="json")
            )
            resulting_revision = topology.revision
            await self._refresh_handoffs(topology, manifest)
            status = await self._status_for_topology(
                topology,
                can_mutate=True,
                persist_state=False,
            )
            topology.state = (
                "runtime_ready"
                if status.runtime_ready
                else "blocked"
                if status.blocker_codes
                else "onboarding"
            )
            topology.blocker_codes = _canonical_json(
                list(status.blocker_codes)
            )
        pending = tuple(
            sorted(
                action.action_id
                for action in plan.actions
                if action.action_id not in approved
                and action.reconciliation_class
                not in {
                    AgentTeamReconciliationClass.NO_CHANGE,
                    AgentTeamReconciliationClass.UNMANAGED,
                }
            )
        )
        blocker_codes = tuple(
            sorted(
                {
                    receipt.blocker_code
                    for receipt in receipts
                    if receipt.blocker_code
                }
            )
        )
        response_status = (
            "blocked"
            if blocked
            else "partial"
            if pending
            else "completed"
        )
        response = AgentTeamApplyResponse(
            apply_id=run.apply_id,
            topology_key=manifest.topology_key,
            manifest_digest=manifest.digest(),
            plan_digest=plan.plan_digest,
            expected_topology_revision=request.expected_topology_revision,
            resulting_topology_revision=resulting_revision,
            status=response_status,
            receipts=tuple(receipts),
            pending_action_ids=pending,
            blocker_codes=blocker_codes,
        )
        run = await self.db.get(AgentTeamApplyRun, run.id)
        assert run is not None
        run.topology_id = topology.id if topology is not None else None
        run.resulting_topology_revision = resulting_revision
        run.status = response_status
        run.blocker_codes = _canonical_json(list(blocker_codes))
        run.response_payload = _canonical_json(response.model_dump(mode="json"))
        await self.db.commit()
        return response

    async def _select_status_topology(
        self,
        actor: AgentActor,
        topology_key: str | None,
    ) -> tuple[AgentTeamTopology | None, bool]:
        if "admin" in actor_scopes(actor):
            if topology_key is not None:
                return (
                    await self._topology(topology_key, load_members=True),
                    True,
                )
            result = await self.db.execute(
                select(AgentTeamTopology.topology_key).order_by(
                    AgentTeamTopology.id
                )
            )
            first = result.scalars().first()
            return (
                await self._topology(first, load_members=True)
                if first is not None
                else None,
                True,
            )
        require_scope(actor, "planning:read")
        result = await self.db.execute(
            select(AgentTeamTopology.topology_key)
            .join(
                AgentTeamTopologyMember,
                AgentTeamTopologyMember.topology_id
                == AgentTeamTopology.id,
            )
            .where(
                AgentTeamTopologyMember.actor_id == actor.id,
                AgentTeamTopologyMember.role == "pm",
                AgentTeamTopology.state != "disabled",
            )
        )
        bound_key = result.scalar_one_or_none()
        if bound_key is None:
            raise AgentPermissionError(
                "Only a topology-bound PM may read agent-team status"
            )
        if topology_key is not None and topology_key != bound_key:
            raise AgentPermissionError(
                "PM status reads are restricted to the bound topology"
            )
        return await self._topology(bound_key, load_members=True), False

    @staticmethod
    def _absent_steps() -> tuple[AgentTeamSetupStep, ...]:
        return (
            AgentTeamSetupStep(
                id="authority",
                state="todo",
                blocker_codes=("operator_authority_required",),
                next_action="Authenticate as an operator",
            ),
            AgentTeamSetupStep(
                id="master",
                state="todo",
                blocker_codes=("master_not_applied",),
                next_action="Import or select an agent-team master",
            ),
            AgentTeamSetupStep(
                id="controller",
                state="blocked",
                blocker_codes=("master_not_applied",),
            ),
            AgentTeamSetupStep(
                id="workers",
                state="blocked",
                blocker_codes=("master_not_applied",),
            ),
            AgentTeamSetupStep(
                id="bindings",
                state="blocked",
                blocker_codes=("master_not_applied",),
            ),
            AgentTeamSetupStep(
                id="verifier",
                state="blocked",
                blocker_codes=("master_not_applied",),
            ),
            AgentTeamSetupStep(
                id="review",
                state="blocked",
                blocker_codes=("topology_not_runtime_ready",),
            ),
        )

    async def status(
        self,
        actor: AgentActor,
        *,
        topology_key: str | None = None,
    ) -> AgentTeamStatusResponse:
        """Return backend-derived secret-free setup and runtime readiness."""

        topology, can_mutate = await self._select_status_topology(
            actor,
            topology_key,
        )
        if topology is None:
            return AgentTeamStatusResponse(
                topology_state="absent",
                runtime_ready=False,
                blocker_codes=("topology_not_configured",),
                steps=self._absent_steps(),
                can_mutate=can_mutate,
                next_action="Validate and plan an agent-team master",
            )
        return await self._status_for_topology(
            topology,
            can_mutate=can_mutate,
            persist_state=False,
        )

    async def report(
        self,
        actor: AgentActor,
        *,
        topology_key: str | None = None,
    ) -> AgentTeamSetupReport:
        """Return a bounded redacted report without availability overclaims."""

        topology, can_mutate = await self._select_status_topology(
            actor,
            topology_key,
        )
        if topology is None:
            status = AgentTeamStatusResponse(
                topology_state="absent",
                runtime_ready=False,
                blocker_codes=("topology_not_configured",),
                steps=self._absent_steps(),
                can_mutate=can_mutate,
                next_action="Validate and plan an agent-team master",
            )
            apply_runs: tuple[AgentTeamApplyRun, ...] = ()
        else:
            status = await self._status_for_topology(
                topology,
                can_mutate=can_mutate,
                persist_state=False,
            )
            apply_runs = tuple(topology.apply_runs)

        redacted_status = status.model_dump(mode="json")
        for member in redacted_status["members"]:
            member.pop("handoff", None)
        redacted_status.pop("can_mutate", None)
        redacted_status.pop("next_action", None)
        latest_apply = max(
            apply_runs,
            key=lambda item: (item.created_at, item.id),
            default=None,
        )
        members = status.members
        counts = AgentTeamSetupReportCounts(
            desired=len(members),
            configured=sum(member.configured for member in members),
            credential_delivered=sum(
                member.credential_delivery_state
                in {"delivered", "not_required"}
                for member in members
            ),
            onboarding=sum(
                member.lifecycle_state
                == AgentTeamMemberLifecycle.ONBOARDING
                for member in members
            ),
            connected=sum(
                member.connection_state == "observed" for member in members
            ),
            runtime_ready=sum(member.runtime_ready for member in members),
            blocked=sum(not member.runtime_ready for member in members),
            disabled=sum(
                member.lifecycle_state == AgentTeamMemberLifecycle.DISABLED
                for member in members
            ),
            queued_assignments=sum(
                member.queued_assignments or 0 for member in members
            ),
            accepted_assignments=sum(
                member.accepted_assignments or 0 for member in members
            ),
            running_runs=sum(member.running_runs or 0 for member in members),
        )
        report = AgentTeamSetupReport(
            generated_at=utc_now(),
            topology_key=status.topology_key,
            topology_revision=status.topology_revision,
            manifest_digest=status.manifest_digest,
            topology_state=status.topology_state,
            runtime_ready=status.runtime_ready,
            status_digest=_digest(redacted_status),
            counts=counts,
            evidence=AgentTeamSetupReportEvidence(
                apply_runs=len(apply_runs),
                action_receipts=sum(
                    len(run.action_receipts) for run in apply_runs
                ),
                latest_apply_id=(
                    latest_apply.apply_id if latest_apply is not None else None
                ),
                latest_apply_status=(
                    latest_apply.status if latest_apply is not None else None
                ),
                pending_actions=len(status.pending_action_ids),
            ),
            dispatch_context=AgentTeamDispatchAvailability(),
            blocker_codes=status.blocker_codes,
        )
        ensure_agent_team_secret_free(report.model_dump(mode="json"))
        return report

    async def _status_for_topology(
        self,
        topology: AgentTeamTopology,
        *,
        can_mutate: bool,
        persist_state: bool,
    ) -> AgentTeamStatusResponse:
        try:
            manifest = AgentTeamMaster.model_validate_json(
                topology.manifest_payload
            )
        except ValueError as exc:
            raise AgentTeamSetupConflictError(
                "agent_team_stored_manifest_invalid",
                "Stored agent-team manifest is invalid",
                topology_key=topology.topology_key,
            ) from exc
        records = {member.actor_key: member for member in topology.members}
        now = utc_now()
        member_statuses: list[AgentTeamMemberStatus] = []
        desired_by_key = {
            member.actor_key: member for member in manifest.all_members
        }
        actor_ids = tuple(
            member.actor_id
            for member in topology.members
            if member.actor_id is not None
        )
        assignment_counts: dict[int, dict[str, int]] = {}
        running_counts: dict[int, int] = {}
        if actor_ids:
            assignment_rows = await self.db.execute(
                select(
                    AgentTaskAssignment.actor_id,
                    AgentTaskAssignment.state,
                    func.count(AgentTaskAssignment.id),
                )
                .where(
                    AgentTaskAssignment.actor_id.in_(actor_ids),
                    AgentTaskAssignment.state.in_(("queued", "accepted")),
                )
                .group_by(
                    AgentTaskAssignment.actor_id,
                    AgentTaskAssignment.state,
                )
            )
            for actor_id, state, count in assignment_rows:
                assignment_counts.setdefault(actor_id, {})[state] = count
            run_rows = await self.db.execute(
                select(AgentRun.actor_id, func.count(AgentRun.id))
                .where(
                    AgentRun.actor_id.in_(actor_ids),
                    AgentRun.status == "running",
                )
                .group_by(AgentRun.actor_id)
            )
            running_counts = {
                actor_id: count for actor_id, count in run_rows
            }
        runtime_ready_by_role = {"pm": 0, "worker": 0, "verifier": 0}
        all_binding_ready = True

        for desired in manifest.all_members:
            record = records.get(desired.actor_key)
            actor = record.actor if record is not None else None
            blockers: set[str] = set()
            profile_revision: str | None = None
            binding_revisions: dict[str, int] = {}
            connection_state = "unobserved"
            package_acknowledged = False
            handoff = None
            lifecycle = (
                AgentTeamMemberLifecycle(record.lifecycle_state)
                if record is not None
                else AgentTeamMemberLifecycle.DESIRED
            )
            credential_state = (
                record.credential_delivery_state
                if record is not None
                else "pending"
            )
            if record is None or actor is None:
                blockers.add("member_not_configured")
            else:
                profile_revision = await self._profile_revision(actor)
                binding_revisions = await self._binding_revisions(actor)
                handoff = await self._handoff(
                    topology=topology,
                    manifest=manifest,
                    member_record=record,
                    member=desired,
                )
                if actor.role != desired.role:
                    blockers.add("actor_role_mismatch")
                if set(actor_scopes(actor)) != set(
                    ROLE_SCOPE_PRESETS[desired.scope_preset]
                ):
                    blockers.add("actor_scope_mismatch")
                if actor.profile is None or actor.profile.seed_key != desired.profile_key:
                    blockers.add("actor_profile_mismatch")
                missing_bindings = set(desired.model_binding_keys).difference(
                    binding_revisions
                )
                if missing_bindings:
                    blockers.add("model_binding_missing_or_disabled")
                default_binding = next(
                    (
                        binding
                        for binding in actor.model_bindings
                        if binding.is_default
                        and binding.enabled
                        and binding.model_catalog is not None
                        and binding.model_catalog.enabled
                    ),
                    None,
                )
                if (
                    default_binding is None
                    or default_binding.model_catalog.key
                    != desired.default_model_binding_key
                ):
                    blockers.add("default_model_binding_mismatch")
                ack_payload = _json_loads(
                    record.runtime_acknowledgement_payload,
                    {},
                )
                package_acknowledged = (
                    isinstance(ack_payload, dict)
                    and ack_payload.get("skill_package")
                    == desired.skill_package.model_dump(mode="json")
                )
                if not package_acknowledged:
                    blockers.add("role_package_not_acknowledged")
                if credential_state not in {"delivered", "not_required"}:
                    blockers.add(
                        "credential_delivery_uncertain"
                        if credential_state == "uncertain"
                        else "credential_not_delivered"
                    )
                if actor.last_seen_at is None:
                    connection_state = "unobserved"
                    blockers.add("runtime_unobserved")
                elif (
                    as_utc(now) - as_utc(actor.last_seen_at)
                    > timedelta(
                        seconds=(
                            manifest.readiness_policy
                            .maximum_runtime_staleness_seconds
                        )
                    )
                ):
                    connection_state = "stale"
                    blockers.add("runtime_stale")
                else:
                    connection_state = "observed"
                if not actor.enabled or actor.lifecycle_state != "active":
                    blockers.add("actor_not_active")

            runtime_ready = (
                record is not None
                and actor is not None
                and lifecycle == AgentTeamMemberLifecycle.RUNTIME_READY
                and not blockers
            )
            if runtime_ready:
                runtime_ready_by_role[desired.role] += 1
            if any(
                "binding" in code
                or code == "role_package_not_acknowledged"
                or code
                in {
                    "member_not_configured",
                    "actor_profile_mismatch",
                }
                for code in blockers
            ):
                all_binding_ready = False
            member_statuses.append(
                AgentTeamMemberStatus(
                    actor_key=desired.actor_key,
                    actor_id=actor.id if actor is not None else None,
                    actor_name=desired.actor_name,
                    display_name=desired.display_name,
                    role=desired.role,
                    desired=True,
                    configured=record is not None and actor is not None,
                    lifecycle_state=lifecycle,
                    enabled=bool(actor and actor.enabled),
                    profile_key=desired.profile_key,
                    profile_revision=profile_revision,
                    binding_revisions=binding_revisions,
                    skill_package=desired.skill_package,
                    package_acknowledged=package_acknowledged,
                    credential_delivery_state=credential_state,
                    connection_state=connection_state,
                    last_seen_at=actor.last_seen_at if actor else None,
                    queued_assignments=(
                        assignment_counts.get(actor.id, {}).get("queued", 0)
                        if actor is not None
                        else None
                    ),
                    accepted_assignments=(
                        assignment_counts.get(actor.id, {}).get("accepted", 0)
                        if actor is not None
                        else None
                    ),
                    running_runs=(
                        running_counts.get(actor.id, 0)
                        if actor is not None
                        else None
                    ),
                    runtime_ready=runtime_ready,
                    blocker_codes=tuple(sorted(blockers)),
                    handoff=handoff,
                )
            )

        topology_blockers: set[str] = set()
        if runtime_ready_by_role["pm"] != 1:
            topology_blockers.add("primary_pm_not_runtime_ready")
        if (
            runtime_ready_by_role["worker"]
            < manifest.readiness_policy.minimum_execution_workers
        ):
            topology_blockers.add("minimum_workers_not_runtime_ready")
        if (
            manifest.readiness_policy.require_independent_verifier_when_assessed
            and runtime_ready_by_role["verifier"] < 1
        ):
            topology_blockers.add("independent_verifier_not_runtime_ready")
        if not all_binding_ready:
            topology_blockers.add("binding_or_package_drift")
        if any(
            member.credential_delivery_state == "uncertain"
            for member in member_statuses
        ):
            topology_blockers.add("credential_delivery_uncertain")
        if any(not member.runtime_ready for member in member_statuses):
            topology_blockers.add("declared_member_not_runtime_ready")
        runtime_ready = not topology_blockers and all(
            member.runtime_ready for member in member_statuses
        )

        latest_run = max(
            topology.apply_runs,
            key=lambda item: (item.created_at, item.id),
            default=None,
        )
        pending_action_ids = (
            AgentTeamApplyResponse.model_validate_json(
                latest_run.response_payload
            ).pending_action_ids
            if latest_run and latest_run.response_payload
            else ()
        )

        controller_blockers = tuple(
            sorted(
                {
                    code
                    for member in member_statuses
                    if member.role == "pm"
                    for code in member.blocker_codes
                }
            )
        )
        worker_blockers = tuple(
            sorted(
                {
                    code
                    for member in member_statuses
                    if member.role == "worker"
                    for code in member.blocker_codes
                }
            )
        )
        verifier_blockers = tuple(
            sorted(
                {
                    code
                    for member in member_statuses
                    if member.role == "verifier"
                    for code in member.blocker_codes
                }
            )
        )
        if (
            manifest.readiness_policy.require_independent_verifier_when_assessed
            and runtime_ready_by_role["verifier"] < 1
        ):
            verifier_blockers = tuple(
                sorted(
                    {
                        *verifier_blockers,
                        "independent_verifier_not_runtime_ready",
                    }
                )
            )
        steps = (
            AgentTeamSetupStep(
                id="authority",
                state="done",
                next_action=(
                    "Operator mutation controls are available"
                    if can_mutate
                    else "Read-only PM topology status"
                ),
            ),
            AgentTeamSetupStep(
                id="master",
                state="done",
                next_action="Reconcile a new manifest revision when desired state changes",
            ),
            AgentTeamSetupStep(
                id="controller",
                state="done" if not controller_blockers else "warn",
                blocker_codes=controller_blockers,
                next_action=(
                    None
                    if not controller_blockers
                    else "Complete the PM runtime handoff and acknowledgement"
                ),
            ),
            AgentTeamSetupStep(
                id="workers",
                state=(
                    "done"
                    if runtime_ready_by_role["worker"]
                    >= manifest.readiness_policy.minimum_execution_workers
                    else "warn"
                ),
                blocker_codes=worker_blockers,
                next_action=(
                    None
                    if not worker_blockers
                    else "Complete worker setup or reconcile drift"
                ),
            ),
            AgentTeamSetupStep(
                id="bindings",
                state="done" if all_binding_ready else "warn",
                blocker_codes=(
                    ()
                    if all_binding_ready
                    else ("binding_or_package_drift",)
                ),
                next_action=(
                    None
                    if all_binding_ready
                    else "Reconcile bindings, packages, and acknowledgements"
                ),
            ),
            AgentTeamSetupStep(
                id="verifier",
                state=(
                    "done"
                    if (
                        not manifest.readiness_policy
                        .require_independent_verifier_when_assessed
                        or runtime_ready_by_role["verifier"] >= 1
                    )
                    else "warn"
                ),
                blocker_codes=verifier_blockers,
                next_action=(
                    None
                    if not verifier_blockers
                    else "Complete independent verifier setup"
                ),
            ),
            AgentTeamSetupStep(
                id="review",
                state="done" if runtime_ready else "blocked",
                blocker_codes=tuple(sorted(topology_blockers)),
                next_action=(
                    "Topology is runtime ready"
                    if runtime_ready
                    else "Resolve server-derived blockers before rollout activation"
                ),
            ),
        )
        topology_state = (
            "disabled"
            if topology.state == "disabled"
            else "runtime_ready"
            if runtime_ready
            else "blocked"
            if topology_blockers
            else "onboarding"
        )
        if persist_state:
            topology.state = topology_state
            topology.blocker_codes = _canonical_json(
                list(sorted(topology_blockers))
            )
        return AgentTeamStatusResponse(
            topology_key=topology.topology_key,
            topology_revision=topology.revision,
            manifest_digest=topology.manifest_digest,
            topology_state=topology_state,
            runtime_ready=runtime_ready,
            blocker_codes=tuple(sorted(topology_blockers)),
            steps=steps,
            members=tuple(member_statuses),
            pending_action_ids=pending_action_ids,
            can_mutate=can_mutate,
            next_action=(
                "Model-aware routing may be enabled for new assignments"
                if runtime_ready
                else "Resume setup at the first warning or blocked step"
            ),
        )

    async def _increment_ack_attempt(
        self,
        member: AgentTeamTopologyMember,
    ) -> None:
        now = utc_now()
        if (
            member.ack_window_started_at is None
            or as_utc(now) - as_utc(member.ack_window_started_at)
            >= timedelta(seconds=ACK_WINDOW_SECONDS)
        ):
            member.ack_window_started_at = now
            member.ack_attempt_count = 0
        if member.ack_attempt_count >= ACK_ATTEMPT_LIMIT:
            raise AgentTeamSetupConflictError(
                "agent_team_ack_rate_limited",
                "Runtime acknowledgement attempt limit reached",
                retry_after_seconds=ACK_WINDOW_SECONDS,
            )
        member.ack_attempt_count += 1
        await self.db.commit()

    async def acknowledge_runtime(
        self,
        api_key: str,
        acknowledgement: AgentTeamRuntimeAcknowledgement,
    ) -> AgentTeamRuntimeAcknowledgementResponse:
        """Accept only the exact restricted onboarding handoff acknowledgement."""

        actor_service = AgentService(self.db)
        actor = await actor_service.authenticate_onboarding(api_key)
        if actor is None:
            actor = await actor_service.authenticate(api_key)
        if actor is None:
            raise AgentPermissionError(
                "Invalid setup onboarding credential"
            )
        result = await self.db.execute(
            select(AgentTeamTopologyMember)
            .options(
                selectinload(AgentTeamTopologyMember.topology)
                .selectinload(AgentTeamTopology.members)
                .selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.profile)
                .selectinload(TeamMemberProfile.skills),
                selectinload(AgentTeamTopologyMember.topology)
                .selectinload(AgentTeamTopology.members)
                .selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.model_bindings)
                .selectinload(AgentModelBinding.model_catalog),
                selectinload(AgentTeamTopologyMember.topology)
                .selectinload(AgentTeamTopology.apply_runs)
                .selectinload(AgentTeamApplyRun.action_receipts),
                selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.profile)
                .selectinload(TeamMemberProfile.skills),
                selectinload(AgentTeamTopologyMember.actor)
                .selectinload(AgentActor.model_bindings)
                .selectinload(AgentModelBinding.model_catalog),
            )
            .where(AgentTeamTopologyMember.actor_id == actor.id)
            .with_for_update()
        )
        member = result.scalar_one_or_none()
        if member is None:
            raise AgentPermissionError(
                "Onboarding identity is not bound to an agent-team topology"
            )
        await self._increment_ack_attempt(member)
        topology = member.topology
        if (
            topology.topology_key != acknowledgement.topology_key
            or topology.revision != acknowledgement.topology_revision
            or member.actor_key != acknowledgement.actor_key
            or member.role != acknowledgement.role
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_ack_identity_mismatch",
                "Acknowledgement does not match the exact current handoff",
            )
        desired = AgentTeamMemberSpec.model_validate_json(
            member.desired_member_payload
        )
        ack_digest = _digest(acknowledgement.model_dump(mode="json"))
        if member.runtime_acknowledgement_digest is not None:
            if secrets.compare_digest(
                member.runtime_acknowledgement_digest,
                ack_digest,
            ):
                status = await self._status_for_topology(
                    topology,
                    can_mutate=False,
                    persist_state=False,
                )
                return AgentTeamRuntimeAcknowledgementResponse(
                    topology_key=topology.topology_key,
                    topology_revision=topology.revision,
                    actor_key=member.actor_key,
                    actor_id=actor.id,
                    lifecycle_state=member.lifecycle_state,
                    acknowledgement_digest=ack_digest,
                    topology_runtime_ready=status.runtime_ready,
                    blocker_codes=status.blocker_codes,
                )
            raise AgentTeamSetupConflictError(
                "agent_team_ack_replay_conflict",
                "Runtime already acknowledged another handoff",
            )
        if acknowledgement.skill_package != desired.skill_package:
            raise AgentTeamSetupConflictError(
                "agent_team_ack_package_mismatch",
                "Runtime package identity does not match the handoff",
            )
        if not set(desired.assignment_modes).issubset(
            acknowledgement.supported_assignment_modes
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_ack_assignment_mode_mismatch",
                "Runtime does not support every assigned mode",
            )
        manifest = AgentTeamMaster.model_validate_json(topology.manifest_payload)
        if not set(manifest.required_server_features).issubset(
            acknowledgement.server_features
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_ack_feature_mismatch",
                "Runtime did not acknowledge required server features",
            )
        profile_revision = await self._profile_revision(actor)
        binding_revisions = await self._binding_revisions(actor)
        if (
            acknowledgement.profile_revision != profile_revision
            or acknowledgement.model_binding_revisions
            != binding_revisions
        ):
            raise AgentTeamSetupConflictError(
                "agent_team_ack_revision_mismatch",
                "Runtime acknowledgement uses stale profile or binding revisions",
            )
        if member.credential_delivery_state not in {
            "delivered",
            "not_required",
        }:
            raise AgentTeamSetupConflictError(
                "agent_team_ack_credential_state_invalid",
                "Credential delivery is not confirmed",
            )
        member.runtime_acknowledgement_digest = ack_digest
        member.runtime_acknowledgement_payload = _canonical_json(
            acknowledgement.model_dump(mode="json")
        )
        member.runtime_acknowledged_at = utc_now()
        member.lifecycle_state = "runtime_ready"
        member.object_revision += 1
        actor.enabled = True
        actor.lifecycle_state = "active"
        actor.last_seen_at = utc_now()
        actor.queue_revision += 1
        status = await self._status_for_topology(
            topology,
            can_mutate=False,
            persist_state=True,
        )
        await self._stage_event(
            event_type="agent.team_runtime_acknowledged",
            actor_id=actor.id,
            correlation_id=f"agent-team-ack:{topology.topology_key}",
            idempotency_key=None,
            payload={
                "topology_key": topology.topology_key,
                "topology_revision": topology.revision,
                "actor_key": member.actor_key,
                "actor_id": actor.id,
                "role": member.role,
                "acknowledgement_digest": ack_digest,
                "runtime_ready": True,
            },
        )
        await self.db.commit()
        return AgentTeamRuntimeAcknowledgementResponse(
            topology_key=topology.topology_key,
            topology_revision=topology.revision,
            actor_key=member.actor_key,
            actor_id=actor.id,
            lifecycle_state=member.lifecycle_state,
            acknowledgement_digest=ack_digest,
            topology_runtime_ready=status.runtime_ready,
            blocker_codes=status.blocker_codes,
        )

    async def membership_boundary(
        self,
        actor_id: int,
    ) -> AgentTeamMembershipBoundary | None:
        """Return the live, drift-aware topology boundary for one bound actor."""

        result = await self.db.execute(
            select(AgentTeamTopology.topology_key)
            .join(
                AgentTeamTopologyMember,
                AgentTeamTopologyMember.topology_id
                == AgentTeamTopology.id,
            )
            .where(
                AgentTeamTopologyMember.actor_id == actor_id,
                AgentTeamTopology.state != "disabled",
            )
        )
        topology_key = result.scalar_one_or_none()
        if topology_key is None:
            return None
        topology = await self._topology(topology_key, load_members=True)
        if topology is None:
            return None
        status = await self._status_for_topology(
            topology,
            can_mutate=False,
            persist_state=False,
        )
        runtime_ready_actor_ids = frozenset(
            member.actor_id
            for member in status.members
            if member.actor_id is not None and member.runtime_ready
        )
        return AgentTeamMembershipBoundary(
            topology_id=topology.id,
            topology_key=topology.topology_key,
            topology_revision=topology.revision,
            primary_actor_id=topology.primary_actor_id,
            member_actor_ids=frozenset(
                member.actor_id
                for member in topology.members
                if member.actor_id is not None
                and member.lifecycle_state != "disabled"
            ),
            runtime_ready_actor_ids=runtime_ready_actor_ids,
        )

    async def require_dispatch_member(
        self,
        principal: AgentActor,
        target_actor_id: int,
    ) -> AgentTeamMembershipBoundary | None:
        """Fail closed when a bound caller selects outside its active roster."""

        boundary = await self.membership_boundary(principal.id)
        if boundary is None:
            return None
        if target_actor_id not in boundary.runtime_ready_actor_ids:
            raise AgentTeamSetupConflictError(
                "agent_team_actor_outside_topology",
                "Exact actor is not runtime-ready in the caller's current topology",
                topology_key=boundary.topology_key,
                topology_revision=boundary.topology_revision,
                target_actor_id=target_actor_id,
            )
        return boundary

    async def routing_readiness(
        self,
        actor: AgentActor,
    ) -> AgentRoutingTopologyReadiness:
        """Project authoritative setup state into the rollout readiness hook."""

        boundary = await self.membership_boundary(actor.id)
        if boundary is None:
            return AgentRoutingTopologyReadiness.unavailable()
        topology = await self._topology(
            boundary.topology_key,
            load_members=True,
        )
        assert topology is not None
        status = await self._status_for_topology(
            topology,
            can_mutate=False,
            persist_state=False,
        )
        if status.runtime_ready:
            return AgentRoutingTopologyReadiness.ready(
                topology_id=boundary.topology_key,
                topology_revision=boundary.topology_revision,
            )
        return AgentRoutingTopologyReadiness.not_ready(
            topology_id=boundary.topology_key,
            topology_revision=boundary.topology_revision,
            blocker_codes=status.blocker_codes
            or ("topology_not_runtime_ready",),
        )
