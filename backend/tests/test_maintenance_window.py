"""A coordinated maintenance window protects only the live claims whose owners acknowledged it."""

from datetime import date, timedelta

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.config import get_settings
from app.models.agent import AgentActor, AgentTaskAssignment
from app.models.identity import Principal, WorkspaceAuthorityState
from app.models.maintenance import MaintenanceWindow
from app.models.task import Task
from app.services import agent_work_service, backlog_snapshot_service, work_metrics
from app.services.agent_service import hash_api_key
from app.services.upgrade_service import alembic_config
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_schedule_follows_actual_dates import NOW, _client, _headers, _seed

OPERATOR_KEY = "maintenance-window-operator-fixture"
PM_KEY = "maintenance-window-pm-fixture"
OPERATOR = {"X-Admin-API-Key": OPERATOR_KEY}
PM = {"X-Agent-API-Key": PM_KEY}


@pytest.fixture
def clock(monkeypatch):
    """A clock the test moves forward explicitly; nothing advances by itself."""
    from app.utils import time

    state = {"now": NOW}
    real_utc_now = time.utc_now
    monkeypatch.setattr(backlog_snapshot_service, "utc_now", real_utc_now)
    for module in (agent_work_service, work_metrics, time):
        monkeypatch.setattr(module, "utc_now", lambda: state["now"])

    def advance(seconds):
        state["now"] = state["now"] + timedelta(seconds=seconds)
        return state["now"]

    return advance


@pytest.fixture
def operator_key(monkeypatch):
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", OPERATOR_KEY)
    get_settings.cache_clear()
    yield
    monkeypatch.delenv("WORKCHORD_ADMIN_API_KEY")
    get_settings.cache_clear()


async def _store(factory, scenario, tasks=("first",)):
    plan = {key: (date(2026, 1, 20), date(2026, 1, 20), (), 1, True) for key in tasks}
    ids = await _seed(factory, scenario, plan)
    async with factory() as db:
        operator = Principal(kind="system", display_name="Operator API")
        db.add(operator)
        await db.flush()
        db.add(WorkspaceAuthorityState(id=1, operator_principal_id=operator.id))
        pm = AgentActor(name="delivery-pm", display_name="Delivery PM", role="pm",
                        api_key_hash=hash_api_key(PM_KEY), scopes='["planning:read"]')
        db.add(pm)
        # The second scenario actor stands in for a legacy client that claims tasks and starts runs directly.
        (await db.get(AgentActor, scenario.actors[1])).scopes = '["tasks:read", "tasks:write", "runs:write"]'
        await db.commit()
        assignments = {
            key: (await db.scalars(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == task_id))).one()
            for key, task_id in ids.items()
        }
        return ids, assignments, pm.id


def _window_body(**overrides):
    body = {
        "release_label": "same-database upgrade",
        "reason": "Apply a reviewed release against the shared database.",
        "planned_start_at": (NOW + timedelta(minutes=5)).isoformat(),
        "planned_end_at": (NOW + timedelta(hours=2)).isoformat(),
        "max_outage_seconds": 300,
        "expiry_margin_seconds": 600,
    }
    return {**body, **overrides}


async def _begin_work(client, scenario, assignment_id, key, lease_seconds):
    decision = (await client.get("/api/agent/me/work", headers=_headers(scenario, f"{key}-poll"))).json()
    begun = await client.post("/api/agent/me/work/begin", headers=_headers(scenario, key), json={
        "assignment_id": assignment_id, "queue_revision": decision["queue_revision"],
        "lease_seconds": lease_seconds,
    })
    return begun


async def _renew(client, scenario, receipt, key, lease_seconds):
    renewed = await client.post("/api/agent/me/work/renew", headers=_headers(scenario, key), json={
        "assignment_id": receipt["assignment"]["id"], "run_id": receipt["run"]["id"],
        "claim_id": receipt["claim_id"], "claim_generation": receipt["claim_generation"],
        "expected_task_version": receipt["task"]["version"], "lease_seconds": lease_seconds,
    })
    assert renewed.status_code == 200, renewed.text
    return renewed.json()


def _codes(response):
    return sorted({blocker["code"] for blocker in response.json()["detail"]["blockers"]})


