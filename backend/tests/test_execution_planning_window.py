"""Date-only planning reservations retain verifiable work without weakening task writes."""

from contextlib import nullcontext
from datetime import datetime, timedelta, timezone
import asyncio
from copy import deepcopy
import json
from time import perf_counter_ns
from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import event as sqlalchemy_event, select, text, update
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
from app.utils import time as server_time
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests import test_team_pm_dispatch
from tests.test_team_pm_recovery import recovery_api

db_session_factory = test_team_pm_dispatch.db_session_factory


def test_cached_snapshot_requires_the_actual_unchanged_payload_bytes(tmp_path):
    from types import SimpleNamespace
    from datetime import date
    from app.services import planning_window_reconciliation as planning
    from app.services.execution_planning_window import digest

    iteration = {
        "id": 818,
        "project_id": 19,
        "calendar_id": 1,
        "name": "Notes",
        "manager_email": None,
        "start_date": "2026-07-01",
    }
    original = {"id": 22, "version": 4, "status": "active", "title": "Original notes", "children": []}
    data = {
        "snapshot_info": {"reason": "before_planning_input_change"},
        "iteration": {**iteration, "end_date": "2026-08-01"},
        "tasks": [original, {"id": 23, "title": "Another note", "children": []}],
    }
    row = SimpleNamespace(
        id=tmp_path.stat().st_ino,
        checksum=planning._canonical_snapshot_checksum(data),
        raw_payload=json.dumps(data),
    )
    context = digest({k: v for k, v in original.items() if k != "version"})

    def observe(allow_cache):
        return planning._snapshot_task(
            row, 22, 4, context, digest(iteration), date(2026, 8, 12), cache_reads=allow_cache
        )

    with patch.object(
        planning, "_canonical_snapshot_checksum", wraps=planning._canonical_snapshot_checksum
    ) as canonical:
        assert observe(True)[1] is None and canonical.call_count == 1
        assert observe(True)[1] is None and canonical.call_count == 1
        assert observe(False)[1] is None and canonical.call_count == 2
        changed = deepcopy(data)
        changed["tasks"][1]["title"] = "Changed outside the selected task"
        row.raw_payload = json.dumps(changed)
        assert observe(True)[1] == "matching_iteration_cutoff" and canonical.call_count == 3
        assert observe(False)[1] == "matching_iteration_cutoff" and canonical.call_count == 4


async def measured_pending_polls(call, work, worker_key, db, record_property):
    from app.services import planning_window_reconciliation as planning, retained_planning_output as retained

    engine = db.bind.sync_engine
    selects = 0
    authority_durations = []
    actual_stamp = retained.authority_stamp

    def count(_conn, _cursor, sql, _params, _context, _many):
        nonlocal selects
        selects += int(sql.lstrip().upper().startswith("SELECT"))

    async def timed_authority(*args, **kwargs):
        start = perf_counter_ns()
        try:
            return await actual_stamp(*args, **kwargs)
        finally:
            authority_durations.append(perf_counter_ns() - start)

    sqlalchemy_event.listen(engine, "before_cursor_execute", count)
    try:
        with (
            patch.object(
                planning, "_canonical_snapshot_checksum", wraps=planning._canonical_snapshot_checksum
            ) as checksum,
            patch.object(retained, "authority_stamp", side_effect=timed_authority),
        ):
            start = perf_counter_ns()
            first = await call(*work, worker_key)
            cold_ns = perf_counter_ns() - start
            cold_selects, cold_hashes = selects, checksum.call_count
            start = perf_counter_ns()
            second = await call(*work, worker_key)
            warm_ns = perf_counter_ns() - start
            warm_selects = selects - cold_selects
            assert first["state"] == second["state"] == "attention_required"
            assert cold_hashes == 1 and checksum.call_count == 1 and len(authority_durations) == 2
            assert (
                first["next"]["assignment"]["routing_snapshot"]
                == second["next"]["assignment"]["routing_snapshot"]
            )
        baseline_start = selects
        with patch.object(retained, "recovery_attestation_hint", return_value=None):
            baseline = await call(*work, worker_key)
        base_selects = selects - baseline_start
        assert baseline["state"] == "start_assigned"
    finally:
        sqlalchemy_event.remove(engine, "before_cursor_execute", count)
    assert cold_selects == warm_selects + (db.get_bind().dialect.name == "postgresql")
    # Both native engines measured 25 additional bounded selects here. Keep a
    # small allowance for transport instrumentation while catching another traversal.
    assert 0 < warm_selects - base_selects <= 32
    for key, value in {
        "cold_selects": cold_selects,
        "warm_selects": warm_selects,
        "without_hint_selects": base_selects,
        "cold_canonical_hashes": 1,
        "warm_canonical_hashes": 0,
        "fresh_authority_reads_per_poll": 1,
        "cold_poll_ms": round(cold_ns / 1e6, 3),
        "warm_poll_ms": round(warm_ns / 1e6, 3),
        "cold_authority_ms": round(authority_durations[0] / 1e6, 3),
        "warm_authority_ms": round(authority_durations[1] / 1e6, 3),
    }.items():
        record_property("planning_poll_" + key, str(value))
    return first


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


