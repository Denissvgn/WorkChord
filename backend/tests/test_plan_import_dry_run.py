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
    assert diff_import_state(state_before, state_after, created_profiles=profiles) == reviewed["changes"]
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


def refuse_planning_reservation(monkeypatch):
    """Fail the test if a refusal is decided only after the workspace planning reservation."""
    import app.commands

    async def reserved(*_args, **_kwargs):
        raise AssertionError("the planning reservation was taken")
    monkeypatch.setattr(app.commands, "lock_planning", reserved)


async def test_oversized_previews_are_refused_before_any_reservation(managed_store, monkeypatch):
    import app.query_limits
    from app.services import import_review_service

    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    path = f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run"
    before = await persisted(factory)
    refuse_planning_reservation(monkeypatch)

    many = {"tasks": [{"title": f"Bulk {index}", "project_id": scenario.projects[0], "effort_hours": 1}
                      for index in range(import_review_service.MAX_DRY_RUN_IMPORT_TASKS + 1)]}
    too_many = await dry_run(PM_KEY, path, many)
    assert too_many.status_code == 409, too_many.text
    assert too_many.json()["detail"]["code"] == "import_dry_run_too_large"

    crowd = {"team_members": [{"name": f"Person {index}"} for index in range(import_review_service.MAX_DRY_RUN_IMPORT_MEMBERS + 1)]}
    too_many_members = await dry_run(PM_KEY, path, crowd)
    assert too_many_members.json()["detail"]["code"] == "import_dry_run_too_large"

    async with factory() as db:
        existing = await db.scalar(select(func.count(Task.id)).where(Task.iteration_id == scenario.iterations[0]))
    monkeypatch.setattr(app.query_limits, "MAX_ITERATION_TREE_TASKS", existing + 2)
    tree = await dry_run(PM_KEY, path, plan_file(scenario.projects[0]))
    assert tree.status_code == 409, tree.text
    assert tree.json()["detail"]["code"] == "import_iteration_tree_too_large"

    chain = {"id": 0, "title": "Level 0", "project_id": scenario.projects[0]}
    node = chain
    for level in range(1, import_review_service.MAX_DRY_RUN_IMPORT_DEPTH + 1):
        child = {"id": level, "title": f"Level {level}"}
        node["children"] = [child]
        node = child
    deep = await dry_run(PM_KEY, path, {"tasks": [chain]})
    assert deep.status_code == 409 and deep.json()["detail"]["code"] == "import_dry_run_too_large", deep.text
    assert "levels of subtasks" in deep.json()["detail"]["message"]

    tangled = {"tasks": [{"id": index, "title": f"Step {index}", "project_id": scenario.projects[0], "effort_hours": 1,
                          "dependencies": list(range(index))} for index in range(40)]}
    tangled_response = await dry_run(PM_KEY, path, tangled)
    assert "dependency references" in tangled_response.json()["detail"]["message"], tangled_response.text

    away = {"team_members": [{"name": "Often away", "vacations": [{"start_date": "2026-01-05", "end_date": "2026-01-05"}]
                              * (import_review_service.MAX_DRY_RUN_IMPORT_VACATIONS + 1)}]}
    away_response = await dry_run(PM_KEY, path, away)
    assert "vacations" in away_response.json()["detail"]["message"], away_response.text

    unhashable = await dry_run(PM_KEY, path, {"tasks": [{"title": "Odd owner", "project_id": scenario.projects[0],
                                                         "owner_profile_id": [2]}]})
    assert unhashable.status_code == 422 and unhashable.json()["detail"]["code"] == "import_file_invalid", unhashable.text

    monkeypatch.setattr(import_review_service, "_dry_run_active", True)
    busy = await dry_run(PM_KEY, path, plan_file(scenario.projects[0]))
    assert busy.status_code == 409 and busy.json()["detail"]["code"] == "import_dry_run_busy", busy.text
    assert await persisted(factory) == before


