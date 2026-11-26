"""Recorded provenance lets work resolved outside recorded runs receive an ordinary independent review."""

import json
from contextlib import nullcontext
from datetime import timedelta
from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy import select, update

from app import database, mcp_server
from app.authority import Authority, AuthorityError
from app.commands import PlanningConflict
from app.config import get_settings
from app.main import app
from app.models.agent import (
    AgentActor, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent,
)
from app.models.identity import (
    CommandAudit, IdentitySubject, Principal, PrincipalProfileLink, ProjectMembership, WorkspaceMembership,
)
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMemberProfile
from app.models.user_session import UserSession
from app.schemas.agent import AgentTaskAssignmentCreate
from app.schemas.manual_provenance import ManualProvenanceWrite
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_work_service import AgentWorkService
from app.services.github_status_service import GitHubStatusService
from app.services.identity_service import IdentityService, digest, initialize_control_plane
from app.services.manual_provenance_service import ManualProvenanceService
from app.services.review_provenance import require_verifiable_candidate, review_history
from app.utils.time import utc_now
from tests.test_agent_routing_service import _rollout, _routing_fixture
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_review_provenance_transports import databases
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401


REPOSITORY = "https://github.com/example/project/"
FIRST, HEAD, UNLISTED = "1" * 40, "2" * 40, "3" * 40
PR_URL = REPOSITORY + "pull/7"
REASON = "Implemented locally and merged as a pull request outside recorded runs"


def provenance_body(task, executor, **changes):
    return {"expected_version": task["version"], "artifact_revision": task["artifact_revision"], "executor": executor,
            "head_commit_url": REPOSITORY + "commit/" + HEAD, "commit_urls": [REPOSITORY + "commit/" + FIRST],
            "pr_url": PR_URL, "reason": REASON, **changes}


def mock_github(monkeypatch, commits, head=HEAD):
    """Serve one pull request whose head and commits the test controls, as the verdict check reads them."""
    def respond(request):
        if request.url.path.endswith("/commits"):
            return httpx.Response(200, json=commits)
        return httpx.Response(200, json={"head": {"sha": head}, "commits": len(commits)})

    async def github(cls, session):
        return GitHubStatusService(session, transport=httpx.MockTransport(respond))
    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(github))


def plain_commits(*shas):
    return [{"sha": sha, "commit": {"message": "Change"}} for sha in shas]


class AgentProtocol:
    """Call agent commands over REST or MCP with the planning command headers."""

    def __init__(self, transport, factory, monkeypatch):
        monkeypatch.setattr(database, "async_session_maker", factory)
        monkeypatch.setattr(mcp_server, "_session_factory", factory)
        self.server = mcp_server.create_mcp_server() if transport == "mcp" else None

    async def __aenter__(self):
        application = mcp_server.MCPAgentKeyMiddleware(self.server.streamable_http_app()) if self.server else app
        self._running = self.server.session_manager.run() if self.server else nullcontext()
        await self._running.__aenter__()
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001")
        return self

    async def __aexit__(self, *exc):
        await self.client.aclose()
        await self._running.__aexit__(*exc)

    async def __call__(self, tool, path, key, *, payload, receipt, task_id=None, error=None):
        headers = {"X-Agent-API-Key": key, "Idempotency-Key": receipt, "X-Correlation-ID": receipt,
                   "X-Agent-Rationale": "Record and review work delivered outside recorded runs"}
        if self.server:
            args = {"payload": payload, "idempotency_key": receipt, "rationale": headers["X-Agent-Rationale"],
                    "correlation_id": receipt}
            if task_id is not None:
                args["task_id"] = task_id
            response = await self.client.post("/", headers={**headers, "Accept": "application/json, text/event-stream"}, json={
                "jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": args}})
            assert response.status_code == 200, response.text
            result = response.json()["result"]
            if error:
                assert result["isError"] and error in result["content"][0]["text"], result
                return result["content"][0]["text"]
            assert not result["isError"], result
            return json.loads(result["content"][0]["text"])
        response = await self.client.post(path, headers=headers, json=payload)
        if error:
            assert response.status_code in {403, 409} and error in response.text, response.text
            return response.text
        assert response.status_code in {200, 201}, response.text
        return response.json()