async def cancel_unconfirmable(http, transport, pm_key, assignment, queue_revision):
    reason = (
        "Original worker cannot confirm the final retained output; preserve its unknown historical publisher."
    )
    body = {"state": "cancelled", "reason": reason, "expected_queue_revision": queue_revision}
    key = "hold-unconfirmable-output"
    if transport == "rest":
        response = await http.patch(
            f"/api/agent/assignments/{assignment}",
            headers={
                "X-Agent-API-Key": pm_key,
                "Idempotency-Key": key,
                "X-Agent-Rationale": reason,
                "X-Correlation-ID": key,
            },
            json=body,
        )
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
            headers={"X-Agent-API-Key": pm_key, "Accept": "application/json, text/event-stream"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "agent_update_assignment",
                    "arguments": {
                        "assignment_id": assignment,
                        "payload": body,
                        "idempotency_key": key,
                        "rationale": reason,
                        "correlation_id": key,
                    },
                },
            },
        )
        result = response.json()["result"]
        assert not result["isError"], result
        return json.loads(result["content"][0]["text"])



def advance_server_clock_past(monkeypatch, instant):
    """Move the server's UTC clock just past ``instant`` without waiting.

    Every lease and window decision reads ``app.utils.time.utc_now``, which
    resolves ``datetime`` from its module at call time, so shifting that one
    name moves the whole server forward while monotonic timers stay real.
    """
    delay = max(instant - datetime.now(timezone.utc), timedelta(0)) + timedelta(milliseconds=120)

    class ShiftedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.now(tz) + delay

    monkeypatch.setattr(server_time, "datetime", ShiftedDatetime)


async def reacknowledge(factory, worker, key, *, extra_feature=None):
    """Refresh the worker runtime so that it adopts the planning-window feature."""
    from app.agent_contract import EXECUTION_PLANNING_WINDOW_FEATURE
    from app.models.agent import AgentTeamTopologyMember
    from app.schemas.agent_team_setup import AgentTeamRuntimeAcknowledgement
    from app.services.agent_team_setup_service import AgentTeamSetupService

    async with factory() as session:
        roster = await session.scalar(
            select(AgentTeamTopologyMember).where(AgentTeamTopologyMember.actor_id == worker.id)
        )
        acknowledgement = json.loads(roster.runtime_acknowledgement_payload)
        assert EXECUTION_PLANNING_WINDOW_FEATURE not in acknowledgement["server_features"]
        acknowledgement["server_features"].append(EXECUTION_PLANNING_WINDOW_FEATURE)
        if extra_feature:
            acknowledgement["server_features"].append(extra_feature)
        prior_digest = roster.runtime_acknowledgement_digest
        acknowledgement["expected_previous_acknowledgement_digest"] = prior_digest
        renewed = await AgentTeamSetupService(session).acknowledge_runtime(
            key, AgentTeamRuntimeAcknowledgement.model_validate(acknowledgement)
        )
        assert renewed.acknowledgement_digest != prior_digest and renewed.topology_runtime_ready


