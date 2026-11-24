"""A replacement's carried contributors stay out of independent review, and their history walk is bounded."""

from copy import deepcopy
from types import SimpleNamespace

import pytest

from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.task_replacement import TaskReplacement
from app.services import review_provenance
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.review_provenance import carried_profile_history, require_independent_profile
from app.services.task_replacement_service import carried_contributors
from app.utils.time import utc_now
from tests import test_agent_team_setup_qualification as setup_qualification
from tests.test_agent_routing_wave6_qualification import _assessment_command
from tests.test_agent_team_setup_qualification import provision_ready_topology
from tests.test_review_provenance_transports import databases, fence
from tests.test_scoped_review_evidence import through
from tests.test_task_replacement import BASE, _replacement, _scenario
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401
from tests.test_team_pm_recovery import recovery_api

REPO = "https://github.com/example/project/"


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


def _with_second_verifier(payload):
    """The standard topology plus one more automation verifier with its own profile and runtime."""
    extra = deepcopy(payload["verifiers"][0])
    extra.update({"actor_key": "second-verifier", "actor_name": "workchord-second-verifier",
                  "display_name": "Second Verifier", "profile_key": "security-scope-agent",
                  "runtime_ref": "runtime://second-verifier",
                  "credential_ref": "agent-team-secure-sink/second-verifier"})
    payload["verifiers"].append(extra)
    return payload


def row_for(preview, actor_id):
    return next(item for item in [*preview["eligible_candidates"], *preview["exclusions"]]
                if item["actor_id"] == actor_id)


async def _carry_run(db, author, original, replacement, unattributed):
    """The original's carried run belongs to ``author``, whose profile its authenticated begin recorded."""
    run = await db.get(AgentRun, unattributed.id)
    run.actor_id = author.id
    run.execution_provenance = {"actor_id": author.id, "profile_id": author.profile_id,
                                "profile_revision": f"p{author.profile_id}-begin", "source": "authenticated_work_begin",
                                "terminal_profile_id": author.profile_id}
    (await db.get(AgentTaskAssignment, run.assignment_id)).actor_id = author.id
    frozen = [SimpleNamespace(id=task.id, version=task.version) for task in (original, replacement)]
    await db.commit()
    return frozen[0], frozen[1]


async def _submit_replacement(transport, db_session_factory, monkeypatch, team, member, replacement_id, version):
    """The worker executes and submits the replacement, so it is resolved and ready for verification."""
    pm_key, worker_key = team.sink.keys[team.manifest.controller.actor_key], team.sink.keys[member.actor_key]
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        assigned = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload={
            "task_id": replacement_id, "actor_id": team.actors[member.actor_key].id,
            "expected_task_version": version}, receipt="carry-execution")
        decision = await call("agent_get_my_work", "/api/agent/me/work", worker_key)
        claim = await call("agent_begin_my_work", "/api/agent/me/work/begin", worker_key, payload={
            "assignment_id": assigned["id"], "queue_revision": decision["queue_revision"],
            "model": member.default_model_binding_key}, receipt="carry-begin")
        return await call("agent_submit_my_work", "/api/agent/me/work/submit", worker_key, payload={
            **fence(claim), "observed_model": member.default_model_binding_key, "summary": "Rebuilt on carried work",
            "evidence": {"tests": "passed"}, "commit_url": REPO + "commit/" + "a" * 40,
            "pr_url": REPO + "pull/11"}, receipt="carry-submit")


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_routing_preview_excludes_a_carried_contributor_without_the_strict_policy(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    (team, member, verifier, _, original, replacement, *_rest, unattributed) = await _scenario(
        db_session, task_factory, team_member_factory, strict=False)
    worker, reviewer = team.actors[member.actor_key], team.actors[verifier.actor_key]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    frozen_original, frozen_replacement = await _carry_run(db_session, worker, original, replacement, unattributed)
    iteration = await db_session.get(Iteration, replacement.iteration_id)
    await team_member_factory(profile=reviewer.profile, iteration=iteration)
    await db_session.commit()
    replacement_id, reviewer_id, reviewer_profile_id, worker_id = (
        frozen_replacement.id, reviewer.id, reviewer.profile_id, worker.id)
    await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement",
                  f"/api/agent/planning/tasks/{frozen_original.id}/replacement", pm_key,
                  _replacement(frozen_original, frozen_replacement, [unattributed.id]), task_id=frozen_original.id,
                  receipt="carry-for-preview")
    version = (await _submit_replacement(transport, db_session_factory, monkeypatch, team, member, replacement_id,
                                         frozen_replacement.version))["task"]["version"]
    command = _assessment_command(task_version=version, required_skill_levels={"security-review": 3},
                                  minimum_reasoning_tier=3, minimum_context_tier="large", review_mode="independent")
    created = await through(transport, db_session_factory, monkeypatch, "agent_create_task_routing_assessment",
                            f"/api/agent/planning/tasks/{replacement_id}/routing-assessment", pm_key,
                            command.model_dump(mode="json"), task_id=replacement_id, receipt="assess-carried-preview")
    preview = await through(transport, db_session_factory, monkeypatch, "agent_preview_task_routing",
                            f"/api/agent/tasks/{replacement_id}/routing-preview", pm_key,
                            {"purpose": "verification", "assessment_id": created["assessment"]["id"],
                             "expected_task_version": version, "reviewer_profile_id": reviewer_profile_id,
                             "focus_actor_id": worker_id}, task_id=replacement_id)
    carried_row = row_for(preview, worker_id)
    assert "verification_actor_not_independent" in carried_row["hard_blocker_codes"]
    assert carried_row["eligible"] is False
    control_row = row_for(preview, reviewer_id)
    assert control_row["hard_blocker_codes"] == [] and control_row["eligible"] is True
    assert preview["recommended_candidate"]["actor_id"] == reviewer_id


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_verification_reassignment_refuses_a_carried_contributor(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    # The same topology carries a second verifier with its own profile, so one can verify the other's work.
    monkeypatch.setattr(setup_qualification, "topology_manifest",
                        lambda **kwargs: setup_qualification.AgentTeamMaster.model_validate(
                            _with_second_verifier(setup_qualification.topology_payload(**kwargs))))
    (team, member, verifier, _, original, replacement, *_rest, unattributed) = await _scenario(
        db_session, task_factory, team_member_factory, strict=False)
    reviewer = team.actors[verifier.actor_key]
    independent = team.actors[team.manifest.verifiers[1].actor_key]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    # The first verifier authored the carried run, so it cannot verify the replacement.
    frozen_original, frozen_replacement = await _carry_run(db_session, reviewer, original, replacement, unattributed)
    iteration = await db_session.get(Iteration, replacement.iteration_id)
    await team_member_factory(profile=independent.profile, iteration=iteration)
    await db_session.commit()
    replacement_id, reviewer_id, independent_id = frozen_replacement.id, reviewer.id, independent.id
    assert independent.id != reviewer.id and independent.profile_id != reviewer.profile_id
    await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement",
                  f"/api/agent/planning/tasks/{frozen_original.id}/replacement", pm_key,
                  _replacement(frozen_original, frozen_replacement, [unattributed.id]), task_id=frozen_original.id,
                  receipt="carry-for-reassign")
    version = (await _submit_replacement(transport, db_session_factory, monkeypatch, team, member, replacement_id,
                                         frozen_replacement.version))["task"]["version"]
    refused = {"task_id": replacement_id, "expected_task_version": version, "purpose": "verification",
               "reviewer_profile_id": reviewer.profile_id}
    await through(transport, db_session_factory, monkeypatch, "agent_create_assignment", "/api/agent/assignments",
                  pm_key, {**refused, "actor_id": reviewer_id}, receipt="carried-review-create",
                  error="verification_actor_not_independent")
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        review = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload={
            **refused, "actor_id": independent_id, "reviewer_profile_id": independent.profile_id},
            receipt="independent-review-create")
    assert review["actor_id"] == independent_id
    async with db_session_factory() as audit:
        queue_revision = (await audit.get(AgentActor, independent_id)).queue_revision
    await through(transport, db_session_factory, monkeypatch, "agent_update_assignment",
                  f"/api/agent/assignments/{review['id']}", pm_key,
                  {"expected_queue_revision": queue_revision, "actor_id": reviewer_id},
                  assignment_id=review["id"], receipt="reassign-to-carried-contributor",
                  error="verification_actor_not_independent")
    # The independent verifier keeps the review when only its queue position changes.
    accepted = await through(transport, db_session_factory, monkeypatch, "agent_update_assignment",
                             f"/api/agent/assignments/{review['id']}", pm_key,
                             {"expected_queue_revision": queue_revision, "queue_rank": 1},
                             assignment_id=review["id"], receipt="reorder-independent-review")
    assert accepted["actor_id"] == independent_id
    async with db_session_factory() as audit:
        assignment = await audit.get(AgentTaskAssignment, review["id"])
        assert assignment.actor_id == independent_id and assignment.state == "queued"
        await audit.rollback()


