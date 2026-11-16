"""Advisory runtime observations: who may record and read them, and that dispatch never sees them."""

from datetime import timedelta
import json
from pathlib import Path

import pytest
from sqlalchemy import func, select

from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment, AgentTeamTopologyMember, TaskEvent
from app.models.runtime_observation import AgentRuntimeObservation
from app.services.agent_team_setup_service import AgentTeamSetupService
from app.utils.time import utc_now
from tests.test_agent_team_setup import operator
from tests.test_agent_team_setup_qualification import provision_ready_topology
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store
from tests.test_observer_sessions import approve_with, bearer, exchange, local_store, pair_managed, start

ROOT = Path(__file__).resolve().parents[1]
DISPATCH_MODULES = ("agent_work_service.py", "agent_routing_service.py", "agent_routing_policy.py",
                    "agent_team_setup_service.py", "agent_readiness.py", "agent_service.py",
                    "agent_model_catalog_service.py", "agent_routing_rollout.py")


def observation(key="obs-1", **overrides):
    return {"kind": "session_active", "harness_kind": "claude-code", "harness_session_id": "7f3c2a10",
            "observed_at": utc_now().isoformat(), "idempotency_key": key, **overrides}


async def pair_local(label="Desk reader"):
    connection = (await start(label=label)).json()
    async with client() as browser:
        await browser.get("/api/session/whoami")
        await approve_with(browser, connection, label)
    return (await exchange(connection)).json()["access_token"]


async def test_a_local_observer_records_advisory_observations_once(local_store):
    _, scenario, _ = local_store
    token = await pair_local()
    task = scenario.tasks["planned"]
    async with bearer(token) as observer:
        created = await observer.post("/api/agent/observations",
                                      json=observation(task_id=task, subject_actor_id=scenario.actors[0]))
        assert created.status_code == 201, created.text
        row = created.json()
        assert row["advisory"] is True and row["affects_dispatch"] is False
        assert row["observer_label"] == "Desk reader" and row["task_id"] == task
        replay = await observer.post("/api/agent/observations",
                                     json=observation(task_id=task, subject_actor_id=scenario.actors[0],
                                                      observed_at=row["observed_at"]))
        assert replay.status_code == 200 and replay.json()["id"] == row["id"]
        reused = await observer.post("/api/agent/observations", json=observation(kind="session_ended", task_id=task))
        assert reused.status_code == 409, reused.text
        missing_model = await observer.post("/api/agent/observations", json=observation("obs-2", kind="model_observed"))
        assert missing_model.status_code == 422
        model = await observer.post("/api/agent/observations",
                                    json=observation("obs-3", kind="model_observed", observed_model="model-a"))
        assert model.status_code == 201, model.text
        assert {item["id"] for item in (await observer.get("/api/agent/observations", params={"task_id": task})).json()} == {row["id"]}
    async with client() as browser:
        refused = await browser.post("/api/agent/observations", json=observation("obs-4"))
        assert refused.status_code == 403 and refused.json()["detail"]["code"] == "observer_required"
        assert len((await browser.get("/api/agent/observations")).json()) == 2


@pytest.mark.parametrize("harness", [{"harness_session_id": "/home/me/.claude/7f3c.jsonl"},
                                     {"harness_kind": "Claude Code"},
                                     {"observed_at": "2026-01-01T00:00:00+00:00"}])
async def test_malformed_observations_are_refused(local_store, harness):
    token = await pair_local()
    async with bearer(token) as observer:
        assert (await observer.post("/api/agent/observations", json=observation(**harness))).status_code == 422


async def test_managed_observations_follow_task_access_and_agents_cannot_use_them(managed_store):
    factory, scenario, tokens, _ = managed_store
    async with factory() as db:
        db.add(AgentTaskAssignment(task_id=scenario.tasks["planned"], actor_id=scenario.actors[0],
                                   purpose="execution", state="accepted", task_version=1))
        await db.commit()
    grant = await pair_managed(tokens[0], "csrf-0")
    async with bearer(grant["access_token"]) as observer:
        created = await observer.post("/api/agent/observations", json=observation(
            task_id=scenario.tasks["planned"], subject_actor_id=scenario.actors[0]))
        assert created.status_code == 201, created.text
        hidden = await observer.post("/api/agent/observations",
                                     json=observation("obs-2", task_id=scenario.tasks["other_project"]))
        assert hidden.status_code == 404
        unverifiable = await observer.post("/api/agent/observations", json=observation(
            "obs-3", task_id=scenario.tasks["planned"], subject_actor_id=scenario.actors[1]))
        assert unverifiable.status_code == 422
    headers = {"X-CSRF-Token": "csrf-0", "Origin": "https://test"}
    async with client(tokens[0], **headers) as person:
        assert (await person.post("/api/agent/observations", json=observation("obs-4"))).status_code == 403
        assert [row["id"] for row in (await person.get("/api/agent/observations")).json()] == [created.json()["id"]]
    async with client(tokens[1]) as other:
        assert (await other.get("/api/agent/observations")).json() == []
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        assert (await agent.get("/api/agent/observations")).status_code == 403
        assert (await agent.post("/api/agent/observations", json=observation("obs-5"))).status_code == 403


