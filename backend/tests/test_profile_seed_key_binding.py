"""Binding a seed key to an existing unkeyed planning profile keeps its history."""

from datetime import date

import pytest
from sqlalchemy import func, select

from app.commands import PlanningConflict
from app.models.agent import AgentActor, AgentTaskAssignment, AgentModelCatalogEntry
from app.models.identity import CommandAudit
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import (
    AgentTeamApplyRequest,
    AgentTeamMaster,
    AgentTeamPlanRequest,
)
from app.schemas.team import TeamMemberProfileSeedKeyBind
from app.services.agent_team_setup_service import AgentTeamSetupService
from app.services.team_service import TeamService
from tests.test_agent_team_setup import CapturingCredentialSink, example_payload, operator
from tests.test_delivery_scenarios import delivery_store  # noqa: F401 - fixture
from tests.test_managed_authority import client, managed_store  # noqa: F401 - fixture

pytestmark = pytest.mark.usefixtures("deployed_agent_skill_release")


async def _unkeyed_agent(db, scenario, name, modes):
    profile = TeamMemberProfile(
        display_name=name, profile_kind="agent", automation_enabled=True,
        assignment_modes=modes,
    )
    db.add(profile)
    await db.flush()
    member = TeamMember(name=name, position="Agent", profile_id=profile.id,
                        iteration_id=scenario.iterations[0])
    db.add(member)
    await db.flush()
    return profile, member


async def _snapshot(db, profile_ids):
    members = (await db.execute(
        select(TeamMember.id, TeamMember.profile_id, TeamMember.iteration_id)
        .where(TeamMember.profile_id.in_(profile_ids)).order_by(TeamMember.id)
    )).all()
    tasks = (await db.execute(
        select(Task.id, Task.assignee_id, Task.status, Task.iteration_id).order_by(Task.id)
    )).all()
    versions = (await db.execute(select(Task.id, Task.version).order_by(Task.id))).all()
    assignments = (await db.execute(
        select(AgentTaskAssignment.id, AgentTaskAssignment.task_version)
        .order_by(AgentTaskAssignment.id))).all()
    return ([tuple(row) for row in members], [tuple(row) for row in tasks],
            [tuple(row) for row in versions], [tuple(row) for row in assignments])


async def test_bound_profile_is_connected_in_place_with_history_intact(delivery_store):
    factory, scenario, _ = delivery_store
    manifest = AgentTeamMaster.model_validate(example_payload())
    worker_key = manifest.workers[0].profile_key
    verifier_key = manifest.verifiers[0].profile_key
    async with factory() as db:
        worker, worker_member = await _unkeyed_agent(db, scenario, "Imported worker", ["execution"])
        verifier, _ = await _unkeyed_agent(db, scenario, "Imported reviewer", ["verification"])
        scheduled = Task(title="Scheduled work", status="planned", priority=2,
                         iteration_id=scenario.iterations[0], project_id=scenario.projects[0],
                         assignee_id=worker_member.id, effort_days=1, effort_hours=8,
                         start_date=date(2026, 1, 12), end_date=date(2026, 1, 13))
        db.add(scheduled)
        for key in {member.default_model_binding_key for member in manifest.all_members}:
            db.add(AgentModelCatalogEntry(
                key=key, provider="configured-provider", configured_model_alias=key,
                reasoning_tier=2, context_tier="medium", modality_tags=["text"],
                cost_tier="medium", latency_tier="balanced", enabled=True, revision=1))
        await db.commit()
        worker_id, verifier_id, task_id = worker.id, verifier.id, scheduled.id
        worker_member_id = worker_member.id
        before = await _snapshot(db, [worker_id, verifier_id])

        service = TeamService(db)
        bound = await service.bind_profile_seed_key(worker_id, TeamMemberProfileSeedKeyBind(
            seed_key=worker_key, reason="Adopt the imported worker"))
        assert bound.id == worker_id and bound.seed_key == worker_key
        await service.bind_profile_seed_key(
            verifier_id, TeamMemberProfileSeedKeyBind(seed_key=verifier_key))
        assert await _snapshot(db, [worker_id, verifier_id]) == before
        audits = (await db.scalars(select(CommandAudit).where(
            CommandAudit.action == "team_member_profile_seed_key_bound"))).all()
        assert {row.details["profile_id"] for row in audits} == {worker_id, verifier_id}
        assert len(audits) == 2

        profiles_before = await db.scalar(select(func.count()).select_from(TeamMemberProfile))
        sink = CapturingCredentialSink()
        setup = AgentTeamSetupService(db, credential_sink=sink)
        admin = operator()
        plan = await setup.plan(
            admin, AgentTeamPlanRequest(manifest=manifest, expected_topology_revision=0))
        applied = await setup.apply(
            admin,
            AgentTeamApplyRequest(
                manifest=manifest, expected_topology_revision=0, plan_digest=plan.plan_digest,
                approved_action_ids=tuple(action.action_id for action in plan.actions)),
            command=AgentPlanningCommandContext(
                idempotency_key="bind-then-connect", rationale="Connect the imported agents",
                correlation_id="bind-then-connect-correlation"),
        )
        assert applied.status == "completed"
        actors = {actor.name: actor for actor in (await db.scalars(select(AgentActor))).all()}
        assert actors[manifest.workers[0].actor_name].profile_id == worker_id
        assert actors[manifest.verifiers[0].actor_name].profile_id == verifier_id
        # Only the controller's preset is new; the bound profiles were not duplicated.
        assert await db.scalar(
            select(func.count()).select_from(TeamMemberProfile)) == profiles_before + 1
        assert await db.scalar(select(func.count()).select_from(TeamMemberProfile).where(
            TeamMemberProfile.seed_key.in_([worker_key, verifier_key]))) == 2
        assert await _snapshot(db, [worker_id, verifier_id]) == before
        assert (await db.get(Task, task_id)).assignee_id == worker_member_id


