"""The onboarding handoff names a runtime instance and the acknowledgement must return it."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent_contract import (
    AGENT_CONTRACT_FEATURES,
    RUNTIME_INSTANCE_IDENTITY_FEATURE,
    agent_contract_features,
)
from app.models.agent import AgentTeamTopologyMember
from app.schemas.agent_team_setup import (
    AgentTeamMaster,
    AgentTeamRuntimeAcknowledgement,
    AgentTeamRuntimeHandoff,
)
from app.services.agent_team_setup_service import (
    AgentTeamSetupConflictError,
    AgentTeamSetupService,
    _digest,
)
from tests.test_agent_team_setup import CapturingCredentialSink, example_payload, operator
from tests.test_delivery_scenarios import delivery_store  # noqa: F401  (fixture)
from tests.test_agent_team_setup_stored_contract import (
    TOPOLOGY_KEY,
    apply_every_action,
    member_records,
    store_team,
)

pytestmark = pytest.mark.usefixtures("deployed_agent_skill_release")
WORKER = "backend-worker"


class SameReceiptSink(CapturingCredentialSink):
    """A sink whose delivery receipt does not change between deliveries, and that can lose one.

    The receipt of the production sink is a digest of fixed inputs, so a runtime
    identity must not depend on it.
    """

    def __init__(self, lose: str | None = None) -> None:
        super().__init__()
        self.lose = lose

    async def deliver(self, *, credential_ref: str, actor_key: str, actor_name: str, api_key: str) -> str:
        if actor_key == self.lose:
            self.lose = None
            raise RuntimeError("simulated uncertain sink delivery")
        await super().deliver(
            credential_ref=credential_ref, actor_key=actor_key, actor_name=actor_name, api_key=api_key
        )
        return "c" * 64


def worker_manifest(**changes: str) -> AgentTeamMaster:
    payload = example_payload()
    assert payload["workers"][0]["actor_key"] == WORKER
    payload["workers"][0].update(changes)
    return AgentTeamMaster.model_validate(payload)


def acknowledgement_for(
    handoff: AgentTeamRuntimeHandoff,
    *,
    identity: str | None = None,
    features: tuple[str, ...] | None = None,
    **extra,
) -> AgentTeamRuntimeAcknowledgement:
    return AgentTeamRuntimeAcknowledgement(
        topology_key=handoff.topology_key,
        topology_revision=handoff.topology_revision,
        actor_key=handoff.actor_key,
        role=handoff.role,
        skill_package=handoff.skill_package,
        profile_revision=handoff.profile_revision,
        model_binding_revisions=handoff.model_binding_revisions,
        server_features=features or handoff.required_server_features,
        supported_assignment_modes=handoff.supported_assignment_modes,
        runtime_instance_id=identity,
        **extra,
    )


async def worker_status(service: AgentTeamSetupService):
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    return next(member for member in status.members if member.actor_key == WORKER)


async def stored(db: AsyncSession) -> AgentTeamTopologyMember:
    return (await member_records(db))[WORKER]


async def team(db: AsyncSession):
    service, sink = await store_team(db, example_payload(), key="runtime-identity-team")
    member = await worker_status(service)
    assert member.handoff is not None
    return service, sink, member.handoff


@pytest.mark.contract
def test_feature_is_advertised_and_a_legacy_acknowledgement_keeps_its_bytes() -> None:
    assert RUNTIME_INSTANCE_IDENTITY_FEATURE in AGENT_CONTRACT_FEATURES
    assert RUNTIME_INSTANCE_IDENTITY_FEATURE in agent_contract_features(include_skill_bundles=False)
    legacy = AgentTeamRuntimeAcknowledgement.model_validate(
        {
            "topology_key": "team",
            "topology_revision": 1,
            "actor_key": "worker",
            "role": "worker",
            "skill_package": {"name": "workchord-worker", "version": "1.0.0", "sha256": "a" * 64},
            "profile_revision": "1",
            "model_binding_revisions": {"model": 1},
            "server_features": ["agent-team-master-v1"],
            "supported_assignment_modes": ["execution"],
        }
    )
    # Without an identity nothing is added, so a runtime that never sends one keeps its digest.
    assert "runtime_instance_id" not in legacy.stored_content()
    with_identity = legacy.model_copy(update={"runtime_instance_id": "rti-" + "b" * 32})
    assert with_identity.stored_content()["runtime_instance_id"] == "rti-" + "b" * 32
    assert _digest(legacy.stored_content()) != _digest(with_identity.stored_content())


async def test_handoff_carries_an_identity_and_a_matching_acknowledgement_shows_it(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    assert handoff.runtime_instance_id.startswith("rti-")
    before = await worker_status(service)
    assert before.runtime_identity.state == "unknown"
    assert before.runtime_identity.expected_instance_id == handoff.runtime_instance_id
    assert before.runtime_identity.acknowledged_instance_id is None

    db_session.info.pop("authority", None)
    response = await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    assert response.lifecycle_state == "runtime_ready"

    after = await worker_status(service)
    assert after.acknowledgement_state == "current"
    assert after.runtime_identity.state == "current"
    assert after.runtime_identity.acknowledged_instance_id == handoff.runtime_instance_id
    assert after.runtime_identity.previous_instance_id is None
    record = await stored(db_session)
    assert json.loads(record.runtime_acknowledgement_payload)["runtime_instance_id"] == handoff.runtime_instance_id
    assert record.acknowledged_runtime_instance_id == handoff.runtime_instance_id
    # The same acknowledgement again is a replay, not a change.
    again = await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    assert again.acknowledgement_digest == response.acknowledgement_digest
    assert (await worker_status(service)).runtime_identity.state == "current"


async def test_other_member_handoffs_carry_their_own_identity(db_session: AsyncSession) -> None:
    service, _, _ = await team(db_session)
    status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
    identities = {member.handoff.runtime_instance_id for member in status.members if member.handoff}
    assert len(identities) == len(status.members)


async def test_a_mismatched_identity_is_refused_by_name_and_shown(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    other = "rti-" + "c" * 32
    assert other != handoff.runtime_instance_id
    db_session.info.pop("authority", None)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff, identity=other))
    assert refused.value.code == "agent_team_ack_runtime_instance_mismatch"

    member = await worker_status(service)
    assert member.runtime_ready is False
    assert member.package_acknowledged is False
    # The refusal is shown beside the state the acknowledgement gives; it is not a state of its own.
    assert member.runtime_identity.state == "unknown"
    assert member.runtime_identity.refused_instance_id == other
    assert member.runtime_identity.refused_at is not None

    # The genuine runtime is still accepted, and the refusal is cleared.
    await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    member = await worker_status(service)
    assert member.runtime_identity.state == "current"
    assert member.runtime_identity.refused_instance_id is None
    assert member.runtime_identity.refused_at is None


async def test_a_refusal_ends_when_the_genuine_runtime_that_had_acknowledged_acknowledges_again(
    db_session: AsyncSession,
) -> None:
    service, sink, handoff = await team(db_session)
    genuine = acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    db_session.info.pop("authority", None)
    first = await service.acknowledge_runtime(sink.keys[WORKER], genuine)

    other = "rti-" + "9" * 32
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff, identity=other))
    assert refused.value.code == "agent_team_ack_runtime_instance_mismatch"
    member = await worker_status(service)
    # The acknowledgement stands, so the state does; the refusal is shown next to it.
    assert member.runtime_ready is True
    assert member.runtime_identity.state == "current"
    assert member.runtime_identity.refused_instance_id == other
    assert member.runtime_identity.refused_at is not None

    # The same genuine acknowledgement again is a replay, and a replay ends the refusal too.
    again = await service.acknowledge_runtime(sink.keys[WORKER], genuine)
    assert again.acknowledgement_digest == first.acknowledgement_digest
    member = await worker_status(service)
    assert member.runtime_identity.state == "current"
    assert member.runtime_identity.refused_instance_id is None
    assert member.runtime_identity.refused_at is None
    record = await stored(db_session)
    assert record.rejected_runtime_instance_id is None and record.rejected_runtime_instance_at is None


async def test_a_replay_without_the_identity_does_not_end_a_refusal(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    db_session.info.pop("authority", None)
    await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    other = "rti-" + "8" * 32
    with pytest.raises(AgentTeamSetupConflictError):
        await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff, identity=other))
    # A runtime that sends no identity has not shown that it holds this one.
    await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    member = await worker_status(service)
    assert member.runtime_identity.state == "unknown"
    assert member.runtime_identity.refused_instance_id == other


async def test_a_legacy_acknowledgement_is_accepted_and_reads_as_identity_unknown(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    db_session.info.pop("authority", None)
    response = await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    assert response.lifecycle_state == "runtime_ready"

    record = await stored(db_session)
    payload = json.loads(record.runtime_acknowledgement_payload)
    assert "runtime_instance_id" not in payload
    assert record.runtime_acknowledgement_digest == _digest(payload)
    member = await worker_status(service)
    assert member.acknowledgement_state == "current"
    assert member.runtime_ready is True
    assert member.runtime_identity.state == "unknown"
    assert member.runtime_identity.acknowledged_instance_id is None
    assert member.runtime_identity.changed_at is None
    # A retry of the legacy acknowledgement stays a replay.
    again = await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    assert again.acknowledgement_digest == response.acknowledgement_digest


async def test_a_legacy_runtime_adopts_the_identity_by_refreshing_without_a_change(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    db_session.info.pop("authority", None)
    legacy = await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    features = (*handoff.required_server_features, RUNTIME_INSTANCE_IDENTITY_FEATURE)
    refreshed = await service.acknowledge_runtime(
        sink.keys[WORKER],
        acknowledgement_for(
            handoff,
            identity=handoff.runtime_instance_id,
            features=features,
            expected_previous_acknowledgement_digest=legacy.acknowledgement_digest,
        ),
    )
    assert refreshed.acknowledgement_digest != legacy.acknowledgement_digest
    member = await worker_status(service)
    assert member.runtime_identity.state == "current"
    assert member.runtime_identity.changed_at is None


async def test_a_runtime_that_lists_the_feature_must_send_the_identity(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    features = (*handoff.required_server_features, RUNTIME_INSTANCE_IDENTITY_FEATURE)
    db_session.info.pop("authority", None)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff, features=features))
    assert refused.value.code == "agent_team_ack_runtime_instance_missing"
    assert (await worker_status(service)).runtime_ready is False


async def test_a_required_feature_refuses_an_acknowledgement_without_the_identity(db_session: AsyncSession) -> None:
    payload = example_payload()
    payload["required_server_features"] = sorted({*payload["required_server_features"], RUNTIME_INSTANCE_IDENTITY_FEATURE})
    service, sink = await store_team(db_session, payload, key="runtime-identity-required")
    handoff = (await worker_status(service)).handoff
    assert handoff is not None and RUNTIME_INSTANCE_IDENTITY_FEATURE in handoff.required_server_features
    db_session.info.pop("authority", None)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff))
    assert refused.value.code == "agent_team_ack_runtime_instance_missing"
    await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    assert (await worker_status(service)).runtime_identity.state == "current"


async def test_a_replaced_member_issues_a_new_identity_and_the_takeover_is_a_visible_change(
    db_session: AsyncSession,
) -> None:
    service, sink = await store_team(
        db_session, example_payload(), key="runtime-identity-replace", sink=SameReceiptSink(), lossy=False
    )
    handoff = (await worker_status(service)).handoff
    assert handoff is not None
    db_session.info.pop("authority", None)
    first = await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    receipt_before = (await stored(db_session)).credential_delivery_receipt_digest

    # The member is replaced through the setup action: a new actor and a new credential. The sink's
    # receipt is the same as before, so nothing but the server's own issuance can tell them apart.
    applied = await apply_every_action(
        service,
        worker_manifest(
            actor_name="workchord-backend-worker-v2",
            runtime_ref="runtime://backend-worker-v2",
            credential_ref="agent-team-secure-sink/backend-worker-v2",
        ),
        expected_revision=1,
        key="runtime-identity-replace-worker",
    )
    assert applied.status == "completed"
    assert next(r for r in applied.receipts if r.actor_key == WORKER).operation == "replace_member"
    assert (await stored(db_session)).credential_delivery_receipt_digest == receipt_before

    renewed = await worker_status(service)
    assert renewed.handoff is not None
    replacement = renewed.handoff.runtime_instance_id
    assert replacement != handoff.runtime_instance_id
    assert replacement.startswith("rti-") and len(replacement) == 36
    assert renewed.runtime_ready is False
    assert renewed.runtime_identity.state == "unknown"
    assert renewed.runtime_identity.expected_instance_id == replacement

    # The earlier runtime's identity is not the one the new handoff carries: refused, named and shown.
    db_session.info.pop("authority", None)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(
            sink.keys[WORKER], acknowledgement_for(renewed.handoff, identity=handoff.runtime_instance_id)
        )
    assert refused.value.code == "agent_team_ack_runtime_instance_mismatch"
    shown = (await worker_status(service)).runtime_identity
    assert shown.refused_instance_id == handoff.runtime_instance_id

    await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(renewed.handoff, identity=replacement)
    )
    member = await worker_status(service)
    assert member.runtime_ready is True
    assert member.runtime_identity.state == "changed"
    assert member.runtime_identity.acknowledged_instance_id == replacement
    assert member.runtime_identity.previous_instance_id == handoff.runtime_instance_id
    assert member.runtime_identity.changed_at is not None
    assert member.runtime_identity.refused_instance_id is None
    assert first.acknowledgement_digest != (await stored(db_session)).runtime_acknowledgement_digest


async def test_a_recovered_credential_issues_a_new_identity(db_session: AsyncSession) -> None:
    service, sink = await store_team(
        db_session, example_payload(), key="runtime-identity-recover", sink=SameReceiptSink(lose=WORKER)
    )
    before = await stored(db_session)
    assert before.credential_delivery_state == "uncertain"
    issued_before = before.issued_runtime_instance_id
    handoff_before = (await worker_status(service)).handoff
    assert handoff_before is not None and handoff_before.runtime_instance_id == issued_before

    applied = await apply_every_action(
        service,
        worker_manifest(credential_ref="agent-team-secure-sink/backend-worker-recovery"),
        expected_revision=1,
        key="runtime-identity-recover-worker",
    )
    assert applied.status == "completed"
    assert next(r for r in applied.receipts if r.actor_key == WORKER).operation == "replace_member"
    record = await stored(db_session)
    assert record.credential_delivery_state == "delivered"
    assert record.issued_runtime_instance_id != issued_before

    recovered = await worker_status(service)
    assert recovered.handoff is not None
    assert recovered.handoff.runtime_instance_id == record.issued_runtime_instance_id
    assert recovered.runtime_identity.expected_instance_id == record.issued_runtime_instance_id
    # The identity the runtime saw before the recovery no longer matches.
    db_session.info.pop("authority", None)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await service.acknowledge_runtime(
            sink.keys[WORKER], acknowledgement_for(recovered.handoff, identity=handoff_before.runtime_instance_id)
        )
    assert refused.value.code == "agent_team_ack_runtime_instance_mismatch"
    await service.acknowledge_runtime(
        sink.keys[WORKER],
        acknowledgement_for(recovered.handoff, identity=recovered.handoff.runtime_instance_id),
    )
    assert (await worker_status(service)).runtime_identity.state == "current"


def test_an_acknowledgement_under_an_earlier_identity_is_stale_and_only_a_match_is_current() -> None:
    expected, earlier = "rti-" + "1" * 32, "rti-" + "2" * 32
    service_status = AgentTeamSetupService._runtime_identity_status

    def state(record: AgentTeamTopologyMember, acknowledgement: dict) -> str:
        return service_status(record, expected_instance_id=expected, acknowledgement=acknowledgement).state

    record = AgentTeamTopologyMember()
    assert state(record, {}) == "unknown"
    assert state(record, {"role": "worker"}) == "unknown"
    assert state(record, {"runtime_instance_id": expected}) == "current"
    assert state(record, {"runtime_instance_id": earlier}) == "stale"
    record.runtime_identity_changed_at = datetime.now(timezone.utc)
    assert state(record, {"runtime_instance_id": expected}) == "changed"
    assert state(record, {"runtime_instance_id": earlier}) == "stale"
    assert state(record, {"role": "worker"}) == "changed"
    assert state(record, {}) == "unknown"


async def test_a_runtime_without_the_field_taking_the_seat_is_a_visible_change(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    db_session.info.pop("authority", None)
    first = await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    # A runtime that predates the identity shares the key and acknowledges without it.
    await service.acknowledge_runtime(
        sink.keys[WORKER],
        acknowledgement_for(handoff, expected_previous_acknowledgement_digest=first.acknowledgement_digest),
    )
    member = await worker_status(service)
    assert member.acknowledgement_state == "current"
    assert member.runtime_identity.state == "changed"
    assert member.runtime_identity.acknowledged_instance_id is None
    assert member.runtime_identity.previous_instance_id == handoff.runtime_instance_id
    assert member.runtime_identity.changed_at is not None


async def test_the_identity_is_not_shown_in_the_redacted_report_counts(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    db_session.info.pop("authority", None)
    await service.acknowledge_runtime(
        sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    report = await service.report(operator(), topology_key=TOPOLOGY_KEY)
    assert handoff.runtime_instance_id not in report.model_dump_json()


async def test_identity_flow_on_each_database(delivery_store) -> None:
    factory, _, _ = delivery_store
    async with factory() as db:
        service, sink, handoff = await team(db)
        status = await service.status(operator(), topology_key=TOPOLOGY_KEY)
        pm = next(member.handoff for member in status.members if member.role == "pm")
        assert pm is not None

        # One runtime still does not send an identity; it stays valid and reads as unknown.
        db.info.pop("authority", None)
        await service.acknowledge_runtime(sink.keys[pm.actor_key], acknowledgement_for(pm))
        # Another sends the wrong identity, is refused and named, and then the right one is accepted.
        other = "rti-" + "f" * 32
        with pytest.raises(AgentTeamSetupConflictError) as refused:
            await service.acknowledge_runtime(sink.keys[WORKER], acknowledgement_for(handoff, identity=other))
        assert refused.value.code == "agent_team_ack_runtime_instance_mismatch"
        refused_status = (await worker_status(service)).runtime_identity
        assert refused_status.state == "unknown" and refused_status.refused_instance_id == other
        await service.acknowledge_runtime(
            sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
        )
        states = {
            member.actor_key: member.runtime_identity.state
            for member in (await service.status(operator(), topology_key=TOPOLOGY_KEY)).members
        }
        assert states[pm.actor_key] == "unknown" and states[WORKER] == "current"
        assert (await worker_status(service)).runtime_identity.refused_instance_id is None

        # The member is replaced: a second runtime takes the seat, and the change and the identity it
        # replaced are recorded.
        applied = await apply_every_action(
            service,
            worker_manifest(
                actor_name="workchord-backend-worker-v2",
                runtime_ref="runtime://backend-worker-v2",
                credential_ref="agent-team-secure-sink/backend-worker-v2",
            ),
            expected_revision=1,
            key="runtime-identity-flow-replace",
        )
        assert applied.status == "completed"
        renewed = (await worker_status(service)).handoff
        assert renewed is not None and renewed.runtime_instance_id != handoff.runtime_instance_id
        await service.acknowledge_runtime(
            sink.keys[WORKER],
            acknowledgement_for(renewed, identity=renewed.runtime_instance_id),
        )
        changed = (await worker_status(service)).runtime_identity
        assert changed.state == "changed"
        assert changed.previous_instance_id == handoff.runtime_instance_id
        assert changed.acknowledged_instance_id == renewed.runtime_instance_id
        assert changed.changed_at is not None


async def acknowledge_over_http(db: AsyncSession, key: str, acknowledgement: AgentTeamRuntimeAcknowledgement):
    """Post one acknowledgement through the REST route, inside the request transaction production uses."""

    import httpx

    from app.commands import command_transaction
    from app.database import get_db
    from app.main import app as main_app

    async def request_database():
        async with command_transaction(db):
            yield db

    original = main_app.dependency_overrides.copy()
    main_app.dependency_overrides[get_db] = request_database
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main_app), base_url="https://test") as client:
            return await client.post(
                "/api/agent/team-setup/onboarding/acknowledge",
                headers={"X-Agent-API-Key": key},
                json=acknowledgement.model_dump(mode="json"),
            )
    finally:
        main_app.dependency_overrides.clear()
        main_app.dependency_overrides.update(original)


async def test_a_refusal_over_http_names_its_code_and_stays_visible(db_session: AsyncSession) -> None:
    service, sink, handoff = await team(db_session)
    other = "rti-" + "e" * 32
    refused = await acknowledge_over_http(db_session, sink.keys[WORKER], acknowledgement_for(handoff, identity=other))
    assert refused.status_code == 409, refused.text
    assert refused.json()["detail"]["code"] == "agent_team_ack_runtime_instance_mismatch"
    member = await worker_status(service)
    assert member.runtime_identity.state == "unknown"
    assert member.runtime_identity.refused_instance_id == other

    accepted = await acknowledge_over_http(
        db_session, sink.keys[WORKER], acknowledgement_for(handoff, identity=handoff.runtime_instance_id)
    )
    assert accepted.status_code == 200, accepted.text
    assert (await worker_status(service)).runtime_identity.state == "current"