@databases
@pytest.mark.parametrize(("recorder", "transport", "executor_kind", "publishers"), [
    ("human", "rest", "agent", "distinct"),
    ("human", "rest", "human", "distinct"),
    ("pm", "mcp", "agent", "distinct"),
    ("pm", "rest", "agent", "distinct"),
    ("human", "rest", "agent", "executor_is_reviewer"),
    ("human", "rest", "agent", "status_route"),
    ("pm", "rest", "agent", "recorder_is_reviewer"),
    ("pm", "rest", "agent", "recorder_unknown"),
    ("pm", "rest", "human", "distinct"),
])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_recorded_provenance_allows_an_independent_review_of_work_merged_outside_runs(
        db_session, db_session_factory, task_factory, team_member_factory, profile_factory, monkeypatch,
        recorder, transport, executor_kind, publishers):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    team = await provision_ready_topology(db)
    member, verifier, controller = team.manifest.workers[0], team.manifest.verifiers[0], team.manifest.controller
    reviewer, executor_actor = team.actors[verifier.actor_key], team.actors[member.actor_key]
    base = await routing_base(db, topology=team, actor_key=member.actor_key, team_member_factory=team_member_factory,
                              task_factory=task_factory, title="Change merged outside recorded runs")
    task = base.task
    project = Project(name="Protected review", require_different_review_publisher=True)
    owner = Principal(kind="human", display_name="Project manager")
    db.add_all([project, owner])
    await db.flush()
    task.project_id = (await db.get(Iteration, task.iteration_id)).project_id = project.id
    owner_profile = await profile_factory(profile_kind="human", automation_enabled=False, assignment_modes=[])
    human_session = "p" * 43
    db.add_all([IdentitySubject(principal_id=owner.id, issuer="https://identity.example.test", subject="manager"),
        PrincipalProfileLink(principal_id=owner.id, profile_id=owner_profile.id, linked_by_principal_id=owner.id),
        WorkspaceMembership(principal_id=owner.id, role="member"),
        ProjectMembership(principal_id=owner.id, project_id=project.id, role="manager"),
        UserSession(principal_id=owner.id, session_token_hash=digest(human_session), csrf_token="fixture-csrf",
            ip_address="192.0.2.1", user_agent="test", authenticated_at=utc_now(), expires_at=utc_now() + timedelta(hours=1))])
    for actor, role in ((base.pm, "manager"), (reviewer, "reviewer")):
        identity = await IdentityService(db).actor_context(actor)
        db.add_all([WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                    ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role)])

    async def catalog(key):
        return await db.scalar(select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == key))
    (await catalog(verifier.default_model_binding_key)).publisher_key = "independent-model-maker"
    executor_publisher = ("independent-model-maker" if publishers in {"executor_is_reviewer", "status_route"}
                          else "executor-model-maker")
    (await catalog(member.default_model_binding_key)).publisher_key = executor_publisher
    (await catalog(controller.default_model_binding_key)).publisher_key = {
        "recorder_is_reviewer": "independent-model-maker", "recorder_unknown": None}.get(publishers, "planning-model-maker")
    if publishers != "status_route":
        # Resolved by hand after a local implementation: no runs and no manual execution history.
        progress = {"criteria": [], "artifacts": [PR_URL], "brief_revision": task.brief_revision, "artifact_revision": 1}
        task.status, task.resolved_at, task.artifact_revision, task.progress = "resolved", utc_now(), 1, progress
    await db.commit()
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    pm_key, reviewer_key = team.sink.keys[controller.actor_key], team.sink.keys[verifier.actor_key]
    executor = ({"kind": "agent", "actor_id": executor_actor.id} if executor_kind == "agent"
                else {"kind": "human", "principal_id": owner.id})
    async with AgentProtocol(transport, db_session_factory, monkeypatch) as agent, httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://localhost",
            headers={"Authorization": "Bearer " + human_session, "X-Correlation-ID": "record-provenance"}) as human:
        if publishers == "status_route":
            # The manager moves the task through the ordinary status route, which stamps them as the
            # executing principal in scheduled mode, and attaches the merged pull request as evidence.
            other = {"X-Correlation-ID": "resolve-by-status"}
            version = (await human.get(f"/api/tasks/{task.id}")).json()["version"]
            started = await human.put(f"/api/tasks/{task.id}/status", headers=other,
                                      json={"status": "active", "expected_version": version})
            assert started.status_code == 200, started.text
            progress = await human.post(f"/api/tasks/{task.id}/progress", headers=other, json={
                "expected_version": started.json()["task"]["version"], "criteria": [], "artifacts": [PR_URL]})
            assert progress.status_code == 200, progress.text
            resolved = await human.put(f"/api/tasks/{task.id}/status", headers=other,
                                       json={"status": "resolved", "expected_version": progress.json()["version"]})
            assert resolved.status_code == 200, resolved.text
            async with db_session_factory() as stored:
                stamped = await stored.get(Task, task.id)
                assert (stamped.status, stamped.execution_mode, stamped.executed_by_principal_id) == (
                    "resolved", "scheduled", owner.id)
        current = (await human.get(f"/api/tasks/{task.id}")).json()
        selection_request = {"task_id": task.id, "expected_task_version": current["version"], "actor_id": reviewer.id,
                             "purpose": "verification"}
        refused = await agent("agent_create_assignment", "/api/agent/assignments", pm_key, payload=selection_request,
                              receipt="unattributed-review", error="verification_publisher_unverifiable")
        assert "manual-provenance" in refused or "agent_record_manual_provenance" in refused

        body = provenance_body(current, executor)
        record_path = f"/api/agent/planning/tasks/{task.id}/manual-provenance"
        if recorder == "pm" and executor_kind == "human":
            # A human executor carries no publisher, so the PM agent cannot attest one.
            await agent("agent_record_manual_provenance", record_path, pm_key, task_id=task.id, payload=body,
                        receipt="record-provenance", error="manual_provenance_human_recorder_required")
            assert (await human.get(f"/api/tasks/{task.id}")).json()["version"] == current["version"]
            return
        if publishers == "recorder_unknown":
            await agent("agent_record_manual_provenance", record_path, pm_key, task_id=task.id, payload=body,
                        receipt="record-provenance", error="manual_provenance_recorder_unattributable")
            return
        if recorder == "human":
            response = await human.post(f"/api/tasks/{task.id}/manual-provenance", json=body)
            assert response.status_code == 201, response.text
            recorded = response.json()
        else:
            receipt = await agent("agent_record_manual_provenance", record_path, pm_key, task_id=task.id, payload=body,
                                  receipt="record-provenance")
            recorded = receipt["result"]
            assert recorded["recorded_by_actor_id"] == base.pm.id and recorded["recorder_publisher_key"]
        assert recorded["executor"]["kind"] == executor_kind
        assert recorded["commit_urls"] == sorted([REPOSITORY + "commit/" + FIRST, REPOSITORY + "commit/" + HEAD])
        if executor_kind == "agent":
            assert recorded["executor"]["actor_id"] == executor_actor.id
            assert recorded["executor"]["publisher_key"] == executor_publisher
        else:
            assert recorded["executor"]["profile_ids"] == [owner_profile.id]

        after = (await human.get(f"/api/tasks/{task.id}")).json()
        assert after["status"] == "resolved" and after["progress"] == current["progress"]
        assert after["version"] == current["version"] + 1 == recorded["task_version"]
        assert after["artifact_revision"] == current["artifact_revision"]

        selection_request["expected_task_version"] = after["version"]
        if publishers in {"executor_is_reviewer", "recorder_is_reviewer", "status_route"}:
            # Neither the executor's nor the recording PM's publisher may review the work.
            await agent("agent_create_assignment", "/api/agent/assignments", pm_key, payload=selection_request,
                        receipt="same-publisher-review", error="verification_publisher_not_independent")
            async with db_session_factory() as stored:
                assert not await stored.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == task.id))
            return
        assignment = await agent("agent_create_assignment", "/api/agent/assignments", pm_key, payload=selection_request,
                                 receipt="assign-recorded-review")
        selection = assignment["review_selection"]
        assert selection["candidate"]["manual_provenance_event_id"] == recorded["event_id"]
        assert selection["candidate"]["commit_url"] == REPOSITORY + "commit/" + HEAD
        contributors = {(row["provenance_role"], row["actor_id"], row["publisher_key"]) for row in selection["contributors"]}
        expected = set()
        if executor_kind == "agent":
            expected.add(("executor", executor_actor.id, "executor-model-maker"))
        else:
            assert selection["manual_execution"]["principal_id"] == owner.id
        if recorder == "pm":
            expected.add(("recorder", base.pm.id, "planning-model-maker"))
        assert contributors == expected
        verdict = {"assignment_id": assignment["id"], "expected_task_version": after["version"], "verdict": "pass",
                   "observed_model": verifier.default_model_binding_key,
                   "reviewed_candidate_digest": selection["candidate"]["digest"], "evidence": {"pull_request": PR_URL}}
        accepted = await agent("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                               payload=verdict, receipt="accept-recorded-work")
        assert accepted["task"]["status"] == "closed"

    async with db_session_factory() as stored:
        event = await stored.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id,
                                                            TaskEvent.event_type == "manual_provenance_recorded"))
        payload = json.loads(event.payload)
        assert payload["reason"] == REASON and payload["executor"]["kind"] == executor_kind
        # The command audit row of the record carries the record's reason, on the human and the planning routes.
        event_audits = [row for row in (await stored.scalars(select(CommandAudit))).all()
                        if row.action.startswith("task_events:") and (row.details or {}).get("entity_id") == event.id]
        assert event_audits and all(row.reason == REASON for row in event_audits)
        if transport == "rest":
            # Over REST the request's correlation id finds every audit row of the command, receipt included.
            audits = (await stored.scalars(select(CommandAudit).where(CommandAudit.correlation_id == "record-provenance"))).all()
            assert audits and all(row.reason == REASON for row in audits)
        if recorder == "human":
            assert payload["principal_id"] == owner.id and event.actor_id is None
            assert all(row.principal_id == owner.id for row in audits)
        else:
            assert event.actor_id == base.pm.id and payload["recorder"]["actor_id"] == base.pm.id
        assert not await stored.scalar(select(AgentRun.id).where(AgentRun.task_id == task.id))


