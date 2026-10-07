"""Event-based scoped delivery metrics; status dates never supply missing instants."""

from collections import defaultdict
from datetime import timedelta
from statistics import mean, median

from sqlalchemy import and_, case, func, or_, select

from app.authority import internal_authority, require_project
from app.models.agent import AgentRun
from app.models.delivery_observation import DeliveryObservation
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.query_limits import CollectionLimitExceededError, MAX_PROJECT_TREE_TASKS
from app.schemas.delivery_metrics import DeliveryMetricsResponse, DeliveryQueueItem, DurationSamples
from app.utils.time import as_utc, utc_now

MAX_OBSERVATIONS = 20_000
MAX_QUEUE_ITEMS = 50


def _samples(values, *, censored=0, unknown=0):
    return DurationSamples(sample_count=len(values), mean=round(mean(values), 3) if values else None,
        median=round(median(values), 3) if values else None, censored_count=censored, unknown_count=unknown)


def summarize_observations(rows, start, end):
    """Use immutable leaf facts, keeping reopened episodes and incomplete histories visible."""
    start, end = as_utc(start), as_utc(end)
    grouped = defaultdict(list)
    for row in rows:
        if as_utc(row.observed_at) <= end:
            grouped[row.original_task_id].append(row)
    accepted, cancellations = set(), set()
    acceptance_events = rejection_events = reopened = unknown_acceptance = 0
    leads, cycles, reviews = [], [], []
    lead_unknown = cycle_unknown = review_unknown = 0
    lead_censored = cycle_censored = review_censored = 0
    for task_id, history in grouped.items():
        history.sort(key=lambda row: (as_utc(row.observed_at), row.id or 0))
        captured = active = resolved = None
        pending = False
        for row in history:
            at = as_utc(row.observed_at)
            in_window = start <= at <= end
            if row.kind == "captured":
                captured = captured or at
                pending = True
            elif row.kind in {"started", "rework_started", "reopened"}:
                active, resolved, pending = at, None, True
                reopened += int(in_window and row.kind in {"rework_started", "reopened"})
            elif row.kind == "reopened_planned":
                active = resolved = None
                pending = True
                reopened += int(in_window)
            elif row.kind == "resolved":
                resolved, pending = at, True
            elif row.kind == "restored":
                active = resolved = None
                pending = True
            elif row.kind in {"removed", "structural"}:
                pending = False
            elif row.kind == "canceled":
                pending = False
                if in_window:
                    cancellations.add(task_id)
            elif row.kind == "rejected":
                rejection_events += int(in_window)
            elif row.kind == "acceptance_unknown":
                unknown_acceptance += int(in_window)
            elif row.kind == "accepted":
                pending = False
                if not in_window:
                    continue
                accepted.add(task_id)
                acceptance_events += 1
                for beginning, values, kind in [(captured, leads, "lead"), (active, cycles, "cycle"), (resolved, reviews, "review")]:
                    if beginning is not None and beginning <= at:
                        values.append((at - beginning).total_seconds())
                    elif kind == "lead":
                        lead_unknown += 1
                    elif kind == "cycle":
                        cycle_unknown += 1
                    else:
                        review_unknown += 1
        lead_censored += int(pending and captured is not None)
        cycle_censored += int(pending and active is not None)
        review_censored += int(pending and resolved is not None)
    return dict(accepted_leaf_tasks=len(accepted), acceptance_events=acceptance_events,
        rejection_events=rejection_events, canceled_leaf_tasks=len(cancellations), reopened_events=reopened,
        lead_time=_samples(leads, censored=lead_censored, unknown=lead_unknown),
        cycle_time=_samples(cycles, censored=cycle_censored, unknown=cycle_unknown),
        review_delay=_samples(reviews, censored=review_censored, unknown=review_unknown),
        coverage={"observation_count": len(rows), "observed_task_identities": len(grouped),
                  "window_observation_count": sum(start <= as_utc(row.observed_at) <= end for row in rows),
                  "unknown_acceptance_events": unknown_acceptance, "history_basis": "recorded_instants_only"})


