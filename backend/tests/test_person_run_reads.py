"""People read the runs of tasks they can see; run logs stay behind keys."""

from datetime import timedelta
import importlib
import json

from app.models.agent import AgentActor, AgentRun
from app.schemas.agent import AgentRunCreate, declared_harness
from app.services.execution_usage_service import ExecutionUsageService
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_execution_usage import usage
from tests.test_managed_authority import client, managed_store
from tests.test_observer_sessions import bearer, local_store, pair_managed

LOG_FIELDS = {"events", "summary", "error", "artifact_links", "commit_url", "pr_url", "metadata", "idempotency_key"}


async def seed_runs(factory, scenario):
    now = utc_now()
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["runs:write","tasks:read","work:execute"]'
        own = AgentRun(task_id=scenario.tasks["planned"], actor_id=actor.id, status="running",
                       started_at=now - timedelta(minutes=5), trace_id="external-run-1", harness_kind="claude-code",
                       harness_session_id="7f3c2a10", run_metadata=json.dumps({"harness": {
                           "kind": "claude-code", "session_id": "7f3c2a10"}, "private": "worker note"}),
                       summary="Private summary", model="model-a")
        other = AgentRun(task_id=scenario.tasks["other_project"], actor_id=scenario.actors[1], status="succeeded",
                         started_at=now - timedelta(minutes=9), ended_at=now - timedelta(minutes=1))
        db.add_all([own, other])
        await db.commit()
        ids = own.id, other.id
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        await ExecutionUsageService(db).write(actor, ids[0], usage(now))
    return ids


async def runs(response):
    assert response.status_code == 200, response.text
    return response.json()


async def test_a_person_reads_runs_of_visible_tasks_without_logs(managed_store):
    factory, scenario, tokens, _ = managed_store
    own, other = await seed_runs(factory, scenario)
    async with client(tokens[0]) as person:
        rows = await runs(await person.get("/api/agent/runs"))
        assert [row["id"] for row in rows] == [own]
        row = rows[0]
        assert row["harness"] == {"kind": "claude-code", "session_id": "7f3c2a10"}
        assert row["actor"]["name"] == "delivery-worker" and row["status"] == "running" and row["model"] == "model-a"
        assert row["usage"]["report"]["report_id"] == "attempt-total" and row["usage"]["independently_reconciled"] is False
        assert LOG_FIELDS.isdisjoint(row)
        found = await runs(await person.get("/api/agent/runs", params={"harness_session_id": "7f3c2a10"}))
        assert [item["id"] for item in found] == [own]
        assert await runs(await person.get("/api/agent/runs", params={"harness_session_id": "unknown"})) == []
        assert await runs(await person.get("/api/agent/runs", params={"task_id": scenario.tasks["other_project"]})) == []
        text = (await person.get("/api/agent/runs")).text
        assert "Private summary" not in text and "worker note" not in text
        # Run detail, with its events and logs, still needs a key.
        assert (await person.get(f"/api/agent/runs/{own}")).status_code in {401, 403, 503}
    async with client(tokens[1]) as other_person:
        assert [row["id"] for row in await runs(await other_person.get("/api/agent/runs"))] == [other]


async def test_an_observer_reads_runs_and_anonymous_callers_cannot(managed_store):
    factory, scenario, tokens, _ = managed_store
    own, _ = await seed_runs(factory, scenario)
    grant = await pair_managed(tokens[0], "csrf-0")
    async with bearer(grant["access_token"]) as observer:
        assert [row["id"] for row in await runs(await observer.get("/api/agent/runs"))] == [own]
    async with client() as anonymous:
        assert (await anonymous.get("/api/agent/runs")).status_code == 401


async def test_an_agent_key_needs_planning_read(managed_store):
    factory, scenario, _, _ = managed_store
    own, _ = await seed_runs(factory, scenario)
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        assert (await agent.get("/api/agent/runs")).status_code == 403
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["tasks:read","planning:read"]'
        await db.commit()
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        assert [row["id"] for row in await runs(await agent.get("/api/agent/runs"))] == [own]


async def test_a_trusted_local_browser_reads_every_run_and_filters(local_store):
    factory, scenario, _ = local_store
    own, other = await seed_runs(factory, scenario)
    async with client() as browser:
        assert {row["id"] for row in await runs(await browser.get("/api/agent/runs"))} == {own, other}
        assert [row["id"] for row in await runs(await browser.get("/api/agent/runs", params={"status": "succeeded"}))] == [other]
        assert [row["id"] for row in await runs(await browser.get("/api/agent/runs", params={
            "actor_id": scenario.actors[0], "harness_kind": "claude-code"}))] == [own]


def test_the_declared_harness_is_read_from_validated_metadata():
    metadata = AgentRunCreate(task_id=1, metadata={"harness": {"kind": "codex", "session_id": "thread-1"}}).metadata
    assert declared_harness(metadata) == ("codex", "thread-1")
    assert declared_harness({"other": 1}) == (None, None)


def test_the_migration_backfills_only_valid_declarations():
    migration = importlib.import_module("app.migrations.versions.20261116_0017_run_harness_session")
    assert migration._declared(json.dumps({"harness": {"kind": "claude-code", "session_id": "7f3c"}})) == ("claude-code", "7f3c")
    for invalid in ("not json", "{}", json.dumps({"harness": {"kind": "Claude", "session_id": "7f3c"}}),
                    json.dumps({"harness": {"kind": "codex", "session_id": "/home/me/s.jsonl"}}),
                    json.dumps({"harness": {"kind": "codex"}})):
        assert migration._declared(invalid) is None


async def test_a_started_run_keeps_its_declared_harness_session(local_store):
    from app.services.agent_service import AgentService

    factory, scenario, _ = local_store
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["runs:write","tasks:read"]'
        await db.commit()
        run = await AgentService(db).start_run(actor, AgentRunCreate(
            task_id=scenario.tasks["planned"], metadata={"harness": {"kind": "codex", "session_id": "thread-9"}}))
        assert (run.harness_kind, run.harness_session_id) == ("codex", "thread-9")