@pytest.mark.asyncio
@databases
async def test_no_verification_assignment_for_a_known_unverifiable_candidate(db_session, actor_factory, profile_factory,
                                                                              team_member_factory, task_factory):
    db = db_session
    pm, worker, task, _, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    project = Project(name="Agent delivery", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    task.project_id = project.id
    catalog.publisher_key = "model-maker-a"
    review_profile = await profile_factory(assignment_modes=["verification"])
    reviewer = await actor_factory(profile=review_profile, role="verifier", scopes=json.dumps(["verification:write", "assignments:read"]))
    review_catalog = AgentModelCatalogEntry(key="review-model", provider=catalog.provider, publisher_key="model-maker-b",
        configured_model_alias="review-runtime", reasoning_tier=2, context_tier="medium", cost_tier="low", latency_tier="fast")
    db.add(review_catalog)
    await db.flush()
    db.add(AgentModelBinding(actor_id=reviewer.id, model_catalog_id=review_catalog.id, is_default=True))
    # An attributed run that never left a matching submission receipt, so no exact candidate exists.
    execution = AgentTaskAssignment(task_id=task.id, task_version=task.version, actor_id=worker.id, state="fulfilled")
    db.add(execution)
    await db.flush()
    db.add(AgentRun(task_id=task.id, actor_id=worker.id, assignment_id=execution.id, claim_generation=1, status="succeeded",
                    ended_at=utc_now(), execution_provenance={"actor_id": worker.id, "profile_id": worker.profile_id,
                                                              "publisher_key": "model-maker-a"}))
    task.status = "resolved"
    await db.commit()
    task_id, version, reviewer_id = task.id, task.version, reviewer.id
    service = AgentWorkService(db, rollout_service=_rollout("shadow"))
    with pytest.raises(AgentRoutingConflictError) as refused:
        await service.create_assignment(pm, AgentTaskAssignmentCreate(task_id=task_id, actor_id=reviewer_id, purpose="verification",
            expected_task_version=version), idempotency_key="unverifiable-candidate",
            rationale="Review the submitted candidate.", correlation_id="unverifiable-candidate")
    assert refused.value.code == "verification_candidate_unverifiable"
    assert refused.value.context["missing"] == [{"task_id": task_id, "facts": ["submitted_candidate"]}]
    assert "remedy" not in refused.value.context
    await db.rollback()
    assert not await db.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == task_id,
                                                                     AgentTaskAssignment.purpose == "verification"))


