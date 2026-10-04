"""Usage provenance, corrections, immutable pricing and permission isolation."""

from datetime import timedelta
from decimal import Decimal

import httpx
import pytest
from sqlalchemy import func, select

from app.main import app
from app.models.agent import AgentActor, AgentRun
from app.models.execution_usage import ExecutionUsageRecord
from app.schemas.execution_usage import ExecutionUsageWrite, UsagePricingBasis
from app.services.agent_service import AgentConflictError, AgentPermissionError
from app.services.execution_usage_service import ExecutionUsageService, estimate_cost
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


async def seed_run(factory, scenario):
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes = '["runs:write","tasks:read","work:execute"]'
        now = utc_now()
        run = AgentRun(task_id=scenario.tasks["planned"], actor_id=actor.id, status="succeeded", started_at=now-timedelta(seconds=10), ended_at=now)
        db.add(run)
        await db.commit()
        return run.id, now


def usage(now, **overrides):
    return ExecutionUsageWrite(report_id="attempt-total", source="disposable-runtime", provenance="simulated", reporting_mode="attempt_total",
        interval_start=now-timedelta(seconds=5), interval_end=now, coverage="partial",
        quantities={"input_tokens": Decimal("10"), "output_tokens": Decimal("0"), "runtime_seconds": None},
        pricing_basis=UsagePricingBasis(currency="USD", unit="input_tokens", price_amount=Decimal("2"), price_quantity=Decimal("10"),
            version="quote-v1", source="declared quote snapshot", quoted_at=now), **overrides)


def test_usage_zero_unknown_and_currency_validation():
    now = utc_now()
    report = usage(now)
    assert report.quantities["output_tokens"] == 0 and report.quantities["runtime_seconds"] is None
    assert estimate_cost(report) == Decimal("2.000000")
    with pytest.raises(ValueError, match="requires its currency"):
        ExecutionUsageWrite(report_id="bad", source="runtime", provenance="simulated", reporting_mode="attempt_total", interval_start=now, interval_end=now,
            coverage="complete", reported_cost=Decimal("1"))
    tiny = report.model_copy(deep=True)
    tiny.pricing_basis.price_amount = Decimal("0.000000000001")
    assert estimate_cost(tiny) == Decimal("0.000000000001")


async def test_usage_replay_correction_and_currency_buckets(delivery_store):
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        service = ExecutionUsageService(db)
        first = await service.write(actor, run_id, usage(now))
        repeated = await service.write(actor, run_id, usage(now))
        assert repeated.id == first.id and repeated.independently_reconciled is False
        different = usage(now).model_copy(update={"quantities": {"input_tokens": Decimal("11")}})
        with pytest.raises(AgentConflictError, match="different content"):
            await service.write(actor, run_id, different)
        actor = await db.get(AgentActor, scenario.actors[0])
        corrected = usage(now).model_copy(update={"report_id": "attempt-correction", "expected_previous_digest": first.digest,
            "reported_cost": Decimal("3"), "currency": "EUR", "coverage": "complete"})
        second = await service.write(actor, run_id, corrected)
        assert second.sequence == 2 and second.previous_digest == first.digest
        summary = await service.summary(project_id=scenario.projects[0], budget_amount=Decimal("5"), budget_currency="EUR")
        assert summary.reported_runs == 1 and summary.unreported_runs == 0
        assert summary.provider_reported_cost == {} and summary.estimated_cost == {}
        assert summary.simulated_reported_cost == {"EUR": Decimal("3")}
        assert summary.simulated_estimated_cost == {"USD": Decimal("2.000000")}
        assert summary.simulated_units["input_tokens"] == 10 and summary.simulated_units["output_tokens"] == 0
        assert summary.simulated_units["runtime_seconds"] is None and summary.measured_report_count == 0
        assert summary.accepted_task_identities == 0 and summary.reports_linked_to_accepted_tasks == 0
        assert summary.simulated_reports == 1 and summary.advisory_budget["advisory_only"]
        assert await db.scalar(select(func.count()).select_from(ExecutionUsageRecord)) == 2
        first_row = await db.get(ExecutionUsageRecord, first.id)
        assert first_row.payload["reported_cost"] is None and first_row.payload["pricing_basis"]["version"] == "quote-v1"


async def test_usage_unknown_without_reports_and_foreign_reporter_is_denied(delivery_store):
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        service = ExecutionUsageService(db)
        summary = await service.summary(project_id=scenario.projects[0])
        assert summary.expected_runs == summary.unreported_runs == 1
        assert summary.provider_reported_cost == {} and summary.estimated_cost == {}
        actor = await db.get(AgentActor, scenario.actors[1])
        actor.scopes = '["runs:write","tasks:read"]'
        await db.commit()
        with pytest.raises(AgentPermissionError):
            await service.write(actor, run_id, usage(now))
        assert await db.scalar(select(func.count()).select_from(ExecutionUsageRecord)) == 0


