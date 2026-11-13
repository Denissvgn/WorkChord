"""A team stored under earlier role rules stays readable and replaceable."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from copy import deepcopy
from dataclasses import dataclass
import json
from typing import Any

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.database import get_db
from app.main import app as main_app
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentTeamTopology,
    AgentTeamTopologyMember,
)
from app.schemas import agent_team_setup as contracts
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import (
    AgentTeamApplyRequest,
    AgentTeamApplyResponse,
    AgentTeamCurrentMember,
    AgentTeamCurrentSnapshot,
    AgentTeamMaster,
    AgentTeamMemberSpec,
    AgentTeamPlanRequest,
    AgentTeamReconciliationClass,
    AgentTeamRuntimeAcknowledgement,
    AgentTeamRuntimeHandoff,
)
from app.services import agent_team_setup_service
from app.services.agent_team_setup_service import (
    AgentTeamSetupConflictError,
    AgentTeamSetupService,
)
from app.services.identity_service import initialize_control_plane
from tests.test_agent_team_setup import (
    CapturingCredentialSink,
    example_payload,
    operator,
)


pytestmark = pytest.mark.usefixtures("deployed_agent_skill_release")

# Role packages an earlier release accepted for verifier members, or that a
# stored team was observed to carry.
EARLIER_VERIFIER_PACKAGES = ("workchord-pm", "workchord-worker")
OUTDATED = "stored_contract_outdated"
VERIFIER_KEYS = ("independent-verifier", "second-verifier")
OPERATOR_KEY = "stored-contract-operator-fixture"
TOPOLOGY_KEY = "default-agent-team"


def team_payload() -> dict[str, Any]:
    """Return the example team with a second verifier."""

    payload = example_payload()
    second = deepcopy(payload["verifiers"][0])
    second.update(
        {
            "actor_key": "second-verifier",
            "actor_name": "workchord-second-verifier",
            "display_name": "Second Verification Runtime",
            "runtime_ref": "runtime://second-verifier",
            "credential_ref": "agent-team-secure-sink/second-verifier",
        }
    )
    payload["verifiers"].append(second)
    return payload


def earlier_team_payload(package_name: str) -> dict[str, Any]:
    """Return the same team with every verifier on another role's package."""

    payload = team_payload()
    donor = next(
        member["skill_package"]
        for member in (payload["controller"], *payload["workers"])
        if member["skill_package"]["name"] == package_name
    )
    for verifier in payload["verifiers"]:
        verifier["skill_package"] = deepcopy(donor)
    return payload


@contextmanager
def earlier_role_rules(package_name: str) -> Iterator[None]:
    """Validate like a release whose verifiers carried ``package_name``."""

    with pytest.MonkeyPatch.context() as patch:
        patch.setitem(
            contracts.ROLE_PACKAGE_COMPATIBILITY,
            "verifier",
            (package_name,),
        )
        yield