async def test_an_acknowledged_worker_renews_and_finishes_across_the_window(delivery_store, clock, operator_key):
    factory, scenario, _ = delivery_store
    ids, assignments, pm_id = await _store(factory, scenario, tasks=("first", "second"))
    async with _client() as client:
        begun = await _begin_work(client, scenario, assignments["first"], "begin-first", 600)
        assert begun.status_code == 200, begun.text
        receipt = begun.json()
        generation = receipt["claim_generation"]

        announced = await client.post("/api/maintenance-windows", headers=OPERATOR, json=_window_body())
        assert announced.status_code == 201, announced.text
        window = announced.json()
        assert window["state"] == "announced" and window["minimum_lease_seconds"] == 900
        assert (await client.post("/api/maintenance-windows", headers=OPERATOR, json=_window_body())).status_code == 409

        # Admission is closed: no new start, through any start path.
        refused = await _begin_work(client, scenario, assignments["second"], "begin-second", 600)
        assert refused.status_code == 409, refused.text
        assert refused.json()["detail"]["code"] == "maintenance_window_admission_closed"
        legacy = {"X-Agent-API-Key": scenario.actor_keys[1], "Idempotency-Key": "legacy-start"}
        for path, body in ((f"/api/agent/tasks/{scenario.tasks['planned']}/claim", {"lease_seconds": 600}),
                           ("/api/agent/runs", {"task_id": scenario.tasks["planned"]})):
            legacy_start = await client.post(path, headers=legacy, json=body)
            assert legacy_start.status_code == 409, legacy_start.text
            assert legacy_start.json()["detail"]["code"] == "maintenance_window_admission_closed"

        early = await client.post(f"/api/maintenance-windows/{window['id']}/begin", headers=OPERATOR)
        assert early.status_code == 409
        assert _codes(early) == ["owner_acknowledgement_missing", "pm_notice_missing", "window_not_started"]

        mine = (await client.get("/api/agent/me/maintenance-windows/current",
                                 headers=_headers(scenario, "read"))).json()
        assert mine["window"]["id"] == window["id"]
        assert [(c["task_id"], c["claim_generation"], c["acknowledged"]) for c in mine["my_live_claims"]] == [
            (ids["first"], generation, False)]

        ack_body = {"task_id": ids["first"], "claim_id": receipt["claim_id"],
                    "claim_generation": generation, "run_id": receipt["run"]["id"]}
        acked = await client.post(f"/api/agent/me/maintenance-windows/{window['id']}/acknowledge",
                                  headers=_headers(scenario, "ack"), json=ack_body)
        assert acked.status_code == 200, acked.text
        assert acked.json()["minimum_lease_seconds"] == 900
        again = await client.post(f"/api/agent/me/maintenance-windows/{window['id']}/acknowledge",
                                  headers=_headers(scenario, "ack"), json=ack_body)
        assert again.json()["receipt"]["id"] == acked.json()["receipt"]["id"]
        noticed = await client.post(f"/api/agent/me/maintenance-windows/{window['id']}/notice-receipt", headers=PM)
        assert noticed.status_code == 200, noticed.text
        assert noticed.json()["receipt"]["actor_id"] == pm_id

        # The lease must outlive the bounded outage plus the margin.
        clock(301)
        short = await client.post(f"/api/maintenance-windows/{window['id']}/begin", headers=OPERATOR)
        assert short.status_code == 409
        assert _codes(short) == ["lease_margin_insufficient"]
        receipt = await _renew(client, scenario, receipt, "renew-before", 1800)

        started = await client.post(f"/api/maintenance-windows/{window['id']}/begin", headers=OPERATOR)
        assert started.status_code == 200, started.text
        started = started.json()
        assert started["state"] == "in_progress" and started["started_at"] == clock(0).isoformat()
        assert [(c["task_id"], c["actor_id"], c["claim_generation"], c["run_id"])
                for c in started["protected_claims"]] == [
            (ids["first"], scenario.actors[0], generation, receipt["run"]["id"])]

        # The restart happens here. The protected worker keeps renewing on the same generation.
        clock(240)
        receipt = await _renew(client, scenario, receipt, "renew-during", 1800)
        assert receipt["claim_generation"] == generation
        still_closed = await _begin_work(client, scenario, assignments["second"], "begin-second-during", 600)
        assert still_closed.json()["detail"]["code"] == "maintenance_window_admission_closed"

        closed = await client.post(f"/api/maintenance-windows/{window['id']}/complete", headers=OPERATOR,
                                   json={"outcome": "completed", "note": "Restart took four minutes."})
        assert closed.status_code == 200, closed.text
        closed = closed.json()
        assert closed["state"] == "completed" and closed["ended_at"] == clock(0).isoformat()
        assert [(c["task_id"], c["claim_generation"], c["state"]) for c in closed["resumption"]["claims"]] == [
            (ids["first"], generation, "preserved")]
        assert closed["resumption"]["unprotected_live_claims"] == []

        receipt = await _renew(client, scenario, receipt, "renew-after", 600)
        submitted = await client.post("/api/agent/me/work/submit", headers=_headers(scenario, "submit"), json=dict(
            assignment_id=receipt["assignment"]["id"], run_id=receipt["run"]["id"], claim_id=receipt["claim_id"],
            claim_generation=generation, expected_task_version=receipt["task"]["version"],
            summary="Implemented result", evidence={"inspection": "Worker observation"},
            criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed",
                                     evidence="Artifact inspected")],
        ))
        assert submitted.status_code == 200, submitted.text
        assert submitted.json()["task"]["status"] == "resolved"

    async with factory() as db:
        assert (await db.get(Task, ids["first"])).claim_generation == generation