async def _linked_chain(db, length, *, cycle=False):
    """Replacement links t0 -> t1 -> ... -> t<length>, each carrying one run id; a cycle closes the chain."""
    project = Project(name="Bounded carried history")
    db.add(project)
    await db.flush()
    tasks = [Task(title=f"Link {index}", project_id=project.id, status="resolved") for index in range(length + 1)]
    db.add_all(tasks)
    await db.flush()
    links = [(index, index + 1) for index in range(length)]
    if cycle:
        links.append((length, 0))
    for index, (original, replacement) in enumerate(links):
        db.add(TaskReplacement(project_id=project.id, original_task_id=tasks[original].id,
                               replacement_task_id=tasks[replacement].id, reason="Bounded history",
                               owner_decision="Bounded history", base_commit_url=BASE,
                               carried_run_ids=[900_000 + index], original_snapshot={}, review_policy={},
                               decided_at=utc_now()))
    await db.commit()
    return tasks


@databases
@pytest.mark.parametrize("case", ["depth", "runs", "cycle"])
async def test_carried_history_walk_is_bounded_and_fails_closed(db_session, db_session_factory, monkeypatch, case):
    if case == "depth":
        tasks = await _linked_chain(db_session, review_provenance.MAX_CARRIED_REPLACEMENT_DEPTH + 2)
        reason, latest = "carried_history_depth", tasks[-1]
    elif case == "runs":
        monkeypatch.setattr(review_provenance, "MAX_CARRIED_HISTORY_RUNS", 3)
        tasks = await _linked_chain(db_session, 5)
        reason, latest = "carried_history_runs", tasks[-1]
    else:
        tasks = await _linked_chain(db_session, 3, cycle=True)
        reason, latest = "carried_history_cycle", tasks[3]
    latest_id = latest.id
    rows = await carried_profile_history(db_session, latest_id)
    assert rows[-1]["truncated"] == reason
    assert all(row.get("truncated") is None for row in rows[:-1])
    with pytest.raises(AgentRoutingConflictError) as refused:
        await require_independent_profile(db_session, [], SimpleNamespace(id=1, profile_id=1), task_id=latest_id)
    assert refused.value.code == "verification_independence_unverifiable"
    contributors = await carried_contributors(db_session, await db_session.get(Task, latest_id))
    assert contributors[-1]["truncated"] == reason
    assert contributors[-1]["run_id"] is None and contributors[-1]["profile_id"] is None
