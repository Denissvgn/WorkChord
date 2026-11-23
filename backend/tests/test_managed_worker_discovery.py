"""Managed discovery attribution, scope and transaction boundaries for assigned workers."""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, nullcontext
from dataclasses import dataclass

import httpx
import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.authority import Authority, AuthorityError
from app.commands import command_transaction, current_command
from app.config import get_settings
from app.main import app
from app.models.agent import AgentActor, AgentIdempotencyRecord, TaskEvent
from app.models.identity import CommandAudit, Principal, ProjectMembership, WorkspaceMembership
from app.models.task import Task
from app.models.triage import TriageItem
from app.schemas.agent import AgentDiscoveryTriageCreate
from app.services.agent_work_service import AgentWorkService
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.triage_service import TriageService
from tests.test_agent_discovery_report import (
    WORKER_SCOPES,
    begin_as_worker,
    discovery_body,
    frozen_working_day,
)
from tests.test_delivery_scenarios import delivery_store


@pytest.fixture(autouse=True)
def reset_cached_settings():
    yield
    get_settings.cache_clear()


@dataclass
class AssignedWorker:
    factory: async_sessionmaker[AsyncSession]
    client: httpx.AsyncClient
    headers: dict[str, str]
    begun: dict
    actor_id: int
    principal_id: int
    other_actor_id: int


@pytest.fixture
async def worker(delivery_store, frozen_working_day, monkeypatch) -> AsyncIterator[AssignedWorker]:
    factory, scenario, _ = delivery_store
    actor_id = scenario.actors[0]
    async with factory() as db:
        operator_id = await initialize_control_plane(db)
        principal = Principal(kind="agent", display_name="Assigned executor", agent_actor_id=actor_id)
        db.add(principal)
        await db.flush()
        principal_id = principal.id
        db.add(ProjectMembership(principal_id=principal_id, project_id=scenario.projects[0], role="executor"))
        await db.commit()

    @asynccontextmanager
    async def provision_assigned_task():
        # Only fixture creation uses the operator. The registered API receives
        # a separate session and authenticates the worker's actual key.
        async with factory() as db:
            db.info["authority"] = Authority(
                operator_id, "system", workspace_role="operator", source="fixture"
            )
            yield db

    with monkeypatch.context() as environment:
        environment.setenv("WORKCHORD_AUTH_MODE", "managed")
        get_settings.cache_clear()
        headers = {"X-Agent-API-Key": scenario.actor_keys[0]}
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            begun = await begin_as_worker(
                provision_assigned_task, scenario, frozen_working_day, client, headers
            )
            assert begun["assignment"]["actor_id"] == actor_id
            assert begun["assignment"]["state"] == "accepted"
            async with factory() as db:
                actor = await db.get(AgentActor, actor_id)
                caller = await IdentityService(db).actor_context(actor, source="agent_rest")
                assert caller.principal_id == principal_id and caller.actor_role == "worker"
                assert (
                    caller.scopes == frozenset(WORKER_SCOPES)
                    and caller.projects[scenario.projects[0]] == "executor"
                )
                assert caller.allows(scenario.projects[0], "execute")
                assert not caller.operator and not caller.allows(scenario.projects[0], "create")
            yield AssignedWorker(factory, client, headers, begun, actor_id, principal_id, scenario.actors[1])