class DeliveryMetricsService:
    def __init__(self, db):
        self.db = db

    async def _window_observations(self, observed, start):
        """Read the window and at most four prior state facts per relevant identity."""
        row = DeliveryObservation
        episodes = {"started", "rework_started", "reopened", "reopened_planned", "restored"}
        pending = episodes | {"captured", "resolved"}
        states = pending | {"removed", "structural", "canceled", "accepted"}

        def rank(kinds, *, earliest=False):
            order = (row.observed_at.asc(), row.id.asc()) if earliest else (row.observed_at.desc(), row.id.desc())
            return func.row_number().over(partition_by=row.original_task_id,
                order_by=(case((row.kind.in_(kinds), 0), else_=1), *order))

        prior = observed.where(row.observed_at < start).with_only_columns(
            row.id, row.original_task_id, row.kind,
            rank({"captured"}, earliest=True).label("capture_rank"),
            rank(episodes).label("episode_rank"),
            rank({"resolved"}).label("resolved_rank"),
            rank(states).label("state_rank"),
        ).cte("prior_delivery_state")
        window = observed.where(row.observed_at >= start)
        relevant = window.with_only_columns(row.original_task_id).union(
            select(prior.c.original_task_id).where(prior.c.state_rank == 1, prior.c.kind.in_(pending))
        ).cte("relevant_delivery_identities")
        seeds = select(prior.c.id).where(
            prior.c.original_task_id.in_(select(relevant.c.original_task_id)),
            or_(and_(prior.c.kind == "captured", prior.c.capture_rank == 1),
                and_(prior.c.kind.in_(episodes), prior.c.episode_rank == 1),
                and_(prior.c.kind == "resolved", prior.c.resolved_rank == 1),
                and_(prior.c.kind.in_(states), prior.c.state_rank == 1)),
        )
        ids = window.with_only_columns(row.id).union(seeds)
        rows = list((await self.db.scalars(observed.where(row.id.in_(ids))
            .order_by(row.id).limit(MAX_OBSERVATIONS + 1))).all())
        if len(rows) > MAX_OBSERVATIONS:
            raise CollectionLimitExceededError("delivery observations", MAX_OBSERVATIONS)
        return rows

    async def report(self, *, project_id=None, iteration_id=None, lookback_days=30, now=None):
        if project_id is None and iteration_id is None:
            raise ValueError("Select a project or an iteration")
        if not 1 <= lookback_days <= 366:
            raise ValueError("Observation window must be between 1 and 366 elapsed days")
        if project_id is not None:
            require_project(self.db, project_id)
            if await self.db.get(Project, project_id) is None:
                raise ValueError("Project not found or inaccessible")
        if iteration_id is not None and await self.db.get(Iteration, iteration_id) is None:
            raise ValueError("Iteration not found or inaccessible")
        end = as_utc(now or utc_now())
        start = end - timedelta(days=lookback_days)
        observed = select(DeliveryObservation).where(DeliveryObservation.observed_at <= end)
        live = select(Task)
        if project_id is not None:
            observed = observed.where(DeliveryObservation.project_id == project_id)
            live = live.where(Task.project_id == project_id)
        if iteration_id is not None:
            observed = observed.where(DeliveryObservation.iteration_id == iteration_id)
            live = live.where(Task.iteration_id == iteration_id)
        if len((await self.db.scalars(live.with_only_columns(Task.id).limit(MAX_PROJECT_TREE_TASKS + 1))).all()) > MAX_PROJECT_TREE_TASKS:
            raise CollectionLimitExceededError("delivery queue context", MAX_PROJECT_TREE_TASKS)
        rows = await self._window_observations(observed, start)
        tasks = list((await self.db.scalars(live.order_by(Task.id).limit(MAX_PROJECT_TREE_TASKS + 1))).all())
        if len(tasks) > MAX_PROJECT_TREE_TASKS:
            raise CollectionLimitExceededError("delivery queue context", MAX_PROJECT_TREE_TASKS)
        result = summarize_observations(rows, start, end)
        with internal_authority(self.db):
            parent_ids = set((await self.db.scalars(select(Task.parent_id).where(Task.parent_id.in_([task.id for task in tasks])).distinct())).all())
        leaves = [task for task in tasks if not task.is_summary and task.id not in parent_ids]
        recorded = set((await self.db.scalars(observed.with_only_columns(DeliveryObservation.original_task_id)
            .where(DeliveryObservation.kind == "captured", DeliveryObservation.original_task_id.in_([task.id for task in leaves]))
            .distinct())).all())
        result["coverage"].update(history_selection="window_with_episode_seeds",
            pre_window_seed_count=sum(as_utc(row.observed_at) < start for row in rows), current_leaf_tasks=len(leaves), current_leaves_without_capture=sum(task.id not in recorded for task in leaves),
            legacy_closed_acceptance_unknown=sum(task.status == "closed" and task.accepted_version is None for task in leaves))
        review = [DeliveryQueueItem(task_id=task.id, title=task.title, reason="awaiting_review",
            age_seconds=max(0, (end - as_utc(task.resolved_at)).total_seconds()) if task.resolved_at else None)
            for task in leaves if task.status == "resolved" and not task.canceled_at]
        runs = list((await self.db.scalars(select(AgentRun).where(AgentRun.task_id.in_([task.id for task in leaves]), AgentRun.status == "running")
            .order_by(AgentRun.id).limit(MAX_PROJECT_TREE_TASKS + 1))).all())
        if len(runs) > MAX_PROJECT_TREE_TASKS:
            raise CollectionLimitExceededError("delivery recovery queue", MAX_PROJECT_TREE_TASKS)
        running = {run.task_id: run for run in runs}
        recovery = []
        for task in leaves:
            if task.id in running and (task.claimed_by is None or task.claim_expires_at is None or as_utc(task.claim_expires_at) <= end):
                run = running[task.id]
                recovery.append(DeliveryQueueItem(task_id=task.id, title=task.title, reason="execution_ownership_unavailable",
                    age_seconds=max(0, (end - as_utc(run.started_at)).total_seconds()) if run.started_at else None))
        order = lambda item: (item.age_seconds is None, -(item.age_seconds or 0), item.task_id)
        review.sort(key=order)
        recovery.sort(key=order)
        return DeliveryMetricsResponse(window_start=start, window_end=end, **result,
            review_queue=review[:MAX_QUEUE_ITEMS], recovery_queue=recovery[:MAX_QUEUE_ITEMS],
            queues_truncated=len(review) > MAX_QUEUE_ITEMS or len(recovery) > MAX_QUEUE_ITEMS)
