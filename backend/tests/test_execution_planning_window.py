"""Date-only planning reservations retain verifiable work without weakening task writes."""

from contextlib import nullcontext
from datetime import datetime, timedelta, timezone
import asyncio
import json
from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import select, text, update
from sqlalchemy.exc import DBAPIError

from app.config import get_settings
from app.main import app
from app import mcp_server
from app.models.agent import (
    AgentIdempotencyRecord,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.identity import CommandAudit, Principal, ProjectMembership, WorkspaceMembership
from app.models.recovery import ApplicationSnapshot
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.agent_service import hash_api_key
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests import test_team_pm_dispatch
from tests.test_team_pm_recovery import recovery_api

db_session_factory = test_team_pm_dispatch.db_session_factory


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=(pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network)
        ),
    ],
)
def test_nullable_window_migration_preserves_the_prior_run(dialect, request, tmp_path, configure_database):
    from alembic import command
    from sqlalchemy import create_engine
    from app.models.agent import AgentActor
    from app.services.upgrade_service import alembic_config

    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_planning_window_migration.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    try:
        with engine.connect() as connection:
            config = alembic_config(connection=connection)
            command.upgrade(config, "20261120_0018")
            project = connection.execute(
                Project.__table__.insert().values(name="Delivery evidence")
            ).inserted_primary_key[0]
            worker = connection.execute(
                AgentActor.__table__.insert().values(
                    name="original-worker",
                    display_name="Original worker",
                    role="worker",
                    api_key_hash="synthetic-hash",
                )
            ).inserted_primary_key[0]
            task = connection.execute(
                Task.__table__.insert().values(
                    title="Retained notes",
                    project_id=project,
                    version=7,
                    status="active",
                    claimed_by=worker,
                    claim_generation=1,
                )
            ).inserted_primary_key[0]
            assignment = connection.execute(
                AgentTaskAssignment.__table__.insert().values(
                    task_id=task, actor_id=worker, purpose="execution", state="accepted", task_version=6
                )
            ).inserted_primary_key[0]
            run = connection.execute(
                AgentRun.__table__.insert().values(
                    task_id=task,
                    assignment_id=assignment,
                    actor_id=worker,
                    status="running",
                    claim_generation=1,
                    execution_provenance={"source": "authenticated_work_begin"},
                )
            ).inserted_primary_key[0]
            checkpoint = connection.execute(
                TaskEvent.__table__.insert().values(
                    task_id=task,
                    actor_id=worker,
                    actor_type="agent",
                    event_type="agent.checkpoint",
                    payload='{"output_state":"retained"}',
                )
            ).inserted_primary_key[0]

            def retained():
                rows = {}
                for table, identity in (
                    ("tasks", task),
                    ("agent_task_assignments", assignment),
                    ("agent_runs", run),
                    ("task_events", checkpoint),
                ):
                    row = dict(
                        connection.execute(text(f"SELECT * FROM {table} WHERE id=:id"), {"id": identity})
                        .mappings()
                        .one()
                    )
                    if table == "tasks" and "execution_planning_window" in row:
                        assert row.pop("execution_planning_window") is None
                    rows[table] = row
                return rows

            original = retained()
            for target in ("20261121_0019", "20261120_0018", "20261121_0019"):
                connection.commit()
                (command.upgrade if target.endswith("0019") else command.downgrade)(config, target)
                assert retained() == original
    finally:
        engine.dispose()


async def planning_patch(client, pm, iteration, revision, key, **changes):
    response = await client.patch(
        f"/api/agent/planning/iterations/{iteration}",
        headers={
            "X-Agent-API-Key": pm,
            "Idempotency-Key": key,
            "X-Correlation-ID": key,
            "X-Agent-Rationale": "Apply the approved planning change",
        },
        json={"expected_revisions": {str(iteration): revision}, **changes},
    )
    return response