@pytest.mark.sqlite
def test_a_candidate_less_refusal_names_only_a_remedy_that_can_help():
    task = SimpleNamespace(id=41)
    with pytest.raises(AgentRoutingConflictError) as unrecorded:
        require_verifiable_candidate(task, {"candidate": None, "contributors": []})
    assert unrecorded.value.context["missing"] == [{"task_id": 41, "facts": ["submitted_candidate", "manual_provenance"]}]
    assert unrecorded.value.context["remedy"]["rest"] == "POST /api/tasks/41/manual-provenance"
    assert unrecorded.value.context["remedy"]["mcp"] == "agent_record_manual_provenance"
    # Manual execution taken from a stale provenance record: a fresh record helps.
    with pytest.raises(AgentRoutingConflictError) as stale_record:
        require_verifiable_candidate(task, {"candidate": None, "contributors": [],
                                            "manual_execution": {"principal_id": 3, "provenance_event_id": 9}})
    assert stale_record.value.context["remedy"]["rest"] == "POST /api/tasks/41/manual-provenance"
    # Authenticated manual execution already supplies provenance, so the record command would refuse.
    with pytest.raises(AgentRoutingConflictError) as manual:
        require_verifiable_candidate(task, {"candidate": None, "contributors": [],
                                            "manual_execution": {"principal_id": 3, "progress_record_id": 4}})
    assert manual.value.context == {"missing": [{"task_id": 41, "facts": ["current_human_artifact"]}]}
    assert "pull request" in manual.value.message and "compare URL" in manual.value.message
    with pytest.raises(AgentRoutingConflictError) as executed:
        require_verifiable_candidate(task, {"candidate": None, "contributors": [{"run_id": 5}]})
    assert "remedy" not in executed.value.context
    require_verifiable_candidate(task, {"candidate": {"digest": "a"}, "contributors": []})
    require_verifiable_candidate(task, None)


