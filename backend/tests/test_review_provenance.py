"""Exercise independent publisher review through the atomic work commands."""

import json
from datetime import timedelta

import httpx
import pytest

from app.authority import Authority, AuthorityError
from app.models.agent import AgentIdempotencyRecord, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentTaskAssignment
from app.models.project import Project
from app.schemas.agent import AgentReviewVerdict, AgentTaskAssignmentCreate, AgentWorkBegin, AgentWorkSubmit
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_work_service import AgentWorkService
from app.services.execution_reconciliation import reconcile_execution
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.services.identity_service import initialize_control_plane
from app.services.github_status_service import GitHubStatusService
from app.services.review_provenance import actor_provenance, record_terminal_observation, review_history
from app.services.task_brief_service import TaskBriefService
from app.services.task_service import TaskService
from app.utils.time import utc_now
from app.utils.github_links import parse_github_url
from tests.support.transactions import reload_session_fixture
from tests.test_agent_routing_service import _rollout, _routing_fixture
from tests.test_team_pm_dispatch import db_session_factory


database_engines = pytest.mark.parametrize("db_session_factory", [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
], indirect=True)


def command(key):
    return {"idempotency_key": key, "rationale": "Review the submitted candidate.", "correlation_id": key}


@pytest.mark.sqlite
def test_omitted_review_fields_preserve_preexisting_idempotency_hashes():
    create = AgentTaskAssignmentCreate(task_id=1, actor_id=2, expected_task_version=1)
    verdict = AgentReviewVerdict(assignment_id=1, expected_task_version=1, verdict="pass", evidence={"result": "ok"})
    for request in (create, verdict):
        _, packet = AgentWorkService._audited_command_request(request, **command("original-request"))
        assert all(field not in packet["payload"] for field in ("review_binding_id", "observed_model", "reviewed_candidate_digest"))


