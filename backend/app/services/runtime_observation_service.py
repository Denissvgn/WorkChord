"""Record and read advisory runtime observations.

Observations come from independent observers, such as a dashboard watching
agent sessions on a host. They are advisory: recording one writes only its own
row, never an actor, assignment, run, task event, topology member or webhook,
and no dispatch, routing or readiness code reads them.
"""

from datetime import timedelta

from sqlalchemy import delete, func, select

from app.authority import AuthorityError, internal_authority, require_operator
from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.runtime_observation import AgentRuntimeObservation
from app.models.task import Task
from app.models.user_session import UserSession
from app.schemas.runtime_observation import AgentRuntimeObservationCreate
from app.utils.time import utc_now

RECORDED_FIELDS = ("kind", "harness_kind", "harness_session_id", "observed_at", "task_id", "run_id",
                   "subject_actor_id", "observed_model")


class RuntimeObservationService:
    def __init__(self, db):
        self.db = db

    def _writer(self):
        authority = self.db.info.get("authority")
        if authority is None or not (authority.read_only or authority.operator):
            raise AuthorityError("observer_required",
                                 "Only a paired observer or an operator records runtime observations.")
        return authority

    async def _references(self, authority, data: AgentRuntimeObservationCreate):
        """Resolve the task a row is filed under; references must be visible to the observer."""
        with internal_authority(self.db):
            task = await self.db.get(Task, data.task_id) if data.task_id else None
            run = await self.db.get(AgentRun, data.run_id) if data.run_id else None
            if data.task_id and task is None or data.run_id and run is None:
                raise AuthorityError("resource_unavailable", "The referenced task or run is unavailable.", 404)
            if run is not None and task is not None and run.task_id != task.id:
                raise AuthorityError("observation_reference_mismatch", "The run belongs to another task.", 422)
            if task is None and run is not None and run.task_id is not None:
                task = await self.db.get(Task, run.task_id)
            actor = await self.db.get(AgentActor, data.subject_actor_id) if data.subject_actor_id else None
            if data.subject_actor_id and actor is None:
                raise AuthorityError("resource_unavailable", "The referenced actor is unavailable.", 404)
            assigned = False
            if actor is not None and task is not None:
                assigned = await self.db.scalar(select(AgentTaskAssignment.id).where(
                    AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.actor_id == actor.id).limit(1)) is not None
        if (task is not None or run is not None) and not authority.operator and not authority.local:
            if task is None or not authority.allows(task.project_id, "read"):
                raise AuthorityError("resource_unavailable", "The referenced task or run is unavailable.", 404)
        if actor is not None and not authority.operator and not authority.local:
            if not (run is not None and run.actor_id == actor.id or assigned):
                raise AuthorityError("observation_actor_unverifiable",
                                     "Name an actor through a run or an assignment of a task you can read.", 422)
        return task

    async def record(self, data: AgentRuntimeObservationCreate):
        """Append one observation; repeating the same key and content returns the first row."""
        authority = self._writer()
        task = await self._references(authority, data)
        values = data.model_dump(include=set(RECORDED_FIELDS))
        values["task_id"] = task.id if task is not None else None
        with internal_authority(self.db):
            session = await self.db.get(UserSession, authority.session_id) if authority.session_id else None
            owner = (AgentRuntimeObservation.observer_session_id == session.id if session is not None else
                     (AgentRuntimeObservation.observer_session_id.is_(None))
                     & (AgentRuntimeObservation.observer_principal_id == authority.principal_id))
            existing = await self.db.scalar(select(AgentRuntimeObservation).where(
                owner, AgentRuntimeObservation.idempotency_key == data.idempotency_key))
            if existing is not None:
                if any(_same(getattr(existing, field), values[field]) is False for field in RECORDED_FIELDS):
                    raise AuthorityError("observation_key_reused",
                                         "This idempotency key already recorded a different observation.", 409)
                return existing, False
            if session is not None:
                recent = await self.db.scalar(select(func.count()).select_from(AgentRuntimeObservation).where(
                    owner, AgentRuntimeObservation.received_at > utc_now() - timedelta(hours=1)))
                if recent >= get_settings().agent_observation_hourly_limit:
                    raise AuthorityError("observation_limit", "Too many observations this hour. Try again later.", 429)
            row = AgentRuntimeObservation(
                **values,
                idempotency_key=data.idempotency_key,
                observer_session_id=session.id if session is not None else None,
                observer_principal_id=authority.principal_id,
                observer_label=session.client_label if session is not None else ("Operator" if authority.operator else None),
            )
            self.db.add(row)
            await self.db.flush()
        return row, True

    async def list(self, *, task_id=None, run_id=None, harness_kind=None, harness_session_id=None, limit=100):
        """Observations this reader can see: the request's task read scope applies."""
        query = select(AgentRuntimeObservation)
        if task_id is not None:
            query = query.where(AgentRuntimeObservation.task_id == task_id)
        if run_id is not None:
            query = query.where(AgentRuntimeObservation.run_id == run_id)
        if harness_kind is not None:
            query = query.where(AgentRuntimeObservation.harness_kind == harness_kind)
        if harness_session_id is not None:
            query = query.where(AgentRuntimeObservation.harness_session_id == harness_session_id)
        rows = await self.db.execute(query.order_by(AgentRuntimeObservation.received_at.desc(),
                                                    AgentRuntimeObservation.id.desc()).limit(limit))
        return list(rows.scalars().all())

    async def cleanup(self, *, limit=500):
        """Remove a bounded batch of observations older than the retention period."""
        require_operator(self.db)
        retention = get_settings().agent_observation_retention_days
        cutoff = utc_now() - timedelta(days=retention)
        with internal_authority(self.db):
            expired = select(AgentRuntimeObservation.id).where(
                AgentRuntimeObservation.received_at < cutoff).order_by(AgentRuntimeObservation.id).limit(limit)
            ids = list((await self.db.execute(expired)).scalars().all())
            if ids:
                await self.db.execute(delete(AgentRuntimeObservation).where(AgentRuntimeObservation.id.in_(ids)))
        return {"removed": len(ids), "retention_days": retention, "limit": limit}


def _same(stored, requested):
    if hasattr(stored, "timestamp") and hasattr(requested, "timestamp"):
        from app.utils.time import as_utc
        return as_utc(stored) == as_utc(requested)
    return stored == requested