async def provenance_scope(factory, scenario):
    async with factory() as db:
        project_id = scenario.projects[0]
        await db.execute(update(Project).where(Project.id == project_id).values(require_different_review_publisher=True))
        recorder, executor = Principal(kind="human", display_name="Recorder"), Principal(kind="human", display_name="Executor")
        db.add_all([recorder, executor])
        task = await db.get(Task, scenario.tasks["resolved"])
        # The pull request is the task's own evidence.
        task.progress = {"criteria": [], "artifacts": [PR_URL], "brief_revision": task.brief_revision, "artifact_revision": 0}
        await db.commit()
        return project_id, recorder.id, executor.id, task.id


def write(task, executor_id, **changes):
    if isinstance(task, Task):
        task = {"version": task.version, "artifact_revision": task.artifact_revision}
    executor = changes.pop("executor", {"kind": "human", "principal_id": executor_id})
    return ManualProvenanceWrite(**provenance_body(task, executor, **changes))


async def task_state(factory, task_id):
    async with factory() as db:
        task = await db.get(Task, task_id)
        return {"version": task.version, "artifact_revision": task.artifact_revision}


async def agent_executor(factory, *, publisher="executor-model-maker", enabled=True, key="executor-model"):
    """An agent actor with a profile and one binding whose catalog entry declares the publisher."""
    async with factory() as db:
        profile = TeamMemberProfile(seed_key=f"{key}-profile", display_name="Executor profile", automation_enabled=True,
                                    profile_kind="agent", assignment_modes=["execution"])
        db.add(profile)
        await db.flush()
        actor = AgentActor(name=f"{key}-actor", display_name="Executor", api_key_hash=f"{key}-hash",
                           scopes='["work:execute"]', role="worker", profile_id=profile.id)
        entry = AgentModelCatalogEntry(key=key, provider="fixture", publisher_key=publisher, configured_model_alias=f"{key}-runtime",
                                       reasoning_tier=2, context_tier="medium", cost_tier="low", latency_tier="fast")
        db.add_all([actor, entry])
        await db.flush()
        binding = AgentModelBinding(actor_id=actor.id, model_catalog_id=entry.id, is_default=enabled, enabled=enabled)
        db.add(binding)
        await db.commit()
        return actor.id, profile.id, binding.id


@pytest.mark.parametrize("authority", [
    lambda pid, principal: Authority(None, "local", local=True),
    lambda pid, principal: Authority(principal, "system", workspace_role="operator", review_override=True, reason=REASON),
    lambda pid, principal: Authority(principal, "agent", actor_id=1, actor_role="worker", projects={pid: "manager"},
                                     scopes=frozenset({"planning:read", "planning:write"})),
    lambda pid, principal: Authority(principal, "human", workspace_role="owner", read_only=True),
    lambda pid, principal: Authority(principal, "human", workspace_role="member", projects={pid: "reviewer"}),
], ids=["trusted-local", "operator-key", "worker-agent", "observer", "project-reviewer"])
async def test_only_an_accountable_owner_or_pm_may_record(delivery_store, authority):  # noqa: F811
    factory, scenario, _ = delivery_store
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    async with factory() as db:
        task = await db.get(Task, task_id)
        version = task.version
        caller = authority(project_id, recorder_id)
        db.info["authority"] = caller
        with pytest.raises(AuthorityError) as refused:
            await ManualProvenanceService(db).record(task_id, write(task, executor_id))
        assert refused.value.code == "provenance_recorder_required"
        assert db.info["authority"] is caller
    async with factory() as db:
        assert (await db.get(Task, task_id)).version == version
        assert not await db.scalar(select(TaskEvent.id).where(TaskEvent.event_type == "manual_provenance_recorded"))