@pytest.mark.asyncio
@database_engines
async def test_supervised_execution_and_exact_independent_review(db_session, actor_factory, profile_factory,
                                                                team_member_factory, task_factory):
    db = db_session
    pm, worker, task, binding, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    project = Project(name="Agent delivery", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    task.project_id = project.id
    worker_profile_id = worker.profile_id
    catalog.publisher_key = "model-maker-a"
    catalog.provider = "shared-runtime"
    review_profile = await profile_factory(assignment_modes=["verification"])
    reviewer = await actor_factory(profile=review_profile, role="verifier", scopes=json.dumps(["verification:write", "assignments:read"]))
    review_catalog = AgentModelCatalogEntry(key="review-model", provider=catalog.provider, publisher_key="model-maker-b",
        configured_model_alias="review-runtime", reasoning_tier=2, context_tier="medium", cost_tier="low", latency_tier="fast")
    db.add(review_catalog)
    await db.flush()
    db.add(AgentModelBinding(actor_id=reviewer.id, model_catalog_id=review_catalog.id, is_default=True))
    await db.commit()
    service = AgentWorkService(db, rollout_service=_rollout("shadow"))
    assignment = await service.create_assignment(pm, AgentTaskAssignmentCreate(task_id=task.id, actor_id=worker.id,
        expected_task_version=task.version), **command("assign-execution"))
    begun = await service.begin(worker, AgentWorkBegin(assignment_id=assignment.id, queue_revision=worker.queue_revision,
        lease_seconds=300, model=catalog.configured_model_alias), idempotency_key="begin-execution")
    assert begun.run.model_trust_state == "unverifiable" and begun.run.model_binding_id is None
    assert begun.run.execution_provenance["publisher_key"] == "model-maker-a"
    assert begun.run.execution_provenance["profile_id"] == worker_profile_id
    completion = AgentWorkSubmit(assignment_id=assignment.id, run_id=begun.run.id,
        claim_id=begun.claim_id, claim_generation=begun.claim_generation, expected_task_version=begun.task.version,
        observed_model=catalog.configured_model_alias,
        summary="Completed the change", evidence={"result": "verified"},
        artifact_links=["https://docs.example.test/static/report-v2"])
    with pytest.raises(AgentRoutingConflictError) as switched:
        await service.submit(worker, completion.model_copy(update={"observed_model": "other-runtime"}), idempotency_key="changed-model")
    assert switched.value.code == "execution_publisher_unverifiable"
    await reload_session_fixture(db)
    submitted = await service.submit(worker, completion, idempotency_key="submit-execution")
    assert submitted.task.status == "resolved"
    catalog.publisher_key = "changed-after-execution"
    review_catalog.publisher_key = "model-maker-a"
    await db.commit()
    request = AgentTaskAssignmentCreate(task_id=task.id, actor_id=reviewer.id, purpose="verification",
        expected_task_version=submitted.task.version)
    with pytest.raises(AgentRoutingConflictError, match="distinct") as conflict:
        await service.create_assignment(pm, request, **command("invalid-reviewer"))
    assert conflict.value.code == "verification_publisher_not_independent"
    await reload_session_fixture(db)
    review_catalog.publisher_key = "model-maker-b"
    await db.commit()
    review = await service.create_assignment(pm, request, **command("assign-reviewer"))
    candidate = review.review_selection["candidate"]["digest"]
    assert review.review_selection["contributors"][0]["publisher_key"] == "model-maker-a"
    with pytest.raises(AuthorityError) as ordinary:
        await TaskBriefService(db).require_review(await TaskService(db).get_by_id(task.id), accepting=True)
    assert ordinary.value.code == "verified_publisher_review_required"
    original_authority = db.info.get("authority")
    db.info["authority"] = Authority(None, "system", workspace_role="operator", review_override=True, reason="Accountable operator")
    for accepting in (True, False):
        with pytest.raises(AuthorityError) as operator_review:
            await TaskBriefService(db).require_review(await TaskService(db).get_by_id(task.id), accepting=accepting)
        assert operator_review.value.code == "verified_publisher_review_required"
    if original_authority is None:
        db.info.pop("authority")
    else:
        db.info["authority"] = original_authority
    verdict = AgentReviewVerdict(assignment_id=review.id, expected_task_version=submitted.task.version,
        verdict="pass", evidence={"checks": "passed"}, observed_model="review-runtime", reviewed_candidate_digest=candidate)
    for changed, code in (({"observed_model": catalog.configured_model_alias}, "verification_publisher_unverifiable"),
                          ({"reviewed_candidate_digest": "0" * 64}, "verification_candidate_stale")):
        with pytest.raises(AgentRoutingConflictError) as wrong:
            await service.review(reviewer, verdict.model_copy(update=changed), **command(code))
        assert wrong.value.code == code
        await reload_session_fixture(db)
    accepted = await service.review(reviewer, verdict, **command("accepted"))
    assert accepted.task.status == "closed"
    assert (await service.review(reviewer, verdict, **command("accepted"))).task.version == accepted.task.version


@pytest.mark.asyncio
@database_engines
async def test_legacy_history_never_uses_the_actors_current_configuration(db_session, actor_factory, profile_factory,
                                                                        team_member_factory, task_factory):
    db = db_session
    _, worker, task, binding, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    catalog.publisher_key = "current-only"
    assignment = AgentTaskAssignment(task_id=task.id, task_version=task.version, actor_id=worker.id, state="fulfilled")
    db.add(assignment)
    await db.flush()
    run = AgentRun(task_id=task.id, actor_id=worker.id, assignment_id=assignment.id, claim_generation=1, status="succeeded",
        model=catalog.configured_model_alias, model_trust_state="unverifiable", ended_at=utc_now())
    db.add(run)
    await db.flush()
    frozen = {"response_without_claim_id": {"run": {"id": run.id, "task_id": task.id, "actor_id": worker.id,
        "assignment_id": assignment.id, "claim_generation": 1, "model": run.model},
        "assignment": {"id": assignment.id, "actor_id": worker.id, "purpose": "execution", "routing_snapshot": {}}}}
    db.add(AgentIdempotencyRecord(actor_id=worker.id, operation="work.begin", target_type="assignment", target_id=assignment.id,
        idempotency_key="old-begin", request_hash="7" * 64, response_payload=json.dumps(frozen)))
    await db.commit()
    with pytest.raises(AuthorityError):
        await reconcile_execution(db, run.id, apply=True)
    operator_id = await initialize_control_plane(db)
    db.info["authority"] = Authority(operator_id, "system", workspace_role="operator")
    result = await reconcile_execution(db, run.id)
    assert set(result["missing"]) == {"profile_id", "profile_revision", "publisher_key"}
    applied = await reconcile_execution(db, run.id, apply=True, expected_evidence_digest=result["evidence_digest"],
        command=AgentPlanningCommandContext(**command("inspect-missing-history")))
    assert not applied["applied"] and run.execution_provenance is None and run.model_trust_state == "unverifiable"


@pytest.mark.asyncio
@database_engines
async def test_binding_receipt_without_independent_catalog_history_cannot_name_a_publisher(db_session, actor_factory, profile_factory,
                                                                              team_member_factory, task_factory):
    db = db_session
    admin, worker, task, binding, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    old = utc_now() - timedelta(minutes=5)
    assignment = AgentTaskAssignment(task_id=task.id, task_version=task.version, actor_id=worker.id, state="fulfilled")
    db.add(assignment)
    await db.flush()
    run = AgentRun(task_id=task.id, actor_id=worker.id, assignment_id=assignment.id, claim_generation=1, status="succeeded",
        model=catalog.configured_model_alias, model_trust_state="unverifiable", ended_at=utc_now())
    db.add(run)
    await db.flush()
    decision = {"schema_version": "routing-decision-snapshot-v1", "authority": "agent-routing-service-v1",
        "actor_id": worker.id, "task_id": task.id, "purpose": "execution", "profile_id": worker.profile_id,
        "profile_revision": f"p{worker.profile_id}-historical", "model_binding_id": binding.id, "model_binding_revision": 1,
        "model_catalog_id": catalog.id, "model_catalog_revision": 1}
    frozen = {"response_without_claim_id": {"run": {"id": run.id, "task_id": task.id, "actor_id": worker.id,
        "assignment_id": assignment.id, "claim_generation": 1, "model": run.model,
        "model_binding_id": binding.id, "model_binding_revision": 1},
        "assignment": {"id": assignment.id, "actor_id": worker.id, "purpose": "execution", "routing_snapshot": decision}}}
    archive = {"response": {"target_id": binding.id, "authoritative_revision": 1, "result": {"id": binding.id,
        "revision": 1, "enabled": True, "actor_id": worker.id, "model_catalog": {"id": catalog.id, "key": catalog.key,
        "revision": 1, "configured_model_alias": catalog.configured_model_alias, "publisher_key": "archived-publisher", "enabled": True}}}}
    db.add_all([
        AgentIdempotencyRecord(actor_id=worker.id, operation="work.begin", target_type="assignment", target_id=assignment.id,
            idempotency_key="historical-begin", request_hash="7"*64, response_payload=json.dumps(frozen)),
        AgentIdempotencyRecord(actor_id=admin.id, operation="model_binding.create", target_type="model_binding", target_id=0,
            idempotency_key="archived-binding", request_hash="8"*64, response_payload=json.dumps(archive), created_at=old),
    ])
    terminal = {"source":"authenticated_terminal", "publisher_key":"known-terminal-publisher"}
    run.execution_provenance = {"terminal_model":terminal}
    catalog.publisher_key = "different-today"
    await db.commit()
    operator_id = await initialize_control_plane(db)
    db.info["authority"] = Authority(operator_id, "system", workspace_role="operator")
    result = await reconcile_execution(db, run.id)
    assert "publisher_key" in result["missing"] and not result["applied"]
    applied = await reconcile_execution(db, run.id, apply=True, expected_evidence_digest=result["evidence_digest"],
        command=AgentPlanningCommandContext(**command("recover-known-profile")))
    assert applied["applied"] and run.execution_provenance["profile_id"] == worker.profile_id
    assert run.execution_provenance.get("publisher_key") is None and run.model_trust_state == "unverifiable"
    assert run.execution_provenance["terminal_model"] == terminal


@pytest.mark.asyncio
@pytest.mark.sqlite
async def test_github_candidate_uses_full_head_and_contributions():
    from types import SimpleNamespace

    old_sha, sha = "a" * 40, "b" * 40
    changes = [{"sha": old_sha, "commit": {"author": {"email": "one@example.test"}, "message": "First"}},
               {"sha": sha, "commit": {"author": {"email": "two@example.test"}, "message": "Second"}}]
    current = {"head": {"sha": sha}, "commits": 2}
    def response(request):
        return httpx.Response(200, json=changes if request.url.path.endswith("/commits") else current)
    service = GitHubStatusService(None, SimpleNamespace(github_api_url="https://api.github.com", github_token="",
        github_request_timeout_seconds=2), httpx.MockTransport(response))
    pr = parse_github_url("https://github.com/example/project/pull/1")
    assert await service.verify_review_head(pr, old_sha, {}) == "verification_candidate_stale"
    assert await service.verify_review_head(pr, sha, {}) == "verification_contributors_unverifiable"
    assert await service.verify_review_head(pr, sha, {old_sha: {2}, sha: {3}}) is None
    changes[1]["commit"]["author"]["email"] = changes[0]["commit"]["author"]["email"]
    assert await service.verify_review_head(pr, sha, {sha: {3}}) == "verification_contributors_unverifiable"
    assert await service.verify_review_head(pr, sha, {old_sha: {3}, sha: {3}}) is None
    changes[-1]["commit"]["message"] += "\n\nCo-authored-by: another contributor"
    assert await service.verify_review_head(pr, sha, {old_sha: {2}, sha: {3}}) == "verification_contributors_unverifiable"


@pytest.mark.asyncio
@pytest.mark.sqlite
async def test_commit_only_review_verifies_the_entire_pinned_range():
    from types import SimpleNamespace
    base_sha, first_sha, head_sha = "1"*40, "2"*40, "3"*40
    base, head = (parse_github_url("https://github.com/example/project/commit/"+sha) for sha in (base_sha, head_sha))
    package = {"status": "ahead", "total_commits": 2, "base_commit": {"sha": base_sha},
               "merge_base_commit": {"sha": base_sha}, "commits": [{"sha": sha, "commit": {"message": "Change"}}
                                                                  for sha in (first_sha, head_sha)]}
    def response(request):
        assert request.url.path.endswith("/compare/"+base_sha+"..."+head_sha)
        return httpx.Response(200, json=package)
    github = GitHubStatusService(None, SimpleNamespace(github_api_url="https://api.github.com", github_token="",
        github_request_timeout_seconds=2), httpx.MockTransport(response))
    assert await github.verify_review_range(base, head, {head_sha: {3}}) == "verification_contributors_unverifiable"
    assert await github.verify_review_range(base, head, {head_sha: {3}, first_sha: {3}}) is None
    package["merge_base_commit"] = {"sha": head_sha}
    assert await github.verify_review_range(base, head, {head_sha: {3}, first_sha: {3}}) == "verification_candidate_unverifiable"


@pytest.mark.asyncio
@database_engines
async def test_interrupted_work_retains_both_observed_publishers(db_session, actor_factory, profile_factory,
                                                                team_member_factory, task_factory):
    db = db_session
    _, actor, task, binding, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    catalog.publisher_key = "terminal-publisher"
    assignment = AgentTaskAssignment(task_id=task.id, task_version=task.version, actor_id=actor.id, state="cancelled")
    db.add(assignment)
    await db.flush()
    run = AgentRun(task_id=task.id, actor_id=actor.id, assignment_id=assignment.id, claim_generation=1,
        status="failed", ended_at=utc_now(), execution_provenance={"actor_id": actor.id, "profile_id": actor.profile_id,
        "publisher_key": "original-publisher", "catalog_key": "previous-model", "different_publisher_required": True})
    db.add(run)
    await db.flush()
    await record_terminal_observation(db, actor, run, catalog.configured_model_alias, submitting=False)
    history = await review_history(db, task, [assignment], strict=True)
    assert {row["publisher_key"] for row in history.contributors} == {"original-publisher", "terminal-publisher"}
    assert history.publisher_blockers("terminal-publisher") == ["verification_publisher_not_independent"]
    assert history.publisher_blockers("original-publisher") == ["verification_publisher_not_independent"]
    assert not history.publisher_blockers("third-publisher")
    with pytest.raises(AgentRoutingConflictError, match="observed"):
        await record_terminal_observation(db, actor, run, None, submitting=False)
    run.commit_url = "https://github.com/example/project/commit/"+"1"*40
    with pytest.raises(AgentRoutingConflictError) as contradicts:
        await record_terminal_observation(db, actor, run, catalog.configured_model_alias, submitting=False, output_state="no_output")
    assert contradicts.value.code == "execution_output_conflict"


@pytest.mark.asyncio
@database_engines
async def test_same_reported_alias_cannot_hide_a_revised_publisher(db_session, actor_factory, profile_factory,
                                                                  team_member_factory, task_factory):
    db = db_session
    _, actor, task, binding, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    catalog.publisher_key = "original-maker"
    await db.flush()
    receipt = await actor_provenance(db, actor, observed_model=catalog.configured_model_alias)
    run = AgentRun(task_id=task.id, actor_id=actor.id, claim_generation=1, execution_provenance=receipt)
    db.add(run)
    await db.flush()
    catalog.publisher_key = "revised-maker"
    catalog.revision += 1
    binding.revision += 1
    await db.flush()
    with pytest.raises(AgentRoutingConflictError) as changed:
        await record_terminal_observation(db, actor, run, catalog.configured_model_alias, submitting=True)
    assert changed.value.code == "execution_publisher_unverifiable"
    await record_terminal_observation(db, actor, run, catalog.configured_model_alias, submitting=False, output_state="retained")
    assert run.execution_provenance["publisher_key"] == "original-maker"
    assert run.execution_provenance["terminal_model"]["publisher_key"] == "revised-maker"


@pytest.mark.asyncio
@database_engines
async def test_unassigned_run_remains_unknown_and_optional_supervisor_needs_no_profile(db_session, actor_factory,
                                                                                      profile_factory, team_member_factory, task_factory):
    db = db_session
    pm, actor, task, _, catalog = await _routing_fixture(db, profile_factory, actor_factory, team_member_factory, task_factory)
    actor.profile_id = None
    await db.commit()
    service = AgentWorkService(db, rollout_service=_rollout("shadow"))
    assignment = await service.create_assignment(pm, AgentTaskAssignmentCreate(task_id=task.id, actor_id=actor.id,
        expected_task_version=task.version), **command("ordinary-assign"))
    begun = await service.begin(actor, AgentWorkBegin(assignment_id=assignment.id, queue_revision=actor.queue_revision,
        lease_seconds=300, model=catalog.configured_model_alias), idempotency_key="ordinary-no-profile")
    assert begun.run.execution_provenance["profile_id"] is None
    unlinked = AgentRun(task_id=task.id, actor_id=actor.id, status="failed")
    db.add(unlinked)
    await db.flush()
    history = await review_history(db, task, [await db.get(AgentTaskAssignment, assignment.id)], strict=True)
    row = next(row for row in history.contributors if row["run_id"] == unlinked.id)
    assert row["publisher_key"] is None and "execution_assignment" in row["missing"]