def stored_text(value: Any) -> str:
    """Serialize a contract the way an apply stores it."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


class FailingForOneMemberSink(CapturingCredentialSink):
    """Lose the first credential delivery for one chosen member."""

    def __init__(self, actor_key: str) -> None:
        super().__init__()
        self.failing_actor_key: str | None = actor_key

    async def deliver(
        self,
        *,
        credential_ref: str,
        actor_key: str,
        actor_name: str,
        api_key: str,
    ) -> str:
        if actor_key == self.failing_actor_key:
            self.failing_actor_key = None
            raise RuntimeError("simulated uncertain sink delivery")
        return await super().deliver(
            credential_ref=credential_ref,
            actor_key=actor_key,
            actor_name=actor_name,
            api_key=api_key,
        )


async def apply_every_action(
    service: AgentTeamSetupService,
    manifest: AgentTeamMaster,
    *,
    expected_revision: int,
    key: str,
    only: tuple[str, ...] | None = None,
) -> AgentTeamApplyResponse:
    """Approve and confirm the planned actions, or just the ``only`` ones."""

    plan = await service.plan(
        operator(),
        AgentTeamPlanRequest(
            manifest=manifest,
            expected_topology_revision=expected_revision,
        ),
    )
    approved = tuple(
        action.action_id
        for action in plan.actions
        if only is None or action.action_id in only
    )
    assert only is None or set(approved) == set(only)
    return await service.apply(
        operator(),
        AgentTeamApplyRequest(
            manifest=manifest,
            expected_topology_revision=expected_revision,
            plan_digest=plan.plan_digest,
            approved_action_ids=approved,
            confirmed_action_ids=tuple(
                action.action_id
                for action in plan.actions
                if action.action_id in approved
                and action.requires_explicit_confirmation
            ),
        ),
        command=AgentPlanningCommandContext(
            idempotency_key=key,
            rationale="Reconcile the reviewed agent-team manifest",
            correlation_id=f"{key}-correlation",
        ),
    )


async def store_team(
    db: AsyncSession,
    payload: dict[str, Any],
    *,
    key: str,
    sink: CapturingCredentialSink | None = None,
) -> tuple[AgentTeamSetupService, CapturingCredentialSink]:
    await initialize_control_plane(db)
    manifest = AgentTeamMaster.model_validate(payload)
    for binding_key in sorted(
        {member.default_model_binding_key for member in manifest.all_members}
    ):
        db.add(
            AgentModelCatalogEntry(
                key=binding_key,
                provider="configured-provider",
                configured_model_alias=binding_key,
                reasoning_tier=2,
                context_tier="medium",
                modality_tags=["text"],
                cost_tier="medium",
                latency_tier="balanced",
                enabled=True,
                revision=1,
            )
        )
    await db.commit()
    lossy = sink is not None
    sink = sink or CapturingCredentialSink()
    service = AgentTeamSetupService(db, credential_sink=sink)
    applied = await apply_every_action(
        service,
        manifest,
        expected_revision=0,
        key=key,
    )
    assert applied.status == ("blocked" if lossy else "completed")
    assert applied.resulting_topology_revision == 1
    return service, sink


@dataclass(frozen=True)
class EarlierTeam:
    service: AgentTeamSetupService
    sink: CapturingCredentialSink
    handoffs: dict[str, AgentTeamRuntimeHandoff]


async def store_team_under_earlier_rules(
    db: AsyncSession,
    package_name: str,
    *,
    acknowledged: bool = False,
) -> EarlierTeam:
    """Apply a team as the earlier release did, then return to today's rules.

    With ``acknowledged`` every runtime also finished onboarding back then.
    """

    payload = earlier_team_payload(package_name)
    with earlier_role_rules(package_name):
        service, sink = await store_team(
            db,
            payload,
            key=f"stored-contract-earlier-{package_name}",
        )
        issued = await service.status(operator(), topology_key=TOPOLOGY_KEY)
        handoffs = {
            member.actor_key: member.handoff
            for member in issued.members
            if member.handoff is not None
        }
        assert set(handoffs) == {"primary-pm", "backend-worker", *VERIFIER_KEYS}
        if acknowledged:
            for actor_key, handoff in handoffs.items():
                await service.acknowledge_runtime(
                    sink.keys[actor_key],
                    acknowledgement_for(handoff),
                )
            ready = await service.status(operator(), topology_key=TOPOLOGY_KEY)
            assert ready.runtime_ready is True

    # The rows are exactly what that release wrote, and today's rules reject
    # them for the role package and nothing else.
    topology = await stored_topology(db)
    assert topology.manifest_payload == stored_text(payload)
    with pytest.raises(ValidationError, match="immutable skill package"):
        AgentTeamMaster.model_validate_json(topology.manifest_payload)
    records = await member_records(db)
    for verifier in payload["verifiers"]:
        record = records[verifier["actor_key"]]
        assert record.desired_member_payload == stored_text(verifier)
        assert record.skill_package_name == package_name
        assert record.lifecycle_state == (
            "runtime_ready" if acknowledged else "onboarding"
        )
        with pytest.raises(ValidationError, match="immutable skill package"):
            AgentTeamMemberSpec.model_validate_json(
                record.desired_member_payload
            )
    return EarlierTeam(service=service, sink=sink, handoffs=handoffs)


async def stored_topology(db: AsyncSession) -> AgentTeamTopology:
    result = await db.execute(
        select(AgentTeamTopology).execution_options(populate_existing=True)
    )
    return result.scalar_one()


async def member_records(
    db: AsyncSession,
) -> dict[str, AgentTeamTopologyMember]:
    result = await db.execute(
        select(AgentTeamTopologyMember)
        .options(
            selectinload(AgentTeamTopologyMember.actor)
            .selectinload(AgentActor.model_bindings)
            .selectinload(AgentModelBinding.model_catalog)
        )
        .execution_options(populate_existing=True)
    )
    return {record.actor_key: record for record in result.scalars()}


def identity_evidence(
    records: dict[str, AgentTeamTopologyMember],
) -> dict[str, Any]:
    """Return what an in-place contract update has to leave untouched."""

    evidence: dict[str, Any] = {}
    for actor_key, record in sorted(records.items()):
        actor = record.actor
        assert actor is not None
        evidence[actor_key] = {
            "actor_id": actor.id,
            "actor_name": actor.name,
            "api_key_hash": actor.api_key_hash,
            "role": actor.role,
            "scopes": actor.scopes,
            "profile_id": actor.profile_id,
            "credential_ref": record.credential_ref,
            "credential_delivery_state": record.credential_delivery_state,
            "credential_delivery_receipt_digest": (
                record.credential_delivery_receipt_digest
            ),
            "bindings": sorted(
                (
                    binding.id,
                    binding.model_catalog.key,
                    binding.is_default,
                    binding.enabled,
                    binding.revision,
                )
                for binding in actor.model_bindings
            ),
        }
    return evidence


def acknowledgement_for(
    handoff: AgentTeamRuntimeHandoff,
) -> AgentTeamRuntimeAcknowledgement:
    return AgentTeamRuntimeAcknowledgement(
        topology_key=handoff.topology_key,
        topology_revision=handoff.topology_revision,
        actor_key=handoff.actor_key,
        role=handoff.role,
        skill_package=handoff.skill_package,
        profile_revision=handoff.profile_revision,
        model_binding_revisions=handoff.model_binding_revisions,
        server_features=handoff.required_server_features,
        supported_assignment_modes=handoff.supported_assignment_modes,
    )


@pytest.mark.contract
def test_stored_contract_keeps_shape_checks_and_names_the_broken_role_rule() -> None:
    from app.schemas.agent_team_setup import (
        load_stored_agent_team_master,
        load_stored_agent_team_member,
    )

    current = team_payload()
    stored = load_stored_agent_team_master(stored_text(current))
    assert stored == AgentTeamMaster.model_validate(current)
    assert stored.canonical_bytes() == stored_text(current).encode("utf-8")
    assert [member.role_rule_violation() for member in stored.all_members] == [
        None,
        None,
        None,
        None,
    ]

    for package_name in EARLIER_VERIFIER_PACKAGES:
        earlier = earlier_team_payload(package_name)
        # Requests keep today's rules; only a stored contract loads.
        with pytest.raises(ValidationError, match="immutable skill package"):
            AgentTeamMaster.model_validate(earlier)
        with pytest.raises(ValidationError, match="immutable skill package"):
            AgentTeamPlanRequest.model_validate(
                {"manifest": earlier, "expected_topology_revision": 1}
            )
        stored = load_stored_agent_team_master(stored_text(earlier))
        assert stored.canonical_bytes() == stored_text(earlier).encode("utf-8")
        assert {
            member.actor_key: member.role_rule_violation()
            for member in stored.all_members
        } == {
            "primary-pm": None,
            "backend-worker": None,
            "independent-verifier": (
                "Role and immutable skill package are incompatible"
            ),
            "second-verifier": (
                "Role and immutable skill package are incompatible"
            ),
        }
        member = load_stored_agent_team_member(
            stored_text(earlier["verifiers"][0])
        )
        assert member.skill_package.name == package_name
        assert member.role_rule_violation() is not None
        # The loaded contract stays readable wherever it is embedded, but
        # turning it back into plain data drops that and today's rules apply.
        embedded = AgentTeamCurrentMember(
            actor_key=member.actor_key,
            actor_name=member.actor_name,
            object_revision=1,
            lifecycle_state="configured",
            desired_spec=member,
        )
        snapshot = AgentTeamCurrentSnapshot(
            topology_key=TOPOLOGY_KEY,
            revision=1,
            members=(embedded,),
        )
        assert snapshot.members[0].desired_spec == member
        with pytest.raises(ValidationError, match="immutable skill package"):
            AgentTeamMemberSpec.model_validate(member.model_dump(mode="json"))

    # A stored contract with a broken shape is still refused.
    broken: list[dict[str, Any]] = []
    undeclared_default = earlier_team_payload("workchord-pm")
    undeclared_default["verifiers"][0]["default_model_binding_key"] = (
        "undeclared-model"
    )
    broken.append(undeclared_default)
    unknown_field = earlier_team_payload("workchord-pm")
    unknown_field["verifiers"][0]["api_key"] = "forbidden"
    broken.append(unknown_field)
    unknown_role = earlier_team_payload("workchord-pm")
    unknown_role["verifiers"][0]["role"] = "reviewer"
    broken.append(unknown_role)
    verifier_listed_as_worker = earlier_team_payload("workchord-pm")
    verifier_listed_as_worker["workers"].append(
        verifier_listed_as_worker["verifiers"].pop()
    )
    broken.append(verifier_listed_as_worker)
    for payload in broken:
        with pytest.raises(ValidationError):
            load_stored_agent_team_master(stored_text(payload))
    with pytest.raises(ValidationError):
        load_stored_agent_team_member(
            stored_text(undeclared_default["verifiers"][0])
        )


@asynccontextmanager
async def operator_client(
    db: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncIterator[httpx.AsyncClient]:
    """Call the public interface as an operator on the test database."""

    async def override_db() -> AsyncIterator[AsyncSession]:
        yield db

    original_overrides = main_app.dependency_overrides.copy()
    with monkeypatch.context() as patch:
        patch.setenv("WORKCHORD_ADMIN_API_KEY", OPERATOR_KEY)
        get_settings.cache_clear()
        main_app.dependency_overrides[get_db] = override_db
        try:
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=main_app),
                base_url="http://workchord.test",
                headers={"X-Admin-API-Key": OPERATOR_KEY},
            ) as client:
                yield client
        finally:
            main_app.dependency_overrides.clear()
            main_app.dependency_overrides.update(original_overrides)
            # Later service calls start without the request's identity context.
            db.info.pop("authority", None)
    get_settings.cache_clear()


@pytest.mark.asyncio
@pytest.mark.parametrize("package_name", EARLIER_VERIFIER_PACKAGES)
async def test_status_names_contracts_stored_under_earlier_role_rules(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    package_name: str,
) -> None:
    team = await store_team_under_earlier_rules(db_session, package_name)
    admin = operator()

    status = await team.service.status(admin, topology_key=TOPOLOGY_KEY)
    assert status.topology_state == "blocked"
    assert status.runtime_ready is False
    assert status.topology_revision == 1
    assert OUTDATED in status.blocker_codes
    by_key = {member.actor_key: member for member in status.members}
    assert set(by_key) == set(team.handoffs)
    for actor_key, member in by_key.items():
        assert member.configured is True
        assert member.runtime_ready is False
        if actor_key in VERIFIER_KEYS:
            assert OUTDATED in member.blocker_codes
            assert member.skill_package.name == package_name
            # No handoff is offered for a contract that cannot be acknowledged.
            assert member.handoff is None
        else:
            assert OUTDATED not in member.blocker_codes
            assert member.handoff == team.handoffs[actor_key]
    steps = {step.id: step for step in status.steps}
    assert steps["master"].state == "blocked"
    assert steps["master"].blocker_codes == (OUTDATED,)
    assert steps["master"].next_action is not None
    assert OUTDATED in steps["verifier"].blocker_codes
    assert OUTDATED not in steps["controller"].blocker_codes
    assert OUTDATED not in steps["workers"].blocker_codes

    report = await team.service.report(admin, topology_key=TOPOLOGY_KEY)
    assert report.topology_state == "blocked"
    assert report.runtime_ready is False
    assert OUTDATED in report.blocker_codes
    assert report.counts.desired == report.counts.blocked == 4

    async with operator_client(db_session, monkeypatch) as client:
        shown = await client.get(
            "/api/agent/team-setup/status",
            params={"topology_key": TOPOLOGY_KEY},
        )
        assert shown.status_code == 200, shown.text
        assert shown.json() == status.model_dump(mode="json")
        exported = await client.get(
            "/api/agent/team-setup/report",
            params={"topology_key": TOPOLOGY_KEY},
        )
        assert exported.status_code == 200, exported.text
        assert OUTDATED in exported.json()["blocker_codes"]


@pytest.mark.asyncio
@pytest.mark.parametrize("package_name", EARLIER_VERIFIER_PACKAGES)
async def test_plan_and_apply_replace_contracts_stored_under_earlier_role_rules(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    package_name: str,
) -> None:
    team = await store_team_under_earlier_rules(db_session, package_name)
    service, sink = team.service, team.sink
    admin = operator()
    records = await member_records(db_session)
    identities_before = identity_evidence(records)
    revisions_before = {
        actor_key: record.object_revision
        for actor_key, record in records.items()
    }
    delivered_keys = dict(sink.keys)

    # The plan for a current manifest replaces each outdated contract in
    # place; nothing else changes and no confirmation is invented.
    payload = team_payload()
    manifest = AgentTeamMaster.model_validate(payload)
    plan = await service.plan(
        admin,
        AgentTeamPlanRequest(manifest=manifest, expected_topology_revision=1),
    )
    assert plan.blocker_codes == ()
    actions = {action.actor_key: action for action in plan.actions}
    assert set(actions) == set(team.handoffs)
    for actor_key, action in actions.items():
        assert action.target_actor_id == identities_before[actor_key]["actor_id"]
        if actor_key not in VERIFIER_KEYS:
            assert action.operation == "no_change"
            continue
        assert action.operation == "update_member"
        assert (
            action.reconciliation_class
            == AgentTeamReconciliationClass.SAFE_UPDATE
        )
        assert action.action_id == f"safe-update-{actor_key}"
        assert action.expected_object_revision == revisions_before[actor_key]
        assert action.requires_explicit_confirmation is False
        assert action.authority_change is False
        assert action.blocker_code is None
        assert action.before is not None and action.after is not None
        assert action.before["skill_package"]["name"] == package_name
        assert action.after["skill_package"]["name"] == "workchord-reviewer"
        assert {
            field
            for field in action.after
            if action.before[field] != action.after[field]
        } == {"skill_package"}

    async with operator_client(db_session, monkeypatch) as client:
        planned = await client.post(
            "/api/agent/team-setup/plan",
            json={"manifest": payload, "expected_topology_revision": 1},
        )
        assert planned.status_code == 200, planned.text
        assert planned.json() == plan.model_dump(mode="json")

    # Reading rewrote nothing.
    records = await member_records(db_session)
    assert identity_evidence(records) == identities_before
    assert {
        actor_key: record.object_revision
        for actor_key, record in records.items()
    } == revisions_before
    for actor_key in VERIFIER_KEYS:
        assert records[actor_key].skill_package_name == package_name
    topology = await stored_topology(db_session)
    assert topology.revision == 1
    assert topology.manifest_payload == stored_text(
        earlier_team_payload(package_name)
    )

    applied = await apply_every_action(
        service,
        manifest,
        expected_revision=1,
        key=f"stored-contract-current-{package_name}",
    )
    assert applied.status == "completed"
    assert applied.resulting_topology_revision == 2
    assert applied.blocker_codes == ()
    assert {
        receipt.actor_key: (receipt.operation, receipt.status.value)
        for receipt in applied.receipts
    } == {
        "primary-pm": ("no_change", "no_change"),
        "backend-worker": ("no_change", "no_change"),
        "independent-verifier": ("update_member", "applied"),
        "second-verifier": ("update_member", "applied"),
    }

    # Each actor, its credential and its bindings survived the update.
    records = await member_records(db_session)
    assert identity_evidence(records) == identities_before
    assert sink.keys == delivered_keys
    topology = await stored_topology(db_session)
    assert topology.manifest_payload == stored_text(payload)
    assert topology.manifest_digest == manifest.digest()
    for member in manifest.all_members:
        record = records[member.actor_key]
        updated = member.actor_key in VERIFIER_KEYS
        assert record.object_revision == (
            revisions_before[member.actor_key] + (1 if updated else 0)
        )
        assert record.lifecycle_state == "onboarding"
        assert record.desired_member_digest == member.digest()
        assert (
            AgentTeamMemberSpec.model_validate_json(record.desired_member_payload)
            == member
        )
    for actor_key in VERIFIER_KEYS:
        assert records[actor_key].skill_package_name == "workchord-reviewer"

    # Status is clean again and the team finishes onboarding as usual.
    current = await service.status(admin, topology_key=TOPOLOGY_KEY)
    assert current.topology_revision == 2
    assert OUTDATED not in current.model_dump_json()
    assert {step.id: step.state for step in current.steps}["master"] == "done"
    for member in current.members:
        assert member.handoff is not None
        if member.role == "verifier":
            assert member.skill_package.name == "workchord-reviewer"
            assert member.handoff.skill_package == member.skill_package
        response = await service.acknowledge_runtime(
            sink.keys[member.actor_key],
            acknowledgement_for(member.handoff),
        )
        assert response.actor_key == member.actor_key
    ready = await service.status(admin, topology_key=TOPOLOGY_KEY)
    assert ready.topology_state == "runtime_ready"
    assert ready.runtime_ready is True
    assert ready.blocker_codes == ()
    assert all(member.runtime_ready for member in ready.members)
    assert identity_evidence(await member_records(db_session)) == (
        identities_before
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("package_name", EARLIER_VERIFIER_PACKAGES)
async def test_outdated_stored_contract_keeps_only_its_own_member_out(
    db_session: AsyncSession,
    package_name: str,
) -> None:
    team = await store_team_under_earlier_rules(db_session, package_name)
    service, sink = team.service, team.sink

    # Members with a current contract still finish onboarding.
    for actor_key in ("primary-pm", "backend-worker"):
        response = await service.acknowledge_runtime(
            sink.keys[actor_key],
            acknowledgement_for(team.handoffs[actor_key]),
        )
        assert response.lifecycle_state == "runtime_ready"
        assert response.topology_runtime_ready is False
        assert OUTDATED in response.blocker_codes

    # A runtime cannot acknowledge a contract the role rules now reject, even
    # with the handoff it was given before the rules changed.
    for actor_key in VERIFIER_KEYS:
        with pytest.raises(AgentTeamSetupConflictError) as refused:
            await service.acknowledge_runtime(
                sink.keys[actor_key],
                acknowledgement_for(team.handoffs[actor_key]),
            )
        assert refused.value.code == "agent_team_ack_contract_outdated"
        assert refused.value.context == {"actor_key": actor_key}
    records = await member_records(db_session)
    for actor_key in VERIFIER_KEYS:
        record = records[actor_key]
        assert record.lifecycle_state == "onboarding"
        assert record.runtime_acknowledgement_digest is None
        assert record.actor is not None and record.actor.enabled is False

    # Dispatch sees the acknowledged members and leaves the verifiers out.
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert {
        member.actor_key: member.runtime_ready for member in status.members
    } == {
        "primary-pm": True,
        "backend-worker": True,
        "independent-verifier": False,
        "second-verifier": False,
    }
    assert status.runtime_ready is False
    assert OUTDATED in status.blocker_codes
    controller_id = records["primary-pm"].actor_id
    worker_id = records["backend-worker"].actor_id
    assert controller_id is not None and worker_id is not None
    boundary = await service.membership_boundary(controller_id)
    assert boundary is not None
    assert boundary.runtime_ready_actor_ids == frozenset(
        {controller_id, worker_id}
    )
    assert boundary.member_actor_ids == frozenset(
        record.actor_id for record in records.values()
    )


@pytest.mark.asyncio
async def test_working_team_stored_under_earlier_role_rules_recovers_in_place(
    db_session: AsyncSession,
) -> None:
    team = await store_team_under_earlier_rules(
        db_session,
        "workchord-pm",
        acknowledged=True,
    )
    service, sink = team.service, team.sink
    records = await member_records(db_session)
    identities_before = identity_evidence(records)
    actor_ids = {
        actor_key: record.actor_id for actor_key, record in records.items()
    }

    # The controller and worker keep working; the verifiers leave dispatch
    # until their contract is replaced and acknowledged again.
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert status.topology_state == "blocked"
    assert OUTDATED in status.blocker_codes
    assert {
        member.actor_key: (member.runtime_ready, member.blocker_codes)
        for member in status.members
    } == {
        "primary-pm": (True, ()),
        "backend-worker": (True, ()),
        "independent-verifier": (False, (OUTDATED,)),
        "second-verifier": (False, (OUTDATED,)),
    }
    boundary = await service.membership_boundary(actor_ids["primary-pm"])
    assert boundary is not None
    assert boundary.runtime_ready_actor_ids == frozenset(
        {actor_ids["primary-pm"], actor_ids["backend-worker"]}
    )

    applied = await apply_every_action(
        service,
        AgentTeamMaster.model_validate(team_payload()),
        expected_revision=1,
        key="stored-contract-working-team",
    )
    assert applied.status == "completed"
    assert applied.resulting_topology_revision == 2
    records = await member_records(db_session)
    assert identity_evidence(records) == identities_before
    for actor_key in VERIFIER_KEYS:
        record = records[actor_key]
        assert record.lifecycle_state == "connected"
        assert record.runtime_acknowledgement_digest is None
        assert record.actor is not None and record.actor.enabled is True

    # Every runtime acknowledges the new revision; nothing was re-issued.
    current = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert OUTDATED not in current.model_dump_json()
    for member in current.members:
        assert member.runtime_ready is False
        assert member.handoff is not None
        acknowledgement = acknowledgement_for(member.handoff)
        await service.acknowledge_runtime(
            sink.keys[member.actor_key],
            acknowledgement.model_copy(
                update={
                    "expected_previous_acknowledgement_digest": (
                        member.handoff.previous_acknowledgement_digest
                    )
                }
            ),
        )
    ready = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert ready.runtime_ready is True
    assert ready.blocker_codes == ()
    assert identity_evidence(await member_records(db_session)) == (
        identities_before
    )


@pytest.mark.asyncio
async def test_partly_approved_replacement_leaves_the_rest_plannable(
    db_session: AsyncSession,
) -> None:
    team = await store_team_under_earlier_rules(db_session, "workchord-pm")
    service, sink = team.service, team.sink
    manifest = AgentTeamMaster.model_validate(team_payload())

    first = await apply_every_action(
        service,
        manifest,
        expected_revision=1,
        key="stored-contract-first-verifier",
        only=("safe-update-independent-verifier",),
    )
    assert first.status == "partial"
    assert first.resulting_topology_revision == 2
    assert first.pending_action_ids == ("safe-update-second-verifier",)

    # The manifest is current now, but the member left out keeps its earlier
    # contract. Status reads the same member contract acknowledgement does,
    # so both name it outdated: no handoff, and its earlier one is refused.
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert status.pending_action_ids == ("safe-update-second-verifier",)
    assert status.runtime_ready is False
    assert OUTDATED in status.blocker_codes
    by_key = {member.actor_key: member for member in status.members}
    waiting = by_key["second-verifier"]
    assert waiting.runtime_ready is False
    assert OUTDATED in waiting.blocker_codes
    assert waiting.handoff is None
    assert OUTDATED not in by_key["independent-verifier"].blocker_codes
    assert by_key["independent-verifier"].handoff is not None
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(
            sink.keys["second-verifier"],
            acknowledgement_for(team.handoffs["second-verifier"]),
        )
    assert refused.value.code == "agent_team_ack_contract_outdated"
    records = await member_records(db_session)
    assert records["independent-verifier"].skill_package_name == (
        "workchord-reviewer"
    )
    assert records["second-verifier"].skill_package_name == "workchord-pm"

    second = await apply_every_action(
        service,
        manifest,
        expected_revision=2,
        key="stored-contract-second-verifier",
    )
    assert second.status == "completed"
    assert second.resulting_topology_revision == 3
    assert {
        receipt.actor_key: receipt.operation for receipt in second.receipts
    } == {
        "primary-pm": "no_change",
        "backend-worker": "no_change",
        "independent-verifier": "no_change",
        "second-verifier": "update_member",
    }
    records = await member_records(db_session)
    assert records["second-verifier"].skill_package_name == (
        "workchord-reviewer"
    )
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert status.pending_action_ids == ()
    for member in status.members:
        assert member.handoff is not None
        await service.acknowledge_runtime(
            sink.keys[member.actor_key],
            acknowledgement_for(member.handoff),
        )
    ready = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert ready.runtime_ready is True


@pytest.mark.asyncio
async def test_lost_credential_on_an_outdated_contract_recovers_and_updates_it(
    db_session: AsyncSession,
) -> None:
    lost = "independent-verifier"
    with earlier_role_rules("workchord-pm"):
        service, sink = await store_team(
            db_session,
            earlier_team_payload("workchord-pm"),
            key="stored-contract-lost-credential",
            sink=FailingForOneMemberSink(lost),
        )
    records = await member_records(db_session)
    assert records[lost].credential_delivery_state == "uncertain"
    assert lost not in sink.keys

    # On an outdated contract, credential recovery may also take the
    # role-governed fields of the current master: one approved recovery
    # delivers a new credential and brings the contract up to date.
    recovery_payload = team_payload()
    recovery_payload["verifiers"][0]["credential_ref"] = (
        f"agent-team-secure-sink/{lost}-recovery"
    )
    recovery = AgentTeamMaster.model_validate(recovery_payload)
    applied = await apply_every_action(
        service,
        recovery,
        expected_revision=1,
        key="stored-contract-recover-credential",
    )
    assert applied.status == "completed"
    assert applied.resulting_topology_revision == 2
    assert {
        receipt.actor_key: (
            receipt.operation,
            receipt.status.value,
            receipt.blocker_code,
        )
        for receipt in applied.receipts
    } == {
        "primary-pm": ("no_change", "no_change", None),
        "backend-worker": ("no_change", "no_change", None),
        lost: ("replace_member", "applied", None),
        "second-verifier": ("update_member", "applied", None),
    }
    records = await member_records(db_session)
    assert records[lost].skill_package_name == "workchord-reviewer"
    assert records[lost].credential_ref == (
        f"agent-team-secure-sink/{lost}-recovery"
    )
    assert records[lost].credential_delivery_state == "delivered"
    assert lost in sink.keys
    assert records["second-verifier"].skill_package_name == (
        "workchord-reviewer"
    )
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert status.topology_revision == 2
    assert OUTDATED not in status.blocker_codes
    assert "credential_delivery_uncertain" not in status.blocker_codes

    # Every member now acknowledges the current handoff and the team is ready.
    for member in status.members:
        assert member.handoff is not None
        await service.acknowledge_runtime(
            sink.keys[member.actor_key],
            acknowledgement_for(member.handoff),
        )
    ready = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    assert ready.runtime_ready is True


@pytest.mark.asyncio
async def test_lost_credential_recovery_still_changes_only_the_credential(
    db_session: AsyncSession,
) -> None:
    lost = "independent-verifier"
    with earlier_role_rules("workchord-pm"):
        service, sink = await store_team(
            db_session,
            earlier_team_payload("workchord-pm"),
            key="stored-contract-lost-credential-drift",
            sink=FailingForOneMemberSink(lost),
        )

    # Only the role-governed fields may change with the credential; any other
    # drift is still refused by name and the member is left as it was.
    recovery_payload = team_payload()
    recovery_payload["verifiers"][0]["credential_ref"] = (
        f"agent-team-secure-sink/{lost}-recovery"
    )
    recovery_payload["verifiers"][0]["display_name"] = "Renamed verifier"
    recovery = AgentTeamMaster.model_validate(recovery_payload)
    applied = await apply_every_action(
        service,
        recovery,
        expected_revision=1,
        key="stored-contract-recover-with-drift",
    )
    receipts = {receipt.actor_key: receipt for receipt in applied.receipts}
    assert receipts[lost].status.value == "blocked"
    assert receipts[lost].blocker_code == (
        "credential_recovery_change_not_isolated"
    )
    records = await member_records(db_session)
    assert records[lost].skill_package_name == "workchord-pm"
    assert records[lost].credential_delivery_state == "uncertain"
    assert lost not in sink.keys


@pytest.mark.asyncio
async def test_current_stored_team_reads_exactly_as_with_strict_validation(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = team_payload()
    service, sink = await store_team(
        db_session,
        payload,
        key="stored-contract-current-team",
    )
    admin = operator()
    manifest = AgentTeamMaster.model_validate(payload)
    changed_payload = team_payload()
    changed_payload["workers"][0]["display_name"] = "Renamed Worker Runtime"
    changed = AgentTeamMaster.model_validate(changed_payload)

    async def readings() -> list[str]:
        status = await service.status(admin, topology_key=TOPOLOGY_KEY)
        report = await service.report(admin, topology_key=TOPOLOGY_KEY)
        plans = [
            await service.plan(
                admin,
                AgentTeamPlanRequest(
                    manifest=desired,
                    expected_topology_revision=1,
                ),
            )
            for desired in (manifest, changed)
        ]
        return [
            status.model_dump_json(),
            report.model_dump_json(exclude={"generated_at"}),
            *(plan.model_dump_json() for plan in plans),
        ]

    async def readings_matching_strict_validation() -> list[str]:
        current = await readings()
        with monkeypatch.context() as patch:
            # Read every stored payload with today's full validation, as the
            # service did before stored contracts had their own loader.
            patch.setattr(
                agent_team_setup_service,
                "load_stored_agent_team_master",
                AgentTeamMaster.model_validate_json,
                raising=False,
            )
            patch.setattr(
                agent_team_setup_service,
                "load_stored_agent_team_member",
                AgentTeamMemberSpec.model_validate_json,
                raising=False,
            )
            strict = await readings()
        assert current == strict
        assert OUTDATED not in "".join(current)
        return current

    onboarding = await readings_matching_strict_validation()
    assert [action["operation"] for action in json.loads(onboarding[2])["actions"]] == [
        "no_change"
    ] * 4
    assert sorted(
        action["operation"] for action in json.loads(onboarding[3])["actions"]
    ) == ["no_change", "no_change", "no_change", "update_member"]

    status = await service.status(admin, topology_key=TOPOLOGY_KEY)
    for member in status.members:
        assert member.handoff is not None
        await service.acknowledge_runtime(
            sink.keys[member.actor_key],
            acknowledgement_for(member.handoff),
        )
    ready = await readings_matching_strict_validation()
    assert json.loads(ready[0])["runtime_ready"] is True
    assert ready[0] != onboarding[0]
