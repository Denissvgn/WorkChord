"""The paged assignment listing reads every row in the plain listing's order, within the same scope."""

import json

from sqlalchemy import insert

from app.mcp_agent_tools import list_agent_assignments_page
from app.models.agent import AgentActor, AgentTaskAssignment
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store


async def seed_many(factory, scenario, *, per_task=260):
    """Closed assignments only, so the one-live-row-per-task rule does not apply."""
    rows = []
    for task_key, owner in (("planned", 0), ("other_project", 1)):
        for index in range(per_task):
            rows.append({
                "task_id": scenario.tasks[task_key],
                # Both actors hold rows on both tasks, with many equal ranks.
                "actor_id": scenario.actors[(index + owner) % 2],
                "purpose": "execution" if index % 3 else "verification",
                "state": "fulfilled" if index % 2 else "cancelled",
                "queue_rank": 1000 + index % 4,
                "task_version": 1,
            })
    async with factory() as db:
        await db.execute(insert(AgentTaskAssignment), rows)
        await db.commit()


async def read_all(http, params=None, *, limit):
    items, cursor, pages = [], None, 0
    while True:
        query = {**(params or {}), "limit": limit, **({"cursor": cursor} if cursor else {})}
        response = await http.get("/api/agent/assignments/page", params=query)
        assert response.status_code == 200, response.text
        body = response.json()
        items.extend(body["items"])
        pages += 1
        assert body["has_more"] == (body["next_cursor"] is not None)
        if not body["has_more"]:
            return items, pages
        cursor = body["next_cursor"]


async def test_a_person_reads_more_than_five_hundred_assignments_without_gaps(managed_store):
    factory, scenario, tokens, _ = managed_store
    await seed_many(factory, scenario, per_task=520)
    async with client(tokens[0]) as person:
        items, pages = await read_all(person, limit=500)
        assert pages == 2 and len(items) == 520
        ids = [row["id"] for row in items]
        assert len(set(ids)) == 520
        assert {row["task_id"] for row in items} == {scenario.tasks["planned"]}
        assert [row["task_id"] for row in items] == sorted(row["task_id"] for row in items)
        # The plain listing stays capped and compatible.
        plain = await person.get("/api/agent/assignments", params={"limit": 500})
        assert len(plain.json()) == 500
        assert [row["id"] for row in plain.json()] == ids[:500]
    async with client(tokens[1]) as other:
        items, _ = await read_all(other, limit=500)
        assert {row["task_id"] for row in items} == {scenario.tasks["other_project"]}


async def test_small_pages_follow_the_plain_order_and_keep_filters(managed_store):
    factory, scenario, tokens, _ = managed_store
    await seed_many(factory, scenario, per_task=40)
    async with client(tokens[0]) as person:
        full = (await person.get("/api/agent/assignments", params={"limit": 500})).json()
        items, pages = await read_all(person, limit=7)
        assert pages == 6 and [row["id"] for row in items] == [row["id"] for row in full]
        filtered, _ = await read_all(person, {"purpose": "verification", "state": "cancelled"}, limit=3)
        expected = [row["id"] for row in full if row["purpose"] == "verification" and row["state"] == "cancelled"]
        assert expected and [row["id"] for row in filtered] == expected
        by_actor, _ = await read_all(person, {"actor_id": scenario.actors[1]}, limit=4)
        assert [row["id"] for row in by_actor] == [row["id"] for row in full if row["actor"]["id"] == scenario.actors[1]]
        hidden = await person.get("/api/agent/assignments/page", params={"task_id": scenario.tasks["other_project"]})
        assert hidden.json() == {"items": [], "has_more": False, "next_cursor": None}
        for bad in ("not-a-cursor", "e30"):
            rejected = await person.get("/api/agent/assignments/page", params={"cursor": bad})
            assert rejected.status_code == 400


async def test_an_agent_key_pages_its_own_queue_and_a_planner_pages_the_team(managed_store):
    factory, scenario, _, _ = managed_store
    await seed_many(factory, scenario, per_task=30)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = json.dumps(["assignments:read", "tasks:read"])
        await db.commit()
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as agent:
        own, pages = await read_all(agent, limit=8)
        plain = (await agent.get("/api/agent/assignments", params={"limit": 500})).json()
        assert pages > 1 and [row["id"] for row in own] == [row["id"] for row in plain]
        assert {row["actor_id"] for row in own} == {scenario.actors[0]} and len(own) == 15  # only the task its project can read
        assert "routing_snapshot" in own[0]
        other = await agent.get("/api/agent/assignments/page", params={"actor_id": scenario.actors[1]})
        assert other.status_code == 403
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = json.dumps(["planning:read", "tasks:read"])
        await db.commit()
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as planner:
        team, _ = await read_all(planner, limit=11)
        plain = (await planner.get("/api/agent/assignments", params={"limit": 500})).json()
        # The team queue spans both actors but stays inside the planner's project.
        assert len(team) == 30 and {r["task_id"] for r in team} == {scenario.tasks["planned"]}
        assert {r["actor_id"] for r in team} == set(scenario.actors)
        assert [row["id"] for row in team] == [row["id"] for row in plain]
        assert [(r["actor_id"], r["queue_rank"], r["id"]) for r in team] == sorted(
            (r["actor_id"], r["queue_rank"], r["id"]) for r in team)
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[1]}) as outsider:
        denied = await outsider.get("/api/agent/assignments/page")
        assert denied.status_code == 403


async def test_the_mcp_handler_pages_with_the_same_cursor(managed_store):
    factory, scenario, _, _ = managed_store
    await seed_many(factory, scenario, per_task=15)
    async with factory() as db:
        planner = await db.get(AgentActor, scenario.actors[0])
        planner.scopes = json.dumps(["planning:read", "tasks:read"])
        await db.commit()
        collected, cursor = [], None
        while True:
            page = await list_agent_assignments_page(db, planner, limit=6, cursor=cursor)
            collected.extend(page["items"])
            if not page["has_more"]:
                break
            cursor = page["next_cursor"]
        assert len(collected) == 30 and len({row["id"] for row in collected}) == 30
        assert page["next_cursor"] is None
