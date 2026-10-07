"""Bounded, permission-scoped keyset reads of the merged task timeline."""

import base64
import json
from datetime import datetime

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import selectinload

from app.models.agent import AgentRun, AgentRunEvent, TaskEvent
from app.models.task import Task
from app.models.task_status_log import TaskStatusLog
from app.utils.time import as_utc


class TaskTimelineService:
    def __init__(self, db, serializer=None):
        self.db = db
        if serializer is None:
            from app.services.agent_service import AgentService
            serializer = AgentService(db)
        self.serializer = serializer

    @staticmethod
    def decode(cursor, task_id):
        if cursor is None:
            return None
        try:
            if len(cursor) > 512:
                raise ValueError()
            data = json.loads(base64.b64decode(cursor, altchars=b"-_", validate=True))
            if set(data) != {"v", "task", "at", "source", "id"} or type(data["v"]) is not int or data["v"] != 1 or type(data["task"]) is not int or data["task"] != task_id:
                raise ValueError()
            if type(data["source"]) is not int or not 0 <= data["source"] <= 3 or type(data["id"]) is not int or not 1 <= data["id"] < 2**63:
                raise ValueError()
            at = datetime.fromisoformat(data["at"])
            if at.tzinfo is None:
                raise ValueError()
            return as_utc(at), data["source"], data["id"]
        except (ValueError, TypeError, KeyError, UnicodeError) as exc:
            raise ValueError("Invalid timeline cursor for this task") from exc

    async def page(self, task_id, *, limit=50, cursor=None):
        if not 1 <= limit <= 500:
            raise ValueError("Use a timeline page limit from 1 to 500")
        # ORM authority is re-evaluated even when a cursor was previously issued.
        if await self.db.scalar(select(Task.id).where(Task.id == task_id)) is None:
            raise LookupError("Task not found or inaccessible")
        after = self.decode(cursor, task_id)
        models = [(TaskEvent, TaskEvent.created_at, select(TaskEvent).where(TaskEvent.task_id == task_id)),
                  (TaskStatusLog, TaskStatusLog.changed_at, select(TaskStatusLog).where(TaskStatusLog.task_id == task_id)),
                  (AgentRun, AgentRun.started_at, select(AgentRun).where(AgentRun.task_id == task_id)),
                  (AgentRunEvent, AgentRunEvent.created_at, select(AgentRunEvent).options(selectinload(AgentRunEvent.run).load_only(AgentRun.actor_id)).join(AgentRun).where(AgentRun.task_id == task_id))]
        selected = []
        for source, (model, timestamp, statement) in enumerate(models):
            if after is not None:
                at, prior_source, identifier = after
                tie = model.id < identifier if source == prior_source else source < prior_source
                statement = statement.where(or_(timestamp < at, and_(timestamp == at, tie)))
            rows = (await self.db.scalars(statement.order_by(timestamp.desc(), model.id.desc()).limit(limit + 1))).all()
            selected.extend((as_utc(getattr(row, timestamp.key)), source, row.id, row) for row in rows)
        selected.sort(key=lambda item: item[:3], reverse=True)
        more = len(selected) > limit
        selected = selected[:limit]
        items = [self.item(source, row, at) for at, source, _, row in selected]
        next_cursor = None
        if more:
            at, source, identifier, _ = selected[-1]
            next_cursor = base64.urlsafe_b64encode(json.dumps({"v": 1, "task": task_id,
                "at": at.isoformat(), "source": source, "id": identifier}, separators=(",", ":")).encode()).decode()
        return dict(task_id=task_id, items=items, has_more=more, next_cursor=next_cursor,
                    limit=limit, consistency="live_timestamp_id_desc")

    def item(self, source, row, at):
        parse = self.serializer.event_to_payload
        common = dict(timestamp=at, event_key=f"{source}:{row.id}", actor_id=None, trace_id=None)
        if source == 0:
            return dict(common, item_type="task_event", title=row.event_type, payload=parse(row.payload),
                        actor_type=row.actor_type, actor_id=row.actor_id, trace_id=row.trace_id)
        if source == 1:
            return dict(common, item_type="status_log", title=f"{row.from_status} -> {row.to_status}",
                payload=dict(from_status=row.from_status, to_status=row.to_status, reason=row.reason,
                    affected_task_ids=self.serializer._loads(row.affected_task_ids, [])), actor_type=row.triggered_by)
        if source == 2:
            return dict(common, item_type="agent_run", title=f"agent_run_{row.status}",
                payload=self.serializer._run_payload(row), actor_type="agent", actor_id=row.actor_id, trace_id=row.trace_id)
        return dict(common, item_type="agent_run_event", title=row.event_type,
            payload=dict(run_id=row.run_id, message=row.message, **parse(row.payload)), actor_type="agent",
            actor_id=row.run.actor_id, trace_id=row.trace_id)