async def test_managed_assigned_discovery_replays_once_and_keeps_the_executor_audit(worker):
    body = discovery_body(worker.begun)
    headers = {**worker.headers, "Idempotency-Key": "report-once", "X-Correlation-ID": "assigned-discovery"}
    created = await worker.client.post("/api/agent/discoveries", headers=headers, json=body)
    assert created.status_code == 201, created.text
    repeated = await worker.client.post("/api/agent/discoveries", headers=headers, json=body)
    assert repeated.status_code == 201 and repeated.json() == created.json()

    stale = await worker.client.post(
        "/api/agent/discoveries",
        headers={**headers, "Idempotency-Key": "stale-fence"},
        json={**body, "claim_generation": body["claim_generation"] + 1},
    )
    assert stale.status_code == 409 and "fence" in stale.text.lower(), stale.text
    async with worker.factory() as db:
        item = (await db.scalars(select(TriageItem))).one()
        event = (
            await db.scalars(select(TaskEvent).where(TaskEvent.event_type == "agent.discovery_reported"))
        ).one()
        audit = (
            await db.scalars(select(CommandAudit).where(CommandAudit.action == "triage_items:execute"))
        ).one()
        receipt = (
            await db.scalars(
                select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.operation == "discovery.report")
            )
        ).one()
        task = worker.begun["task"]
        assert item.id == created.json()["id"] and item.source == "agent-discovery"
        assert (item.project_hint_id, item.iteration_hint_id) == (task["project_id"], task["iteration_id"])
        assert (
            item.metadata_json["source_task_id"],
            item.metadata_json["source_assignment_id"],
            item.metadata_json["source_run_id"],
            item.metadata_json["source_actor_id"],
        ) == (task["id"], body["assignment_id"], body["run_id"], worker.actor_id)
        assert (event.task_id, event.actor_id, json.loads(event.payload)["triage_item_id"]) == (
            task["id"],
            worker.actor_id,
            item.id,
        )
        assert (audit.principal_id, audit.project_id, audit.correlation_id) == (
            worker.principal_id,
            task["project_id"],
            "assigned-discovery",
        )
        assert (receipt.actor_id, receipt.target_id, receipt.idempotency_key) == (
            worker.actor_id,
            body["assignment_id"],
            "report-once",
        )


@pytest.mark.parametrize(
    "case", ["matching", "second_item", "wrong_iteration", "different_actor", "missing_scope", "viewer"]
)
async def test_managed_executor_consumes_one_matching_triage_item(worker, case):
    task = worker.begun["task"]
    async with worker.factory() as db:
        actor = await db.get(AgentActor, worker.actor_id)
        if case == "missing_scope":
            actor.scopes = json.dumps([scope for scope in WORKER_SCOPES if scope != "triage:write"])
        elif case == "viewer":
            membership = await db.get(ProjectMembership, (worker.principal_id, task["project_id"]))
            membership.role = "viewer"
        await db.flush()
        authority = await IdentityService(db).actor_context(actor, source="agent_rest")
        assert authority.principal_id == worker.principal_id and authority.actor_id == worker.actor_id
        assert authority.allows(task["project_id"], "execute") == (case != "viewer")
        db.info["authority"] = authority
        first_inserted = False
        expected = pytest.raises(AuthorityError) if case != "matching" else nullcontext()
        with expected:
            async with command_transaction(db):
                announced = {
                    "actor_id": worker.other_actor_id if case == "different_actor" else actor.id,
                    "project_hint_id": task["project_id"],
                    "iteration_hint_id": task["iteration_id"],
                    "remaining": 1,
                }
                db.info["claim_bound_discovery"] = announced
                data = dict(
                    source="agent-discovery",
                    status="new",
                    project_hint_id=task["project_id"],
                    iteration_hint_id=None if case == "wrong_iteration" else task["iteration_id"],
                    labels=[],
                    metadata_json={},
                )
                first = TriageItem(title="Assigned discovery", **data)
                db.add(first)
                await db.flush()
                assert first.id is not None and announced["remaining"] == 0
                first_inserted = True
                if case == "second_item":
                    db.add(TriageItem(title="Another discovery", **data))
                    await db.flush()
        assert "claim_bound_discovery" not in db.info
        assert first_inserted == (case in {"matching", "second_item"})
    async with worker.factory() as db:
        count = await db.scalar(select(func.count()).select_from(TriageItem))
        assert count == (1 if case == "matching" else 0)


class PlannedRollback(Exception):
    pass


