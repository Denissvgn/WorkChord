"""Only the named independent reviewer can consume current, operator-attested review material."""

import json
from contextlib import nullcontext
from datetime import timedelta
from functools import partial

import httpx
import pytest
from app import database, mcp_server
from app.authority import Authority, AuthorityError
from app.config import get_settings
from app.main import app
from app.models.agent import AgentModelBinding, AgentModelCatalogEntry, AgentTaskAssignment, TaskRoutingAssessment
from app.models.identity import PrincipalProfileLink, ProjectMembership, WorkspaceAuthorityState, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.routers.agent import _admin_header_actor
from app.schemas.agent import (
    AgentReviewVerdict,
    AgentTaskAssignmentCreate,
    AgentTaskAssignmentUpdate,
    AgentWorkBegin,
    AgentWorkSubmit,
)
from app.schemas.agent_routing import AgentModelBindingUpdate, AgentRoutingPreviewCreate
from app.schemas.agent_team_setup import AgentTeamMaster
from app.schemas.review_evidence import ReviewTestEvidence
from app.services.agent_model_catalog_service import AgentModelCatalogService
from app.services.agent_routing_service import (
    AgentRoutingConflictError,
    AgentRoutingService,
)
from app.services.agent_service import hash_api_key
from app.services.agent_team_setup_service import AgentTeamSetupService
from app.services.agent_work_service import AgentWorkService
from app.services.github_status_service import GitHubStatusService
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.review_evidence import record_review_evidence
from app.services.task_service import TaskService
from app.utils.time import utc_now
from pydantic import ValidationError
from sqlalchemy import select

from tests.support.transactions import reload_session_fixture
from tests.test_agent_routing_service import (
    _assessment_command,
    _command_context,
    _rollout,
)
from tests.test_agent_team_setup_qualification import (
    CapturingCredentialSink,
    ReadyTopology,
    acknowledge_all,
    apply_manifest,
    routing_base,
    seed_model_catalog,
    topology_actors,
    topology_payload,
)
from tests.test_review_provenance import command, database_engines
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory


@pytest.mark.contract
def test_scope_is_optional_and_only_substitutes_the_named_review_tool():
    from app.services.review_evidence import requirements_for

    envelope = {
        "modality_tags": ["text"],
        "tool_tags": ["host-shell", "repository-reader"],
        "data_policy_tags": ["private"],
    }
    scope = {"reviewer": {"actor_id": 3, "binding_id": 7}, "method": "source_and_tests", "tests": ["checked"]}
    assert requirements_for(envelope, {**scope, "method": "source_only", "tests": []}, 3, 7) is envelope
    assert requirements_for(envelope, None, 3, 7) is envelope
    assert requirements_for(envelope, scope, 3, 8) is envelope
    assert requirements_for(envelope, scope, 4, 7) is envelope
    assert requirements_for(envelope, scope, 3, 7) == {**envelope, "tool_tags": ["repository-reader"]}
    assert envelope["tool_tags"] == ["host-shell", "repository-reader"]
    ordinary = AgentRoutingPreviewCreate(purpose="verification", assessment_id=9, expected_task_version=2)
    assert (
        "review_evidence_id" not in ordinary.model_dump()
        and "review_assignment_id" not in ordinary.model_dump()
    )
    with pytest.raises(ValidationError):
        AgentRoutingPreviewCreate(**ordinary.model_dump(), review_assignment_id=1)
    with pytest.raises(ValidationError):
        ReviewTestEvidence(name="tests/../outside", result_sha256="e" * 64)
    unique = next(c for c in TaskRoutingAssessment.__table__.constraints
                  if c.name == "uq_task_routing_assessments_task_version_policy")
    assert tuple(unique.columns.keys()) == ("task_id", "task_version", "policy_version")


@pytest.mark.contract
async def test_packet_acknowledgement_requires_receipted_assignment():
    from types import SimpleNamespace
    from app.services.review_provenance import verify_verdict
    actor = SimpleNamespace(id=7)
    assignment = SimpleNamespace(actor_id=actor.id, review_selection={"reviewer": {"actor_id": actor.id}})
    verdict = SimpleNamespace(reviewed_packet_sha256="d" * 64)
    with pytest.raises(AgentRoutingConflictError, match="acknowledge the exact"):
        await verify_verdict(None, None, [], assignment, actor, verdict, None)