async def test_a_pm_agent_cannot_attest_a_human_executor(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    pm = Authority(recorder_id, "agent", actor_id=1, actor_role="pm", projects={project_id: "manager"},
                   scopes=frozenset({"planning:read", "planning:write"}))
    async with factory() as db:
        db.info["authority"] = pm
        with pytest.raises(AuthorityError) as refused:
            await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), executor_id))
        assert refused.value.code == "manual_provenance_human_recorder_required"


async def test_record_refuses_unresolved_stale_executed_and_unattributable_work(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    manager = Authority(recorder_id, "human", workspace_role="member", projects={project_id: "manager"})
    async with factory() as db:
        actor = AgentActor(name="profileless-executor", display_name="Profileless executor",
                           api_key_hash="profileless-executor-hash", scopes='["work:execute"]', role="worker")
        db.add(actor)
        await db.commit()
        actor_id = actor.id
    task = await task_state(factory, task_id)
    async with factory() as db:
        db.info["authority"] = manager
        other = await db.get(Task, scenario.tasks["active"])
        other = {"id": other.id, "version": other.version, "artifact_revision": other.artifact_revision}
        service = ManualProvenanceService(db)
        with pytest.raises(ValueError, match="stale"):
            await service.record(task_id, write(task, executor_id, artifact_revision=task["artifact_revision"] + 1))
        with pytest.raises(ValueError, match="commit URL"):
            await service.record(task_id, write(task, executor_id, head_commit_url=PR_URL))
        with pytest.raises(PlanningConflict) as unknown:
            await service.record(task_id, write(task, executor_id, executor={"kind": "human", "principal_id": 999_999}))
        assert unknown.value.code == "manual_provenance_executor_unknown"
        with pytest.raises(ValueError):
            write(task, executor_id, pr_url=None)
        with pytest.raises(ValueError):
            write(task, executor_id, executor={"kind": "agent", "principal_id": executor_id})
        with pytest.raises(PlanningConflict) as unattributable:
            await service.record(task_id, write(task, executor_id, executor={"kind": "agent", "actor_id": actor_id}))
        assert unattributable.value.code == "manual_provenance_executor_unattributable"
        with pytest.raises(PlanningConflict) as unrelated:
            await service.record(task_id, write(task, executor_id, pr_url=REPOSITORY + "pull/8"))
        assert unrelated.value.code == "manual_provenance_pr_not_task_evidence"

        recorded = await service.record(task_id, write(task, executor_id))
        assert recorded["task_version"] == task["version"] + 1 and recorded["recorded_by_principal_id"] == recorder_id
        assert recorded["artifact_revision"] == task["artifact_revision"]
        with pytest.raises(PlanningConflict) as unresolved:
            await service.record(other["id"], write(other, executor_id))
        assert unresolved.value.code == "manual_provenance_requires_resolved_work"

    task = await task_state(factory, task_id)
    async with factory() as db:
        db.add(TaskEvent(task_id=task_id, actor_type="agent", event_type="agent.work_began", payload="{}"))
        await db.commit()
    async with factory() as db:
        db.info["authority"] = manager
        with pytest.raises(PlanningConflict) as began:
            await ManualProvenanceService(db).record(task_id, write(task, executor_id))
        assert began.value.code == "manual_provenance_execution_recorded"
    async with factory() as db:
        db.add(AgentRun(task_id=task_id, actor_id=actor_id, status="failed"))
        await db.commit()
    async with factory() as db:
        db.info["authority"] = manager
        with pytest.raises(PlanningConflict) as executed:
            await ManualProvenanceService(db).record(task_id, write(task, executor_id))
        assert executed.value.code == "manual_provenance_execution_recorded"
    async with factory() as db:
        stored = await db.get(Task, task_id)
        assert (stored.status, stored.version) == ("resolved", recorded["task_version"])
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == task_id,
                                                           TaskEvent.event_type == "manual_provenance_recorded"))).all()
        assert len(events) == 1


