"""A clean replacement of unattributable work: audited, counted once, and held when it carries unknown work."""

import json
from datetime import timedelta
from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy import select

from app.authority import Authority, AuthorityError
from app.config import get_settings
from app.models.agent import AgentModelCatalogEntry, AgentRun, AgentTaskAssignment
from app.models.delivery_dependency import DeliveryDependency
from app.models.delivery_observation import DeliveryObservation
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.release import Release, release_tasks
from app.models.task import Task, TaskDependency
from app.models.task_replacement import TaskReplacement
from app.services.delivery_dependency_service import DeliveryDependencyService
from app.services.delivery_metrics_service import summarize_observations
from app.services.release_service import ReleaseService
from app.services.github_status_service import GitHubStatusService
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_replacement_service import TaskReplacementService
from app.services.work_metrics import leaf_metrics
from app.utils.time import utc_now
from tests.test_agent_team_setup_qualification import _TASK_BRIEF, provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401
from tests.test_team_pm_recovery import recovery_api

URL = "https://github.com/example/project/"
BASE = URL + "commit/" + "0" * 40


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


async def _scenario(db, task_factory, team_member_factory, *, strict=True):
    """An original whose only run was executed without a model binding, so its publisher is unknown."""
    team = await provision_ready_topology(db)
    member, verifier = team.manifest.workers[0], team.manifest.verifiers[0]
    worker = team.actors[member.actor_key]
    base = await routing_base(db, topology=team, actor_key=member.actor_key, team_member_factory=team_member_factory,
                              task_factory=task_factory, title="Deliver the kernel change")
    original = base.task
    project = Project(name="Kernel", require_different_review_publisher=strict)
    db.add(project)
    await db.flush()
    iteration = await db.get(Iteration, original.iteration_id)
    iteration.project_id = original.project_id = project.id
    # Execution moves the task to its actual dates; keep them inside the iteration.
    iteration.start_date, iteration.end_date = original.start_date, utc_now().date() + timedelta(days=30)
    original.effort_hours = 8
    for key, publisher in ((member.default_model_binding_key, "first-publisher"),
                           (verifier.default_model_binding_key, "second-publisher")):
        model = await db.scalar(select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == key))
        model.publisher_key = publisher
    execution = AgentTaskAssignment(task_id=original.id, actor_id=worker.id, purpose="execution", queue_class="normal",
                                    state="fulfilled", task_version=original.version, routing_snapshot="{}")
    db.add(execution)
    await db.flush()
    unattributed = AgentRun(task_id=original.id, actor_id=worker.id, assignment_id=execution.id, status="succeeded",
                            commit_url=URL + "commit/" + "e" * 40, ended_at=utc_now())
    db.add(unattributed)
    original.status = "resolved"
    replacement = await task_factory(iteration=iteration, assignee=base.member, title="Deliver the kernel change (clean)",
                                     description=_TASK_BRIEF, tags=original.tags, priority=2, effort_hours=8,
                                     status="planned", start_date=original.start_date, end_date=original.end_date,
                                     project_id=project.id)
    schedule_dependent = await task_factory(iteration=iteration, title="Build on the kernel", project_id=project.id,
                                            status="planned", effort_hours=8)
    delivery_dependent = await task_factory(iteration=iteration, title="Ship the kernel", project_id=project.id,
                                            status="planned", effort_hours=8)
    unrelated = await task_factory(iteration=iteration, title="Unrelated docs", project_id=project.id,
                                   status="planned", effort_hours=8)
    db.add_all([TaskDependency(task_id=schedule_dependent.id, depends_on_id=original.id),
                DeliveryDependency(task_id=delivery_dependent.id, prerequisite_task_id=original.id)])
    release = Release(name="Kernel 1.0", project_id=project.id, status="planned")
    db.add(release)
    await db.flush()
    await db.execute(release_tasks.insert().values(release_id=release.id, task_id=original.id, created_at=utc_now()))
    await db.commit()
    return team, member, verifier, project, original, replacement, schedule_dependent, delivery_dependent, unrelated, release, unattributed