async def through(
    transport,
    factory,
    monkeypatch,
    tool,
    path,
    key,
    payload,
    *,
    task_id=None,
    assignment_id=None,
    receipt=None,
    error=None,
    admin_key=False,
):
    monkeypatch.setattr(database, "async_session_maker", factory)
    monkeypatch.setattr(mcp_server, "_session_factory", factory)
    server = mcp_server.create_mcp_server() if transport == "mcp" else None
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app()) if server else app
    args = {"payload": payload}
    headers = {"X-Admin-API-Key" if admin_key else "X-Agent-API-Key": key}
    if task_id is not None:
        args["task_id"] = task_id
    if assignment_id is not None:
        args["assignment_id"] = assignment_id
    if receipt:
        args.update(command(receipt))
        headers.update(
            {
                "Idempotency-Key": receipt,
                "X-Agent-Rationale": args["rationale"],
                "X-Correlation-ID": args["correlation_id"],
            }
        )
    async with server.session_manager.run() if server else nullcontext():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=application),
            base_url="http://localhost:8001",
        ) as client:
            if server:
                headers["Accept"] = "application/json, text/event-stream"
                r = await client.post(
                    "/",
                    headers=headers,
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {"name": tool, "arguments": args},
                    },
                )
                assert r.status_code == 200, r.text
                result = r.json()["result"]
                if error:
                    assert result["isError"] and error in result["content"][0]["text"], result
                    return
                assert not result.get("isError"), result
                return json.loads(result["content"][0]["text"])
            r = await client.request("PATCH" if assignment_id is not None else "POST", path, headers=headers, json=payload)
            if error:
                assert r.status_code in (400, 403, 409, 422) and error in r.text, r.text
                return
            assert r.is_success, r.text
            return r.json()


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize(
    "method,transport,terminal_case",
    [
        ("source_only", "rest", "pass"),
        ("source_and_tests", "mcp", "revoked"),
        ("source_only", "mcp", "pass"),
        ("source_and_tests", "rest", "pass"),
        ("source_only", "rest", "binding-revised"),
        ("source_only", "mcp", "actual-contributor-publisher"),
        ("source_and_tests", "rest", "artifact-changed"),
        ("source_only", "rest", "task-changed"),
        ("source_only", "mcp", "cancelled"),
        ("source_only", "rest", "no-opt-in"),
        ("source_only", "rest", "issuer-lost-authority"),
        ("source_only", "mcp", "issuer-profile-alias"),
        ("source_and_tests", "rest", "system-issuer"),
        ("source_only", "mcp", "renew-assignment"),
        ("source_and_tests", "rest", "enforced-update"),
        ("source_only", "rest", "expired-cancel"),
        ("source_only", "rest", "rework"),
    ],
)
async def test_scoped_source_packet_from_submission_through_verdict(
    db_session,
    db_session_factory,
    actor_factory,
    profile_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    method,
    transport,
    terminal_case,
):
    db = db_session
    managed = terminal_case in {"pass", "issuer-lost-authority", "system-issuer"}
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed" if managed else "trusted_local")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    system_id = await initialize_control_plane(db)
    payload = topology_payload(two_workers=False)
    payload["verifiers"][0].update(
        model_binding_keys=["planning-default", "verification-advanced"],
        default_model_binding_key="planning-default",
    )
    if terminal_case == "renew-assignment":
        await profile_factory(seed_key="package-reviewer", assignment_modes=["verification"])
        payload["verifiers"].append({
            **payload["verifiers"][0], "actor_key": "package-reviewer", "actor_name": "package-reviewer",
            "profile_key": "package-reviewer", "runtime_ref": "runtime://package-reviewer",
            "credential_ref": "agent-team-secure-sink/package-reviewer", "display_name": "Package reviewer",
        })
    manifest = AgentTeamMaster.model_validate(payload)
    await seed_model_catalog(db, manifest)
    sink = CapturingCredentialSink()
    setup = AgentTeamSetupService(db, credential_sink=sink)
    await apply_manifest(setup, manifest, expected_revision=0, key="provision-scoped-review")
    await acknowledge_all(setup, manifest, sink.keys)
    team = ReadyTopology(manifest, sink, setup, await topology_actors(db, manifest))
    member, review_member = team.manifest.workers[0], team.manifest.verifiers[0]
    pm = team.actors[team.manifest.controller.actor_key]
    worker = team.actors[member.actor_key]
    reviewer = team.actors[review_member.actor_key]
    manager_key = team.sink.keys[team.manifest.controller.actor_key]
    reviewer_key = team.sink.keys[review_member.actor_key]
    base = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Verify the package",
    )
    task = base.task
    iteration = await db.get(Iteration, task.iteration_id)
    project = Project(name="Package tools", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    task.project_id = iteration.project_id = project.id
    task.effort_hours = 8
    task.start_date = iteration.start_date = utc_now().date()
    task.end_date = iteration.end_date = utc_now().date() + timedelta(days=10)
    profile = reviewer.profile
    reviewer_member = await team_member_factory(profile=profile, iteration=iteration)
    if terminal_case == "renew-assignment":
        other_reviewer = team.actors["package-reviewer"]
        await team_member_factory(profile=other_reviewer.profile, iteration=iteration)
    model = await db.scalar(
        select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == member.default_model_binding_key)
    )
    rc = await db.scalar(
        select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == "verification-advanced")
    )
    model.publisher_key = "implementation-publisher"
    rc.publisher_key = "review-publisher"
    worker_binding = await db.scalar(
        select(AgentModelBinding).where(
            AgentModelBinding.actor_id == worker.id,
            AgentModelBinding.model_catalog_id == model.id,
        )
    )
    rb = await db.scalar(
        select(AgentModelBinding).where(
            AgentModelBinding.actor_id == reviewer.id,
            AgentModelBinding.model_catalog_id == rc.id,
        )
    )
    assert not rb.is_default
    default_binding = await db.scalar(
        select(AgentModelBinding).where(
            AgentModelBinding.actor_id == reviewer.id, AgentModelBinding.is_default.is_(True)
        )
    )
    default_catalog = await db.get(AgentModelCatalogEntry, default_binding.model_catalog_id)
    default_catalog.publisher_key = "other-review-publisher"
    technical_operator = await actor_factory(
        role="pm",
        scopes=json.dumps(["admin"]),
        api_key_hash=hash_api_key("private-test-operator"),
    )
    if managed:
        identity = IdentityService(db)
        for member_actor, project_role in ((pm, "manager"), (worker, "executor"), (reviewer, "reviewer")):
            principal = await identity.actor_context(member_actor)
            db.add_all(
                [
                    WorkspaceMembership(principal_id=principal.principal_id, role="member"),
                    ProjectMembership(
                        principal_id=principal.principal_id, project_id=project.id, role=project_role
                    ),
                ]
            )
        principal = await identity.actor_context(technical_operator)
        db.add(WorkspaceMembership(principal_id=principal.principal_id, role="operator"))
        nonowner = await actor_factory(
            role="pm", scopes=json.dumps(["admin"]), api_key_hash=hash_api_key("private-test-member")
        )
        guest = await identity.actor_context(nonowner)
        db.add(WorkspaceMembership(principal_id=guest.principal_id, role="member"))
    await db.commit()
    task = await TaskService(db).get_by_id(task.id)
    tid = task.id
    worker_id = worker.id
    reviewer_id = reviewer.id
    bid = rb.id
    work = AgentWorkService(db, rollout_service=_rollout("shadow"))
    routing = AgentRoutingService(db, rollout_service=_rollout("shadow"))

    def requirements():
        request = _assessment_command(task_version=task.version)
        return request.model_copy(
            update={
                "review_mode": "independent",
                "required_skill_levels": {},
                "required_model": request.required_model.model_copy(update={"tool_tags": ["host-shell"],
                    "allow_source_only_review": method == "source_only" and terminal_case != "no-opt-in"}),
            }
        )

    initial = await routing.create_assessment(
        tid, pm, requirements(), _command_context("assess-implementation")
    )
    execute = AgentRoutingPreviewCreate(
        assessment_id=initial.assessment.id,
        expected_task_version=task.version,
        purpose="execution",
    )
    missing = await routing.preview_task_routing(tid, pm, execute)
    assert any(
        x.actor_id == worker_id and "model_tool_missing" in x.hard_blocker_codes for x in missing.exclusions
    )
    with pytest.raises(ValidationError):
        AgentRoutingPreviewCreate(**{**execute.model_dump(), "review_evidence_id": 1})
    db.info["authority"] = Authority(None, "system", workspace_role="operator")
    await AgentModelCatalogService(db).update_binding(
        worker_binding.id,
        _admin_header_actor(),
        AgentModelBindingUpdate(expected_revision=worker_binding.revision, tool_tags=["host-shell"]),
        command=_command_context("declare-worker-capability"),
    )
    db.info.pop("authority")
    await acknowledge_all(team.service, team.manifest, team.sink.keys)
    positive = await routing.preview_task_routing(tid, pm, execute)
    assert any(x.actor_id == worker_id for x in positive.eligible_candidates), (
        positive.hard_blocker_codes,
        [(x.actor_id, x.hard_blocker_codes) for x in positive.exclusions],
    )
    ass = await work.create_assignment(
        pm,
        AgentTaskAssignmentCreate(task_id=tid, actor_id=worker_id, expected_task_version=task.version),
        **command("execute"),
    )
    begun = await work.begin(
        worker,
        AgentWorkBegin(
            assignment_id=ass.id,
            queue_revision=worker.queue_revision,
            lease_seconds=300,
            model=model.configured_model_alias,
        ),
        idempotency_key="begin",
    )
    commit = "a" * 40
    url = "https://github.com/example/package/"
    submitted = await work.submit(
        worker,
        AgentWorkSubmit(
            assignment_id=ass.id,
            run_id=begun.run.id,
            claim_id=begun.claim_id,
            claim_generation=begun.claim_generation,
            expected_task_version=begun.task.version,
            observed_model=model.configured_model_alias,
            summary="Prepared package",
            evidence={"check": "passed"},
            commit_url=url + "commit/" + commit,
            commit_urls=[url + "commit/" + commit],
            pr_url=url + "pull/1",
        ),
        idempotency_key="submit-package",
    )
    await db.refresh(task)
    assert submitted.task.status == "resolved"
    assess = await routing.create_assessment(tid, pm, requirements(), _command_context("assess-candidate"))
    preview = AgentRoutingPreviewCreate(
        assessment_id=assess.assessment.id,
        expected_task_version=task.version,
        purpose="verification",
        reviewer_profile_id=profile.id,
    )
    first = await routing.preview_task_routing(tid, pm, preview)
    assert any(
        x.actor_id == reviewer_id and "model_tool_missing" in x.hard_blocker_codes for x in first.exclusions
    )
    body = {
        "action": "issue",
        "expected_assessment_id": assess.assessment.id,
        "expected_task_version": task.version,
        "expected_brief_revision": task.brief_revision,
        "expected_artifact_revision": task.artifact_revision,
        "commit_sha": commit,
        "reviewer_actor_id": reviewer_id,
        "binding_id": bid,
        "expected_binding_revision": rb.revision,
        "method": method,
        "packet_sha256": "3" * 64,
        "tests": []
        if method == "source_only"
        else [{"name": "tests/test_package.py::test_version", "result_sha256": "4" * 64}],
        "expires_at": (utc_now() + timedelta(minutes=20)).isoformat(),
    }
    with pytest.raises(AuthorityError):
        await record_review_evidence(db, pm, tid, body, **command("pm-cannot-issue"))
    db.info["authority"] = Authority(system_id, "system", workspace_role="operator")
    operator = _admin_header_actor()
    if terminal_case == "no-opt-in":
        with pytest.raises(AgentRoutingConflictError, match="explicitly allow"):
            await record_review_evidence(db, operator, tid, body, **command("require-assessed-method"))
        return
    issued = await record_review_evidence(db, operator, tid, body, **command("review-package"))
    assert issued == await record_review_evidence(db, operator, tid, body, **command("review-package"))
    for change in (
        {"expected_assessment_id": assess.assessment.id + 1},
        {"expected_task_version": task.version + 1},
        {"expected_binding_revision": rb.revision + 1},
        {"commit_sha": "d" * 40},
        {"expires_at": (utc_now() - timedelta(seconds=1)).isoformat()},
    ):
        with pytest.raises(AgentRoutingConflictError):
            await record_review_evidence(
                db,
                operator,
                tid,
                {**body, **change},
                **command("invalid-" + next(iter(change))),
            )
        await reload_session_fixture(db)
    eid = issued["event_id"]
    db.info.pop("authority")
    rpc = partial(through, transport, db_session_factory, monkeypatch)
    issue_tool = "agent_attest_review_evidence"
    issue_url = f"/api/agent/tasks/{tid}/review-evidence"
    if terminal_case == "issuer-profile-alias":
        original = await IdentityService(db).actor_context(technical_operator)
        db.add(PrincipalProfileLink(principal_id=original.principal_id, profile_id=worker.profile_id,
                                    linked_by_principal_id=system_id))
        await db.commit()
        await rpc(issue_tool, issue_url, "private-test-operator", body, task_id=tid,
                  receipt="contributing-identity", error="verification_evidence_unavailable")
        return
    if terminal_case in {"binding-revised", "actual-contributor-publisher"}:
        participant = worker if transport == "rest" else reviewer
        original_scopes = participant.scopes
        participant.scopes = json.dumps([*json.loads(original_scopes), "admin"])
        await db.commit()
        participant_key = team.sink.keys[member.actor_key if participant is worker else review_member.actor_key]
        await rpc(issue_tool, issue_url, participant_key, body, task_id=tid,
                  receipt="participant-cannot-attest", error="verification_evidence_unavailable")
        participant.scopes = original_scopes
        await db.commit()
    if managed:
        await rpc(
            issue_tool,
            issue_url,
            "private-test-member",
            body,
            task_id=tid,
            receipt="membership-does-not-issue",
            error="operator_required",
        )
    system = terminal_case == "system-issuer"
    if system:
        monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "system-fixture-key")
        get_settings.cache_clear()
    actual = await rpc(
        issue_tool,
        issue_url,
        "system-fixture-key" if system else "private-test-operator",
        body,
        task_id=tid,
        receipt="transport-issue",
        admin_key=system,
    )
    eid = actual["event_id"]
    scoped = preview.model_copy(update={"review_evidence_id": eid})
    second = await routing.preview_task_routing(tid, pm, scoped)
    assert [(x.actor_id, x.model_binding_id) for x in second.eligible_candidates] == [(reviewer_id, bid)], (
        second.model_dump(mode="json")
    )
    assert second.review_evidence.id == eid
    assert (
        second.review_evidence.method,
        second.review_evidence.binding_id,
        second.review_evidence.packet_sha256,
    ) == (method, bid, body["packet_sha256"])
    assert first.review_evidence is None
    assert first.input_digest != second.input_digest and first.preview_digest != second.preview_digest
    from app.services import review_evidence

    with monkeypatch.context() as expired:
        expired.setattr(
            review_evidence,
            "utc_now",
            lambda: submitted.run.started_at + timedelta(days=4),
        )
        with pytest.raises(AgentRoutingConflictError, match="expired"):
            await routing.preview_task_routing(tid, pm, scoped)
    await reload_session_fixture(db)
    assert rb.tool_tags == [] and worker_binding.tool_tags == ["host-shell"]
    if method == "source_and_tests":
        monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "enforced")
        get_settings.cache_clear()
    live = await rpc(
        "agent_preview_task_routing",
        f"/api/agent/tasks/{tid}/routing-preview",
        manager_key,
        scoped.model_dump(mode="json"),
        task_id=tid,
    )
    assert [(x["actor_id"], x["model_binding_id"]) for x in live["eligible_candidates"]] == [
        (reviewer_id, bid)
    ]
    req = {
        "task_id": tid,
        "actor_id": reviewer_id,
        "purpose": "verification",
        "review_evidence_id": eid,
        "expected_task_version": task.version,
        "reviewer_profile_id": profile.id,
    }
    if method == "source_and_tests":
        req.update(
            assessment_id=assess.assessment.id,
            model_binding_id=bid,
            model_binding_revision=rb.revision,
            routing_preview_id=live["preview_id"],
            routing_preview_digest=live["preview_digest"],
        )
    else:
        req["review_binding_id"] = bid
    other = dict(req)
    if method == "source_and_tests":
        other.update(model_binding_id=default_binding.id, model_binding_revision=default_binding.revision)
        incorrect = "routing_selection_ineligible"
    else:
        other["review_binding_id"] = default_binding.id
        incorrect = "verification_evidence_unavailable"
    await rpc(
        "agent_create_assignment",
        "/api/agent/assignments",
        manager_key,
        other,
        receipt="wrong-review-binding",
        error=incorrect,
    )
    review = await rpc(
        "agent_create_assignment",
        "/api/agent/assignments",
        manager_key,
        req,
        receipt="assign-verifier",
    )
    assert review["review_selection"]["review_evidence"]["digest"] == actual["evidence_digest"]
    assert review["review_selection"]["review_evidence"]["method"] == method

    def live_receipt(assignment_id):
        return rpc(
            "agent_preview_task_routing",
            f"/api/agent/tasks/{tid}/routing-preview",
            manager_key,
            {**scoped.model_dump(mode="json"), "review_assignment_id": assignment_id},
            task_id=tid,
        )

    current = await live_receipt(review["id"])
    await rpc(
        "agent_preview_task_routing",
        f"/api/agent/tasks/{tid}/routing-preview",
        manager_key,
        {**scoped.model_dump(mode="json"), "review_assignment_id": ass.id},
        task_id=tid,
        error="verification_evidence_unavailable",
    )
    assert current["review_evidence"]["assignment_id"] == review["id"]
    assert (
        current["review_evidence"]["assignment_state"] == "queued"
        and current["review_evidence"]["digest"] == actual["evidence_digest"]
    )
    assert current["review_evidence"]["candidate_digest"] == review["review_selection"]["candidate"]["digest"]
    async def update_review(key, fields, *, error=None):
        await db.refresh(reviewer)
        return await rpc("agent_update_assignment", f"/api/agent/assignments/{review['id']}", manager_key,
                         {"expected_queue_revision": reviewer.queue_revision, **fields},
                         assignment_id=review["id"], receipt=key, error=error)

    if terminal_case == "enforced-update":
        proof = await rpc("agent_preview_task_routing", f"/api/agent/tasks/{tid}/routing-preview",
                          manager_key, scoped.model_dump(mode="json"), task_id=tid)
        changed = await update_review("reuse-enforced-selection", {
            "assessment_id":assess.assessment.id, "model_binding_id":bid, "model_binding_revision":rb.revision,
            "routing_preview_id":proof["preview_id"], "routing_preview_digest":proof["preview_digest"], "queue_rank":2})
        assert changed["review_selection"]["review_evidence"]["id"] == eid
    if terminal_case == "renew-assignment":
        await rpc(issue_tool, issue_url, "private-test-operator", {"action":"revoke", "evidence_id":eid},
                  task_id=tid, receipt="withdraw-prior-offer")
        other_binding = await db.scalar(select(AgentModelBinding).where(
            AgentModelBinding.actor_id == other_reviewer.id, AgentModelBinding.model_catalog_id == rc.id))
        changed_owner = {"actor_id":other_reviewer.id, "review_binding_id":other_binding.id,
                         "reviewer_profile_id":other_reviewer.profile_id}
        await update_review("replacement-needs-evidence", changed_owner, error="verification_evidence_unavailable")
        next_offer = await rpc(issue_tool, issue_url, "private-test-operator", {
            **body, "reviewer_actor_id":other_reviewer.id, "binding_id":other_binding.id,
            "expected_binding_revision":other_binding.revision}, task_id=tid, receipt="fresh-offer")
        replacement = await update_review("replace-reviewer", {**changed_owner, "review_evidence_id":next_offer["event_id"]})
        assert replacement["actor_id"] == other_reviewer.id
        assert replacement["review_selection"]["review_evidence"]["id"] == next_offer["event_id"] != eid
        return
    assert current["eligibility_basis"] == "task_policy_configuration_and_review_evidence"
    if terminal_case == "pass":
        # A stored accepted verification owner has the same readback contract as a queued one.
        # The worker execution begin command cannot produce this verification state.
        if transport == "rest":
            from app.models.agent import AgentTaskAssignment
            stored = await db.get(AgentTaskAssignment, review["id"])
            stored.state = "accepted"
            await db.commit()
            observed = await live_receipt(review["id"])
            assert observed["review_evidence"] == {**current["review_evidence"], "assignment_state":"accepted"}
            stored.state = "queued"
            await db.commit()
        # Occupancy and fresh-dispatch capacity are separate from the existing owner's evidence.
        full_capacity = reviewer_member.availability_percent
        reviewer_member.availability_percent = 0
        await db.commit()
        occupied = await live_receipt(review["id"])
        assert (
            not occupied["eligible_candidates"] and occupied["review_evidence"] == current["review_evidence"]
        )
        reviewer_member.availability_percent = full_capacity
        await db.commit()

    repository_head = {"sha": commit}

    async def github(cls, session):
        def respond(req):
            return httpx.Response(
                200,
                json=[
                    {
                        "sha": commit,
                        "commit": {
                            "author": {"email": "worker@example.test"},
                            "message": "Prepared package",
                        },
                    }
                ]
                if req.url.path.endswith("/commits")
                else {"head": repository_head, "commits": 1},
            )

        return GitHubStatusService(session, transport=httpx.MockTransport(respond))

    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(github))
    verdict = AgentReviewVerdict(
        assignment_id=review["id"],
        expected_task_version=task.version,
        verdict="pass",
        evidence={"tests": "observed"},
        observed_model=rc.configured_model_alias,
        reviewed_candidate_digest=review["review_selection"]["candidate"]["digest"],
        reviewed_packet_sha256=body["packet_sha256"],
    )
    await rpc(
        "agent_submit_review_verdict",
        "/api/agent/me/reviews/verdict",
        reviewer_key,
        verdict.model_copy(update={"reviewed_packet_sha256": "0" * 64}).model_dump(mode="json"),
        receipt="wrong-packet",
        error="verification_evidence_unavailable",
    )

    async def rejected(key, code, data=verdict):
        await rpc(
            "agent_submit_review_verdict",
            "/api/agent/me/reviews/verdict",
            reviewer_key,
            data.model_dump(mode="json"),
            receipt=key,
            error=code,
        )

    with monkeypatch.context() as expired:
        expired.setattr(review_evidence, "utc_now", lambda: submitted.run.started_at + timedelta(days=4))
        await rpc(
            "agent_preview_task_routing",
            f"/api/agent/tasks/{tid}/routing-preview",
            manager_key,
            {**scoped.model_dump(mode="json"), "review_assignment_id": review["id"]},
            task_id=tid,
            error="verification_evidence_unavailable",
        )
        await rejected("expired-during-review", "verification_evidence_unavailable")
        await rejected("expired-rejection", "verification_evidence_unavailable", verdict.model_copy(
            update={"verdict":"reject", "reason":"The package needs a corrected submitted source.",
                    "rework_actor_id":worker_id}))
        if terminal_case == "expired-cancel":
            await db.refresh(reviewer)
            cancelled = await work.update_assignment(review["id"], pm, AgentTaskAssignmentUpdate(
                expected_queue_revision=reviewer.queue_revision, state="cancelled"), **command("cancel-expired"))
            assert cancelled.state == "cancelled"
            return
    repository_head["sha"] = "9" * 40
    await rejected("changed-pr-head", "verification_candidate_stale")
    repository_head["sha"] = commit
    if terminal_case == "binding-revised":
        rb.revision += 1
        await db.commit()
        await rejected("stale-runtime", "agent_team_actor_outside_topology")
        await acknowledge_all(team.service, team.manifest, team.sink.keys)
        await rejected("changed-binding", "verification_evidence_unavailable")
    elif terminal_case == "actual-contributor-publisher":
        rc.publisher_key = model.publisher_key
        await db.commit()
        await rejected("contributing-publisher", "verification_publisher_not_independent")
    elif terminal_case in {"issuer-lost-authority", "system-issuer"}:
        if terminal_case == "system-issuer":
            assert actual["evidence"]["issuer"]["actor_id"] is None
            assert actual["evidence"]["issuer"]["principal_id"] == system_id
            state = await db.get(WorkspaceAuthorityState, 1)
            state.operator_principal_id = None
        else:
            identity = actual["evidence"]["issuer"]
            membership = await db.get(WorkspaceMembership, identity["principal_id"])
            membership.role = "member"
        await db.commit()
        await rejected("issuing-authority-changed", "verification_evidence_unavailable")
    elif terminal_case == "artifact-changed":
        task.artifact_revision += 1
        await db.commit()
        await rejected("changed-artifact", "verification_evidence_unavailable")
    elif terminal_case == "task-changed":
        task.version += 1
        await db.commit()
        await rejected(
            "changed-version",
            "agent_state_conflict",
            verdict.model_copy(update={"expected_task_version": task.version}),
        )
        from app.models.agent import AgentTaskAssignment
        from app.services.review_provenance import review_history

        history = await review_history(
            db,
            task,
            list(await db.scalars(select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == tid))),
            strict=True,
        )
        with pytest.raises(AgentRoutingConflictError, match="another candidate"):
            await review_evidence.resolve(db, task, eid, history)
    elif terminal_case == "cancelled":
        await db.refresh(reviewer)
        await work.update_assignment(
            review["id"],
            pm,
            AgentTaskAssignmentUpdate(state="cancelled", expected_queue_revision=reviewer.queue_revision),
            **command("withdraw-review"),
        )
        await rpc(
            "agent_preview_task_routing",
            f"/api/agent/tasks/{tid}/routing-preview",
            manager_key,
            {**scoped.model_dump(mode="json"), "review_assignment_id": review["id"]},
            task_id=tid,
            error="verification_evidence_unavailable",
        )
    elif terminal_case == "revoked":
        db.info["authority"] = Authority(None, "system", workspace_role="operator")
        revocation = await record_review_evidence(
            db,
            operator,
            tid,
            {"action": "revoke", "evidence_id": eid},
            **command("revoke-review"),
        )
        assert revocation["evidence_id"] == eid
        assert (
            await record_review_evidence(
                db, operator, tid, {"action": "revoke", "evidence_id": eid}, **command("revoke-review")
            )
            == revocation
        )
        with pytest.raises(AgentRoutingConflictError, match="already been revoked"):
            await record_review_evidence(
                db, operator, tid, {"action": "revoke", "evidence_id": eid}, **command("duplicate-revocation")
            )
        db.info.pop("authority")
        await rpc(
            "agent_preview_task_routing",
            f"/api/agent/tasks/{tid}/routing-preview",
            manager_key,
            {**scoped.model_dump(mode="json"), "review_assignment_id": review["id"]},
            task_id=tid,
            error="verification_evidence_unavailable",
        )
        await rpc(
            "agent_submit_review_verdict",
            "/api/agent/me/reviews/verdict",
            reviewer_key,
            verdict.model_dump(mode="json"),
            receipt="after-revocation",
            error="verification_evidence_unavailable",
        )
        updated = await update_review("order-revoked", {"queue_rank":3})
        assert updated["queue_rank"] == 3
        cancelled = await update_review("cancel-revoked", {"state":"cancelled"})
        assert cancelled["state"] == "cancelled"
    elif terminal_case == "rework":
        changed = await rpc("agent_submit_review_verdict", "/api/agent/me/reviews/verdict", reviewer_key,
                            verdict.model_copy(update={"verdict":"reject", "reason":"Correct the package version.",
                                "rework_actor_id":worker_id}).model_dump(mode="json"), receipt="return-for-rework")
        assert changed["task"]["status"] == "active"
        await rpc(issue_tool, issue_url, "private-test-operator", body, task_id=tid,
                  receipt="reworked-subject", error="verification_evidence_unavailable")
    else:
        accepted = await rpc(
            "agent_submit_review_verdict",
            "/api/agent/me/reviews/verdict",
            reviewer_key,
            verdict.model_dump(mode="json"),
            receipt="verdict",
        )
        assert accepted["task"]["status"] == "closed"
        await rpc(issue_tool, issue_url, "private-test-operator", body, task_id=tid,
                  receipt="completed-subject", error="verification_evidence_unavailable")
