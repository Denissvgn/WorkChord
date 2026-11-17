"""Team-member responses say whether an agent is connected, to every reader, without naming it."""

import pytest

from app.models.agent import AgentActor
from app.models.identity import WorkspaceMembership
from app.models.team_member import TeamMember, TeamMemberProfile
from app.services.agent_service import hash_api_key
from tests.test_delivery_scenarios import delivery_store  # noqa: F401 - fixture used by managed_store
from tests.test_managed_authority import client, managed_store  # noqa: F401 - fixture


COMPACT_PROFILE_FIELDS = {
    "id", "display_name", "email", "headline", "automation_enabled", "profile_kind",
    "assignment_modes", "skills", "agent_connected",
}
SECRET_KEYS = ("connected-builder-secret-key", "disabled-builder-secret-key", "onboarding-builder-secret-key")


async def _seed_agent_members(factory, scenario, people, *, workspace_member=True):
    """One connected agent, one whose only actor is disabled, one still onboarding, beside the human row."""
    async with factory() as db:
        connected, disabled, onboarding = (
            TeamMemberProfile(display_name=name, profile_kind="agent", automation_enabled=True)
            for name in ("Connected agent", "Disabled agent", "Onboarding agent")
        )
        connected.email, connected.headline = "connected-agent@example.test", "Builds the release"
        db.add_all([connected, disabled, onboarding])
        await db.flush()
        db.add_all([
            AgentActor(name="connected-builder", display_name="Connected builder", role="worker",
                       api_key_hash=hash_api_key(SECRET_KEYS[0]), scopes='["tasks:read"]',
                       profile_id=connected.id),
            AgentActor(name="disabled-builder", display_name="Disabled builder", role="worker",
                       api_key_hash=hash_api_key(SECRET_KEYS[1]), scopes='["tasks:read"]',
                       enabled=False, lifecycle_state="disabled", profile_id=disabled.id),
            AgentActor(name="onboarding-builder", display_name="Onboarding builder", role="worker",
                       api_key_hash=hash_api_key(SECRET_KEYS[2]), scopes='["tasks:read"]',
                       enabled=False, lifecycle_state="onboarding", profile_id=onboarding.id),
            WorkspaceMembership(principal_id=people[1], role="owner"),
        ])
        if workspace_member:
            # A plain workspace member: not an owner or operator, and holding no agent or admin key.
            # Without it the same person is only an editor of the iteration's project.
            db.add(WorkspaceMembership(principal_id=people[0], role="member"))
        # The scenario's worker agent is a member of the project; let its key read the team.
        (await db.get(AgentActor, scenario.actors[0])).scopes = '["tasks:read","team:read"]'
        for profile in (connected, disabled, onboarding):
            db.add(TeamMember(name=profile.display_name, position="Agent", profile_id=profile.id,
                              iteration_id=scenario.iterations[0]))
        await db.commit()
        return (
            {"Connected agent": True, "Disabled agent": False, "Onboarding agent": False, "Shared owner": False},
            {connected.id, disabled.id, onboarding.id},
        )


READERS = {
    "workspace member": lambda tokens, scenario: client(tokens[0]),
    "workspace owner": lambda tokens, scenario: client(tokens[1]),
    "operator key": lambda tokens, scenario: client(**{"X-Admin-API-Key": "managed-operator-fixture"}),
    # These two read the project's team rows but not the profiles themselves.
    "project-only member": lambda tokens, scenario: client(tokens[0]),
    "project-scoped agent key": lambda tokens, scenario: client(**{"X-Agent-API-Key": scenario.actor_keys[0]}),
}
PROFILE_READERS = {"workspace member", "workspace owner", "operator key"}


@pytest.mark.parametrize("reader", list(READERS))
async def test_every_reader_sees_agent_connected_on_the_embedded_profile(managed_store, reader):
    factory, scenario, tokens, people = managed_store
    expected, agent_profiles = await _seed_agent_members(
        factory, scenario, people, workspace_member=reader != "project-only member")
    async with READERS[reader](tokens, scenario) as caller:
        response = await caller.get(f"/api/iterations/{scenario.iterations[0]}/team")
    assert response.status_code == 200, response.text
    members = {member["name"]: member for member in response.json()}
    assert {name: members[name]["profile"]["agent_connected"] for name in expected} == expected
    assert {members[name]["profile"]["id"] for name in expected} >= agent_profiles
    assert {name: members[name]["profile"]["profile_kind"] for name in expected} == {
        name: "human" if name == "Shared owner" else "agent" for name in expected}
    for member in members.values():
        # The compact profile carries the flag and nothing that identifies or unlocks the agent.
        assert set(member["profile"]) == COMPACT_PROFILE_FIELDS
        assert member["profile"]["id"] == member["profile_id"]
        if reader not in PROFILE_READERS:
            assert (member["profile"]["email"], member["profile"]["headline"], member["profile"]["skills"]) == (None, None, [])
    connected = members["Connected agent"]["profile"]
    if reader in PROFILE_READERS:
        assert (connected["email"], connected["headline"]) == ("connected-agent@example.test", "Builds the release")
    else:
        # A reader who cannot read the profile itself gets no personal profile details.
        assert "connected-agent@example.test" not in response.text
    _assert_names_no_agent(response.text)


async def test_reader_without_profile_access_still_cannot_read_the_profile(managed_store):
    """The team row carries the reader-safe part; the profile endpoints stay closed to that reader."""
    factory, scenario, tokens, people = managed_store
    _, agent_profiles = await _seed_agent_members(factory, scenario, people, workspace_member=False)
    async with client(tokens[0]) as member:
        listed = await member.get("/api/team-member-profiles")
        single = await member.get(f"/api/team-member-profiles/{min(agent_profiles)}")
    assert listed.status_code == 200, listed.text
    assert not {profile["id"] for profile in listed.json()} & agent_profiles
    assert single.status_code == 404, single.text


def _assert_names_no_agent(text):
    for leaked in ("builder", "Builder", "actor", "api_key", *SECRET_KEYS, *(hash_api_key(key) for key in SECRET_KEYS)):
        assert leaked not in text


@pytest.mark.parametrize("workspace_member", [True, False], ids=["workspace member", "project-only member"])
async def test_single_member_read_carries_agent_connected(managed_store, workspace_member):
    factory, scenario, tokens, people = managed_store
    await _seed_agent_members(factory, scenario, people, workspace_member=workspace_member)
    async with client(tokens[0]) as member:
        team = (await member.get(f"/api/iterations/{scenario.iterations[0]}/team")).json()
        by_name = {row["name"]: row["id"] for row in team}
        connected = await member.get(f"/api/team-members/{by_name['Connected agent']}")
        disabled = await member.get(f"/api/team-members/{by_name['Disabled agent']}")
    assert connected.status_code == 200, connected.text
    assert connected.json()["profile"]["agent_connected"] is True
    assert disabled.json()["profile"]["agent_connected"] is False
    assert set(connected.json()["profile"]) == COMPACT_PROFILE_FIELDS