@pytest.mark.parametrize("outcome", ["commit", "rollback", "preview"])
async def test_discovery_marker_ends_with_its_command(worker, outcome):
    payload = AgentDiscoveryTriageCreate.model_validate(discovery_body(worker.begun))
    async with worker.factory() as db:
        actor = await db.get(AgentActor, worker.actor_id)
        db.info["authority"] = await IdentityService(db).actor_context(actor, source="agent_rest")
        service = AgentWorkService(db)
        assert current_command(db) is None
        if outcome == "commit":
            # Direct invocation must own its transaction without an HTTP wrapper.
            await service.report_discovery(actor, payload, idempotency_key="one-owner")
        else:
            expected = pytest.raises(PlannedRollback) if outcome == "rollback" else nullcontext()
            with expected:
                async with command_transaction(
                    db, mode="preview" if outcome == "preview" else "apply"
                ) as command:
                    await service.report_discovery(actor, payload, idempotency_key="one-owner")
                    assert current_command(db) is command
                    assert db.info["claim_bound_discovery"]["remaining"] == 0
                    if outcome == "rollback":
                        raise PlannedRollback
        assert current_command(db) is None and "claim_bound_discovery" not in db.info
    async with worker.factory() as db:
        expected_count = int(outcome == "commit")
        assert await db.scalar(select(func.count()).select_from(TriageItem)) == expected_count
        assert (
            await db.scalar(
                select(func.count())
                .select_from(TaskEvent)
                .where(TaskEvent.event_type == "agent.discovery_reported")
            )
            == expected_count
        )


async def test_discovery_and_pm_recovery_lock_the_same_task_until_the_insert_is_flushed(worker, monkeypatch):
    task_id = worker.begun["task"]["id"]
    original_lock, original_create = AgentWorkService._lock_task, TriageService.create
    locked = []
    insertion_checked = []

    async def observe_lock(service, selected):
        command = current_command(service.db)
        assert command is not None
        task = await original_lock(service, selected)
        locked.append((task.id, service.db.sync_session.get_transaction(), command))
        return task

    async def observe_create(service, data, *, commit=True):
        row = await original_create(service, data, commit=commit)
        assert row.id and not commit
        assert locked[-1] == (task_id, service.db.sync_session.get_transaction(), current_command(service.db))
        if service.db.get_bind().dialect.name == "postgresql":
            # A separate connection requests the same row lock without waiting or modifying the task.
            async with worker.factory() as independent:
                with pytest.raises(DBAPIError) as contended:
                    await independent.scalar(
                        select(Task.id).where(Task.id == task_id).with_for_update(nowait=True)
                    )
                assert getattr(contended.value.orig, "sqlstate", None) == "55P03"
        insertion_checked.append(row.id)
        return row

    monkeypatch.setattr(AgentWorkService, "_lock_task", observe_lock)
    monkeypatch.setattr(TriageService, "create", observe_create)
    reported = await worker.client.post(
        "/api/agent/discoveries",
        headers={**worker.headers, "Idempotency-Key": "locked-discovery"},
        json=discovery_body(worker.begun),
    )
    assert reported.status_code == 201, reported.text
    assert insertion_checked == [reported.json()["id"]]

    async with worker.factory() as db:
        pm = await db.scalar(select(AgentActor).where(AgentActor.name == "protocol-pm"))
        pm.scopes = json.dumps([*json.loads(pm.scopes), "planning:read", "planning:write"])
        identity = await IdentityService(db).actor_context(pm)
        db.add(WorkspaceMembership(principal_id=identity.principal_id, role="member"))
        db.add(
            ProjectMembership(
                principal_id=identity.principal_id,
                project_id=worker.begun["task"]["project_id"],
                role="manager",
            )
        )
        await db.commit()
    recovery = await worker.client.post(
        f"/api/agent/recovery/{task_id}/requeue",
        headers={
            "X-Agent-API-Key": "disposable-protocol-pm-key",
            "Idempotency-Key": "inspect-active",
            "X-Agent-Rationale": "Check active assignment ownership",
            "X-Correlation-ID": "recovery-ownership",
        },
        json={
            "actor_id": worker.actor_id,
            "expected_task_version": worker.begun["task"]["version"],
            "expected_claim_generation": worker.begun["claim_generation"],
            "expected_live_assignment_ids": [worker.begun["assignment"]["id"]],
            "expected_running_run_ids": [worker.begun["run"]["id"]],
            "reason": "Check active ownership",
        },
    )
    assert recovery.status_code == 409 and "healthy accepted assignment" in recovery.text, (
        recovery.text,
        [row[0] for row in locked],
    )
    assert [row[0] for row in locked] == [task_id, task_id]
    assert locked[0][1] is not locked[1][1] and locked[0][2] is not locked[1][2]
