"""Run detail returns the stored execution provenance through REST and MCP alike."""

from datetime import timedelta

import httpx
import pytest

from app import mcp_agent_tools
from app.main import app
from app.models.agent import AgentActor, AgentRun
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


def fresh_provenance(actor_id):
    return {
        "actor_id": actor_id,
        "profile_id": 7,
        "profile_revision": "p7-0123456789abcdef01234567",
        "publisher_key": "model-maker-a",
        "source": "authenticated_work_begin",
    }


def reconciled_provenance(actor_id):
    # Historical evidence: the profile was recovered, the publisher stays unknown and is not filled in.
    return {
        "actor_id": actor_id,
        "profile_id": 38,
        "profile_revision": None,
    }


@pytest.mark.parametrize("build", [fresh_provenance, reconciled_provenance], ids=["fresh", "reconciled"])
async def test_run_detail_rest_and_mcp_return_the_same_stored_provenance(delivery_store, build):
    factory, scenario, _ = delivery_store
    now = utc_now()
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["planning:read","tasks:read"]'
        provenance = build(actor.id)
        run = AgentRun(task_id=scenario.tasks["planned"], actor_id=actor.id, status="succeeded",
                       started_at=now - timedelta(seconds=10), ended_at=now, execution_provenance=provenance)
        db.add(run)
        await db.commit()
        run_id = run.id

    headers = {"X-Agent-API-Key": scenario.actor_keys[0]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/api/agent/runs/{run_id}", headers=headers)
    assert response.status_code == 200, response.text
    rest = response.json()

    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        mcp = await mcp_agent_tools.get_agent_run_detail(db, actor, run_id)

    assert rest["execution_provenance"] == provenance
    assert mcp["execution_provenance"] == provenance
    assert rest["execution_provenance"] == mcp["execution_provenance"]
    if build is reconciled_provenance:
        assert "publisher_key" not in rest["execution_provenance"]
        assert rest["execution_provenance"]["profile_revision"] is None
