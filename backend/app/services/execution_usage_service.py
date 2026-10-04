"""Bounded usage corrections, immutable pricing and scoped advisory totals."""

from collections import defaultdict
from datetime import timedelta
from decimal import Decimal, localcontext
import hashlib
import json

from sqlalchemy import select, update

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import atomic_command
from app.models.agent import AgentActor, AgentRun
from app.models.delivery_observation import DeliveryObservation
from app.models.execution_usage import ExecutionUsageRecord
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.query_limits import CollectionLimitExceededError
from app.schemas.execution_usage import ExecutionUsageResponse, ExecutionUsageSummary, ExecutionUsageWrite
from app.services.agent_service import AgentConflictError, AgentPermissionError, actor_has_scope
from app.services.delivery_metrics_service import DeliveryMetricsService
from app.utils.time import as_utc, utc_now

MAX_USAGE_REVISIONS = 32
MAX_USAGE_RECORDS = 20_000


def run_identity(run):
    """Distinguish attempts even if a legacy numeric run ID is reused."""
    return hashlib.sha256(json.dumps([run.id, run.actor_id, run.task_id, run.claim_generation,
        as_utc(run.started_at).isoformat()], separators=(",", ":")).encode()).hexdigest()


def estimate_cost(report):
    basis = report.pricing_basis
    if basis is None or report.quantities.get(basis.unit) is None:
        return None
    with localcontext() as context:
        context.prec = 64
        return (report.quantities[basis.unit] * basis.price_amount / basis.price_quantity).quantize(Decimal("0.000000000001"))


def add_exact(bucket, key, amount):
    with localcontext() as context:
        context.prec = 64
        bucket[key] += amount


