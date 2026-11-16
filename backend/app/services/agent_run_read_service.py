"""List runs for readers within the task read scope."""

from sqlalchemy import select

from app.authority import internal_authority
from app.models.agent import AgentActor, AgentRun
from app.models.execution_usage import ExecutionUsageRecord
from app.schemas.agent import AgentAssignmentActorSummary
from app.schemas.agent_run_read import AgentRunHarness, AgentRunReadItem
from app.services.execution_usage_service import ExecutionUsageService, run_identity


class AgentRunReadService:
    def __init__(self, db):
        self.db = db

    async def list(self, *, task_id=None, harness_kind=None, harness_session_id=None, status=None, actor_id=None,
                   limit=50) -> list[AgentRunReadItem]:
        """Runs of the tasks this request's reader can see, newest first.

        Rows follow the request's ORM read scope. The actors and usage reports
        the visible runs name are then read internally.
        """
        query = select(AgentRun)
        if task_id is not None:
            query = query.where(AgentRun.task_id == task_id)
        if harness_kind is not None:
            query = query.where(AgentRun.harness_kind == harness_kind)
        if harness_session_id is not None:
            query = query.where(AgentRun.harness_session_id == harness_session_id)
        if status is not None:
            query = query.where(AgentRun.status == status)
        if actor_id is not None:
            query = query.where(AgentRun.actor_id == actor_id)
        runs = list((await self.db.execute(
            query.order_by(AgentRun.started_at.desc(), AgentRun.id.desc()).limit(limit))).scalars().all())
        identities = {run.id: run_identity(run) for run in runs}
        actors: dict[int, AgentActor] = {}
        latest: dict[str, ExecutionUsageRecord] = {}
        with internal_authority(self.db):
            if runs:
                actors = {actor.id: actor for actor in (await self.db.execute(
                    select(AgentActor).where(AgentActor.id.in_({run.actor_id for run in runs})))).scalars().all()}
                for record in (await self.db.execute(select(ExecutionUsageRecord).where(
                        ExecutionUsageRecord.run_identity.in_(set(identities.values()))))).scalars().all():
                    current = latest.get(record.run_identity)
                    if current is None or record.sequence > current.sequence:
                        latest[record.run_identity] = record
        items = []
        for run in runs:
            actor = actors.get(run.actor_id)
            usage = latest.get(identities[run.id])
            items.append(AgentRunReadItem(
                id=run.id, task_id=run.task_id, assignment_id=run.assignment_id, actor_id=run.actor_id,
                actor=AgentAssignmentActorSummary(id=actor.id, name=actor.name, display_name=actor.display_name,
                                                  role=actor.role) if actor is not None else None,
                status=run.status, trace_id=run.trace_id,
                harness=AgentRunHarness(kind=run.harness_kind, session_id=run.harness_session_id)
                if run.harness_kind and run.harness_session_id else None,
                model=run.model, configured_model_alias=run.configured_model_alias,
                resolved_model_id=run.resolved_model_id, model_trust_state=run.model_trust_state,
                started_at=run.started_at, heartbeat_at=run.heartbeat_at, ended_at=run.ended_at,
                usage=ExecutionUsageService.response(usage) if usage is not None else None,
            ))
        return items