async def test_an_observer_is_capped_per_hour(local_store, monkeypatch):
    monkeypatch.setenv("AGENT_OBSERVATION_HOURLY_LIMIT", "2")
    get_settings.cache_clear()
    token = await pair_local()
    async with bearer(token) as observer:
        for key in ("a", "b"):
            assert (await observer.post("/api/agent/observations", json=observation(key))).status_code == 201
        limited = await observer.post("/api/agent/observations", json=observation("c"))
        assert limited.status_code == 429 and limited.json()["detail"]["code"] == "observation_limit"


async def test_operators_remove_observations_past_retention(managed_store):
    factory, _, tokens, _ = managed_store
    async with factory() as db:
        for key, age in (("old", timedelta(days=31)), ("recent", timedelta(days=1))):
            db.add(AgentRuntimeObservation(kind="session_ended", harness_kind="codex", harness_session_id="thread-1",
                                           idempotency_key=key, observed_at=utc_now() - age, received_at=utc_now() - age))
        await db.commit()
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0", "Origin": "https://test"}) as person:
        assert (await person.post("/api/agent/observations/cleanup")).status_code == 403
    async with client(**{"X-Admin-API-Key": "managed-operator-fixture"}) as operator_client:
        cleaned = await operator_client.post("/api/agent/observations/cleanup")
        assert cleaned.status_code == 200, cleaned.text
        assert cleaned.json() == {"removed": 1, "retention_days": 30, "limit": 500}
    async with factory() as db:
        assert (await db.scalars(select(AgentRuntimeObservation.idempotency_key))).all() == ["recent"]


def test_no_dispatch_code_reads_observations():
    """Routing, readiness, assignment and work decisions never import or query the observation table."""
    for name in DISPATCH_MODULES:
        source = (ROOT / "app" / "services" / name).read_text(encoding="utf-8")
        assert "runtime_observation" not in source and "AgentRuntimeObservation" not in source, name


@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_recording_observations_changes_nothing_dispatch_reads(local_store, monkeypatch):
    fixed = utc_now()
    monkeypatch.setattr("app.services.agent_team_setup_service.utc_now", lambda: fixed)
    factory, _, _ = local_store
    async with factory() as db:
        ready = await provision_ready_topology(db)
        await db.commit()

    async def snapshot():
        async with factory() as db:
            service = AgentTeamSetupService(db)
            status = await service.status(operator(), topology_key=ready.manifest.topology_key)
            report = await service.report(operator(), topology_key=ready.manifest.topology_key)
            actors = [(row.id, row.last_seen_at, row.queue_revision, row.lifecycle_state, row.enabled, row.scopes)
                      for row in (await db.scalars(select(AgentActor).order_by(AgentActor.id))).all()]
            members = [(row.id, row.updated_at, row.lifecycle_state)
                       for row in (await db.scalars(select(AgentTeamTopologyMember).order_by(AgentTeamTopologyMember.id))).all()]
            counts = [await db.scalar(select(func.count()).select_from(model))
                      for model in (AgentTaskAssignment, AgentRun, TaskEvent)]
            return status.model_dump(mode="json"), report.availability, actors, members, counts

    before = await snapshot()
    token = await pair_local()
    async with bearer(token) as observer:
        for index, actor in enumerate(ready.actors.values()):
            for kind, extra in (("session_ended", {}), ("model_observed", {"observed_model": "another-model"})):
                response = await observer.post("/api/agent/observations", json=observation(
                    f"{kind}-{index}", kind=kind, subject_actor_id=actor.id, **extra))
                assert response.status_code == 201, response.text
    after = await snapshot()
    assert after == before
    assert after[1] == "availability_unknown"
    assert all(member["availability"] == "availability_unknown" for member in after[0]["members"])
