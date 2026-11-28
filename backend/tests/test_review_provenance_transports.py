"""Exercise strict review, interruption and return through the registered worker and PM protocols."""

from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from app.config import get_settings
from app.models.agent import AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.services.github_status_service import GitHubStatusService
from app.services.review_provenance import recover_terminal_observation
from app.utils.time import utc_now
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_team_pm_dispatch import db_session_factory
from tests.test_team_pm_recovery import recovery_api


databases = pytest.mark.parametrize("db_session_factory", [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
], indirect=True)


def fence(receipt):
    return {"assignment_id": receipt["assignment"]["id"], "run_id": receipt["run"]["id"],
            "claim_id": receipt["claim_id"], "claim_generation": receipt["claim_generation"],
            "expected_task_version": receipt["task"]["version"]}


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("outcome", ["sealed_pass", "sealed_rework", "unknown"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_strict_recovery_and_provider_review(db_session, db_session_factory, task_factory,
                                                   team_member_factory, monkeypatch, transport, outcome):
    sealed = outcome != "unknown"
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    team = await provision_ready_topology(db)
    member, verifier = team.manifest.workers[0], team.manifest.verifiers[0]
    worker, reviewer = team.actors[member.actor_key], team.actors[verifier.actor_key]
    worker_profile_id = worker.profile_id
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    worker_key, reviewer_key = team.sink.keys[member.actor_key], team.sink.keys[verifier.actor_key]
    base = await routing_base(db, topology=team, actor_key=member.actor_key, team_member_factory=team_member_factory,
                              task_factory=task_factory, title="Review the delivered change")
    task = base.task
    project = Project(name="Release tools", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    iteration = await db.get(Iteration, task.iteration_id)
    task.project_id = iteration.project_id = project.id
    task.effort_hours = 8
    for key, publisher in ((member.default_model_binding_key, "first-publisher"), (verifier.default_model_binding_key, "second-publisher")):
        model = await db.scalar(select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == key))
        model.publisher_key = publisher
    await db.commit()
    first_sha, head_sha = "a" * 40, "b" * 40
    url = "https://github.com/example/project/"
    pulls = {"head": {"sha": head_sha}, "commits": 2}
    commits = [{"sha": sha, "commit": {"author": {"email": "bot@example.test"}, "message": "Update"}}
               for sha in (first_sha, head_sha)]
    def response(request):
        return httpx.Response(200, json=commits if request.url.path.endswith("/commits") else pulls)
    async def github(cls, session):
        return GitHubStatusService(session, transport=httpx.MockTransport(response))
    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(github))
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        assign = "agent_create_assignment", "/api/agent/assignments"
        begin = "agent_begin_my_work", "/api/agent/me/work/begin"
        requeue = "agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue"
        work = "agent_get_my_work", "/api/agent/me/work"
        original = await call(*assign, pm_key, payload={"task_id": task.id, "actor_id": worker.id,
            "expected_task_version": task.version}, receipt="first-assignment")
        decision = await call(*work, worker_key)
        await call(*begin, worker_key, payload={"assignment_id": original["id"], "queue_revision": decision["queue_revision"],
            "model": "unbound-model"}, receipt="decline-unbound-model", error="execution_publisher_unverifiable")
        async with db_session_factory() as audit:
            unclaimed = await audit.get(Task, task.id)
            assert unclaimed.claimed_by is None and unclaimed.claim_id is None
            assert (await audit.get(AgentTaskAssignment, original["id"])).state == "queued"
            assert not await audit.scalar(select(AgentRun.id).where(AgentRun.task_id == task.id))
        claim = await call(*begin, worker_key, payload={"assignment_id": original["id"], "queue_revision": decision["queue_revision"],
            "model": member.default_model_binding_key}, receipt="first-begin")
        if sealed:
            claim = await call("agent_renew_my_work", "/api/agent/me/work/renew", worker_key,
                payload={**fence(claim), "interruption_checkpoint": {"output_state": "no_output", "observed_model": member.default_model_binding_key}},
                receipt="sealed-renew")
        else:
            async with db_session_factory() as clock:
                interrupted = await clock.get(Task, task.id)
                interrupted.claim_expires_at = utc_now() - timedelta(minutes=1)
                await clock.commit()
        recovery = await call(*requeue, pm_key, task_id=task.id, payload={"actor_id": worker.id,
            "expected_task_version": claim["task"]["version"], "expected_claim_generation": claim["claim_generation"],
            "expected_live_assignment_ids": [original["id"]], "expected_running_run_ids": [claim["run"]["id"]],
            "reason": "Resume the interrupted scope"}, receipt="recover-interruption")
        async with db_session_factory() as audit:
            interrupted_run = await audit.get(AgentRun, claim["run"]["id"])
            terminal, sources = await recover_terminal_observation(audit, interrupted_run)
            assert (terminal is not None and bool(sources)) == sealed
            assert interrupted_run.execution_provenance["terminal_model"]["output_state"] == ("no_output" if sealed else "unknown")
            # PM recovery ended the run, so it records the actor's profile as the terminal command would.
            assert interrupted_run.execution_provenance["terminal_profile_id"] == worker_profile_id
            if sealed:
                interrupted_run.execution_provenance = {key: value for key, value in interrupted_run.execution_provenance.items()
                                                        if key != "interruption_checkpoint"}
                reconstructed, source_ids = await recover_terminal_observation(audit, interrupted_run)
                assert reconstructed == terminal and source_ids == sources
        decision = await call(*work, worker_key)
        next_run = await call(*begin, worker_key, payload={"assignment_id": recovery["assignment"]["id"],
            "queue_revision": decision["queue_revision"], "model": member.default_model_binding_key}, receipt="next-begin")
        submitted = await call("agent_submit_my_work", "/api/agent/me/work/submit", worker_key, payload={
            **fence(next_run), "observed_model": member.default_model_binding_key, "summary": "Ready for review",
            "evidence": {"tests": "passed"}, "commit_url": url+"commit/"+head_sha, "pr_url": url+"pull/1",
            "commit_urls": [url+"commit/"+first_sha, url+"commit/"+head_sha]}, receipt="submit-candidate")
        request = {"task_id": task.id, "actor_id": reviewer.id, "expected_task_version": submitted["task"]["version"], "purpose": "verification"}
        if not sealed:
            await call(*assign, pm_key, payload=request, receipt="unresolved-review", error="terminal_model")
            returned = await call(*requeue, pm_key, task_id=task.id, payload={"actor_id": worker.id,
                "return_for_evidence": True, "expected_task_version": submitted["task"]["version"],
                "expected_claim_generation": next_run["claim_generation"], "expected_live_assignment_ids": [],
                "expected_running_run_ids": [], "reason": "Collect missing runtime evidence"}, receipt="return-for-evidence")
            assert returned["task"]["status"] == "active"
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(TaskEvent.id).where(TaskEvent.task_id==task.id, TaskEvent.event_type=="agent.verification_verdict"))
            return
        assignment = await call(*assign, pm_key, payload=request, receipt="assign-review")
        candidate = assignment["review_selection"]["candidate"]
        verdict = {"assignment_id": assignment["id"], "expected_task_version": submitted["task"]["version"],
                   "observed_model": verifier.default_model_binding_key, "reviewed_candidate_digest": candidate["digest"],
                   "evidence": {"tests": "passed"}, "verdict": "pass"}
        pulls["head"]["sha"] = first_sha
        await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                   payload=verdict, receipt="stale-head", error="verification_candidate_stale")
        if outcome == "sealed_rework":
            reject = {"assignment_id": assignment["id"], "expected_task_version": submitted["task"]["version"],
                      "observed_model": verifier.default_model_binding_key, "evidence": {"defect": "changed PR head"},
                      "verdict": "reject", "reason": "Rebuild the changed candidate", "rework_actor_id": worker.id}
            await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                payload={**reject, "reviewed_candidate_digest": "0" * 64}, receipt="wrong-review-candidate",
                error="verification_candidate_stale")
            await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                payload={**reject, "observed_model": member.default_model_binding_key}, receipt="wrong-reviewer-model",
                error="verification_publisher_unverifiable")
            result = await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                payload=reject, receipt="return-changed-head")
            assert result["task"]["status"] == "active" and result["rework_assignment"]["actor_id"] == worker.id
            return
        pulls["head"]["sha"] = head_sha
        accepted = await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                              payload=verdict, receipt="accepted-current")
        assert accepted["task"]["status"] == "closed"
