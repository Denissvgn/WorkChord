"""A plan import is reviewed under planning scope and applied exactly as reviewed."""

import json

import httpx
from sqlalchemy import func, select

from app import mcp_server
from app.config import get_settings
from app.main import app
from app.models.agent import AgentActor
from app.models.identity import Principal, ProjectMembership
from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency
from app.models.team_member import TeamMember, TeamMemberProfile
from app.services.agent_service import hash_api_key
from app.services.import_review_service import compose_review_digest
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_managed_authority import managed_store  # noqa: F401


ADMIN = {"X-Admin-API-Key": "managed-operator-fixture"}
PM_KEY = "plan-import-pm-key"
OTHER_TEAM_KEY = "plan-import-other-team-key"
READER_KEY = "plan-import-reader-key"


def plan_file(project_id, *, title="Reviewed parent"):
    return {
        "team_members": [{"name": "Reviewed new hire", "position": "Engineer"}],
        "tasks": [
            {"id": 1, "title": title, "project_id": project_id,
             "external_key": "PLAN-1", "source": "plan", "source_url": "https://example.com/plan/1",
             "children": [{"id": 2, "title": "Reviewed child", "effort_hours": 2,
                           "assignee_name": "Reviewed new hire",
                           "start_date": "2026-01-06", "end_date": "2026-01-07"}]},
            {"id": 3, "title": "Reviewed follower", "project_id": project_id, "effort_hours": 3,
             "dependencies": [2], "min_start_date": "2026-01-08"},
        ],
    }


def upload(data):
    return {"file": ("plan.json", json.dumps(data), "application/json")}


async def add_agents(factory, scenario):
    """A PM of the first project, a PM of the other project only, and a planning reader."""
    async with factory() as db:
        rows = [
            (PM_KEY, ["planning:write", "planning:read", "tasks:read"], scenario.projects[0]),
            (OTHER_TEAM_KEY, ["planning:write", "planning:read", "tasks:read"], scenario.projects[1]),
            (READER_KEY, ["planning:read", "tasks:read"], scenario.projects[0]),
        ]
        for key, scopes, project_id in rows:
            actor = AgentActor(name=key, display_name=key, role="pm", api_key_hash=hash_api_key(key), scopes=json.dumps(scopes))
            db.add(actor)
            await db.flush()
            principal = Principal(kind="agent", display_name=key, agent_actor_id=actor.id)
            db.add(principal)
            await db.flush()
            db.add(ProjectMembership(principal_id=principal.id, project_id=project_id, role="manager"))
        await db.commit()


async def persisted(factory):
    async with factory() as db:
        return {
            "tasks": await db.scalar(select(func.count(Task.id))),
            "dependencies": await db.scalar(select(func.count(TaskDependency.id))),
            "members": await db.scalar(select(func.count(TeamMember.id))),
            "profiles": await db.scalar(select(func.count(TeamMemberProfile.id))),
            "iterations": dict((await db.execute(select(Iteration.id, Iteration.revision))).all()),
        }


def client(**headers):
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://test", headers=headers)


async def dry_run(key, path, data):
    async with client(**{"X-Agent-API-Key": key}) as api:
        return await api.post(path, files=upload(data))