def _replacement(original, replacement, carried):
    return {"replacement_task_id": replacement.id, "expected_original_version": original.version,
            "expected_replacement_version": replacement.version,
            "reason": "The original run has no model binding, so its publisher is unknown.",
            "owner_decision": "Owner approved a clean rebuild from main, keeping the original for audit.",
            "base_commit_url": BASE, "carried_run_ids": carried}


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("reuse", ["clean", "carried"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_clean_replacement_is_accepted_once_and_carried_work_stays_held(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport, reuse,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    (team, member, verifier, project, original, replacement, schedule_dependent, delivery_dependent, unrelated,
     release, unattributed) = await _scenario(db_session, task_factory, team_member_factory)
    worker, reviewer = team.actors[member.actor_key], team.actors[verifier.actor_key]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    worker_key, reviewer_key = team.sink.keys[member.actor_key], team.sink.keys[verifier.actor_key]
    carried = [unattributed.id] if reuse == "carried" else []
    payload = _replacement(original, replacement, carried)
    path = f"/api/agent/planning/tasks/{original.id}/replacement"
    versions = {task.id: task.version for task in (schedule_dependent, delivery_dependent, unrelated, replacement)}

    # Only the project's PM (or an operator) may decide; a worker holds no planning authority.
    await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement", path, worker_key,
                  payload, task_id=original.id, receipt="worker-replacement", error="planning:write")
    receipt = await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement", path, pm_key,
                            payload, task_id=original.id, receipt="replace-original")
    view = receipt["result"]
    assert receipt["operation"] == "planning.task.replacement"
    assert view["original"]["unattributed_run_ids"] == [unattributed.id]
    assert view["original"]["independently_accepted"] is False and view["original"]["status_at_decision"] == "resolved"
    assert view["decision"]["owner_decision"].startswith("Owner approved") and view["decision"]["decided_by_actor_id"]
    assert view["review_policy"] == {"require_different_review_publisher_at_decision": True,
                                     "require_different_review_publisher": True}
    assert view["replacement"]["recorded_base_commit_url"] == BASE
    assert sorted((item["task_id"], item["kind"], item["action"]) for item in view["moved_dependencies"]) == sorted(
        [(schedule_dependent.id, "schedule", "moved"), (delivery_dependent.id, "delivery", "moved")])
    assert view["moved_release_ids"] == [release.id]
    if reuse == "carried":
        assert view["acceptance"] == {"deliverable_task_id": replacement.id, "state": "held",
                                      "hold_reasons": ["carried_contribution_unattributed"],
                                      "unattributed_carried_run_ids": [unattributed.id]}
        assert view["carried_contributions"][0]["carried_from_task_id"] == original.id
    else:
        assert view["acceptance"]["state"] == "clean" and view["carried_contributions"] == []
    # An exact replay returns the same receipt; a second disposition for the same original is refused.
    replay = await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement", path, pm_key,
                           payload, task_id=original.id, receipt="replace-original")
    assert replay == receipt

    async with db_session_factory() as audit:
        kept = await audit.get(Task, original.id)
        assert kept.canceled_at is not None and f"Replaced by task {replacement.id}" in kept.canceled_reason
        assert kept.accepted_at is None and kept.version == original.version + 1
        assert await audit.get(AgentRun, unattributed.id) is not None
        assert (await audit.scalar(select(TaskDependency.depends_on_id).where(
            TaskDependency.task_id == schedule_dependent.id))) == replacement.id
        assert (await audit.scalar(select(DeliveryDependency.prerequisite_task_id).where(
            DeliveryDependency.task_id == delivery_dependent.id))) == replacement.id
        # Re-pointing dependents keeps issued work on them, and on unrelated work, current.
        for task_id, version in versions.items():
            assert (await audit.get(Task, task_id)).version == version
        assert set((await audit.scalars(select(release_tasks.c.task_id).where(
            release_tasks.c.release_id == release.id))).all()) == {original.id, replacement.id}
        # The original can never be reviewed or reopened into a second count.
        with pytest.raises(AuthorityError, match="replaced by task"):
            await TaskBriefService(audit).require_review(kept, accepting=False)
        actions = {item.action: item for item in (await TaskDomainService(audit).allowed_actions(original.id)).actions}
        assert not actions["reopen"].allowed and "task_replaced" in {b.code for b in actions["reopen"].blockers}
        await audit.rollback()

    url = URL
    head = ("d" if reuse == "carried" else "c") * 40
    pulls = {"head": {"sha": head}, "commits": 1}
    commits = [{"sha": head, "commit": {"author": {"email": "bot@example.test"}, "message": "Rebuild cleanly"}}]

    def response(request):
        return httpx.Response(200, json=commits if request.url.path.endswith("/commits") else pulls)

    async def github(cls, session):
        return GitHubStatusService(session, transport=httpx.MockTransport(response))

    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(github))
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        assigned = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload={
            "task_id": replacement.id, "actor_id": worker.id, "expected_task_version": replacement.version},
            receipt="replacement-execution")
        decision = await call("agent_get_my_work", "/api/agent/me/work", worker_key)
        claim = await call("agent_begin_my_work", "/api/agent/me/work/begin", worker_key, payload={
            "assignment_id": assigned["id"], "queue_revision": decision["queue_revision"],
            "model": member.default_model_binding_key}, receipt="replacement-begin")
        submitted = await call("agent_submit_my_work", "/api/agent/me/work/submit", worker_key, payload={
            **fence(claim), "observed_model": member.default_model_binding_key, "summary": "Rebuilt from main",
            "evidence": {"tests": "passed"}, "commit_url": url + "commit/" + head, "pr_url": url + "pull/9"},
            receipt="replacement-submit")
        version = submitted["task"]["version"]
        request = {"task_id": replacement.id, "actor_id": reviewer.id, "expected_task_version": version,
                   "purpose": "verification"}
        if reuse == "carried":
            await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload=request,
                       receipt="held-review", error="replacement_contribution_unattributed")
            async with db_session_factory() as audit:
                held = await audit.get(Task, replacement.id)
                assert held.status == "resolved" and held.accepted_at is None
                assert not await DeliveryDependencyService(audit).ready(delivery_dependent.id)
                view = await TaskReplacementService(audit).get(replacement.id)
                assert view["role"] == "replacement" and view["acceptance"]["state"] == "held"
                assert view["replacement"]["candidate"]["commit_url"] == url + "commit/" + head
            return
        review = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload=request,
                            receipt="clean-review")
        assert review["review_selection"]["contributors"][0]["publisher_key"] == "first-publisher"
        accepted = await call("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key, payload={
            "assignment_id": review["id"], "expected_task_version": version,
            "observed_model": verifier.default_model_binding_key,
            "reviewed_candidate_digest": review["review_selection"]["candidate"]["digest"],
            "evidence": {"tests": "passed"}, "verdict": "pass"}, receipt="accept-replacement")
        assert accepted["task"]["status"] == "closed"

    async with db_session_factory() as audit:
        pair = [await audit.get(Task, original.id), await audit.get(Task, replacement.id)]
        counts = leaf_metrics(pair)
        assert (counts["total_tasks"], counts["accepted_tasks"], counts["implemented_tasks"]) == (1, 1, 1)
        shipped = await ReleaseService(audit).get_by_id(release.id)
        assert (shipped.total_tasks, shipped.accepted_tasks) == (1, 1)
        # The dependent that waited on the original is ready once the replacement is accepted.
        assert await DeliveryDependencyService(audit).ready(delivery_dependent.id)
        rows = (await audit.scalars(select(DeliveryObservation).where(
            DeliveryObservation.original_task_id.in_([original.id, replacement.id])))).all()
        assert "replaced" in {row.kind for row in rows if row.original_task_id == original.id}
        delivered = summarize_observations(rows, utc_now() - timedelta(days=1), utc_now() + timedelta(minutes=1))
        assert (delivered["accepted_leaf_tasks"], delivered["canceled_leaf_tasks"]) == (1, 0)
        view = await TaskReplacementService(audit).get(original.id)
        assert view["role"] == "original" and view["original"]["independently_accepted"] is False
        assert view["original"]["status"] == "resolved" and view["replacement"]["accepted"] is True
        assert view["replacement"]["candidate"]["pr_url"] == url + "pull/9"
        await audit.rollback()


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_replacement_read_and_human_route_authority(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    team, member, _, _, original, replacement, *_ = await _scenario(db_session, task_factory, team_member_factory)
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    worker_key = team.sink.keys[member.actor_key]
    payload = _replacement(original, replacement, [])
    async with recovery_api("rest", db_session_factory, monkeypatch):
        from app.main import app
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as client:
            refused = await client.post(f"/api/tasks/{original.id}/replacement", json=payload,
                                        headers={"X-Agent-API-Key": worker_key})
            assert refused.status_code == 403, refused.text
            recorded = await client.post(f"/api/tasks/{original.id}/replacement", json=payload,
                                         headers={"X-Agent-API-Key": pm_key})
            assert recorded.status_code == 201, recorded.text
            again = await client.post(f"/api/tasks/{original.id}/replacement", json=payload,
                                      headers={"X-Agent-API-Key": pm_key})
            assert again.status_code == 409, again.text
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        view = await call("agent_get_task_replacement", f"/api/agent/planning/tasks/{replacement.id}/replacement",
                          pm_key, task_id=replacement.id)
    assert view["role"] == "replacement" and view["original_task_id"] == original.id
    assert view["acceptance"]["state"] == "clean" and view["decision"]["decided_by_actor_id"] is not None


async def _plain(db, task_factory, *, status="resolved"):
    project = Project(name="Plain")
    db.add(project)
    await db.flush()
    original = await task_factory(title="Original", project_id=project.id, status=status)
    replacement = await task_factory(title="Replacement", project_id=project.id, status="planned")
    iteration = await db.get(Iteration, original.iteration_id)
    replacement.iteration_id = iteration.id
    iteration.project_id = project.id
    await db.commit()
    return project, original, replacement


def _data(original, replacement, **overrides):
    from app.schemas.task_replacement import TaskReplacementCreate
    return TaskReplacementCreate.model_validate({**_replacement(original, replacement, []), **overrides})


@pytest.mark.sqlite
async def test_replacement_refuses_ineligible_pairs(db_session, task_factory, monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    from app.commands import PlanningConflict
    project, original, replacement = await _plain(db_session, task_factory)
    iteration = await db_session.get(Iteration, original.iteration_id)
    started = await task_factory(title="Started", project_id=project.id, status="active", iteration=iteration)
    accepted = await task_factory(title="Accepted", project_id=project.id, status="closed", iteration=iteration)
    other = Project(name="Elsewhere")
    db_session.add(other)
    await db_session.flush()
    foreign = await task_factory(title="Foreign", project_id=other.id, status="planned")
    await db_session.commit()
    # A refused command rolls back the session, so compare plain identities.
    project_id, iteration_id = project.id, iteration.id
    original, replacement, started, accepted, foreign = (SimpleNamespace(id=task.id, version=task.version)
                                                         for task in (original, replacement, started, accepted, foreign))
    service = TaskReplacementService(db_session)
    with pytest.raises(PlanningConflict, match="no attempts"):
        await service.record(original.id, _data(original, started))
    with pytest.raises(PlanningConflict, match="not recorded contributions"):
        await service.record(original.id, _data(original, replacement, carried_run_ids=[987654]))
    with pytest.raises(ValueError, match="immutable GitHub commit"):
        await service.record(original.id, _data(original, replacement, base_commit_url=URL + "tree/main"))
    with pytest.raises(PlanningConflict, match="same project"):
        await service.record(original.id, _data(original, foreign))
    with pytest.raises(PlanningConflict, match="Accepted work"):
        await service.record(accepted.id, _data(accepted, replacement))
    await service.record(original.id, _data(original, replacement))
    assert await db_session.scalar(select(TaskReplacement.id).where(TaskReplacement.original_task_id == original.id))
    with pytest.raises(PlanningConflict, match="already been replaced"):
        await service.record(original.id, _data(SimpleNamespace(id=original.id, version=original.version + 1), started))
    # A replacement whose own work proves unattributable can be replaced in turn.
    second = await task_factory(title="Second replacement", project_id=project_id, status="planned",
                                iteration=await db_session.get(Iteration, iteration_id))
    await db_session.commit()
    second = SimpleNamespace(id=second.id, version=second.version)
    chained = await service.record(replacement.id, _data(replacement, second))
    assert (chained["original_task_id"], chained["replacement_task_id"]) == (replacement.id, second.id)
    assert (await service.get(replacement.id))["role"] == "original"
    # Retained for audit: neither task can be deleted while the disposition exists.
    from app.services.delivery_dependency_service import DeliveryDependencyService
    with pytest.raises(PlanningConflict, match="retains this work"):
        await DeliveryDependencyService(db_session).require_unreferenced({replacement.id})


@pytest.mark.sqlite
@pytest.mark.parametrize(("kind", "role", "scopes", "allowed"), [
    ("human", None, (), False),
    ("human", None, (), True),
    ("agent", "worker", ("planning:read", "planning:write"), False),
    ("agent", "pm", ("planning:read", "planning:write"), True),
])
async def test_only_a_project_manager_or_pm_actor_decides(db_session, task_factory, kind, role, scopes, allowed):
    project, original, replacement = await _plain(db_session, task_factory)
    project_role = ("manager" if allowed else "editor") if kind == "human" else None
    db_session.info["authority"] = Authority(None, kind, projects={project.id: project_role} if project_role else {project.id: "manager"},
                                             actor_role=role, scopes=frozenset(scopes))
    try:
        service = TaskReplacementService(db_session)
        if allowed:
            view = await service.record(original.id, _data(original, replacement))
            assert view["original_task_id"] == original.id
        else:
            with pytest.raises(AuthorityError):
                await service.record(original.id, _data(original, replacement))
    finally:
        db_session.info.pop("authority", None)


@pytest.mark.sqlite
async def test_held_replacement_is_refused_acceptance_without_the_strict_policy(db_session, task_factory, monkeypatch,
                                                                                actor_factory):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    project, original, replacement = await _plain(db_session, task_factory)
    worker = await actor_factory()
    execution = AgentTaskAssignment(task_id=original.id, actor_id=worker.id, purpose="execution", queue_class="normal",
                                    state="fulfilled", task_version=original.version, routing_snapshot="{}")
    db_session.add(execution)
    await db_session.flush()
    run = AgentRun(task_id=original.id, actor_id=worker.id, assignment_id=execution.id, status="succeeded",
                   commit_url=URL + "commit/" + "f" * 40)
    db_session.add(run)
    await db_session.commit()
    await TaskReplacementService(db_session).record(original.id, _data(original, replacement, carried_run_ids=[run.id]))
    held = await db_session.get(Task, replacement.id)
    held.status = "resolved"
    await db_session.commit()
    with pytest.raises(AuthorityError) as refused:
        await TaskBriefService(db_session).require_review(held, accepting=True)
    assert refused.value.code == "replacement_contribution_unattributed"
    # Returning held work for rework stays possible.
    await TaskBriefService(db_session).require_review(held, accepting=False)
    assert json.loads(json.dumps((await TaskReplacementService(db_session).get(original.id))["acceptance"],
                                 default=str))["state"] == "held"


@pytest.mark.sqlite
async def test_an_owner_override_cannot_accept_a_held_replacement_so_no_next_step_offers_it(db_session, task_factory,
                                                                                              monkeypatch, actor_factory):
    from app.commands import command_transaction
    from app.refusal_next_steps import NEXT_STEPS, VARIANTS
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    project, original, replacement = await _plain(db_session, task_factory)
    project.require_different_review_publisher = True
    worker = await actor_factory()
    execution = AgentTaskAssignment(task_id=original.id, actor_id=worker.id, purpose="execution", queue_class="normal",
                                    state="fulfilled", task_version=original.version, routing_snapshot="{}")
    db_session.add(execution)
    await db_session.flush()
    run = AgentRun(task_id=original.id, actor_id=worker.id, assignment_id=execution.id, status="succeeded",
                   commit_url=URL + "commit/" + "f" * 40)
    db_session.add(run)
    await db_session.commit()
    await TaskReplacementService(db_session).record(original.id, _data(original, replacement, carried_run_ids=[run.id]))
    held = await db_session.get(Task, replacement.id)
    held.status = "resolved"
    await db_session.commit()
    async with command_transaction(db_session, mode="preview") as command:
        command.owner_acceptance_overrides.add((held.id, held.version, held.brief_revision, held.artifact_revision))
        with pytest.raises(AuthorityError) as refused:
            await TaskBriefService(db_session).require_review(held, accepting=True)
    assert refused.value.code == "replacement_contribution_unattributed"
    # The owner override cannot lift the hold, so the steps for a held replacement never offer it.
    for step in (NEXT_STEPS["replacement_contribution_unattributed"], VARIANTS["carried_run_unattributed"]):
        assert step["ui_action"] is None and "owner-acceptance" not in " ".join(step["commands"].values())
        assert "owner" not in step["message"].lower().replace("even an owner cannot", "")


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("overlap", ["same_actor", "same_profile"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_carried_contributor_cannot_verify_without_the_strict_policy(
    db_session, db_session_factory, task_factory, team_member_factory, actor_factory, monkeypatch, transport, overlap,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    (team, member, verifier, _, original, replacement, *_rest, unattributed) = await _scenario(
        db_session, task_factory, team_member_factory, strict=False)
    worker, reviewer = team.actors[member.actor_key], team.actors[verifier.actor_key]
    pm_key, worker_key = team.sink.keys[team.manifest.controller.actor_key], team.sink.keys[member.actor_key]
    # The carried run was executed by the reviewer itself, or by another actor holding its profile.
    author = reviewer if overlap == "same_actor" else await actor_factory(profile=reviewer.profile)
    run = await db_session.get(AgentRun, unattributed.id)
    run.actor_id = author.id
    run.execution_provenance = {"actor_id": author.id, "profile_id": reviewer.profile_id,
                                "profile_revision": f"p{reviewer.profile_id}-begin", "source": "authenticated_work_begin",
                                "terminal_profile_id": reviewer.profile_id}
    (await db_session.get(AgentTaskAssignment, run.assignment_id)).actor_id = author.id
    await db_session.commit()
    ids = {"worker": worker.id, "reviewer": reviewer.id, "author": author.id, "profile": reviewer.profile_id,
           "run": run.id, "replacement": replacement.id, "version": replacement.version}
    await through(transport, db_session_factory, monkeypatch, "agent_record_task_replacement",
                  f"/api/agent/planning/tasks/{original.id}/replacement", pm_key,
                  _replacement(original, replacement, [ids["run"]]), task_id=original.id, receipt="carry-reviewer-run")
    head = "a" * 40
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        assigned = await call("agent_create_assignment", "/api/agent/assignments", pm_key, payload={
            "task_id": ids["replacement"], "actor_id": ids["worker"], "expected_task_version": ids["version"]},
            receipt="carry-execution")
        decision = await call("agent_get_my_work", "/api/agent/me/work", worker_key)
        claim = await call("agent_begin_my_work", "/api/agent/me/work/begin", worker_key, payload={
            "assignment_id": assigned["id"], "queue_revision": decision["queue_revision"],
            "model": member.default_model_binding_key}, receipt="carry-begin")
        submitted = await call("agent_submit_my_work", "/api/agent/me/work/submit", worker_key, payload={
            **fence(claim), "observed_model": member.default_model_binding_key, "summary": "Rebuilt on carried work",
            "evidence": {"tests": "passed"}, "commit_url": URL + "commit/" + head, "pr_url": URL + "pull/11"},
            receipt="carry-submit")
    expected = "verification_actor_not_independent" if overlap == "same_actor" else "verification_profile_not_independent"
    await through(transport, db_session_factory, monkeypatch, "agent_create_assignment", "/api/agent/assignments", pm_key,
                  {"task_id": ids["replacement"], "actor_id": ids["reviewer"], "purpose": "verification",
                   "expected_task_version": submitted["task"]["version"], "reviewer_profile_id": ids["profile"]},
                  receipt="carried-author-review", error=expected)
    async with db_session_factory() as audit:
        from app.services.review_provenance import execution_profile_history
        assignments = (await audit.scalars(select(AgentTaskAssignment).where(
            AgentTaskAssignment.task_id == ids["replacement"]))).all()
        history = await execution_profile_history(audit, assignments, task_id=ids["replacement"])
        # The verification preview reads the same history, so it excludes the carried run's author too.
        carried = [row for row in history if row.get("carried_from_task_id")]
        assert {(row["run_id"], row["actor_id"], row["profile_id"]) for row in carried} == {
            (ids["run"], ids["author"], ids["profile"])}
        await audit.rollback()


@pytest.mark.sqlite
async def test_a_chained_replacement_inherits_the_earlier_carried_work(db_session, task_factory, actor_factory,
                                                                      monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    from app.services.task_replacement_service import carried_contributors
    project, original, first = await _plain(db_session, task_factory)
    second = await task_factory(title="Second", project_id=project.id, status="planned",
                                iteration=await db_session.get(Iteration, original.iteration_id))
    worker = await actor_factory()
    worker_id = worker.id
    frozen = [SimpleNamespace(id=task.id, version=task.version) for task in (original, first, second)]

    async def attempt(task):
        execution = AgentTaskAssignment(task_id=task.id, actor_id=worker_id, purpose="execution", queue_class="normal",
                                        state="fulfilled", task_version=task.version, routing_snapshot="{}")
        db_session.add(execution)
        await db_session.flush()
        run = AgentRun(task_id=task.id, actor_id=worker_id, assignment_id=execution.id, status="succeeded")
        db_session.add(run)
        await db_session.commit()
        return run.id

    service = TaskReplacementService(db_session)
    carried = await attempt(frozen[0])
    await service.record(frozen[0].id, _data(frozen[0], frozen[1], carried_run_ids=[carried]))
    # The first replacement then ran; its own run is carried into the second replacement.
    rebuilt = await attempt(frozen[1])
    await service.record(frozen[1].id, _data(frozen[1], frozen[2], carried_run_ids=[rebuilt]))
    run_ids = [carried, rebuilt]
    rows = await carried_contributors(db_session, await db_session.get(Task, frozen[2].id))
    assert {(row["run_id"], row["carried_from_task_id"]) for row in rows} == {
        (run_ids[1], frozen[1].id), (run_ids[0], frozen[0].id)}


async def _replaced_pair(db, task_factory, *, backlog):
    project = Project(name="Restorable")
    db.add(project)
    await db.flush()
    if backlog:
        original, replacement, dependent = (Task(title=title, project_id=project.id, status=status)
                                            for title, status in (("Original", "resolved"), ("Replacement", "planned"),
                                                                  ("Dependent", "planned")))
        db.add_all([original, replacement, dependent])
        await db.flush()
    else:
        original = await task_factory(title="Original", project_id=project.id, status="resolved")
        iteration = await db.get(Iteration, original.iteration_id)
        iteration.project_id = project.id
        replacement = await task_factory(title="Replacement", project_id=project.id, status="planned", iteration=iteration)
        dependent = await task_factory(title="Dependent", project_id=project.id, status="planned", iteration=iteration)
    db.add(TaskDependency(task_id=dependent.id, depends_on_id=original.id))
    await db.commit()
    frozen = [SimpleNamespace(id=task.id, version=task.version, iteration_id=task.iteration_id)
              for task in (original, replacement, dependent)]
    await TaskReplacementService(db).record(frozen[0].id, _data(frozen[0], frozen[1]))
    return project.id, frozen


@databases
@pytest.mark.parametrize("scope", ["iteration", "backlog"])
async def test_restoring_a_pre_replacement_snapshot_is_refused(db_session, task_factory, monkeypatch, scope):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    from app.commands import PlanningConflict
    from app.models.recovery import ApplicationSnapshot
    project_id, (original, replacement, dependent) = await _replaced_pair(db_session, task_factory,
                                                                         backlog=scope == "backlog")
    if scope == "iteration":
        from app.services.snapshot_service import SnapshotService
        saved = [item for item in await SnapshotService(db_session).list_snapshots(original.iteration_id)
                 if item["reason"] == "before_task_replacement"]
        assert len(saved) == 1
        restore = SnapshotService(db_session).restore(original.iteration_id, saved[0]["filename"])
    else:
        from app.services.backlog_snapshot_service import BacklogSnapshotService
        snapshot = await db_session.scalar(select(ApplicationSnapshot.id).where(
            ApplicationSnapshot.project_id == project_id).order_by(ApplicationSnapshot.id.desc()).limit(1))
        versions = dict((await db_session.execute(select(Task.id, Task.version).where(
            Task.project_id == project_id, Task.iteration_id.is_(None)))).all())
        restore = BacklogSnapshotService(db_session).restore(project_id, snapshot, versions, reason="Undo the replacement")
    with pytest.raises(PlanningConflict) as refused:
        await restore
    assert refused.value.code == "restore_conflicts_with_task_replacement"
    # Nothing changed: the original stays withdrawn and its dependent still waits on the replacement.
    assert (await db_session.get(Task, original.id)).canceled_at is not None
    assert (await db_session.scalar(select(TaskDependency.depends_on_id).where(
        TaskDependency.task_id == dependent.id))) == replacement.id