async def report_under_window(call, factory, lane, task, current, running, worker, wk, pk, retained):
    """Report, renew and end live work while a sealed forward planning window is in force."""
    from app.services.execution_planning_window import current_window

    renew = ("agent_renew_my_work", "/api/agent/me/work/renew")
    submit = ("agent_submit_my_work", "/api/agent/me/work/submit")
    fail = ("agent_fail_my_work", "/api/agent/me/work/fail")
    claim = {"claim_id": running["claim_id"], "claim_generation": running["claim_generation"]}
    live = {**fence(running), "expected_task_version": current.version}
    handback = {
        **live,
        "observed_model": retained["observed_model"],
        "output_state": "retained",
        "status": "failed",
        "summary": "Hand back the retained draft notes",
        "evidence": {"artifact": "the retained draft notes"},
    }

    async def observe():
        async with factory() as read:
            saved = await read.get(Task, task.id)
            run = await read.get(AgentRun, running["run"]["id"])
            return saved, current_window(saved), run.status

    if lane in {"checkpoint", "progress", "blocker"}:
        body = {
            "checkpoint": {"output_state": "retained", "note": "Draft notes saved"},
            "progress": {"completed": "first half of the notes"},
            "blocker": {"blocker": "Waiting for the release owner to confirm the notes"},
        }[lane]
        event = await call(
            "agent_append_task_event",
            f"/api/agent/tasks/{task.id}/events",
            wk,
            task_id=task.id,
            payload={"event_type": f"agent.{lane}", "payload": body, **claim},
            receipt=f"{lane}-under-window",
        )
        assert event["event_type"] == f"agent.{lane}"
    if lane.startswith("reacknowledged"):
        await reacknowledge(
            factory,
            worker,
            wk,
            extra_feature="unrelated-server-feature-v1" if lane == "reacknowledged_other" else None,
        )
    saved, window, status = await observe()
    assert saved.version == current.version and status == "running"
    if lane in {"checkpoint", "progress", "reacknowledged"}:
        # The report or feature-only acknowledgement leaves the window and run in force.
        assert window == current.execution_planning_window
        renewed = await call(*renew, wk, payload=live, receipt=f"renew-after-{lane}")
        # Renewal re-anchors the original assignment at a newly reserved
        # version, so the window has done its job and is no longer current.
        assert renewed["run"]["id"] == running["run"]["id"]
        assert renewed["assignment"]["task_version"] == renewed["task"]["version"] == current.version + 1
        saved, window, status = await observe()
        assert window is None and status == "running" and saved.claim_id
        done = await call(*submit, wk, payload={**fence(renewed), **retained}, receipt=f"submit-after-{lane}")
        assert done["run"]["id"] == running["run"]["id"] and done["run"]["status"] == "succeeded"
        assert done["task"]["status"] == "resolved"
        return
    if lane == "fail":
        assert window == current.execution_planning_window
        ended = await call(*fail, wk, payload=handback, receipt="retain-under-window")
        assert ended["recovery_required"] and ended["run"]["id"] == running["run"]["id"]
        assert ended["run"]["status"] == "failed" and ended["assignment"]["state"] == "cancelled"
        saved, window, status = await observe()
        # Failure reserves a new version, which deliberately ends the window.
        assert status == "failed" and saved.version > current.version and window is None
        assert not saved.claim_id
        (item,) = (await call("agent_list_recovery_tasks", "/api/agent/recovery", pk))["items"]
        assert item["task"]["id"] == task.id
        return
    if lane == "blocker":
        # The worker's own blocker changes the task state the window was sealed
        # against. The task is visibly blocked, and the PM resolves it.
        assert window is None and saved.blocked_reason
        expected_error = "scope changed"
    else:
        # Any acknowledgement change beyond adopting the planning-window feature
        # ends the window's authority. The PM must recover the work.
        assert window == current.execution_planning_window
        expected_error = "no longer matches current ownership"
    await call(*renew, wk, payload=live, receipt=f"renew-after-{lane}", error=expected_error)
    await call(*fail, wk, payload=handback, receipt=f"retain-after-{lane}", error=expected_error)
    saved, _, status = await observe()
    assert status == "running" and saved.version == current.version and saved.claim_id
    if lane == "reacknowledged_other":
        (item,) = (await call("agent_list_recovery_tasks", "/api/agent/recovery", pk))["items"]
        assert item["task"]["id"] == task.id and item["recovery_codes"], item


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
        "legacy_unconfirmable",
        "legacy_no_checkpoint",
        "queued_normal",
        "queued_recovery",
        "legacy_queued_normal",
        "legacy_queued_recovery",
        "checkpoint",
        "progress",
        "fail",
        "blocker",
        "reacknowledged",
        "reacknowledged_other",
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
    recovered_original = lane in {"recovered_rework", "queued_recovery"}
    post_expiry = lane in {"drained", "unconfirmable", "no_checkpoint"}
    if lane == "recovered_rework":
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
        running = (
            None
            if lane in {"queued_normal", "queued_recovery"}
            else await call(
                *begin,
                wk,
                payload={
                    "assignment_id": assigned["id"],
                    "queue_revision": queue["queue_revision"],
                    "lease_seconds": 60 if post_expiry else 3600,
                    "model": member.default_model_binding_key,
                },
                receipt="begin-notes",
            )
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
            if case == "running":
                evidence = current.execution_planning_window["evidence"]
                assert set(evidence) == {
                    "iteration_id",
                    "previous_end",
                    "new_end",
                    "snapshot_id",
                    "snapshot_sha256",
                    "input_revision",
                }
                saved = await read.get(ApplicationSnapshot, evidence["snapshot_id"])
                assert (saved.checksum, saved.input_revision, saved.iteration_id) == (
                    evidence["snapshot_sha256"],
                    revision,
                    iteration.id,
                )
                assert len(json.dumps(evidence).encode()) < 512
                event = await read.scalar(
                    select(TaskEvent).where(
                        TaskEvent.task_id == task.id, TaskEvent.event_type == "task.execution_planning_window"
                    )
                )
                event_payload = json.loads(event.payload)
                assert {key: event_payload[key] for key in evidence} == evidence and len(
                    event.payload.encode()
                ) < 1024
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
            if post_expiry:
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
                    "pr_url": origin + "/pull/7/",
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
                        "payload": {
                            **mark,
                            "pr_url": {"foreign": "value"}
                            if transport == "rest"
                            else "https://example.invalid/notes/pull/1",
                        }
                        if lane == "no_checkpoint"
                        else mark,
                        "claim_id": running["claim_id"],
                        "claim_generation": running["claim_generation"],
                    },
                )
                assert checkpoint.status_code == 200, checkpoint.text
                expiry = datetime.fromisoformat(running["claim_expires_at"].replace("Z", "+00:00"))
                advance_server_clock_past(monkeypatch, expiry)
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
                    "pr_url": origin + "/pull/7",
                    "terminal_native_turn": mark["terminal_native_turn"],
                    "confirmed_final_output": True,
                }
                replacement_id = recovery["assignment"]["id"]
                before = (
                    await measured_pending_polls(call, work, wk, db, record_property)
                    if lane == "drained"
                    else await call(*work, wk)
                )
                old_etag = (await http.get("/api/agent/me/work", headers={"X-Agent-API-Key": wk})).headers[
                    "etag"
                ]
                if lane == "no_checkpoint":
                    context = await call(
                        "agent_get_complete_task_context",
                        f"/api/agent/tasks/{task.id}/context",
                        wk,
                        task_id=task.id,
                    )
                    assert (
                        context["start_ready"]
                        and "retained_output_attestation_required" not in context["blocker_codes"]
                    )
                    assert (
                        before["state"] == "start_assigned"
                        and before["next"]["assignment"]["id"] == replacement_id
                    )
                    assert (
                        "retained_output_attestation" not in before["next"]["assignment"]["routing_snapshot"]
                    )
                    fresh = await call(
                        *begin,
                        wk,
                        payload={
                            "assignment_id": replacement_id,
                            "queue_revision": before["queue_revision"],
                            "model": member.default_model_binding_key,
                        },
                        receipt="begin-normal-recovery",
                    )
                    assert (
                        fresh["run"]["id"] != running["run"]["id"]
                        and fresh["claim_generation"] > running["claim_generation"]
                    )
                    record_property("no_usable_checkpoint_accepted_ordinary_begin", True)
                    return
                (blocked,) = before["blocked_assigned"]
                assert before["state"] == "attention_required" and before["recovery_codes"] == [
                    "retained_output_attestation_required"
                ]
                assert (
                    blocked["assignment"]["id"] == replacement_id
                    and "retained_output_attestation_required" in blocked["blocker_codes"]
                )
                hint = blocked["assignment"]["routing_snapshot"]["retained_output_attestation"]
                assert (
                    hint["tool"] == "agent_attest_retained_planning_output"
                    and hint["checkpoint_id"] == body["checkpoint_id"]
                )
                assert (hint["run_id"], hint["assignment_id"], hint["claim_generation"]) == (
                    running["run"]["id"],
                    assigned["id"],
                    running["claim_generation"],
                )
                assert hint["commit_url"] == body["commit_url"] and hint["git_tree"] == body["git_tree"]
                assert hint["pr_url"] == body["pr_url"] and hint["pr_url"] != mark["pr_url"]
                assert (
                    "claim_id" not in hint
                    and "claim_sha256" not in hint
                    and running["claim_id"] not in json.dumps(hint)
                )
                assert (
                    "terminal_native_turn" not in hint
                    and "saved begin or renew response" in hint["private_fence_source"]
                )
                context = await call(
                    "agent_get_complete_task_context",
                    f"/api/agent/tasks/{task.id}/context",
                    wk,
                    task_id=task.id,
                )
                assert (
                    not context["start_ready"]
                    and context["assignment"]["routing_snapshot"]["retained_output_attestation"] == hint
                )
                from app.services import planning_window_reconciliation as planning

                with patch.object(
                    planning, "_canonical_snapshot_checksum", wraps=planning._canonical_snapshot_checksum
                ) as locked_checksum:
                    await call(
                        *begin,
                        wk,
                        payload={
                            "assignment_id": replacement_id,
                            "queue_revision": before["queue_revision"],
                            "model": member.default_model_binding_key,
                        },
                        receipt="ordinary-begin-held",
                        error="retained_output_attestation_required",
                    )
                    assert locked_checksum.call_count == 1
                    record_property("locked_begin_verified_current_snapshot", True)
                async with db_session_factory() as check:
                    assert not await check.scalar(
                        select(AgentRun.id).where(AgentRun.assignment_id == replacement_id)
                    )
                    assert not (await check.get(Task, task.id)).claim_id
                record_property("ordinary_begin_refused_before_attestation", True)
                if lane == "unconfirmable":
                    separate = await task_factory(
                        iteration=iteration,
                        assignee=scope.member,
                        title="Independent release note",
                        description=task.description,
                        tags=task.tags,
                        status="planned",
                        start_date=task.start_date,
                        end_date=task.end_date,
                        effort_days=1,
                        priority=2,
                    )
                    separate.project_id = project.id
                    separate.effort_hours = 8
                    await db.commit()
                    separate_assignment = await call(
                        *dispatch,
                        pk,
                        payload={
                            "actor_id": worker.id,
                            "task_id": separate.id,
                            "expected_task_version": separate.version,
                            "reviewer_profile_id": reviewer.profile_id,
                        },
                        receipt="assign-unrelated",
                    )
                    available = await call(*work, wk)
                    assert (
                        available["state"] == "start_assigned"
                        and available["next"]["assignment"]["id"] == separate_assignment["id"]
                    )
                    assert any(i["assignment"]["id"] == replacement_id for i in available["blocked_assigned"])
                    cancellation = await cancel_unconfirmable(
                        http, transport, pk, replacement_id, available["queue_revision"]
                    )
                    assert cancellation["state"] == "cancelled" and "cannot confirm" in cancellation["reason"]
                    left = await call(*work, wk)
                    unrelated = await call(
                        *begin,
                        wk,
                        payload={
                            "assignment_id": separate_assignment["id"],
                            "queue_revision": left["queue_revision"],
                            "model": member.default_model_binding_key,
                        },
                        receipt="start-unrelated",
                    )
                    assert unrelated["run"]["task_id"] == separate.id
                    async with db_session_factory() as check:
                        unchanged = await check.get(AgentRun, running["run"]["id"])
                        assert (
                            unchanged.status,
                            unchanged.ended_at,
                            unchanged.execution_provenance,
                        ) == history
                        assert not await check.scalar(
                            select(AgentIdempotencyRecord.id).where(
                                AgentIdempotencyRecord.operation == "work.attest_retained_planning_output",
                                AgentIdempotencyRecord.target_id == unchanged.id,
                            )
                        )
                    record_property("unconfirmable_task_canceled_unrelated_began", True)
                    return
                other = team.sink.keys[team.manifest.workers[1].actor_key]
                async with db_session_factory() as corrupt:
                    snap = await corrupt.scalar(
                        select(ApplicationSnapshot).where(
                            ApplicationSnapshot.iteration_id == iteration.id,
                            ApplicationSnapshot.input_revision == revision,
                        )
                    )
                    saved_payload = deepcopy(snap.payload)
                    snap.payload = {**saved_payload, "content_integrity_control": "other bytes"}
                    await corrupt.commit()
                unproved = await call(*work, wk)
                assert (
                    unproved["state"] == "start_assigned"
                    and "retained_output_attestation"
                    not in unproved["next"]["assignment"]["routing_snapshot"]
                )
                await worker_attest(
                    http,
                    transport,
                    wk,
                    running["run"]["id"],
                    body,
                    "uncorroborated-snapshot",
                    error="planning_matching_iteration_cutoff",
                )
                async with db_session_factory() as restored:
                    restored_snapshot = await restored.get(ApplicationSnapshot, snap.id)
                    restored_snapshot.payload = saved_payload
                    await restored.commit()
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
                await worker_attest(
                    http,
                    transport,
                    wk,
                    running["run"]["id"],
                    {**body, "pr_url": "https://example.invalid/notes/pull/1"},
                    "invalid-pr",
                    error="checkpoint_receipt_or_repository",
                )
                await worker_attest(
                    http,
                    transport,
                    wk,
                    running["run"]["id"],
                    {**body, "pr_url": origin + "/pull/8"},
                    "wrong-valid-pull",
                    error="checkpoint_receipt_or_repository",
                )
                await worker_attest(
                    http,
                    transport,
                    wk,
                    running["run"]["id"],
                    {**body, "commit_url": "not-a-github-commit"},
                    "invalid-commit",
                    error="checkpoint_receipt_or_repository",
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
                refreshed = await http.get(
                    "/api/agent/me/work", headers={"X-Agent-API-Key": wk, "If-None-Match": old_etag}
                )
                assert (
                    refreshed.status_code == 200
                    and refreshed.headers["etag"] != old_etag
                    and refreshed.json()["state"] == "start_assigned"
                )
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
                patch("app.services.execution_planning_window.seal_authority", side_effect=observe_locks)
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
        elif lane in {"checkpoint", "progress", "fail", "blocker", "reacknowledged", "reacknowledged_other"}:
            await report_under_window(
                call, db_session_factory, lane, task, current, running, worker, wk, pk, retained
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
            if lane == "rework":
                assert (
                    next_run["run"]["execution_provenance"]["supervised_rework"]["reviewer_profile_id"]
                    == reviewer.profile_id
                )
            if recovered_original and lane == "rework":
                lineage = next_run["run"]["execution_provenance"]["supervised_rework"]
                assert (
                    lineage["contributor_count"] == 2
                    and lineage["source_recovery"]["assignment_id"] == assigned["id"]
                )
            assert next_run["assignment"]["task_version"] == next_run["task"]["version"] > current.version
            renewed = await call(
                "agent_renew_my_work",
                "/api/agent/me/work/renew",
                wk,
                payload=fence(next_run),
                receipt="renew-correction",
            )
            assert renewed["assignment"]["task_version"] == renewed["task"]["version"]
            delivered = await call(
                *submit, wk, payload={**fence(renewed), **retained}, receipt="deliver-correction"
            )
            assert (
                delivered["run"]["status"] == "succeeded" and delivered["run"]["id"] == next_run["run"]["id"]
            )
            review = await call(
                *dispatch,
                pk,
                payload={
                    "actor_id": reviewer.id,
                    "task_id": task.id,
                    "purpose": "verification",
                    "reviewer_profile_id": reviewer.profile_id,
                    "expected_task_version": delivered["task"]["version"],
                },
                receipt="verify-completed-window",
            )
            expected = {next_run["run"]["id"]: worker.id}
            if running:
                expected[running["run"]["id"]] = worker.id
            if recovered_original:
                expected[previous["run"]["id"]] = earlier_actor.id
            selection = review["review_selection"]
            assert len(selection["contributors"]) == len(expected)
            assert {r["run_id"]: r["actor_id"] for r in selection["contributors"]} == expected
            assert {r["publisher_key"] for r in selection["contributors"]} == {"first-publisher"}
            assert selection["reviewer"]["publisher_key"] == "second-publisher"
            decision = await call(
                *verdict,
                rk,
                payload={
                    "assignment_id": review["id"],
                    "verdict": "pass",
                    "reason": "Verified the submitted notes and each recorded contributor",
                    "observed_model": verifier.default_model_binding_key,
                    "reviewed_candidate_digest": selection["candidate"]["digest"],
                    "expected_task_version": delivered["task"]["version"],
                    "evidence": {"criteria": "complete"},
                },
                receipt="accept-completed-window",
            )
            assert decision["task"]["status"] == "closed"
            record_property("closed_after_window_renew_submit_review", len(expected))