class ExecutionUsageService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def response(row):
        return ExecutionUsageResponse(id=row.id, original_run_id=row.original_run_id, original_task_id=row.original_task_id,
            sequence=row.sequence, digest=row.digest, previous_digest=row.previous_digest,
            report=ExecutionUsageWrite.model_validate(row.payload), reported_at=row.reported_at)

    async def _run(self, actor, run_id, *, writing=False):
        scopes = ("runs:write", "work:execute", "admin") if writing else ("tasks:read", "runs:write", "work:execute", "planning:read", "admin")
        if not any(actor_has_scope(actor, scope) for scope in scopes):
            raise AgentPermissionError("The actor cannot access execution usage")
        statement = select(AgentRun).where(AgentRun.id == run_id)
        if writing:
            statement = statement.with_for_update()
        run = await self.db.scalar(statement)
        if run is None:
            raise LookupError("Run not found or inaccessible")
        if run.actor_id != actor.id and not actor_has_scope(actor, "admin") and (writing or not actor_has_scope(actor, "planning:read")):
            raise AgentPermissionError("Usage reporting belongs to the execution actor")
        return run

    def _scope(self, row):
        authority = self.db.info.get("authority")
        if row.project_id is None and row.original_project_id is not None and authority is not None and not authority.operator and not authority.local:
            raise AuthorityError("usage_scope_unavailable", "The historical usage scope is unavailable.", 404)
        require_project(self.db, row.project_id)

    async def _history(self, identity):
        # Scope is rechecked before exposing history. A correction must never
        # start a second sequence merely because an older scope is inaccessible.
        with internal_authority(self.db):
            rows = list((await self.db.scalars(select(ExecutionUsageRecord).where(ExecutionUsageRecord.run_identity == identity)
                .order_by(ExecutionUsageRecord.sequence).limit(MAX_USAGE_REVISIONS + 1))).all())
        if len(rows) > MAX_USAGE_REVISIONS:
            raise CollectionLimitExceededError("usage report revisions", MAX_USAGE_REVISIONS)
        if rows:
            self._scope(rows[-1])
        return rows

    async def latest(self, actor, run_id):
        run = await self._run(actor, run_id)
        rows = await self._history(run_identity(run))
        return self.response(rows[-1]) if rows else None

    @atomic_command
    async def write(self, actor, run_id, data: ExecutionUsageWrite):
        hint = await self._run(actor, run_id)
        task = await self.db.scalar(select(Task).where(Task.id == hint.task_id).with_for_update().execution_options(populate_existing=True)) if hint.task_id is not None else None
        if task is None:
            raise LookupError("Run task scope is unavailable")
        # Keep the same Task -> Actor -> Run order as execution commands.
        # SQLite reserves the already-visible task before rechecking ownership.
        with internal_authority(self.db):
            await self.db.execute(update(Task).where(Task.id == task.id).values(id=Task.id, updated_at=Task.updated_at).execution_options(synchronize_session=False))
        fresh_actor = await self.db.scalar(select(AgentActor).where(AgentActor.id == actor.id).with_for_update().execution_options(populate_existing=True))
        if fresh_actor is None or not fresh_actor.enabled:
            raise AgentPermissionError("Usage reporter is disabled or unavailable")
        authority = self.db.info.get("authority")
        if authority is not None and authority.kind == "agent":
            from app.services.identity_service import IdentityService
            self.db.info["authority"] = await IdentityService(self.db).actor_context(fresh_actor, source=authority.source)
        run = await self._run(fresh_actor, run_id, writing=True)
        if run.task_id != task.id:
            raise AgentConflictError("Run task scope changed while reserving usage")
        task = await self.db.scalar(select(Task).where(Task.id == task.id).execution_options(populate_existing=True))
        if task is None:
            raise LookupError("Run task scope is unavailable")
        identity = run_identity(run)
        rows = await self._history(identity)
        payload = data.model_dump(mode="json", exclude={"expected_previous_digest"})
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        prior = next((row for row in rows if row.report_id == data.report_id), None)
        if prior is not None:
            if prior.digest != digest:
                raise AgentConflictError("Usage report ID already records different content")
            return self.response(prior)
        latest = rows[-1] if rows else None
        if data.expected_previous_digest != (latest.digest if latest else None):
            raise AgentConflictError("Usage report changed. Read the current digest before appending a correction")
        if len(rows) >= MAX_USAGE_REVISIONS:
            raise AgentConflictError("Usage report correction limit reached")
        now = utc_now()
        if as_utc(data.interval_start) < as_utc(run.started_at) - timedelta(minutes=5) or as_utc(data.interval_end) > now + timedelta(minutes=5):
            raise ValueError("Usage interval falls outside the attributable attempt window")
        if run.ended_at is not None and as_utc(data.interval_end) > as_utc(run.ended_at) + timedelta(minutes=5):
            raise ValueError("Usage interval extends beyond the terminal attempt")
        row = ExecutionUsageRecord(run_id=run.id, original_run_id=run.id, run_identity=identity, original_task_id=task.id,
            project_id=latest.project_id if latest else task.project_id, iteration_id=latest.iteration_id if latest else task.iteration_id,
            original_project_id=latest.original_project_id if latest else task.project_id,
            original_iteration_id=latest.original_iteration_id if latest else task.iteration_id,
            reporter_actor_id=actor.id if actor.id else None, report_id=data.report_id, sequence=len(rows) + 1,
            digest=digest, previous_digest=latest.digest if latest else None, payload=payload)
        authorization = (row.run_identity, row.report_id, row.sequence, row.digest)
        approved = self.db.info.setdefault("usage_report_authorizations", set())
        approved.add(authorization)
        try:
            self.db.add(row)
            await self.db.flush()
        finally:
            approved.discard(authorization)
        return self.response(row)

    async def summary(self, *, project_id=None, iteration_id=None, lookback_days=30, budget_amount=None, budget_currency=None):
        if not 1 <= lookback_days <= 366:
            raise ValueError("Observation window must be between 1 and 366 elapsed days")
        if project_id is None and iteration_id is None:
            raise ValueError("Select a project or an iteration")
        if project_id is not None:
            require_project(self.db, project_id)
            if await self.db.get(Project, project_id) is None:
                raise LookupError("Project not found or inaccessible")
        if iteration_id is not None and await self.db.get(Iteration, iteration_id) is None:
            raise LookupError("Iteration not found or inaccessible")
        end = utc_now()
        start = end - timedelta(days=lookback_days)
        records = select(ExecutionUsageRecord).where(ExecutionUsageRecord.reported_at >= start, ExecutionUsageRecord.reported_at <= end)
        runs = select(AgentRun).join(Task, Task.id == AgentRun.task_id).where(AgentRun.started_at >= start, AgentRun.started_at <= end)
        outcomes = select(DeliveryObservation.original_task_id).where(DeliveryObservation.kind == "accepted", DeliveryObservation.observed_at >= start, DeliveryObservation.observed_at <= end)
        if project_id is not None:
            records = records.where(ExecutionUsageRecord.project_id == project_id)
            runs = runs.where(Task.project_id == project_id)
            outcomes = outcomes.where(DeliveryObservation.project_id == project_id)
        if iteration_id is not None:
            records = records.where(ExecutionUsageRecord.iteration_id == iteration_id)
            runs = runs.where(Task.iteration_id == iteration_id)
            outcomes = outcomes.where(DeliveryObservation.iteration_id == iteration_id)
        rows = list((await self.db.scalars(records.order_by(ExecutionUsageRecord.id).limit(MAX_USAGE_RECORDS + 1))).all())
        known_runs = list((await self.db.scalars(runs.order_by(AgentRun.id).limit(MAX_USAGE_RECORDS + 1))).all())
        accepted_rows = list((await self.db.scalars(outcomes.limit(MAX_USAGE_RECORDS + 1))).all())
        if len(rows) > MAX_USAGE_RECORDS or len(known_runs) > MAX_USAGE_RECORDS or len(accepted_rows) > MAX_USAGE_RECORDS:
            raise CollectionLimitExceededError("execution usage", MAX_USAGE_RECORDS)
        accepted = set(accepted_rows)
        heads = {}
        for row in rows:
            if row.run_identity not in heads or row.sequence > heads[row.run_identity].sequence:
                heads[row.run_identity] = row
        expected = {run_identity(run) for run in known_runs} | set(heads)
        provider, estimated, costs, units, unit_counts = defaultdict(Decimal), defaultdict(Decimal), defaultdict(int), defaultdict(Decimal), defaultdict(int)
        sim_provider, sim_estimated, sim_units, sim_counts = defaultdict(Decimal), defaultdict(Decimal), defaultdict(Decimal), defaultdict(int)
        declared_units = set()
        declared_sim_units = set()
        measured_reports = 0
        partial = unavailable = simulated = missing_cost = linked = human_reports = 0
        human_minutes = Decimal(0)
        for row in heads.values():
            report = ExecutionUsageWrite.model_validate(row.payload)
            partial += report.coverage == "partial"
            unavailable += report.coverage == "unavailable"
            simulated += report.provenance == "simulated"
            linked += row.original_task_id in accepted
            if report.provenance == "simulated":
                if report.reported_cost is not None:
                    add_exact(sim_provider, report.currency, report.reported_cost)
                estimate = estimate_cost(report)
                if estimate is not None:
                    add_exact(sim_estimated, report.pricing_basis.currency, estimate)
                for unit, quantity in report.quantities.items():
                    declared_sim_units.add(unit)
                    if quantity is not None:
                        add_exact(sim_units, unit, quantity)
                        sim_counts[unit] += 1
                continue
            measured_reports += report.coverage != "unavailable"
            if report.reported_cost is not None:
                add_exact(provider, report.currency, report.reported_cost)
                costs[report.currency] += 1
            else:
                missing_cost += 1
            estimate = estimate_cost(report)
            if estimate is not None:
                add_exact(estimated, report.pricing_basis.currency, estimate)
            for unit, quantity in report.quantities.items():
                declared_units.add(unit)
                if quantity is not None:
                    add_exact(units, unit, quantity)
                    unit_counts[unit] += 1
            if report.reported_human_effort_minutes is not None:
                human_minutes += report.reported_human_effort_minutes
                human_reports += 1
        delivery = await DeliveryMetricsService(self.db).report(project_id=project_id, iteration_id=iteration_id, lookback_days=lookback_days, now=end)
        budget = None
        if budget_amount is not None:
            if budget_amount < 0 or not budget_amount.is_finite() or budget_currency is None or len(budget_currency) != 3 or not budget_currency.isascii() or not budget_currency.isupper():
                raise ValueError("Advisory budget needs a non-negative amount and explicit three-letter currency")
            budget = {"amount": budget_amount, "currency": budget_currency, "advisory_only": True,
                      "known_reported_cost": provider.get(budget_currency), "known_estimated_cost": estimated.get(budget_currency),
                      "coverage": "partial" if missing_cost or len(expected) > len(heads) or partial or unavailable or simulated else "reported_only"}
        return ExecutionUsageSummary(window_start=start, window_end=end, expected_runs=len(expected), reported_runs=len(heads), unreported_runs=len(expected - set(heads)),
            partial_reports=partial, unavailable_reports=unavailable, simulated_reports=simulated,
            provider_reported_cost=dict(provider), estimated_cost=dict(estimated), known_cost_reports=dict(costs), unknown_cost_reports=missing_cost,
            accepted_task_identities=len(accepted), reports_linked_to_accepted_tasks=linked,
            reported_human_effort_minutes=human_minutes if human_reports else None, human_effort_reports=human_reports,
            reported_units={unit: units[unit] if unit_counts.get(unit, 0) else None for unit in declared_units},
            unit_report_counts={unit: unit_counts.get(unit, 0) for unit in declared_units}, advisory_budget=budget,
            simulated_reported_cost=dict(sim_provider), simulated_estimated_cost=dict(sim_estimated),
            simulated_units={unit: sim_units[unit] if sim_counts.get(unit, 0) else None for unit in declared_sim_units},
            measured_report_count=measured_reports,
            linked_delivery={"rejection_events": delivery.rejection_events, "reopened_events": delivery.reopened_events,
                "review_delay": delivery.review_delay.model_dump(mode="json"), "recovery_queue_count": len(delivery.recovery_queue)})