async def test_profiles_the_caller_cannot_read_are_refused_alike(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    async with factory() as db:
        hidden = TeamMemberProfile(display_name="Hidden directory person", profile_kind="human", automation_enabled=False)
        db.add(hidden)
        await db.commit()
        hidden_id = hidden.id
    path = f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run"
    before = await persisted(factory)

    by_name = await dry_run(PM_KEY, path, {"team_members": [{"name": "Hidden directory person"}]})
    assert by_name.status_code == 403, by_name.text
    assert by_name.json()["detail"]["code"] == "incomplete_authorized_graph"
    assert str(hidden_id) not in by_name.text

    def owned(profile_id):
        return {"tasks": [{"title": "Owned task", "project_id": scenario.projects[0], "effort_hours": 1,
                           "owner_profile_id": profile_id}]}
    existing = await dry_run(PM_KEY, path, owned(hidden_id))
    missing = await dry_run(PM_KEY, path, owned(999_999))
    assert existing.status_code == missing.status_code == 403
    assert existing.json() == missing.json()

    unknown = await dry_run(PM_KEY, path, {"team_members": [{"name": "Nobody known yet"}]})
    assert unknown.status_code == 200, unknown.text
    assert await persisted(factory) == before


async def test_a_planner_may_name_people_already_on_a_team_it_can_read(managed_store):
    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    async with factory() as db:
        current = await db.get(Iteration, scenario.iterations[0])
        earlier = Iteration(name="Earlier delivery", start_date=current.start_date, end_date=current.end_date,
                            calendar_id=current.calendar_id, project_id=scenario.projects[0])
        colleague = TeamMemberProfile(display_name="Iteration colleague", profile_kind="human", automation_enabled=False)
        db.add_all([earlier, colleague])
        await db.flush()
        # The colleague is on another team of the planner's own project, so the planner sees them there.
        db.add(TeamMember(name="Iteration colleague", position="Engineer", profile_id=colleague.id,
                          iteration_id=earlier.id))
        await db.commit()
        colleague_id = colleague.id
    path = f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run"

    named = await dry_run(PM_KEY, path, {"team_members": [{"name": "Iteration colleague"}]})

    assert named.status_code == 200, named.text
    created = named.json()["changes"]["team_members"]["created"]
    assert [(row["name"], row["profile_id"]) for row in created] == [("Iteration colleague", colleague_id)]
    assert named.json()["changes"]["profiles"]["created"] == []


async def test_a_dry_run_over_its_budget_is_refused_and_rolled_back(managed_store, monkeypatch):
    import asyncio
    from sqlalchemy import text
    import app.routers.export as export
    from app.services import import_review_service

    factory, scenario, _, _ = managed_store
    await add_agents(factory, scenario)
    path = f"/api/agent/planning/iterations/{scenario.iterations[0]}/import/dry-run"
    data = plan_file(scenario.projects[0])
    before = await persisted(factory)
    original = export._process_import

    async def slow(iteration_id, payload, db, **kwargs):
        result = await original(iteration_id, payload, db, **kwargs)
        if db.bind.dialect.name == "postgresql":
            await db.execute(text("SELECT pg_sleep(3)"))
        else:
            await asyncio.sleep(3)
        return result
    monkeypatch.setattr(export, "_process_import", slow)
    monkeypatch.setattr(import_review_service, "DRY_RUN_BUDGET_SECONDS", 0.5)

    refused = await dry_run(PM_KEY, path, data)

    assert refused.status_code == 409, refused.text
    assert refused.json()["detail"]["code"] == "import_dry_run_too_slow"
    assert await persisted(factory) == before
    monkeypatch.setattr(export, "_process_import", original)
    again = await dry_run(PM_KEY, path, data)
    assert again.status_code == 200, again.text
    assert await persisted(factory) == before


async def test_the_elevated_writer_cannot_commit_and_needs_a_preview_root(managed_store, monkeypatch):
    import pytest
    import app.routers.export as export
    from app.authority import Authority
    from app.commands import command_transaction
    from app.services.import_review_service import dry_run_import

    factory, scenario, _, _ = managed_store
    data = plan_file(scenario.projects[0])
    before = await persisted(factory)
    operator = Authority(None, "system", workspace_role="operator")
    original = export._process_import

    async def committing(iteration_id, payload, db, **kwargs):
        result = await original(iteration_id, payload, db, **kwargs)
        await db.commit()
        return result
    monkeypatch.setattr(export, "_process_import", committing)

    async with factory() as db:
        db.info["authority"] = operator
        with pytest.raises(RuntimeError, match="cannot commit"):
            async with command_transaction(db, mode="preview"):
                await dry_run_import(db, scenario.iterations[0], data)
    assert await persisted(factory) == before

    monkeypatch.setattr(export, "_process_import", original)
    async with factory() as db:
        db.info["authority"] = operator
        with pytest.raises(RuntimeError, match="rollback-only"):
            async with command_transaction(db, mode="apply"):
                await dry_run_import(db, scenario.iterations[0], data)
    assert await persisted(factory) == before