async def operator_call(
    http, transport, credential, task, receipt, *, apply=False, expected=None, key=None, denied=None
):
    params = {"task_id": task, "apply": apply}
    params.update(receipt if isinstance(receipt, dict) else {"planning_receipt_id": receipt})
    if expected:
        params["expected_evidence_digest"] = expected
    if key:
        params.update(
            idempotency_key=key, rationale="Reconcile the verified planning reservation", correlation_id=key
        )
    if transport == "rest":
        controls = {
            name: params.pop(name)
            for name in ["idempotency_key", "rationale", "correlation_id"]
            if name in params
        }
        headers = {"X-Agent-API-Key": credential} | {
            header: controls[field]
            for field, header in [
                ("idempotency_key", "Idempotency-Key"),
                ("rationale", "X-Agent-Rationale"),
                ("correlation_id", "X-Correlation-ID"),
            ]
            if field in controls
        }
        params.pop("task_id")
        response = await http.post(
            f"/api/agent/tasks/{task}/reconcile-planning-window", params=params, headers=headers
        )
        if denied:
            assert response.status_code in {403, 409} and denied in response.text, response.text
            return
        assert response.status_code == 200, response.text
        return response.json()
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with (
        server.session_manager.run(),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
        ) as client,
    ):
        response = await client.post(
            "/",
            headers={"X-Agent-API-Key": credential, "Accept": "application/json, text/event-stream"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "agent_reconcile_planning_window", "arguments": params},
            },
        )
        result = response.json()["result"]
        if denied:
            assert result["isError"] and denied in result["content"][0]["text"], result
            return
        assert not result["isError"], result
        return json.loads(result["content"][0]["text"])


async def worker_attest(http, transport, key, run_id, body, request_key, *, error=None):
    if transport == "rest":
        response = await http.post(
            f"/api/agent/me/runs/{run_id}/attest-retained-output",
            headers={"X-Agent-API-Key": key, "Idempotency-Key": request_key},
            json=body,
        )
        if error:
            assert response.status_code in {403, 409} and error in response.text, response.text
            return
        assert response.status_code == 200, response.text
        return response.json()
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with (
        server.session_manager.run(),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
        ) as client,
    ):
        response = await client.post(
            "/",
            headers={"X-Agent-API-Key": key, "Accept": "application/json, text/event-stream"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "agent_attest_retained_planning_output",
                    "arguments": {"run_id": run_id, "payload": body, "idempotency_key": request_key},
                },
            },
        )
        result = response.json()["result"]
        if error:
            assert result["isError"] and error in result["content"][0]["text"], result
            return
        assert not result["isError"], result
        return json.loads(result["content"][0]["text"])


