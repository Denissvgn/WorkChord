"""The Gantt projection names the project that owns its iteration, over REST and MCP."""

from datetime import date

import httpx
import pytest

from app.main import app
from app.models.iteration import Iteration
from app.models.project import Project
from tests.test_delivery_scenarios import delivery_store  # noqa: F401 - fixture


async def _add_unscoped_iteration(db, bound_iteration_id):
    bound = await db.get(Iteration, bound_iteration_id)
    unscoped = Iteration(name="Unscoped delivery", start_date=date(2026, 2, 2),
                         end_date=date(2026, 2, 27), calendar_id=bound.calendar_id, project_id=None)
    db.add(unscoped)
    await db.commit()
    return unscoped.id


async def test_gantt_rest_carries_owning_project_for_bound_and_unscoped_iterations(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        bound_id = scenario.iterations[0]
        unscoped_id = await _add_unscoped_iteration(db, bound_id)
        bound = await db.get(Iteration, bound_id)
        project = await db.get(Project, bound.project_id)
        expected_project = {"id": project.id, "name": project.name,
                            "status": project.status, "health": project.health}

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        bound_response = await client.get(f"/api/iterations/{bound_id}/gantt")
        unscoped_response = await client.get(f"/api/iterations/{unscoped_id}/gantt")
    assert bound_response.status_code == 200, bound_response.text
    assert unscoped_response.status_code == 200, unscoped_response.text

    bound_iteration = bound_response.json()["iteration"]
    assert bound_iteration["project_id"] == expected_project["id"]
    assert bound_iteration["project"] == expected_project
    unscoped_iteration = unscoped_response.json()["iteration"]
    assert unscoped_iteration["project_id"] is None
    assert unscoped_iteration["project"] is None


async def test_gantt_mcp_carries_owning_project_for_bound_and_unscoped_iterations(delivery_store):
    from app.mcp_agent_tools import get_iteration, get_iteration_gantt

    factory, scenario, _ = delivery_store
    async with factory() as db:
        bound_id = scenario.iterations[0]
        unscoped_id = await _add_unscoped_iteration(db, bound_id)

    async with factory() as db:
        bound_gantt = await get_iteration_gantt(db, bound_id)
        bound_single = await get_iteration(db, bound_id)
    async with factory() as db:
        unscoped_gantt = await get_iteration_gantt(db, unscoped_id)
        unscoped_single = await get_iteration(db, unscoped_id)

    # The Gantt iteration must match the single-iteration view for the same identity.
    assert bound_gantt["iteration"]["project_id"] == bound_single["project_id"]
    assert bound_gantt["iteration"]["project"] == bound_single["project"]
    assert bound_single["project"] is not None
    assert bound_gantt["iteration"]["project"]["id"] == bound_gantt["iteration"]["project_id"]
    assert unscoped_gantt["iteration"]["project_id"] is None
    assert unscoped_gantt["iteration"]["project"] is None
    assert unscoped_single["project_id"] is None and unscoped_single["project"] is None
