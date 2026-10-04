"""Version rollout rejects missing inputs without weakening identity or rollback."""

import httpx
import pytest
from sqlalchemy import func, select

from app.config import get_settings
from app.main import app
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.commands import command_transaction
from app.mcp_server import _structured_tool_error
from app.mutation_versions import MissingMutationRevision, require_mutation_revision
from app.authority import Authority
from tests.test_delivery_scenarios import delivery_store


@pytest.fixture(autouse=True)
def strict_versions(monkeypatch):
    monkeypatch.setenv("STRICT_MUTATION_VERSIONS", "true")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


async def test_missing_task_version_is_structured_and_rolls_back(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["planned"]
    async with factory() as db:
        before = await db.get(Task, task_id)
        version, title = before.version, before.title
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        missing = await client.put(f"/api/tasks/{task_id}", json={"title": "Lost update"})
        assert missing.status_code == 422, missing.text
        assert missing.json()["detail"]["code"] == "mutation_revision_required"
        assert missing.json()["detail"]["field"] == "expected_version"
        async with factory() as db:
            task = await db.get(Task, task_id)
            assert (task.version, task.title) == (version, title)
            assert (await db.get(Iteration, scenario.iterations[0])).revision == revision
            assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots
        current = await client.put(f"/api/tasks/{task_id}", json={"title": "Versioned edit", "expected_version": version})
        assert current.status_code == 200, current.text
        stale = await client.put(f"/api/tasks/{task_id}", json={"title": "Stale edit", "expected_version": version})
        assert stale.status_code == 409 and stale.json()["detail"]["code"] == "task_version_conflict", stale.text
        monkeypatch.setenv("STRICT_MUTATION_VERSIONS", "false")
        get_settings.cache_clear()
        legacy = await client.put(f"/api/tasks/{task_id}", json={"title": "Compatible edit"})
        assert legacy.status_code == 200, legacy.text
        denied = await client.put(f"/api/tasks/{task_id}", json={"title": "Unauthorized"}, headers={"X-Agent-API-Key": scenario.actor_keys[0]})
        assert denied.status_code == 403, denied.text


async def test_aggregate_revision_required_for_import_and_structural_writes(delivery_store):
    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        missing = await client.post(f"/api/iterations/{iteration_id}/tasks/import", json={"text": "- Captured request", "destination": "triage"})
        assert missing.status_code == 422, missing.text
        assert missing.json()["detail"]["field"] == "expected_revision"
        async with factory() as db:
            revision = (await db.get(Iteration, iteration_id)).revision
        imported = await client.post(f"/api/iterations/{iteration_id}/tasks/import", json={"text": "- Captured request", "destination": "triage", "expected_revision": revision})
        assert imported.status_code == 201 and imported.json()["triage_count"] == 1, imported.text
        task_id = scenario.tasks["planned"]
        async with factory() as db:
            version = (await db.get(Task, task_id)).version
            revision = (await db.get(Iteration, iteration_id)).revision
        missing = await client.delete(f"/api/tasks/{task_id}", params={"expected_version": version})
        assert missing.status_code == 422, missing.text
        assert missing.json()["detail"]["field"] == "expected_revision"
        removed = await client.delete(f"/api/tasks/{task_id}", params={"expected_version": version, "expected_revision": revision})
        assert removed.status_code == 200, removed.text


async def test_dependency_bulk_preview_and_partial_move_versions(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, prerequisite = scenario.tasks["planned"], scenario.tasks["closed_low"]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        missing = await client.post(f"/api/tasks/{task_id}/dependencies", json={"depends_on_id": prerequisite})
        assert missing.status_code == 422 and missing.json()["detail"]["field"] == "expected_version", missing.text
        before = (await client.get(f"/api/tasks/{task_id}")).json()
        added = await client.post(f"/api/tasks/{task_id}/dependencies", json={"depends_on_id": prerequisite, "expected_version": before["version"]})
        assert added.status_code == 200, added.text
        stale = await client.delete(f"/api/tasks/{task_id}/dependencies/{prerequisite}", params={"expected_version": before["version"]})
        assert stale.status_code == 409 and stale.json()["detail"]["code"] == "task_version_conflict", stale.text
        current = (await client.get(f"/api/tasks/{task_id}")).json()
        preview = await client.post("/api/tasks/bulk-operations", json={"task_ids": [task_id], "action": "set_priority", "payload": {"priority": 4}, "dry_run": True})
        assert preview.status_code == 200 and preview.json()["dry_run"], preview.text
        async with factory() as db:
            revision = (await db.get(Iteration, scenario.iterations[0])).revision
        missing = await client.post("/api/tasks/bulk-operations", json={"task_ids": [task_id], "action": "set_priority", "payload": {"priority": 4}, "dry_run": False,
            "expected_revisions": {str(scenario.iterations[0]): revision}})
        assert missing.status_code == 422 and missing.json()["detail"]["field"] == "expected_version", missing.text
        missing = await client.post(f"/api/tasks/{task_id}/move", json={"iteration_id": scenario.iterations[1], "expected_version": current["version"],
            "expected_revisions": {str(scenario.iterations[0]): revision}})
        assert missing.status_code == 422 and missing.json()["detail"]["field"] == "expected_revisions", missing.text
        async with factory() as db:
            task = await db.get(Task, task_id)
            assert task.iteration_id == scenario.iterations[0] and task.priority == before["priority"]
            assert (await db.get(Iteration, scenario.iterations[0])).revision == revision


async def test_text_context_is_a_revision_bound_editing_base(delivery_store):
    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        legacy = await client.get(f"/api/iterations/{iteration_id}/tasks/text")
        context = await client.get(f"/api/iterations/{iteration_id}/tasks/text-context")
        assert context.status_code == 200, context.text
        assert context.json()["text"] == legacy.json()
        async with factory() as db:
            assert context.json()["iteration_revision"] == (await db.get(Iteration, iteration_id)).revision
        task_id = scenario.tasks["planned"]
        before = (await client.get(f"/api/tasks/{task_id}")).json()
        changed = await client.put(f"/api/tasks/{task_id}", json={"title": "New context", "expected_version": before["version"]})
        assert changed.status_code == 200, changed.text
        stale = await client.post(f"/api/iterations/{iteration_id}/tasks/bulk-update", json={"text": context.json()["text"], "expected_revision": context.json()["iteration_revision"]})
        assert stale.status_code == 409 and stale.json()["detail"]["code"] == "iteration_version_conflict", stale.text


async def test_header_revision_context_is_validated_without_auth_bypass(delivery_store):
    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    path = f"/api/iterations/{iteration_id}/tasks/import"
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        invalid = await client.post(path, json={"text": "- Request", "destination": "triage"}, headers={"X-Expected-Revisions": '{"1":true}'})
        assert invalid.status_code == 422 and invalid.json()["detail"]["code"] == "invalid_revision_context", invalid.text
        async with factory() as db:
            revision = (await db.get(Iteration, iteration_id)).revision
        mismatch = await client.post(path, json={"text": "- Request", "destination": "triage", "expected_revision": revision},
            headers={"X-Expected-Revisions": f'{{"{iteration_id}":{revision+1}}}'})
        assert mismatch.status_code == 409 and mismatch.json()["detail"]["code"] == "conflicting_revision_context", mismatch.text
        imported = await client.post(path, json={"text": "- Request", "destination": "triage"},
            headers={"X-Expected-Revisions": f'{{"{iteration_id}":{revision}}}'})
        assert imported.status_code == 201, imported.text
        denied = await client.post(path, json={"text": "- Unauthorized", "destination": "triage"},
            headers={"X-Agent-API-Key": scenario.actor_keys[0], "X-Expected-Revisions": f'{{"{iteration_id}":{revision}}}'})
        assert denied.status_code == 403, denied.text


async def test_operator_web_commands_still_require_versions_and_offline_repair_is_explicit(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        db.info["authority"] = Authority(None, "system", workspace_role="operator")
        with pytest.raises(MissingMutationRevision) as captured:
            async with command_transaction(db):
                require_mutation_revision(db, None, field="expected_version", resource="task", resource_id=scenario.tasks["planned"])
        import json
        assert json.loads(_structured_tool_error(captured.value)) == captured.value.detail()
        monkeypatch.setenv("DATABASE_PROCESS_ROLE", "repair")
        monkeypatch.setenv("DATABASE_POOL_SIZE", "1")
        monkeypatch.setenv("DATABASE_MAX_OVERFLOW", "1")
        get_settings.cache_clear()
        async with command_transaction(db):
            require_mutation_revision(db, None, field="expected_version", resource="task", resource_id=scenario.tasks["planned"])


async def test_mcp_mutation_uses_the_same_missing_version_policy(delivery_store):
    from app.models.agent import AgentActor
    from app import mcp_agent_tools
    factory, scenario, _ = delivery_store
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes, actor.role = '["tasks:write","tasks:read"]', "pm"
        await db.commit()
        with pytest.raises(MissingMutationRevision):
            await mcp_agent_tools.update_task(db, actor, scenario.tasks["planned"], {"title": "Unversioned MCP edit"})


async def test_strict_agent_schedule_accepts_verified_task_versions_and_input_digest(delivery_store):
    from app.models.agent import AgentActor
    from app.schemas.agent_planning import AgentPlanningCommandContext, AgentScheduleCommand
    from app.services.agent_planning_service import AgentPlanningService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes, actor.role = '["planning:write"]', "pm"
        await db.commit()
        service = AgentPlanningService(db)
        preview = await service.preview_schedule(scenario.iterations[0], actor,
            command=AgentPlanningCommandContext(idempotency_key="strict-preview", rationale="Observe schedule inputs", correlation_id="strict-preview"))
        data = AgentScheduleCommand(expected_task_versions={row["task_id"]: row["version"] for row in preview.result["task_states"]},
            expected_input_digest=preview.result["input_digest"])
        await db.refresh(actor)
        applied = await service.apply_schedule(scenario.iterations[0], actor, data,
            command=AgentPlanningCommandContext(idempotency_key="strict-apply", rationale="Apply the observed inputs", correlation_id="strict-apply"))
        assert applied.operation == "planning.schedule.apply" and applied.result["input_digest"]
        from app.services.agent_service import AgentConflictError
        with pytest.raises(AgentConflictError, match="Schedule task versions changed"):
            await service.apply_schedule(scenario.iterations[0], actor, data,
                command=AgentPlanningCommandContext(idempotency_key="strict-stale-apply", rationale="Check stale input rejection", correlation_id="strict-stale-apply"))