async def test_binding_refuses_keyed_duplicate_and_invalid_keys(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        profile, _ = await _unkeyed_agent(db, scenario, "Unkeyed", ["execution"])
        await db.commit()
        profile_id = profile.id
        service = TeamService(db)
        with pytest.raises(PlanningConflict) as keyed:
            await service.bind_profile_seed_key(
                scenario.profile, TeamMemberProfileSeedKeyBind(seed_key="another-key"))
        assert keyed.value.code == "profile_seed_key_already_bound"
        with pytest.raises(PlanningConflict) as duplicate:
            await service.bind_profile_seed_key(
                profile_id, TeamMemberProfileSeedKeyBind(seed_key="shared-delivery-owner"))
        assert duplicate.value.code == "profile_seed_key_in_use"
        assert (await db.get(TeamMemberProfile, scenario.profile)).seed_key == "shared-delivery-owner"
        assert await service.bind_profile_seed_key(
            999999, TeamMemberProfileSeedKeyBind(seed_key="x1")) is None
    for bad in ("Has Capitals", "-leading", "", "x" * 101):
        with pytest.raises(ValueError):
            TeamMemberProfileSeedKeyBind(seed_key=bad)


async def test_only_the_operator_can_bind_a_seed_key_over_http(managed_store):
    factory, scenario, tokens, _ = managed_store
    async with factory() as db:
        profile, _ = await _unkeyed_agent(db, scenario, "Imported agent", ["execution"])
        await db.commit()
        profile_id = profile.id
    url = f"/api/team-member-profiles/{profile_id}/seed-key"
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0", "Origin": "https://test"}) as editor:
        denied = await editor.post(url, json={"seed_key": "imported-agent"})
        assert denied.status_code == 403, denied.text
        assert denied.json()["detail"]["code"] == "operator_required"
    async with factory() as db:
        assert (await db.get(TeamMemberProfile, profile_id)).seed_key is None
    async with client(**{"X-Admin-API-Key": "managed-operator-fixture"}) as admin:
        done = await admin.post(url, json={"seed_key": "imported-agent", "reason": "Adopt"})
        assert done.status_code == 200, done.text
        assert done.json()["seed_key"] == "imported-agent"
        again = await admin.post(url, json={"seed_key": "other-key"})
        assert again.status_code == 409, again.text
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(CommandAudit).where(
            CommandAudit.action == "team_member_profile_seed_key_bound")) == 1


async def _agent_attempt(factory, scenario, monkeypatch=None, role="pm"):
    async with factory() as db:
        profile, _ = await _unkeyed_agent(db, scenario, "Imported agent", ["execution"])
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.role = role
        actor.scopes = '["tasks:read","team:read","team:write"]'
        await db.commit()
        return profile.id


async def test_agent_key_cannot_bind_a_seed_key_in_trusted_local_mode(delivery_store, monkeypatch):
    from app.config import get_settings
    factory, scenario, _ = delivery_store
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    try:
        profile_id = await _agent_attempt(factory, scenario)
        async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
            denied = await agent.post(
                f"/api/team-member-profiles/{profile_id}/seed-key", json={"seed_key": "agent-chosen"})
        assert denied.status_code == 403, denied.text
        assert denied.json()["detail"]["code"] == "operator_required"
        async with factory() as db:
            assert (await db.get(TeamMemberProfile, profile_id)).seed_key is None
    finally:
        get_settings.cache_clear()


async def test_agent_key_cannot_bind_a_seed_key_in_managed_mode(managed_store):
    factory, scenario, _, _ = managed_store
    profile_id = await _agent_attempt(factory, scenario)
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        denied = await agent.post(
            f"/api/team-member-profiles/{profile_id}/seed-key", json={"seed_key": "agent-chosen"})
    assert denied.status_code == 403, denied.text
    assert denied.json()["detail"]["code"] == "operator_required"
    async with factory() as db:
        assert (await db.get(TeamMemberProfile, profile_id)).seed_key is None


async def test_a_concurrent_binding_is_never_overwritten(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        profile, _ = await _unkeyed_agent(db, scenario, "Contended agent", ["execution"])
        await db.commit()
        profile_id = profile.id
    async with factory() as first, factory() as second:
        # The first session has already read the profile as unkeyed when the second binds.
        assert (await TeamService(first)._get_profile_by_id(profile_id)).seed_key is None
        await TeamService(second).bind_profile_seed_key(
            profile_id, TeamMemberProfileSeedKeyBind(seed_key="second-key"))
        with pytest.raises(PlanningConflict) as lost:
            await TeamService(first).bind_profile_seed_key(
                profile_id, TeamMemberProfileSeedKeyBind(seed_key="first-key"))
        assert lost.value.code == "profile_seed_key_already_bound"
    async with factory() as db:
        assert (await db.get(TeamMemberProfile, profile_id)).seed_key == "second-key"
        audits = (await db.scalars(select(CommandAudit).where(
            CommandAudit.action == "team_member_profile_seed_key_bound"))).all()
        assert [row.details["seed_key"] for row in audits] == ["second-key"]
