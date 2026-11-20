"""Authenticated human delivery still requires an assigned agent decision in a strict project."""

from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from app.config import get_settings
from app.main import app
from app.models.agent import AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.identity import IdentitySubject, Principal, PrincipalProfileLink, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.task_brief import TaskProgressRecord
from app.models.user_session import UserSession
from app.services.identity_service import IdentityService, digest, initialize_control_plane
from app.services.review_provenance import review_history
from app.services.github_status_service import GitHubStatusService
from app.services.agent_routing_policy import RoutingProfileEvidence, evaluate_assignment_compatibility
from app.utils.time import utc_now
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases
from tests.test_team_pm_dispatch import db_session_factory
from tests.test_team_pm_recovery import recovery_api


@databases
@pytest.mark.parametrize(("transport", "delivery"), [("rest", "document"), ("mcp", "repository"),
                                                   ("rest", "coauthored"), ("mcp", "missing_artifact")])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_authenticated_manual_submission_and_assigned_agent_verdict(db_session, db_session_factory,
    task_factory, team_member_factory, profile_factory, monkeypatch, transport, delivery):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    team = await provision_ready_topology(db)
    member, verifier = team.manifest.workers[0], team.manifest.verifiers[0]
    reviewer = team.actors[verifier.actor_key]
    base = await routing_base(db, topology=team, actor_key=member.actor_key, team_member_factory=team_member_factory,
                              task_factory=task_factory, title="Owner-operated configuration")
    task = base.task
    project = Project(name="Protected review", require_different_review_publisher=True)
    owner = Principal(kind="human", display_name="Operator of the project")
    db.add_all([project, owner])
    await db.flush()
    task.project_id = (await db.get(Iteration, task.iteration_id)).project_id = project.id
    owner_profile = await profile_factory(profile_kind="human", automation_enabled=False, assignment_modes=[])
    human_session = "h" * 43
    db.add_all([IdentitySubject(principal_id=owner.id, issuer="https://identity.example.test", subject="owner"),
        PrincipalProfileLink(principal_id=owner.id, profile_id=owner_profile.id, linked_by_principal_id=owner.id),
        WorkspaceMembership(principal_id=owner.id, role="member"),
        ProjectMembership(principal_id=owner.id, project_id=project.id, role="manager"),
        UserSession(principal_id=owner.id, session_token_hash=digest(human_session), csrf_token="fixture-csrf",
            ip_address="192.0.2.1", user_agent="test", authenticated_at=utc_now(), expires_at=utc_now()+timedelta(hours=1))])
    for actor, role in ((base.pm, "manager"), (reviewer, "reviewer")):
        identity = await IdentityService(db).actor_context(actor)
        db.add_all([WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                    ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role)])
    model = await db.scalar(select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == verifier.default_model_binding_key))
    model.publisher_key = "independent-model-maker"
    await db.commit()
    head = "a"*40
    url = "https://github.com/example/project/"
    artifacts = [] if delivery == "missing_artifact" else ["https://example.test/reports/revision-24"] if delivery == "document" else [url+"pull/1", url+"commit/"+head]
    message = "Reviewed configuration" + ("\nCo-authored-by: fixture contributor" if delivery == "coauthored" else "")
    commits = [{"sha": head, "commit": {"message": message}}]
    def respond(request):
        return httpx.Response(200, json=commits if request.url.path.endswith("/commits") else {"head": {"sha": head}, "commits": 1})
    async def github(cls, session):
        return GitHubStatusService(session, transport=httpx.MockTransport(respond))
    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(github))
    async with recovery_api(transport, db_session_factory, monkeypatch) as agent, httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://localhost",
            headers={"Authorization": "Bearer "+human_session}) as human:
        async def post(action, data):
            result = await human.post(f"/api/tasks/{task.id}/{action}", json=data)
            assert result.status_code == 200, result.text
            return result.json()
        started = await post("commands", {"action": "start_manual", "expected_version": task.version, "reason": "Perform owner work"})
        progress = await post("progress", {"expected_version": started["version"], "criteria": [], "artifacts": artifacts})
        resolved = await post("commands", {"action": "resolve_manual", "expected_version": progress["version"], "reason": "Submit the artifact"})
        pm_key, reviewer_key = team.sink.keys[team.manifest.controller.actor_key], team.sink.keys[verifier.actor_key]
        selection_request = {"task_id": task.id, "expected_task_version": resolved["version"], "actor_id": reviewer.id, "purpose": "verification"}
        if delivery == "missing_artifact":
            await agent("agent_create_assignment", "/api/agent/assignments", pm_key, payload=selection_request,
                        receipt="missing-manual-artifact", error="current_human_artifact")
            async with db_session_factory() as recorded:
                assert not await recorded.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == task.id))
            return
        assignment = await agent("agent_create_assignment", "/api/agent/assignments", pm_key, payload=selection_request, receipt="assign-manual-review")
        selection = assignment["review_selection"]
        assert selection["manual_execution"]["principal_id"] == owner.id
        assert selection["manual_execution"]["profile_ids"] == [owner_profile.id]
        assert selection["candidate"]["manual_progress_record_id"] == selection["manual_execution"]["progress_record_id"]
        assert selection["contributors"] == [] and selection["reviewer"]["publisher_key"] == "independent-model-maker"
        assert (await human.post(f"/api/tasks/{task.id}/review", json={"expected_version": resolved["version"],
            "brief_revision": resolved["brief_revision"], "artifact_revision": resolved["artifact_revision"],
            "verdict": "accept", "reason": "Owner acceptance"})).status_code == 403
        verdict={"assignment_id": assignment["id"], "expected_task_version": resolved["version"], "verdict": "pass",
                 "observed_model": verifier.default_model_binding_key, "reviewed_candidate_digest": selection["candidate"]["digest"],
                 "evidence": {"artifact": artifacts[0]}}
        await agent("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
            payload={**verdict, "reviewed_candidate_digest": "f"*64}, receipt="stale-manual-candidate", error="verification_candidate_stale")
        if delivery == "coauthored":
            await agent("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                        payload=verdict, receipt="unresolved-coauthor", error=head)
        else:
            accepted = await agent("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                payload=verdict, receipt="accept-manual-configuration")
            assert accepted["task"]["status"] == "closed"
    async with db_session_factory() as recorded:
        assert not await recorded.scalar(select(AgentRun.id).where(AgentRun.task_id==task.id))
        assert not await recorded.scalar(select(AgentTaskAssignment.id).where(
            AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.purpose == "execution"))
        assert await recorded.scalar(select(TaskProgressRecord.principal_id).where(TaskProgressRecord.task_id==task.id)) == owner.id
        if delivery == "coauthored":
            assert (await recorded.get(Task, task.id)).status == "resolved"


@databases
async def test_unconfirmed_manual_work_stays_held(db_session, db_session_factory, task_factory, actor_factory):
    db = db_session
    task = await task_factory(status="resolved", execution_mode="manual")
    task.progress = {"artifacts": ["https://example.test/unconfirmed"], "artifact_revision": 1, "brief_revision": 0}
    task.artifact_revision = 1
    await db.flush()
    history = await review_history(db, task, [], strict=True)
    assert history.manual_execution is None and history.publisher_blockers("model-maker")
    principal = Principal(kind="human", display_name="Named owner")
    db.add(principal)
    await db.flush()
    task.executed_by_principal_id = principal.id
    await db.flush()
    history = await review_history(db, task, [], strict=True)
    assert history.manual_execution is None and history.missing_manual_fact == "task_start_manual"
    actor = await actor_factory()
    db.add(AgentRun(task_id=task.id, actor_id=actor.id, status="failed"))
    await db.flush()
    history = await review_history(db, task, [], strict=True)
    assert not history.manual_execution and history.publisher_blockers("model-maker") and history.contributors


@pytest.mark.sqlite
def test_verifier_preview_keeps_the_authenticated_humans_profile_independent():
    reviewer = RoutingProfileEvidence(profile_id=7, profile_kind="agent", automation_enabled=True,
                                      assignment_modes=frozenset({"verification"}))
    context = {"intent": "verification", "actor_id": 13, "actor_profile": reviewer, "reviewer_profile_id": 7}
    assert "verification_independence_unverifiable" in evaluate_assignment_compatibility(**context).compatibility_blocker_codes
    assert not evaluate_assignment_compatibility(**context, manual_executor_profile_ids=[12]).compatibility_blocker_codes
    assert "verification_profile_not_independent" in evaluate_assignment_compatibility(
        **context, manual_executor_profile_ids=[7]).compatibility_blocker_codes