async def test_a_long_lease_and_a_quiet_worker_are_not_consent(delivery_store, clock, operator_key):
    factory, scenario, _ = delivery_store
    ids, assignments, pm_id = await _store(factory, scenario)
    async with _client() as client:
        begun = await _begin_work(client, scenario, assignments["first"], "begin", 86400)
        assert begun.status_code == 200, begun.text
        receipt = begun.json()
        window = (await client.post("/api/maintenance-windows", headers=OPERATOR, json=_window_body())).json()

        # An out-of-band notice reaches only a PM, and never admits a claim.
        worker_notice = await client.post(f"/api/maintenance-windows/{window['id']}/notices", headers=OPERATOR,
                                          json={"actor_id": scenario.actors[0], "channel": "email",
                                                "reference": "change-123"})
        assert worker_notice.status_code == 400
        pm_notice = await client.post(f"/api/maintenance-windows/{window['id']}/notices", headers=OPERATOR,
                                      json={"actor_id": pm_id, "channel": "email", "reference": "change-123"})
        assert pm_notice.status_code == 200, pm_notice.text

        # Another actor cannot acknowledge for the owner, even holding the fence.
        foreign = await client.post(
            f"/api/agent/me/maintenance-windows/{window['id']}/acknowledge",
            headers={"X-Agent-API-Key": scenario.actor_keys[1]},
            json={"task_id": ids["first"], "claim_id": receipt["claim_id"],
                  "claim_generation": receipt["claim_generation"]},
        )
        assert foreign.status_code == 409
        assert foreign.json()["detail"]["code"] == "maintenance_claim_not_live"
        # A non-operator cannot run the window.
        assert (await client.post(f"/api/maintenance-windows/{window['id']}/begin",
                                  headers=PM)).status_code == 403

        # An hour without any worker traffic, inside the planned window, on a lease good for a day.
        clock(3600)
        refused = await client.post(f"/api/maintenance-windows/{window['id']}/begin", headers=OPERATOR)
        assert refused.status_code == 409
        detail = refused.json()["detail"]
        assert detail["code"] == "maintenance_window_not_ready"
        assert detail["blockers"] == [{
            "code": "owner_acknowledgement_missing", "task_id": ids["first"], "actor_id": scenario.actors[0],
            "claim_generation": receipt["claim_generation"], "run_id": receipt["run"]["id"],
        }]
        status = (await client.get(f"/api/maintenance-windows/{window['id']}", headers=OPERATOR)).json()
        assert status["state"] == "announced" and status["started_at"] is None
        assert status["readiness"]["ready"] is False

        canceled = await client.post(f"/api/maintenance-windows/{window['id']}/cancel", headers=OPERATOR,
                                     json={"note": "Owner did not confirm."})
        assert canceled.json()["state"] == "canceled" and canceled.json()["outcome"] == "canceled"
        assert (await client.get("/api/agent/me/maintenance-windows/current",
                                 headers=_headers(scenario, "read"))).json()["window"] is None


async def test_an_expired_lease_on_a_running_run_blocks_the_window(delivery_store, clock, operator_key):
    factory, scenario, _ = delivery_store
    ids, assignments, pm_id = await _store(factory, scenario)
    async with _client() as client:
        receipt = (await _begin_work(client, scenario, assignments["first"], "begin", 60)).json()
        window = (await client.post("/api/maintenance-windows", headers=OPERATOR, json=_window_body())).json()
        await client.post(f"/api/agent/me/maintenance-windows/{window['id']}/notice-receipt", headers=PM)
        clock(400)
        # The claim expired, so its owner can no longer acknowledge it; the stale run needs recovery first.
        late = await client.post(
            f"/api/agent/me/maintenance-windows/{window['id']}/acknowledge", headers=_headers(scenario, "ack"),
            json={"task_id": ids["first"], "claim_id": receipt["claim_id"],
                  "claim_generation": receipt["claim_generation"]},
        )
        assert late.json()["detail"]["code"] == "maintenance_claim_not_live"
        refused = await client.post(f"/api/maintenance-windows/{window['id']}/begin", headers=OPERATOR)
        assert refused.status_code == 409
        assert _codes(refused) == ["running_run_without_live_claim"]


@pytest.mark.sqlite
def test_downgrade_refuses_an_open_window(tmp_path, configure_database):
    path = tmp_path / "workchord_test_maintenance_window.db"
    configure_database(f"sqlite+aiosqlite:///{path}")
    engine = create_engine(f"sqlite:///{path}")
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, "20261124_0021")
            table = MaintenanceWindow.__table__
            db.execute(table.insert().values(
                state="announced", active_slot=1, release_label="release", reason="upgrade",
                planned_start_at=NOW, planned_end_at=NOW + timedelta(hours=1), max_outage_seconds=60,
                expiry_margin_seconds=600, announced_at=NOW,
            ))
            db.commit()
            with pytest.raises(RuntimeError, match="open maintenance window"):
                command.downgrade(config, "20261121_0020")
            db.rollback()
            db.execute(table.update().values(state="canceled", active_slot=None, outcome="canceled"))
            db.commit()
            command.downgrade(config, "20261121_0020")
            assert not inspect(db).has_table("maintenance_windows")
            db.commit()
    finally:
        engine.dispose()
