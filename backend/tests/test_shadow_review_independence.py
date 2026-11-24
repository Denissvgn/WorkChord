"""Compatibility dispatch keeps the execution profile that independent review needs."""

import json
from datetime import timedelta

import pytest
from sqlalchemy import select

from app.config import get_settings
from app.models.agent import AgentRun, AgentTaskAssignment
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.utils.time import utc_now
from tests.test_agent_routing_wave6_qualification import _assessment_command
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401
from tests.test_team_pm_recovery import recovery_api


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


def row_for(preview, actor_id):
    return next(item for item in [*preview["eligible_candidates"], *preview["exclusions"]]
                if item["actor_id"] == actor_id)


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("history", ["recorded", "unknown"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_compatibility_dispatch_reaches_an_independent_reviewer(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport, history,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    db = db_session
    team = await provision_ready_topology(db)
    worker, reviewer = team.actors["operations-worker"], team.actors["independent-verifier"]
    member = next(item for item in team.manifest.workers if item.actor_key == "operations-worker")
    verifier = team.manifest.verifiers[0]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    worker_key, reviewer_key = team.sink.keys[member.actor_key], team.sink.keys[verifier.actor_key]
    base = await routing_base(db, topology=team, actor_key="operations-worker", team_member_factory=team_member_factory,
                              task_factory=task_factory, title="Ship the reviewed release change",
                              skill_key="security-review")
    task = base.task
    project = Project(name="Compatibility review")
    db.add(project)
    await db.flush()
    iteration = await db.get(Iteration, task.iteration_id)
    task.project_id = iteration.project_id = project.id
    task.effort_hours = 8
    # Execution moves the task to its actual dates; keep them inside the iteration.
    iteration.start_date, iteration.end_date = task.start_date, utc_now().date() + timedelta(days=30)
    await team_member_factory(profile=reviewer.profile, iteration=iteration)
    await db.commit()
    task_id = task.id
    worker_id, worker_profile_id = worker.id, worker.profile_id
    reviewer_id, reviewer_profile_id = reviewer.id, reviewer.profile_id
    url = "https://github.com/example/project/"

    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        execution = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload={
            "task_id": task_id, "actor_id": worker_id, "expected_task_version": task.version,
            "reviewer_profile_id": reviewer_profile_id}, receipt="compatibility-execution")
        assert execution["routing_snapshot"] == {}
        decision = await call("agent_get_my_work", "/api/agent/me/work", worker_key)
        claim = await call("agent_begin_my_work", "/api/agent/me/work/begin", worker_key, payload={
            "assignment_id": execution["id"], "queue_revision": decision["queue_revision"],
            "model": member.default_model_binding_key}, receipt="compatibility-begin")
        submitted = await call("agent_submit_my_work", "/api/agent/me/work/submit", worker_key, payload={
            **fence(claim), "observed_model": member.default_model_binding_key, "summary": "Ready for review",
            "evidence": {"tests": "passed"}, "commit_url": url + "commit/" + "c" * 40, "pr_url": url + "pull/7"},
            receipt="compatibility-submit")
    assert submitted["task"]["status"] == "resolved"

    async with db_session_factory() as audit:
        fulfilled = await audit.get(AgentTaskAssignment, execution["id"])
        assert fulfilled.state == "fulfilled" and json.loads(fulfilled.routing_snapshot) == {}
        run = await audit.get(AgentRun, claim["run"]["id"])
        recorded = run.execution_provenance
        assert recorded["source"] == "authenticated_work_begin"
        assert (recorded["actor_id"], recorded["profile_id"]) == (worker_id, worker_profile_id)
        assert recorded["terminal_profile_id"] == worker_profile_id
        if history == "unknown":
            # A run that predates server-recorded execution provenance.
            run.execution_provenance = None
        await audit.commit()
        version = (await audit.get(Task, task_id)).version
    command = _assessment_command(task_version=version, required_skill_levels={"security-review": 3},
                                  minimum_reasoning_tier=3, minimum_context_tier="large", review_mode="independent")
    created = await through(transport, db_session_factory, monkeypatch, "agent_create_task_routing_assessment",
                            f"/api/agent/planning/tasks/{task_id}/routing-assessment", pm_key,
                            command.model_dump(mode="json"), task_id=task_id, receipt="assess-compatibility-review")
    assessment_id = created["assessment"]["id"]

    async def preview(profile_id, focus):
        return await through(transport, db_session_factory, monkeypatch, "agent_preview_task_routing",
                             f"/api/agent/tasks/{task_id}/routing-preview", pm_key,
                             {"purpose": "verification", "assessment_id": assessment_id, "expected_task_version": version,
                              "reviewer_profile_id": profile_id, "focus_actor_id": focus}, task_id=task_id)

    independent = await preview(reviewer_profile_id, reviewer_id)
    reviewer_row = row_for(independent, reviewer_id)
    if history == "unknown":
        assert independent["recommended_candidate"] is None
        assert "verification_independence_unverifiable" in reviewer_row["hard_blocker_codes"]
    else:
        assert reviewer_row["hard_blocker_codes"] == [] and reviewer_row["eligible"] is True
        assert independent["recommended_candidate"]["actor_id"] == reviewer_id

    same_actor = row_for(await preview(worker_profile_id, worker_id), worker_id)
    assert "verification_actor_not_independent" in same_actor["hard_blocker_codes"]
    if history == "recorded":
        assert "verification_profile_not_independent" in same_actor["hard_blocker_codes"]

    request = {"task_id": task_id, "actor_id": reviewer_id, "expected_task_version": version,
               "purpose": "verification", "reviewer_profile_id": reviewer_profile_id}
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        await through(transport, db_session_factory, monkeypatch, "agent_create_assignment", "/api/agent/assignments",
                      pm_key, {**request, "actor_id": worker_id}, receipt="same-actor-review",
                      error="actor_role_incompatible")
        if history == "recorded":
            await through(transport, db_session_factory, monkeypatch, "agent_create_assignment",
                          "/api/agent/assignments", pm_key, {**request, "reviewer_profile_id": worker_profile_id},
                          receipt="same-profile-review", error="verification_profile_not_independent")
        review = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload=request,
                            receipt="independent-review")
        if history == "unknown":
            return
        accepted = await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key, payload={
            "assignment_id": review["id"], "expected_task_version": version,
            "observed_model": verifier.default_model_binding_key, "evidence": {"tests": "passed"},
            "verdict": "pass"}, receipt="independent-verdict")
    assert accepted["task"]["status"] == "closed"
    async with db_session_factory() as audit:
        assert (await audit.scalar(select(AgentTaskAssignment.state).where(
            AgentTaskAssignment.id == review["id"]))) == "fulfilled"
