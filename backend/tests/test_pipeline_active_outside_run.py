"""Active work with no WorkChord run is shown in its own pipeline stage."""

import json
from datetime import date, timedelta

from sqlalchemy import select

from app import mcp_agent_tools
from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.calendar import Calendar
from app.models.identity import Principal, WorkspaceAuthorityState
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_managed_authority import client

KEY = "pipeline-outside-run-key"


async def seed(factory):
    async with factory() as db:
        if await db.get(WorkspaceAuthorityState, 1) is None:
            system = Principal(kind="system", display_name="Operator API")
            db.add(system)
            await db.flush()
            db.add(WorkspaceAuthorityState(id=1, operator_principal_id=system.id))
        profile = TeamMemberProfile(seed_key="outside-run-agent", display_name="Outside Agent",
                                    automation_enabled=True, profile_kind="agent", assignment_modes=["execution"])
        iteration = Iteration(name="Outside run iteration", start_date=date(2026, 7, 1), end_date=date(2026, 7, 31),
                              calendar=Calendar(name="Outside run calendar", year=2026))
        db.add_all([profile, iteration])
        await db.flush()
        actor = AgentActor(name="outside-run-actor", display_name="Outside Actor", api_key_hash="outside-run-hash",
                           scopes=json.dumps(["work:execute"]), enabled=True, role="worker", profile_id=profile.id)
        owner = TeamMember(name="Capacity Agent", position="Agent", iteration_id=iteration.id, profile_id=profile.id)
        db.add_all([actor, owner])
        await db.flush()

        def task(title, **values):
            created = Task(title=title, iteration_id=iteration.id, assignee_id=owner.id, **values)
            db.add(created)
            return created

        outside = task("Delivered outside WorkChord", status="active")
        claimed = task("Claimed by an agent", status="active", claimed_by=actor.id,
                       claim_id="claim-live", claim_expires_at=utc_now() + timedelta(hours=1))
        stale = task("Claim expired", status="active", claimed_by=actor.id,
                     claim_id="claim-stale", claim_expires_at=utc_now() - timedelta(hours=1))
        running = task("Run in progress", status="active")
        planned = task("Not started", status="planned")
        await db.flush()
        db.add(AgentRun(task_id=running.id, actor_id=actor.id, status="running"))
        await db.commit()
        ids = {"outside": outside.id, "claimed": claimed.id, "stale": stale.id,
               "running": running.id, "planned": planned.id}
        return ids, owner.id


def stage_of(pipeline, task_id):
    stages = [stage for stage, tasks in pipeline.items() if task_id in {item["id"] for item in tasks}]
    assert len(stages) == 1, (task_id, stages)
    return stages[0]


async def test_active_task_without_a_run_is_its_own_stage_on_rest_and_mcp(delivery_store, monkeypatch):
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", KEY)
    get_settings.cache_clear()
    factory, _, _ = delivery_store
    ids, owner_id = await seed(factory)

    async with client() as reader:
        response = await reader.get("/api/agent/pipeline")
    assert response.status_code == 200, response.text
    rest = response.json()
    async with factory() as db:
        mcp = await mcp_agent_tools.get_agent_pipeline(db, None)

    for pipeline in (rest, mcp):
        assert "active_outside_run" in pipeline
        assert stage_of(pipeline, ids["outside"]) == "active_outside_run"
        assert stage_of(pipeline, ids["claimed"]) == "executing"
        assert stage_of(pipeline, ids["running"]) == "executing"
        assert stage_of(pipeline, ids["stale"]) == "recovery_required"
        assert stage_of(pipeline, ids["planned"]) in {"needs_definition", "ready_to_assign"}
        [outside] = [item for item in pipeline["active_outside_run"] if item["id"] == ids["outside"]]
        assert outside["assignee"]["id"] == owner_id
        assert outside["assignee"]["kind"] == "agent"
        assert outside["claimed_by"] is None


async def test_every_open_task_appears_in_exactly_one_stage(delivery_store):
    factory, _, _ = delivery_store
    await seed(factory)
    async with factory() as db:
        pipeline = await mcp_agent_tools.get_agent_pipeline(db, None)
        open_ids = set((await db.scalars(
            select(Task.id).where(Task.status != "closed", Task.is_deferred == False)  # noqa: E712
        )).all())
    listed = [item["id"] for tasks in pipeline.values() for item in tasks]
    assert len(listed) == len(set(listed))
    assert set(listed) == open_ids


async def test_outside_run_task_is_not_offered_for_recovery(delivery_store):
    factory, _, _ = delivery_store
    ids, _ = await seed(factory)
    async with factory() as db:
        assert await db.scalar(
            select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == ids["outside"])
        ) is None
        pipeline = await mcp_agent_tools.get_agent_pipeline(db, None)
    assert ids["outside"] not in {item["id"] for item in pipeline["recovery_required"]}