async def test_a_record_cannot_contradict_the_recorded_executor(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    agent_id, _, _ = await agent_executor(factory)
    manager = Authority(recorder_id, "human", workspace_role="member", projects={project_id: "manager"})
    async with factory() as db:
        # In scheduled mode any status change stamps its caller; that stamp is not evidence of execution.
        await db.execute(update(Task).where(Task.id == task_id).values(executed_by_principal_id=recorder_id))
        await db.commit()
    async with factory() as db:
        db.info["authority"] = manager
        scheduled = await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), executor_id,
                                                                            executor={"kind": "agent", "actor_id": agent_id}))
        assert scheduled["executor"]["actor_id"] == agent_id
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == task_id).values(execution_mode="manual", executed_by_principal_id=None))
        await db.commit()
    async with factory() as db:
        db.info["authority"] = manager
        with pytest.raises(PlanningConflict) as manual:
            await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), executor_id,
                                                                    executor={"kind": "agent", "actor_id": agent_id}))
        assert manual.value.code == "manual_provenance_executor_conflict"
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == task_id).values(executed_by_principal_id=executor_id))
        await db.commit()
    async with factory() as db:
        db.info["authority"] = manager
        with pytest.raises(PlanningConflict) as other_person:
            await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), recorder_id))
        assert other_person.value.code == "manual_provenance_executor_conflict"
        recorded = await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), executor_id))
        assert recorded["executor"]["principal_id"] == executor_id


@pytest.mark.parametrize(("commits", "head", "sha", "gap"), [
    (plain_commits(FIRST, UNLISTED, HEAD), HEAD, UNLISTED, "commit_attribution"),
    (plain_commits(FIRST) + [{"sha": HEAD, "commit": {"message": "Change\n\nCo-authored-by: Pair <pair@example.test>"}}],
     HEAD, HEAD, "coauthor_trailer"),
    (plain_commits(FIRST, HEAD), UNLISTED, None, "head_mismatch"),
], ids=["unlisted-commit", "coauthor-trailer", "different-head"])
async def test_record_refuses_a_candidate_the_verdict_could_never_pass(delivery_store, monkeypatch,  # noqa: F811
                                                                      commits, head, sha, gap):
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, commits, head=head)
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    task = await task_state(factory, task_id)
    async with factory() as db:
        db.info["authority"] = Authority(recorder_id, "human", workspace_role="owner")
        with pytest.raises(PlanningConflict) as refused:
            await ManualProvenanceService(db).record(task_id, write(task, executor_id))
    detail = refused.value.detail()
    assert detail["code"] == "manual_provenance_candidate_unverifiable" and detail["attribution_gap"] == gap
    if sha:
        assert detail["offending_sha"] == sha and sha in detail["message"]
    assert await task_state(factory, task_id) == task