async def competing_updates(factory, task, assignment_id, *, blocked, run_id=None):
    writes = {
        "task": update(Task).where(Task.id == task.id).values(title=Task.title),
        "iteration": update(Iteration)
        .where(Iteration.id == task.iteration_id)
        .values(end_date=Iteration.end_date),
        "project": update(Project).where(Project.id == task.project_id).values(name=Project.name),
        "assignment": update(AgentTaskAssignment)
        .where(AgentTaskAssignment.id == assignment_id)
        .values(reason=AgentTaskAssignment.reason),
    }
    if run_id is not None:
        writes["original_run"] = update(AgentRun).where(AgentRun.id == run_id).values(error=AgentRun.error)
    for name, statement in writes.items():
        async with factory() as writer:
            await writer.execute(text("SET LOCAL lock_timeout = '160ms'"))
            if blocked:
                with pytest.raises(DBAPIError) as failure:
                    await writer.execute(statement)
                assert getattr(failure.value.orig, "sqlstate", None) == "55P03", name
                await writer.rollback()
            else:
                assert (await writer.execute(statement)).rowcount == 1, name
                await writer.commit()
    return sorted(writes)


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize(
    "case",
    [
        "running",
        "verification",
        "rework",
        "substantive",
        "legacy_running",
        "legacy_refresh",
        "legacy_verification",
        "legacy_rework",
        "legacy_recovered_rework",
        "legacy_missing",
        "legacy_stale",
        "legacy_scope",
        "authority_changed",
        "artifact_changed",
        "consecutive_extensions",
        "legacy_drained",
    ],
)
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_date_only_reservation(
    db_session,
    db_session_factory,
    task_factory,
    team_member_factory,
    actor_factory,
    monkeypatch,
    transport,
    case,
    record_property,
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    legacy = case.startswith("legacy_")
    lane = case.removeprefix("legacy_")
    recovered_original = lane == "recovered_rework"
    if recovered_original:
        lane = "rework"
    if legacy:
        operator_key = "isolated-planning-recovery-operator"
        operator = await actor_factory(role="pm", scopes='["admin"]', api_key_hash=hash_api_key(operator_key))
        principal = Principal(kind="agent", display_name="Planning operator", agent_actor_id=operator.id)
        db.add(principal)
        await db.flush()
        db.add(WorkspaceMembership(principal_id=principal.id, role="operator"))
        await db.commit()
    team = await provision_ready_topology(db)
    member, verifier = team.manifest.workers[0], team.manifest.verifiers[0]
    worker = team.actors[member.actor_key]
    reviewer = team.actors[verifier.actor_key]
    pm = team.actors[team.manifest.controller.actor_key]
    wk, rk, pk = (team.sink.keys[m.actor_key] for m in (member, verifier, team.manifest.controller))
    scope = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Qualify the delivery notes",
    )
    task = scope.task
    project = Project(name="Delivery notes", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    iteration = await db.get(Iteration, task.iteration_id)
    task.project_id = iteration.project_id = project.id
    task.effort_hours = 8
    grants = [(pm, "manager"), (worker, "executor"), (reviewer, "reviewer")]
    models = [(member, "first-publisher"), (verifier, "second-publisher")]
    if recovered_original:
        other_member = team.manifest.workers[1]
        earlier_actor = team.actors[other_member.actor_key]
        earlier_key = team.sink.keys[other_member.actor_key]
        earlier_capacity = await team_member_factory(profile=earlier_actor.profile, iteration=iteration)
        task.assignee_id = earlier_capacity.id
        grants.append((earlier_actor, "executor"))
        models.append((other_member, "first-publisher"))
    for actor, role in grants:
        principal = await IdentityService(db).actor_context(actor)
        db.add_all(
            [
                WorkspaceMembership(principal_id=principal.principal_id, role="member"),
                ProjectMembership(principal_id=principal.principal_id, project_id=project.id, role=role),
            ]
        )
    for model, publisher in models:
        entry = await db.scalar(
            select(AgentModelCatalogEntry).where(
                AgentModelCatalogEntry.key == model.default_model_binding_key
            )
        )
        entry.publisher_key = publisher
    await db.commit()
    work = ("agent_get_my_work", "/api/agent/me/work")
    begin = ("agent_begin_my_work", "/api/agent/me/work/begin")
    submit = ("agent_submit_my_work", "/api/agent/me/work/submit")
    dispatch = ("agent_create_assignment", "/api/agent/assignments")
    verdict = ("agent_submit_review_verdict", "/api/agent/me/reviews/verdict")
    async with (
        recovery_api(transport, db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        first_actor = earlier_actor if recovered_original else worker
        assigned = await call(
            *dispatch,
            pk,
            payload={
                "actor_id": first_actor.id,
                "task_id": task.id,
                "expected_task_version": task.version,
                "reviewer_profile_id": reviewer.profile_id,
            },
            receipt="assign-notes",
        )
        if recovered_original:
            ready = await call(*work, earlier_key)
            previous = await call(
                *begin,
                earlier_key,
                payload={
                    "assignment_id": assigned["id"],
                    "queue_revision": ready["queue_revision"],
                    "model": other_member.default_model_binding_key,
                },
                receipt="attempt-earlier-notes",
            )
            stopped = await call(
                "agent_fail_my_work",
                "/api/agent/me/work/fail",
                earlier_key,
                payload={
                    **fence(previous),
                    "observed_model": other_member.default_model_binding_key,
                    "output_state": "retained",
                    "status": "failed",
                    "summary": "Hand back the draft notes",
                    "evidence": {"artifact": "the earlier original draft"},
                },
                receipt="retain-earlier",
            )
            changed_owner = await http.patch(
                f"/api/agent/planning/tasks/{task.id}",
                headers={
                    "X-Agent-API-Key": pk,
                    "Idempotency-Key": "transfer-notes",
                    "X-Correlation-ID": "transfer-notes",
                    "X-Agent-Rationale": "Transfer the retained draft to its new capacity owner",
                },
                json={"expected_version": stopped["task"]["version"], "assignee_id": scope.member.id},
            )
            assert changed_owner.status_code == 200, changed_owner.text
            (item,) = (await call("agent_list_recovery_tasks", "/api/agent/recovery", pk))["items"]
            recovered = await call(
                "agent_requeue_recovery",
                f"/api/agent/recovery/{task.id}/requeue",
                pk,
                task_id=task.id,
                payload={
                    "actor_id": worker.id,
                    "expected_task_version": item["task"]["version"],
                    "expected_claim_generation": item["claim_generation"],
                    "expected_live_assignment_ids": [],
                    "expected_running_run_ids": [],
                    "reason": "Recover the retained source notes",
                },
                receipt="resume-with-author",
            )
            assigned = recovered["assignment"]
        queue = await call(*work, wk)
        running = await call(
            *begin,
            wk,
            payload={
                "assignment_id": assigned["id"],
                "queue_revision": queue["queue_revision"],
                "lease_seconds": 60 if lane == "drained" else 3600,
                "model": member.default_model_binding_key,
            },
            receipt="begin-notes",
        )
        retained = {
            "summary": "Delivery notes complete",
            "observed_model": member.default_model_binding_key,
            "evidence": {"criteria": "checked instructions"},
            "artifact_links": ["https://example.test/guide"],
        }
        live_id = assigned["id"]
        if lane in {"verification", "rework"}:
            submitted = await call(
                *submit, wk, payload={**fence(running), **retained}, receipt="submit-notes"
            )
            verification = await call(
                *dispatch,
                pk,
                payload={
                    "actor_id": reviewer.id,
                    "task_id": task.id,
                    "purpose": "verification",
                    "reviewer_profile_id": reviewer.profile_id,
                    "expected_task_version": submitted["task"]["version"],
                },
                receipt="assign-review",
            )
            live_id = verification["id"]
            rejection = {
                "assignment_id": live_id,
                "verdict": "reject",
                "reason": "Clarify the verification example",
                "rework_actor_id": worker.id,
                "observed_model": verifier.default_model_binding_key,
                "reviewed_candidate_digest": verification["review_selection"]["candidate"]["digest"],
                "evidence": {"criterion": "example needs clarification"},
            }
            if lane == "rework":
                rejected = await call(
                    *verdict,
                    rk,
                    payload={**rejection, "expected_task_version": submitted["task"]["version"]},
                    receipt="reject-notes",
                )
                live_id = rejected["rework_assignment"]["id"]
        cohort = {}
        if case == "running" and transport == "rest":
            async with db_session_factory() as cohort_db:
                peers = [
                    Task(
                        title=f"Unassigned note {i}",
                        project_id=project.id,
                        iteration_id=iteration.id,
                        status="planned",
                    )
                    for i in range(87)
                ]
                closed = Task(
                    title="Already approved note",
                    project_id=project.id,
                    iteration_id=iteration.id,
                    status="closed",
                )
                cohort_db.add_all([*peers, closed])
                await cohort_db.commit()
                cohort = {peer.id: (peer.version, peer.status) for peer in [*peers, closed]}
        async with db_session_factory() as read:
            prior_version = (await read.get(Task, task.id)).version
            prior_iteration = await read.get(Iteration, iteration.id)
            revision, end = prior_iteration.revision, prior_iteration.end_date
            live = await read.get(AgentTaskAssignment, live_id)
            original = live.task_version, live.routing_snapshot, live.review_selection
        params = {"end_date": (end + timedelta(days=7)).isoformat()}
        if lane in {"substantive", "scope"}:
            params["name"] = "Changed iteration"
        from app.services.execution_planning_window import seal_authority

        is_pg = db.get_bind().dialect.name == "postgresql"
        writers = []

        async def observe_locks(*args, **kwargs):
            sealed = await seal_authority(*args, **kwargs)
            if kwargs.get("lock"):
                writers.extend(await competing_updates(db_session_factory, task, live_id, blocked=True))
            return sealed

        # Legacy state executes the authentic scheduling, snapshot and PM receipt
        # code. The predecessor had no prospective equivalence writer.
        with (
            patch("app.services.execution_planning_window.extension_input", return_value=None)
            if legacy
            else nullcontext(),
            (
                patch("app.services.execution_planning_window.seal_authority", side_effect=observe_locks)
                if is_pg and case == "running"
                else nullcontext()
            ),
        ):
            changed = await planning_patch(http, pk, iteration.id, revision, "extend-delivery", **params)
        assert changed.status_code == 200, changed.text
        replay = await planning_patch(http, pk, iteration.id, revision, "extend-delivery", **params)
        assert replay.json() == changed.json()
        outdated = await planning_patch(http, pk, iteration.id, revision, "stale-extension", **params)
        assert outdated.status_code == 409
        async with db_session_factory() as read:
            current = await read.get(Task, task.id)
            assert current.version == prior_version + 1
            live = await read.get(AgentTaskAssignment, live_id)
            assert (live.task_version, live.routing_snapshot, live.review_selection) == original
            assert bool(current.execution_planning_window) == (not legacy and lane != "substantive")
            if cohort:
                observed = (await read.scalars(select(Task).where(Task.id.in_(cohort)))).all()
                assert len(observed) == 88
                assert all(
                    row.version == cohort[row.id][0] + (row.status != "closed")
                    and row.execution_planning_window is None
                    for row in observed
                )
                record_property("nonclosed_task_reservations", 88)
                record_property("closed_task_versions_unchanged", 1)
        if lane == "consecutive_extensions":
            moved = await planning_patch(
                http,
                pk,
                iteration.id,
                changed.json()["result"]["revision"],
                "extend-again",
                end_date=(end + timedelta(days=10)).isoformat(),
            )
            assert moved.status_code == 200, moved.text
            async with db_session_factory() as read:
                current = await read.get(Task, task.id)
                assert current.version == prior_version + 2
                assert (
                    current.execution_planning_window["from"],
                    current.execution_planning_window["through"],
                ) == (prior_version, current.version)
        if legacy:
            async with db_session_factory() as inspect:
                receipt = await inspect.scalar(
                    select(AgentIdempotencyRecord).where(
                        AgentIdempotencyRecord.operation == "planning.iteration.update",
                        AgentIdempotencyRecord.idempotency_key == "extend-delivery",
                    )
                )
                receipt_id = receipt.id
                if lane == "missing":
                    snapshot = await inspect.scalar(
                        select(ApplicationSnapshot).where(
                            ApplicationSnapshot.iteration_id == iteration.id,
                            ApplicationSnapshot.input_revision == revision,
                        )
                    )
                    await inspect.delete(snapshot)
                if lane == "stale":
                    (await inspect.get(Task, task.id)).description = "Materially changed instructions"
                await inspect.commit()
            if lane == "refresh":
                from app.agent_contract import EXECUTION_PLANNING_WINDOW_FEATURE
                from app.models.agent import AgentTeamTopologyMember
                from app.schemas.agent_team_setup import AgentTeamRuntimeAcknowledgement
                from app.services.agent_team_setup_service import AgentTeamSetupService

                async with db_session_factory() as refreshed:
                    roster = await refreshed.scalar(
                        select(AgentTeamTopologyMember).where(AgentTeamTopologyMember.actor_id == worker.id)
                    )
                    acknowledgement = json.loads(roster.runtime_acknowledgement_payload)
                    assert EXECUTION_PLANNING_WINDOW_FEATURE not in acknowledgement["server_features"]
                    acknowledgement["server_features"].append(EXECUTION_PLANNING_WINDOW_FEATURE)
                    prior_digest = roster.runtime_acknowledgement_digest
                    acknowledgement["expected_previous_acknowledgement_digest"] = prior_digest
                    renewed_ack = await AgentTeamSetupService(refreshed).acknowledge_runtime(
                        wk, AgentTeamRuntimeAcknowledgement.model_validate(acknowledgement)
                    )
                    assert (
                        renewed_ack.acknowledgement_digest != prior_digest
                        and renewed_ack.topology_runtime_ready
                    )
            if lane == "drained":
                head = "a" * 40
                origin = "https://github.com/example/release-notes"
                mark = {
                    "run_id": running["run"]["id"],
                    "assignment_id": assigned["id"],
                    "observed_model": member.default_model_binding_key,
                    "model_publisher": "first-publisher",
                    "output_state": "retained",
                    "candidate": head,
                    "git_tree": "b" * 40,
                    "pr_url": origin + "/pull/7",
                    "terminal_native_turn": "retained-runtime-turn",
                    "brief_revision": task.brief_revision,
                    "artifact_revision": task.artifact_revision,
                    "stale_assignment_version": prior_version,
                    "observed_task_version": current.version,
                }
                checkpoint = await http.post(
                    f"/api/agent/tasks/{task.id}/events",
                    headers={"X-Agent-API-Key": wk, "Idempotency-Key": "retained-output"},
                    json={
                        "event_type": "agent.checkpoint",
                        "payload": mark,
                        "claim_id": running["claim_id"],
                        "claim_generation": running["claim_generation"],
                    },
                )
                assert checkpoint.status_code == 200, checkpoint.text
                expiry = datetime.fromisoformat(running["claim_expires_at"].replace("Z", "+00:00"))
                while (delay := (expiry - datetime.now(timezone.utc)).total_seconds()) >= 0:
                    await asyncio.sleep(min(delay + 0.12, 30))
                recovery = await call(
                    "agent_requeue_recovery",
                    f"/api/agent/recovery/{task.id}/requeue",
                    pk,
                    task_id=task.id,
                    payload={
                        "actor_id": worker.id,
                        "expected_task_version": current.version,
                        "expected_claim_generation": running["claim_generation"],
                        "expected_live_assignment_ids": [assigned["id"]],
                        "expected_running_run_ids": [running["run"]["id"]],
                        "reason": "Preserve expired, checkpointed output under fresh ownership",
                    },
                    receipt="recover-ended-window",
                )
                async with db_session_factory() as read:
                    rec = await read.scalar(
                        select(AgentIdempotencyRecord).where(
                            AgentIdempotencyRecord.operation == "recovery.requeue",
                            AgentIdempotencyRecord.idempotency_key == "recover-ended-window",
                        )
                    )
                    earlier = await read.get(AgentRun, running["run"]["id"])
                    history = (earlier.status, earlier.ended_at, earlier.execution_provenance)
                    assert (
                        history[0] == "canceled"
                        and history[1] >= expiry
                        and history[2]["terminal_model"]["publisher_key"] is None
                    )
                body = {
                    "assignment_id": assigned["id"],
                    "claim_generation": running["claim_generation"],
                    "claim_id": running["claim_id"],
                    "planning_actor_id": pm.id,
                    "planning_command_key": "extend-delivery",
                    "recovery_actor_id": pm.id,
                    "recovery_command_key": "recover-ended-window",
                    "checkpoint_id": checkpoint.json()["id"],
                    "observed_model": mark["observed_model"],
                    "commit_url": origin + "/commit/" + head,
                    "git_tree": mark["git_tree"],
                    "pr_url": mark["pr_url"],
                    "terminal_native_turn": mark["terminal_native_turn"],
                    "confirmed_final_output": True,
                }
                other = team.sink.keys[team.manifest.workers[1].actor_key]
                await worker_attest(
                    http,
                    transport,
                    other,
                    running["run"]["id"],
                    body,
                    "foreign-output",
                    error="original authenticated worker",
                )
                await worker_attest(
                    http,
                    transport,
                    wk,
                    running["run"]["id"],
                    {**body, "git_tree": "c" * 40},
                    "wrong-tree",
                    error="must all match",
                )
                from app.services.retained_planning_output import _authenticate_checkpoint

                attestation_writers = []

                async def observe_retained(*args, **kwargs):
                    verified = await _authenticate_checkpoint(*args, **kwargs)
                    attestation_writers.extend(
                        await competing_updates(
                            db_session_factory,
                            task,
                            recovery["assignment"]["id"],
                            run_id=running["run"]["id"],
                            blocked=True,
                        )
                    )
                    return verified

                with (
                    patch(
                        "app.services.retained_planning_output._authenticate_checkpoint",
                        side_effect=observe_retained,
                    )
                    if is_pg
                    else nullcontext()
                ):
                    latest = await worker_attest(
                        http, transport, wk, running["run"]["id"], body, "attest-final-output"
                    )
                assert (
                    await worker_attest(
                        http, transport, wk, running["run"]["id"], body, "attest-final-output"
                    )
                    == latest
                )
                if is_pg:
                    assert attestation_writers == await competing_updates(
                        db_session_factory,
                        task,
                        recovery["assignment"]["id"],
                        run_id=running["run"]["id"],
                        blocked=False,
                    )
                    record_property("postgres_retained_attestation_writers", ",".join(attestation_writers))
                assert (
                    latest["source"] == "authenticated_post_interruption_attestation"
                    and latest["checkpoint_id"] == checkpoint.json()["id"]
                    and latest["recovery_receipt_id"] == rec.id
                )
                async with db_session_factory() as read:
                    original_run = await read.get(AgentRun, running["run"]["id"])
                    assert (
                        original_run.status,
                        original_run.ended_at,
                        original_run.execution_provenance,
                    ) == history
                    assert not (await read.get(Task, task.id)).claim_id
                fresh = await call(*work, wk)
                next_run = await call(
                    *begin,
                    wk,
                    payload={
                        "assignment_id": recovery["assignment"]["id"],
                        "queue_revision": fresh["queue_revision"],
                        "model": member.default_model_binding_key,
                    },
                    receipt="resume-evidence",
                )
                assert (
                    next_run["run"]["id"] != running["run"]["id"]
                    and next_run["claim_generation"] > running["claim_generation"]
                )
                resolved = await call(
                    *submit,
                    wk,
                    payload={**fence(next_run), **retained, "commit_urls": [body["commit_url"]]},
                    receipt="submit-fresh",
                )
                review = await call(
                    *dispatch,
                    pk,
                    payload={
                        "actor_id": reviewer.id,
                        "task_id": task.id,
                        "purpose": "verification",
                        "reviewer_profile_id": reviewer.profile_id,
                        "expected_task_version": resolved["task"]["version"],
                    },
                    receipt="review-after-drain",
                )
                sources = {r["run_id"]: r for r in review["review_selection"]["contributors"]}
                assert set(sources) == {running["run"]["id"], next_run["run"]["id"]}
                assert (
                    sources[running["run"]["id"]]["retained_output_attestation"]["event_id"]
                    == latest["event_id"]
                )
                assert sources[running["run"]["id"]]["commit_urls"] == [body["commit_url"]]
                return
            await operator_call(
                http,
                transport,
                pk,
                task.id,
                receipt_id,
                denied="admin:write" if transport == "mcp" else "operator",
            )
            preview = await operator_call(http, transport, operator_key, task.id, receipt_id)
            public_source = {"planning_actor_id": pm.id, "planning_command_key": "extend-delivery"}
            assert await operator_call(http, transport, operator_key, task.id, public_source) == preview
            if lane in {"missing", "scope", "stale"}:
                assert preview["missing"] == [
                    {
                        "missing": "unique_server_snapshot",
                        "scope": "end_date_only_request",
                        "stale": "unchanged_saved_task",
                    }[lane]
                ], preview
                await operator_call(
                    http,
                    transport,
                    operator_key,
                    task.id,
                    receipt_id,
                    apply=True,
                    expected=preview["evidence_digest"],
                    key="cannot-reconcile",
                    denied="planning_window_evidence_unavailable",
                )
                return
            assert preview["missing"] == [] and preview["assignment_ids"] == [live_id], preview
            await operator_call(
                http,
                transport,
                operator_key,
                task.id,
                receipt_id,
                apply=True,
                expected="0" * 64,
                key="stale-preview",
                denied="planning_window_evidence_unavailable",
            )
            with (
                patch("app.services.planning_window_reconciliation.seal_authority", side_effect=observe_locks)
                if is_pg and lane == "running"
                else nullcontext()
            ):
                if is_pg and lane == "running":
                    first, duplicate = await asyncio.gather(
                        *(
                            operator_call(
                                http,
                                transport,
                                operator_key,
                                task.id,
                                public_source,
                                apply=True,
                                expected=preview["evidence_digest"],
                                key="restore-window",
                            )
                            for _ in range(2)
                        )
                    )
                    assert first == duplicate
                    applied = first
                    record_property("concurrent_reconciliation_receipts", 1)
                else:
                    applied = await operator_call(
                        http,
                        transport,
                        operator_key,
                        task.id,
                        public_source,
                        apply=True,
                        expected=preview["evidence_digest"],
                        key="restore-window",
                    )
            assert applied["applied"] and applied["task_version"] == current.version
            assert (
                await operator_call(
                    http,
                    transport,
                    operator_key,
                    task.id,
                    receipt_id,
                    apply=True,
                    expected=preview["evidence_digest"],
                    key="restore-window",
                )
                == applied
            )
            async with db_session_factory() as audit:
                ev = await audit.get(TaskEvent, applied["event_id"])
                assert (
                    ev.actor_type == "operator"
                    and json.loads(ev.payload)["principal_id"] == applied["principal_id"]
                )
                entry = await audit.scalar(
                    select(CommandAudit).where(CommandAudit.action == "agent.planning_window_reconciled")
                )
                assert entry.details["response"] == applied
                current = await audit.get(Task, task.id)
                assert (
                    current.version == prior_version + 1
                    and (await audit.get(AgentTaskAssignment, live_id)).task_version == original[0]
                )
        if writers:
            assert writers == await competing_updates(db_session_factory, task, live_id, blocked=False)
            record_property("postgres_competing_writers", ",".join(writers))
            record_property("postgres_lock_outcome", "55P03 during command; committed afterward")
        if lane in {"authority_changed", "artifact_changed"}:
            async with db_session_factory() as audit:
                if lane == "authority_changed":
                    (await audit.get(Project, project.id)).require_different_review_publisher = False
                else:
                    (await audit.get(Task, task.id)).artifact_revision += 1
                await audit.commit()
            await call(
                *submit,
                wk,
                payload={**fence(running), **retained, "expected_task_version": current.version},
                receipt="real-change",
                error="no longer matches current ownership"
                if lane == "authority_changed"
                else "scope changed",
            )
        elif lane == "substantive":
            await call(
                *submit,
                wk,
                payload={**fence(running), **retained, "expected_task_version": current.version},
                receipt="cannot-submit",
                error="scope changed",
            )
        elif lane in {"running", "refresh", "consecutive_extensions"}:
            assert (await call(*work, wk))["state"] == "resume"
            replay = await call(
                *begin,
                wk,
                payload={
                    "assignment_id": assigned["id"],
                    "queue_revision": queue["queue_revision"],
                    "lease_seconds": 3600,
                    "model": member.default_model_binding_key,
                },
                receipt="begin-notes",
                error="no longer authoritative" if lane == "refresh" else None,
            )
            if lane != "refresh":
                assert replay == running
            renewed = await call(
                "agent_renew_my_work",
                "/api/agent/me/work/renew",
                wk,
                payload={**fence(running), "expected_task_version": current.version},
                receipt="renew-notes",
            )
            done = await call(*submit, wk, payload={**fence(renewed), **retained}, receipt="submit-notes")
            assert done["run"]["id"] == running["run"]["id"] and done["run"]["status"] == "succeeded"
        elif lane == "verification":
            done = await call(
                *verdict,
                rk,
                payload={
                    **rejection,
                    "verdict": "pass",
                    "rework_actor_id": None,
                    "expected_task_version": current.version,
                },
                receipt="accept-notes",
            )
            assert done["task"]["status"] == "closed"
        else:
            work_queue = await call(*work, wk)
            assert (
                work_queue["state"] == "start_assigned" and work_queue["next"]["assignment"]["id"] == live_id
            )
            next_run = await call(
                *begin,
                wk,
                payload={
                    "assignment_id": live_id,
                    "queue_revision": work_queue["queue_revision"],
                    "model": member.default_model_binding_key,
                },
                receipt="begin-correction",
            )
            assert (
                next_run["run"]["execution_provenance"]["supervised_rework"]["reviewer_profile_id"]
                == reviewer.profile_id
            )
            if recovered_original:
                lineage = next_run["run"]["execution_provenance"]["supervised_rework"]
                assert (
                    lineage["contributor_count"] == 2
                    and lineage["source_recovery"]["assignment_id"] == assigned["id"]
                )