async def test_dry_run_returns_the_exact_changes_and_writes_nothing(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    before = await persisted(factory)

    response = await dry_run(PM_KEY, f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run",
                             plan_file(scenario.projects[0]))

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["written"] is False and body["target_iteration_id"] == scenario.iterations[0]
    assert body["review_digest"].startswith("ipr1:")
    changes = body["changes"]
    created = {row["ref"]: row for row in changes["tasks"]["created"]}
    assert {ref: row["title"] for ref, row in created.items()} == {
        "new-task-1": "Reviewed parent", "new-task-2": "Reviewed child", "new-task-3": "Reviewed follower"}
    assert created["new-task-2"]["parent_id"] == "new-task-1"
    assert created["new-task-2"]["assignee_id"] == "new-member-1"
    assert created["new-task-1"]["project_id"] == scenario.projects[0]
    assert changes["tasks"]["changed"] == [] and changes["tasks"]["removed"] == []
    assert changes["dependencies"] == {"created": [{"task": "new-task-3", "depends_on": "new-task-2"}], "removed": []}
    assert changes["links"]["created"] == [{"kind": "source", "task": "new-task-1", "external_key": "PLAN-1",
                                            "source": "plan", "source_url": "https://example.com/plan/1"}]
    assert {"task": "new-task-2", "field": "start_date", "from": None, "to": "2026-01-06"} in changes["dates"]
    assert {"task": "new-task-3", "field": "min_start_date", "from": None, "to": "2026-01-08"} in changes["dates"]
    assert [row["name"] for row in changes["team_members"]["created"]] == ["Reviewed new hire"]
    assert changes["team_members"]["created"][0]["profile_id"] == "new-profile-1"
    assert [row["display_name"] for row in changes["profiles"]["created"]] == ["Reviewed new hire"]
    assert body["summary"]["tasks_created"] == 3 and body["summary"]["dependencies_created"] == 1
    assert await persisted(factory) == before


async def test_apply_with_the_digest_makes_exactly_the_reviewed_changes(managed_store, monkeypatch):
    from app.services.import_review_service import capture_import_state, diff_import_state

    factory, scenario, _, _ = managed_store
    # The digest carries the observed context, so strict revision checks need no extra header.
    monkeypatch.setenv("STRICT_MUTATION_VERSIONS", "true")
    get_settings.cache_clear()
    await add_agents(factory, scenario)
    iteration_id = scenario.iterations[0]
    data = plan_file(scenario.projects[0])
    reviewed = (await dry_run(PM_KEY, f"/api/agent/planning/iterations/{iteration_id}/import/dry-run", data)).json()
    async with factory() as db:
        state_before = await capture_import_state(db, iteration_id)
        floor = await db.scalar(select(func.max(TeamMemberProfile.id)))

    try:
        async with client(**ADMIN) as api:
            applied = await api.post(f"/api/iterations/{iteration_id}/import", files=upload(data),
                                     data={"review_digest": reviewed["review_digest"]})
    finally:
        monkeypatch.delenv("STRICT_MUTATION_VERSIONS")
        get_settings.cache_clear()

    assert applied.status_code == 200, applied.text
    async with factory() as db:
        state_after = await capture_import_state(db, iteration_id)
        profiles = {row.id: {"display_name": row.display_name, "email": row.email, "profile_kind": row.profile_kind}
                    for row in (await db.execute(select(TeamMemberProfile).where(TeamMemberProfile.id > floor))).scalars()}
        new_tasks = {task.title: task for task in (await db.scalars(select(Task).where(
            Task.iteration_id == iteration_id, Task.id.not_in(list(state_before["tasks"]))))).all()}
        dependency = await db.scalar(select(TaskDependency).where(TaskDependency.task_id == new_tasks["Reviewed follower"].id))
    assert diff_import_state(state_before, state_after, profile_floor=floor, profiles=profiles) == reviewed["changes"]
    assert set(new_tasks) == {"Reviewed parent", "Reviewed child", "Reviewed follower"}
    assert new_tasks["Reviewed child"].parent_id == new_tasks["Reviewed parent"].id
    assert dependency.depends_on_id == new_tasks["Reviewed child"].id


async def test_concurrent_edit_or_changed_file_refuses_the_reviewed_write(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    iteration_id = scenario.iterations[0]
    data = plan_file(scenario.projects[0])
    reviewed = (await dry_run(PM_KEY, f"/api/agent/planning/iterations/{iteration_id}/import/dry-run", data)).json()
    path = f"/api/iterations/{iteration_id}/import"

    async with client(**ADMIN) as api:
        changed_file = await api.post(path, files=upload(plan_file(scenario.projects[0], title="Edited after review")),
                                      data={"review_digest": reviewed["review_digest"]})
        assert changed_file.status_code == 409, changed_file.text
        assert changed_file.json()["detail"]["code"] == "import_review_file_changed"

        task_path = f"/api/tasks/{scenario.tasks['planned']}"
        current = (await api.get(task_path)).json()
        edited = await api.put(task_path, json={"title": "Edited concurrently", "expected_version": current["version"]})
        assert edited.status_code == 200, edited.text
        before = await persisted(factory)
        stale = await api.post(path, files=upload(data), data={"review_digest": reviewed["review_digest"]})
        assert stale.status_code == 409, stale.text
        assert stale.json()["detail"]["code"] == "import_review_target_changed"
    assert await persisted(factory) == before


async def test_a_change_set_that_differs_from_the_review_is_rolled_back(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    iteration_id = scenario.iterations[0]
    data = plan_file(scenario.projects[0])
    reviewed = (await dry_run(PM_KEY, f"/api/agent/planning/iterations/{iteration_id}/import/dry-run", data)).json()
    _, file_sha, target_sha, _ = reviewed["review_digest"].split(":")
    before = await persisted(factory)

    async with client(**ADMIN) as api:
        forged = await api.post(f"/api/iterations/{iteration_id}/import", files=upload(data),
                                data={"review_digest": compose_review_digest(file_sha, target_sha, "0" * 64)})
        assert forged.status_code == 409, forged.text
        assert forged.json()["detail"]["code"] == "import_review_changes_differ"
        malformed = await api.post(f"/api/iterations/{iteration_id}/import", files=upload(data),
                                   data={"review_digest": "not-a-digest"})
        assert malformed.status_code == 422, malformed.text
        assert malformed.json()["detail"]["code"] == "import_review_digest_invalid"
    assert await persisted(factory) == before


async def test_callers_without_planning_scope_or_from_another_team_are_refused(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    path = f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run"
    data = plan_file(scenario.projects[0])
    before = await persisted(factory)

    reader = await dry_run(READER_KEY, path, data)
    assert reader.status_code == 403, reader.text
    other_team = await dry_run(OTHER_TEAM_KEY, path, data)
    assert other_team.status_code in {403, 404}, other_team.text
    assert "changes" not in other_team.text
    other_team_new = await dry_run(OTHER_TEAM_KEY, "/api/agent/planning/iterations/import/dry-run", {
        "iteration": {"name": "Foreign plan", "start_date": "2026-02-02", "end_date": "2026-02-27",
                      "project_id": scenario.projects[0]}, "tasks": [{"title": "Foreign task", "effort_hours": 1}]})
    assert other_team_new.status_code == 403, other_team_new.text
    async with client() as api:
        anonymous = await api.post(path, files=upload(data))
        assert anonymous.status_code == 401, anonymous.text
    assert await persisted(factory) == before


async def test_new_iteration_is_reviewed_and_applied_and_a_write_without_digest_is_unchanged(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    data = {"iteration": {"name": "Reviewed plan", "start_date": "2026-02-02", "end_date": "2026-02-27",
                          "project_id": scenario.projects[0]},
            "tasks": [{"id": 1, "title": "First reviewed step", "effort_hours": 2},
                      {"id": 2, "title": "Second reviewed step", "effort_hours": 2, "dependencies": [1]}]}
    reviewed = await dry_run(PM_KEY, "/api/agent/planning/iterations/import/dry-run", data)
    assert reviewed.status_code == 200, reviewed.text
    body = reviewed.json()
    assert body["changes"]["iteration"]["created"]["name"] == "Imported: Reviewed plan"
    assert body["changes"]["dependencies"]["created"] == [{"task": "new-task-2", "depends_on": "new-task-1"}]
    assert body["target_iteration_id"] is None

    async with client(**ADMIN) as api:
        applied = await api.post("/api/iterations/import", files=upload(data), data={"review_digest": body["review_digest"]})
        assert applied.status_code == 200, applied.text
        plain = await api.post(f"/api/iterations/{scenario.iterations[0]}/import",
                               files=upload({"tasks": [{"title": "Unreviewed task", "project_id": scenario.projects[0], "effort_hours": 1}]}))
        assert plain.status_code == 200, plain.text
    async with factory() as db:
        assert await db.scalar(select(func.count(Iteration.id)).where(Iteration.name == "Imported: Reviewed plan")) == 1
        assert await db.scalar(select(func.count(Task.id)).where(Task.title == "Unreviewed task")) == 1


async def test_mcp_preview_matches_the_rest_dry_run(managed_store, monkeypatch):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    monkeypatch.setattr(mcp_server, "_session_factory", factory)
    iteration_id = scenario.iterations[0]
    data = plan_file(scenario.projects[0])
    rest = (await dry_run(PM_KEY, f"/api/agent/planning/iterations/{iteration_id}/import/dry-run", data)).json()
    before = await persisted(factory)

    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with server.session_manager.run(), httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
    ) as api:
        async def call(key, arguments):
            response = await api.post("/", headers={"X-Agent-API-Key": key, "Accept": "application/json, text/event-stream"},
                                      json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                            "params": {"name": "agent_preview_iteration_import", "arguments": arguments}})
            assert response.status_code == 200, response.text
            return response.json()["result"]

        result = await call(PM_KEY, {"iteration_id": iteration_id, "import_data": data})
        assert not result["isError"], result
        body = json.loads(result["content"][0]["text"])
        assert body["review_digest"] == rest["review_digest"]
        assert body["changes"] == rest["changes"]
        denied = await call(READER_KEY, {"iteration_id": iteration_id, "import_data": data})
        assert denied["isError"]
    assert await persisted(factory) == before