async def test_recorded_contribution_survives_rework_and_accepts_a_retired_binding(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, recorder_id, _, task_id = await provenance_scope(factory, scenario)
    # The work predates the retirement of the binding; its catalog publisher is still known.
    agent_id, profile_id, binding_id = await agent_executor(factory, enabled=False)
    async with factory() as db:
        db.info["authority"] = Authority(recorder_id, "human", workspace_role="owner")
        recorded = await ManualProvenanceService(db).record(task_id, write(
            await task_state(factory, task_id), None,
            executor={"kind": "agent", "actor_id": agent_id, "model_binding_id": binding_id}))
    assert (recorded["executor"]["binding_id"], recorded["executor"]["publisher_key"]) == (binding_id, "executor-model-maker")
    rework_actor, _, _ = await agent_executor(factory, publisher="rework-model-maker", key="rework-model")
    async with factory() as db:
        # A rejection led to a rework run that built on the recorded commits and changed the artifact.
        rework = AgentTaskAssignment(task_id=task_id, task_version=recorded["task_version"], actor_id=rework_actor, state="fulfilled")
        db.add(rework)
        await db.flush()
        db.add(AgentRun(task_id=task_id, actor_id=rework_actor, assignment_id=rework.id, claim_generation=1, status="succeeded",
                        ended_at=utc_now(), execution_provenance={"actor_id": rework_actor, "publisher_key": "rework-model-maker"}))
        await db.execute(update(Task).where(Task.id == task_id).values(artifact_revision=Task.artifact_revision + 1))
        await db.commit()
    async with factory() as db:
        task = await db.get(Task, task_id)
        history = await review_history(db, task, [await db.get(AgentTaskAssignment, rework.id)], strict=True)
    recorded_rows = [row for row in history.contributors if row.get("provenance_role") == "executor"]
    assert [(row["actor_id"], row["profile_id"], row["publisher_key"], row["commit_urls"]) for row in recorded_rows] == [
        (agent_id, profile_id, "executor-model-maker", recorded["commit_urls"])]
    assert {row["actor_id"] for row in history.contributors if row["run_id"]} == {rework_actor}
    assert history.publisher_blockers("executor-model-maker") == ["verification_publisher_not_independent"]
    assert history.publisher_blockers("third-model-maker") == []


async def test_a_stale_human_record_points_at_a_fresh_record(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    async with factory() as db:
        db.info["authority"] = Authority(recorder_id, "human", workspace_role="owner")
        recorded = await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), executor_id))
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == task_id).values(artifact_revision=Task.artifact_revision + 1))
        await db.commit()
    async with factory() as db:
        task = await db.get(Task, task_id)
        history = await review_history(db, task, [], strict=True)
    assert history.candidate is None and history.manual_execution["provenance_event_id"] == recorded["event_id"]
    with pytest.raises(AgentRoutingConflictError) as refused:
        require_verifiable_candidate(task, {"candidate": history.candidate, "contributors": history.contributors,
                                            "manual_execution": history.manual_execution})
    assert refused.value.code == "verification_candidate_unverifiable"
    assert refused.value.context["missing"] == [{"task_id": task_id, "facts": ["submitted_candidate", "manual_provenance"]}]
    assert refused.value.context["remedy"]["mcp"] == "agent_record_manual_provenance"


async def test_record_refuses_once_review_could_no_longer_read_every_record(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, recorder_id, executor_id, task_id = await provenance_scope(factory, scenario)
    async with factory() as db:
        db.add_all([TaskEvent(task_id=task_id, actor_type="user", event_type="manual_provenance_recorded", payload="{}")
                    for _ in range(50)])
        await db.commit()
    task = await task_state(factory, task_id)
    async with factory() as db:
        db.info["authority"] = Authority(recorder_id, "human", workspace_role="owner")
        with pytest.raises(PlanningConflict) as refused:
            await ManualProvenanceService(db).record(task_id, write(task, executor_id))
    assert refused.value.code == "manual_provenance_record_limit"
    assert await task_state(factory, task_id) == task


async def test_an_agent_recorder_counts_under_every_enabled_binding(delivery_store, monkeypatch):  # noqa: F811
    factory, scenario, _ = delivery_store
    mock_github(monkeypatch, plain_commits(FIRST, HEAD))
    project_id, _, _, task_id = await provenance_scope(factory, scenario)
    executor_id, _, _ = await agent_executor(factory)
    recorder_id, recorder_profile, _ = await agent_executor(factory, publisher="planning-maker-a", key="planning-model")
    async with factory() as db:
        second = AgentModelCatalogEntry(key="planning-other", provider="fixture", publisher_key="planning-maker-b",
                                        configured_model_alias="planning-other-runtime", reasoning_tier=2,
                                        context_tier="medium", cost_tier="low", latency_tier="fast")
        db.add(second)
        await db.flush()
        db.add(AgentModelBinding(actor_id=recorder_id, model_catalog_id=second.id, is_default=False, enabled=True))
        await db.commit()
    pm = Authority(None, "agent", actor_id=recorder_id, actor_role="pm", projects={project_id: "manager"},
                   scopes=frozenset({"planning:read", "planning:write"}))
    async with factory() as db:
        db.info["authority"] = pm
        await ManualProvenanceService(db).record(task_id, write(await task_state(factory, task_id), None,
                                                                executor={"kind": "agent", "actor_id": executor_id}))
    async with factory() as db:
        history = await review_history(db, await db.get(Task, task_id), [], strict=True)
    recorders = {(row["actor_id"], row["profile_id"], row["publisher_key"])
                 for row in history.contributors if row.get("provenance_role") == "recorder"}
    assert recorders == {(recorder_id, recorder_profile, "planning-maker-a"), (recorder_id, recorder_profile, "planning-maker-b")}
    assert history.publisher_blockers("planning-maker-b") == ["verification_publisher_not_independent"]
