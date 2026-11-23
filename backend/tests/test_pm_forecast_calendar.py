"""A managed planning principal can forecast an iteration using a single annual calendar."""

import json

import httpx
import pytest

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.models.calendar import Calendar
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.project import Project
from app.models.iteration import Iteration
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases
from tests import test_team_pm_dispatch

db_session_factory = test_team_pm_dispatch.db_session_factory


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_scoped_single_year_forecast(
    db_session, db_session_factory, team_member_factory, task_factory, monkeypatch, transport
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    await initialize_control_plane(db_session)
    await db_session.commit()
    team = await provision_ready_topology(db_session)
    controller = team.manifest.controller
    pm = team.actors[controller.actor_key]
    scope = await routing_base(
        db_session,
        topology=team,
        actor_key=team.manifest.workers[0].actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Publish the guide",
    )
    project, other = Project(name="Handbook"), Project(name="Restricted workspace project")
    db_session.add_all([project, other])
    await db_session.flush()
    iteration = await db_session.get(Iteration, scope.task.iteration_id)
    iteration.project_id = scope.task.project_id = project.id
    private = Iteration(
        name="Restricted annual plan",
        project_id=other.id,
        calendar_id=iteration.calendar_id,
        start_date=iteration.start_date,
        end_date=iteration.end_date,
    )
    following = Calendar(name="Later year", year=2027)
    db_session.add_all([private, following])
    scope.task.effort_hours = 8
    principal = await IdentityService(db_session).actor_context(pm)
    db_session.add_all(
        [
            WorkspaceMembership(principal_id=principal.principal_id, role="member"),
            ProjectMembership(principal_id=principal.principal_id, project_id=project.id, role="manager"),
        ]
    )
    await db_session.commit()
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    headers = {"X-Agent-API-Key": team.sink.keys[controller.actor_key]}
    label = "single-year-forecast"
    rationale = "Preview the approved handbook schedule"
    if transport == "rest":
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001"
        ) as http:
            response = await http.post(
                f"/api/agent/planning/iterations/{iteration.id}/schedule/preview",
                headers={
                    **headers,
                    "Idempotency-Key": label,
                    "X-Correlation-ID": label,
                    "X-Agent-Rationale": rationale,
                },
            )
            assert response.status_code == 200, response.text
            receipt = response.json()
            refused = await http.post(
                f"/api/agent/planning/iterations/{private.id}/schedule/preview",
                headers={
                    **headers,
                    "Idempotency-Key": "foreign",
                    "X-Correlation-ID": "foreign",
                    "X-Agent-Rationale": rationale,
                },
            )
            assert refused.status_code in {403, 404} and private.name not in refused.text
    else:
        server = mcp_server.create_mcp_server()
        application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
        async with (
            server.session_manager.run(),
            httpx.AsyncClient(
                transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
            ) as http,
        ):

            async def tool(name, target=iteration.id, key=None, **inputs):
                args = {"iteration_id": target, **inputs}
                if key is not None:
                    args.update(idempotency_key=key, rationale=rationale, correlation_id=key)
                response = await http.post(
                    "/",
                    headers={**headers, "Accept": "application/json, text/event-stream"},
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": name,
                            "arguments": args,
                        },
                    },
                )
                return response.json()["result"]

            async def successful(name, **args):
                result = await tool(name, **args)
                assert not result["isError"], result["content"][0]["text"]
                return json.loads(result["content"][0]["text"])

            receipt = await successful("agent_preview_schedule", key=label)
            refused = await tool("agent_preview_schedule", target=private.id, key="foreign")
            assert refused["isError"] and private.name not in refused["content"][0]["text"]
            previous = await successful("workspace_get_iteration")
            assert previous["additional_calendar_ids"] == [] and previous["missing_calendar_years"] == []
            extended = await successful(
                "agent_update_iteration",
                key="extend",
                payload={
                    "expected_revisions": {str(iteration.id): previous["revision"]},
                    "end_date": "2027-01-05",
                },
            )
            assert extended["result"]["missing_calendar_years"] == [2027]
            bound = await successful(
                "agent_update_iteration",
                key="bind",
                payload={
                    "expected_revisions": {str(iteration.id): extended["result"]["revision"]},
                    "additional_calendar_ids": [following.id],
                },
            )
            assert bound["result"]["additional_calendar_ids"] == [following.id]
            ready = await successful("agent_get_iteration_plan_readiness")
            assert ready["checkpoints"][0]["state"] == "done" and ready["missing_calendar_years"] == []
            forecast = (await successful("agent_preview_schedule", key="complete-preview"))["result"]
            applied = await successful(
                "agent_apply_schedule",
                key="complete-apply",
                expected_task_versions={str(t["task_id"]): t["version"] for t in forecast["task_states"]},
                expected_input_digest=forecast["input_digest"],
            )
            assert applied["result"]["success"]

            async def unexpected_failure(*_args, **_kwargs):
                raise RuntimeError("Internal synthetic detail")

            monkeypatch.setattr(mcp_server.mcp_agent_tools, "get_iteration", unexpected_failure)
            private_failure = await tool("workspace_get_iteration")
            assert private_failure["isError"] and "MCP tool failed" in private_failure["content"][0]["text"]
            assert "Internal synthetic detail" not in private_failure["content"][0]["text"]
    assert receipt["correlation_id"] == label
    assert receipt["result"]["success"] and receipt["result"]["preview"]
