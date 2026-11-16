"""People read the assignments of tasks they can see; agent keys keep the full projection."""

from datetime import timedelta
import json

from app.models.agent import AgentActor, AgentModelBinding, AgentModelCatalogEntry, AgentTaskAssignment
from app.models.identity import Principal
from app.models.task import Task
from app.models.user_session import UserSession
from app.services.identity_service import digest
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store
from tests.test_observer_sessions import bearer, local_store, pair_managed


AGENT_ONLY_FIELDS = {"routing_snapshot", "reason", "reviewer_profile_id", "assigned_by_actor_id"}


async def seed_assignments(factory, scenario):
    async with factory() as db:
        catalog = AgentModelCatalogEntry(key="balanced-code", provider="configured-provider",
            configured_model_alias="balanced-code", reasoning_tier=2, context_tier="medium", modality_tags=["text"],
            cost_tier="medium", latency_tier="balanced", enabled=True, revision=1)
        db.add(catalog)
        await db.flush()
        binding = AgentModelBinding(actor_id=scenario.actors[0], model_catalog_id=catalog.id, is_default=True, enabled=True)
        db.add(binding)
        await db.flush()
        own = await db.get(Task, scenario.tasks["planned"])
        other = await db.get(Task, scenario.tasks["other_project"])
        db.add_all([
            AgentTaskAssignment(task_id=own.id, actor_id=scenario.actors[0], purpose="execution", state="queued",
                task_version=own.version, model_binding_id=binding.id, model_binding_revision=binding.revision,
                reason="Private planning note", routing_snapshot=json.dumps({"candidates": [1, 2]})),
            AgentTaskAssignment(task_id=other.id, actor_id=scenario.actors[1], purpose="verification", state="queued",
                task_version=other.version),
        ])
        await db.commit()


async def assignments(response):
    assert response.status_code == 200, response.text
    return response.json()


async def test_a_person_reads_assignments_of_visible_tasks_without_routing_evidence(managed_store):
    factory, scenario, tokens, _ = managed_store
    await seed_assignments(factory, scenario)
    async with client(tokens[0]) as person:
        rows = await assignments(await person.get("/api/agent/assignments"))
        assert [row["task_id"] for row in rows] == [scenario.tasks["planned"]]
        row = rows[0]
        assert row["actor"] == {"id": scenario.actors[0], "name": "delivery-worker", "display_name": "Worker", "role": "worker"}
        assert row["purpose"] == "execution" and row["state"] == "queued"
        assert row["model"] == {"model_catalog_key": "balanced-code", "provider": "configured-provider",
                                "configured_model_alias": "balanced-code"}
        # The binding is read internally, so a project-only reader does not see it as missing.
        assert row["model_binding_status"] == "current" and row["model_binding_stale_reasons"] == []
        assert AGENT_ONLY_FIELDS.isdisjoint(row)
        hidden = await person.get("/api/agent/assignments", params={"task_id": scenario.tasks["other_project"]})
        assert await assignments(hidden) == []
        response = await person.get("/api/agent/assignments")
        assert "Private planning note" not in response.text and "candidates" not in response.text
    async with client(tokens[1]) as other:
        rows = await assignments(await other.get("/api/agent/assignments"))
        assert [(row["task_id"], row["purpose"], row["model"]) for row in rows] == [
            (scenario.tasks["other_project"], "verification", None)]


async def test_a_person_without_any_work_cannot_list_assignments(managed_store):
    factory, scenario, _, _ = managed_store
    await seed_assignments(factory, scenario)
    token = "c" * 43
    async with factory() as db:
        outsider = Principal(kind="human", display_name="Outsider")
        db.add(outsider)
        await db.flush()
        db.add(UserSession(principal_id=outsider.id, session_token_hash=digest(token), csrf_token="csrf-2",
            ip_address="192.0.2.1", authenticated_at=utc_now(), expires_at=utc_now() + timedelta(hours=1)))
        await db.commit()
    async with client(token) as person:
        assert (await person.get("/api/agent/assignments")).status_code == 401
    async with client() as anonymous:
        assert (await anonymous.get("/api/agent/assignments")).status_code == 401


async def test_an_agent_key_keeps_the_full_projection(managed_store):
    factory, scenario, _, _ = managed_store
    await seed_assignments(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = json.dumps(["tasks:read", "planning:read"])
        await db.commit()
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        rows = await assignments(await agent.get("/api/agent/assignments"))
    assert [row["task_id"] for row in rows] == [scenario.tasks["planned"]]
    assert rows[0]["reason"] == "Private planning note"
    assert rows[0]["routing_snapshot"] == {"candidates": [1, 2]}
    assert "actor" not in rows[0]


async def test_an_observer_reads_the_assignments_its_person_can_read(managed_store):
    factory, scenario, tokens, _ = managed_store
    await seed_assignments(factory, scenario)
    grant = await pair_managed(tokens[0], "csrf-0")
    async with bearer(grant["access_token"]) as observer:
        rows = await assignments(await observer.get("/api/agent/assignments"))
    assert [row["task_id"] for row in rows] == [scenario.tasks["planned"]]
    assert AGENT_ONLY_FIELDS.isdisjoint(rows[0])


async def test_a_trusted_local_browser_reads_every_assignment(local_store):
    factory, scenario, _ = local_store
    await seed_assignments(factory, scenario)
    async with client() as browser:
        rows = await assignments(await browser.get("/api/agent/assignments"))
        assert sorted(row["task_id"] for row in rows) == sorted([scenario.tasks["planned"], scenario.tasks["other_project"]])
        filtered = await assignments(await browser.get("/api/agent/assignments", params={"purpose": "verification"}))
        assert [row["task_id"] for row in filtered] == [scenario.tasks["other_project"]]
