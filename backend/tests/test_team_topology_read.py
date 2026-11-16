"""The team topology read names members, model bindings and runtime references, never credentials."""

from datetime import timedelta
import json

import pytest

from app.mcp_server import mcp
from app.models.agent import AgentActor
from app.models.identity import Principal, WorkspaceMembership
from app.models.user_session import UserSession
from app.services.agent_service import AgentPermissionError
from app.services.agent_team_setup_service import AgentTeamSetupService
from app.services.identity_service import digest
from app.utils.time import utc_now
from tests.test_agent_team_setup import operator
from tests.test_agent_team_setup_qualification import provision_ready_topology
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store
from tests.test_observer_sessions import bearer, local_store, pair_managed


# Team setup checks role packages against a built release catalog.
pytestmark = pytest.mark.usefixtures("deployed_agent_skill_release")


def assert_no_credentials(payload):
    text = json.dumps(payload)
    assert "credential_ref" not in text and "pmag_" not in text and "handoff" not in text


async def test_operator_reads_members_bindings_and_runtime_references(db_session):
    ready = await provision_ready_topology(db_session)
    topology = await AgentTeamSetupService(db_session).topology(operator())
    assert topology.topology_key == ready.manifest.topology_key
    assert topology.topology_state == "runtime_ready" and topology.availability == "availability_unknown"
    expected = {member.actor_key: member for member in ready.manifest.all_members}
    assert {member.actor_key for member in topology.members} == set(expected)
    for member in topology.members:
        spec = expected[member.actor_key]
        assert member.runtime_ref == spec.runtime_ref
        assert member.default_model_binding_key == spec.default_model_binding_key
        assert member.model_binding_keys == spec.model_binding_keys
        assert member.actor_id == ready.actors[member.actor_key].id
        assert member.runtime_ready is True and member.role == spec.role
    assert_no_credentials(topology.model_dump(mode="json"))


async def test_a_pm_reads_only_its_bound_team_and_a_worker_cannot_read_it(db_session):
    ready = await provision_ready_topology(db_session)
    service = AgentTeamSetupService(db_session)
    pm = next(actor for actor in ready.actors.values() if actor.role == "pm")
    assert (await service.topology(pm)).topology_key == ready.manifest.topology_key
    with pytest.raises(AgentPermissionError):
        await service.topology(pm, topology_key="another-team")
    worker = next(actor for actor in ready.actors.values() if actor.role == "worker")
    with pytest.raises(AgentPermissionError):
        await service.topology(worker)


async def test_an_absent_team_reads_as_absent(db_session):
    topology = await AgentTeamSetupService(db_session).topology(None)
    assert topology.topology_state == "absent" and topology.members == ()


async def test_mcp_registers_the_topology_read_as_read_only():
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert tools["agent_get_team_topology"].annotations.readOnlyHint is True


async def test_workspace_people_and_their_observers_read_the_team_but_project_roles_do_not(managed_store):
    factory, _, tokens, people = managed_store
    async with factory() as db:
        ready = await provision_ready_topology(db)
        db.add(WorkspaceMembership(principal_id=people[1], role="member"))
        await db.commit()
    async with client(tokens[0]) as project_only:
        refused = await project_only.get("/api/agent/team-setup/topology")
        assert refused.status_code == 401, refused.text
    async with client(tokens[1]) as member:
        response = await member.get("/api/agent/team-setup/topology")
        assert response.status_code == 200, response.text
        assert response.headers["cache-control"] == "private, no-store"
    payload = response.json()
    assert payload["topology_key"] == ready.manifest.topology_key
    assert sorted(member["runtime_ref"] for member in payload["members"]) == sorted(
        member.runtime_ref for member in ready.manifest.all_members)
    assert_no_credentials(payload)
    grant = await pair_managed(tokens[1], "csrf-1")
    async with bearer(grant["access_token"]) as observer:
        observed = await observer.get("/api/agent/team-setup/topology")
        assert observed.status_code == 200, observed.text
        assert observed.json()["members"] == payload["members"]
    async with client() as anonymous:
        assert (await anonymous.get("/api/agent/team-setup/topology")).status_code == 401


async def test_an_agent_key_without_team_authority_is_refused_over_http(managed_store):
    factory, _, _, _ = managed_store
    async with factory() as db:
        ready = await provision_ready_topology(db)
        await db.commit()
    worker_key = next(key for actor_key, key in ready.sink.keys.items()
                      if ready.actors[actor_key].role == "worker")
    async with client(**{"X-Agent-API-Key": worker_key}) as worker:
        response = await worker.get("/api/agent/team-setup/topology")
        assert response.status_code == 403, response.text


async def test_a_trusted_local_browser_reads_the_team(local_store):
    factory, _, _ = local_store
    async with factory() as db:
        ready = await provision_ready_topology(db)
        await db.commit()
    async with client() as browser:
        response = await browser.get("/api/agent/team-setup/topology",
                                     params={"topology_key": ready.manifest.topology_key})
        assert response.status_code == 200, response.text
        assert len(response.json()["members"]) == len(ready.manifest.all_members)