async def test_usage_rest_mcp_parity_and_readonly_human_summary(delivery_store):
    from app import mcp_agent_tools
    from app.services.identity_service import IdentityService
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    path = f"/api/agent/runs/{run_id}/usage"
    headers = {"X-Agent-API-Key": scenario.actor_keys[0]}
    payload = usage(now).model_dump(mode="json")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        written = await client.post(path, json=payload, headers=headers)
        assert written.status_code == 200, written.text
        rest = await client.get(path, headers=headers)
        assert rest.status_code == 200, rest.text
        async with factory() as db:
            actor = await db.get(AgentActor, scenario.actors[0])
            db.info["authority"] = await IdentityService(db).actor_context(actor, source="mcp")
            mcp = await mcp_agent_tools.get_execution_usage(db, actor, run_id)
        assert rest.json() == mcp == written.json()
        summary = await client.get("/api/tasks/execution-usage", params={"project_id": scenario.projects[0]})
        assert summary.status_code == 200 and summary.json()["reported_runs"] == 1, summary.text


async def test_reported_zero_and_unknown_are_not_repriced_by_live_metadata(delivery_store):
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        data = usage(now).model_copy(update={"provenance": "provider_reported", "coverage": "complete",
            "reported_cost": Decimal("0"), "currency": "EUR"})
        written = await ExecutionUsageService(db).write(actor, run_id, data)
        data.pricing_basis.price_amount = Decimal("99")
        summary = await ExecutionUsageService(db).summary(project_id=scenario.projects[0])
        assert summary.provider_reported_cost == {"EUR": Decimal("0")}
        assert summary.estimated_cost == {"USD": Decimal("2.000000")}
        assert summary.reported_units["runtime_seconds"] is None and summary.measured_report_count == 1
        row = await db.get(ExecutionUsageRecord, written.id)
        row.payload = {**row.payload, "source": "replaced"}
        with pytest.raises(ValueError, match="append-only"):
            await db.commit()


async def test_usage_correction_is_versioned_and_atomic(delivery_store):
    from app.commands import command_transaction
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        first = await ExecutionUsageService(db).write(actor, run_id, usage(now))
        with pytest.raises(AgentConflictError, match="current digest"):
            await ExecutionUsageService(db).write(actor, run_id, usage(now).model_copy(update={"report_id": "wrong-correction"}))
        actor = await db.get(AgentActor, scenario.actors[0])
        with pytest.raises(RuntimeError, match="Abort"):
            async with command_transaction(db):
                await ExecutionUsageService(db).write(actor, run_id, usage(now).model_copy(update={"report_id": "aborted-correction", "expected_previous_digest": first.digest}))
                raise RuntimeError("Abort")
        assert await db.scalar(select(func.count()).select_from(ExecutionUsageRecord)) == 1


async def test_concurrent_usage_corrections_reserve_one_head(delivery_store):
    import asyncio
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        first = await ExecutionUsageService(db).write(actor, run_id, usage(now))

    async def correct(report_id):
        async with factory() as db:
            actor = await db.get(AgentActor, scenario.actors[0])
            try:
                return await ExecutionUsageService(db).write(actor, run_id, usage(now).model_copy(update={"report_id": report_id, "expected_previous_digest": first.digest}))
            except AgentConflictError as exc:
                return exc

    results = await asyncio.gather(correct("correction-a"), correct("correction-b"))
    assert sum(isinstance(result, AgentConflictError) for result in results) == 1
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(ExecutionUsageRecord)) == 2


@pytest.mark.parametrize("effort", [None, Decimal("0"), Decimal("12.5")])
@pytest.mark.parametrize("coverage", ["complete", "partial", "unavailable"])
def test_human_effort_is_a_measurement_for_coverage(effort, coverage):
    now = utc_now()
    payload = dict(report_id="human-only", source="manual-work-log", provenance="manual_reported",
        reporting_mode="attempt_total", interval_start=now, interval_end=now,
        coverage=coverage, reported_human_effort_minutes=effort)
    if coverage == "complete" and effort is None:
        with pytest.raises(ValueError, match="Complete coverage requires"):
            ExecutionUsageWrite(**payload)
    elif coverage == "unavailable" and effort is not None:
        with pytest.raises(ValueError, match="must not contain measured values"):
            ExecutionUsageWrite(**payload)
    else:
        assert ExecutionUsageWrite(**payload).reported_human_effort_minutes == effort


async def test_human_only_usage_summary_preserves_zero_and_unknown(delivery_store):
    factory, scenario, _ = delivery_store
    run_id, now = await seed_run(factory, scenario)
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        report = ExecutionUsageWrite(report_id="human-only", source="manual-work-log", provenance="manual_reported",
            reporting_mode="attempt_total", interval_start=now, interval_end=now,
            coverage="complete", reported_human_effort_minutes=Decimal("0"))
        await ExecutionUsageService(db).write(actor, run_id, report)
        summary = await ExecutionUsageService(db).summary(project_id=scenario.projects[0])
        assert summary.reported_human_effort_minutes == 0 and summary.human_effort_reports == 1
        assert summary.unavailable_reports == 0 and summary.measured_report_count == 1
        assert summary.provider_reported_cost == {} and summary.unknown_cost_reports == 1
