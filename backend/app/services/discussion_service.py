"""Versioned discussion and inbox delivery with live recipient authorization."""

from hashlib import sha256

from sqlalchemy import or_, select, update

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command
from app.models.discussion import InboxNotification, TaskComment, TaskCommentRevision, TaskSubscription
from app.models.identity import Principal, ProjectMembership, WorkspaceMembership
from app.models.outbound_webhook import OutboundWebhookDelivery, OutboundWebhookEvent
from app.models.task import Task


EVENTS = {"discussion", "mention", "review", "block"}
SUPPRESSED_DELIVERY_ERRORS = {"Recipient access is unavailable; notification stopped", "Subscription is disabled; notification stopped"}


class DiscussionService:
    def __init__(self, db):
        self.db = db

    def principal_id(self):
        authority = self.db.info.get("authority")
        if authority is None or authority.principal_id is None or authority.kind != "human":
            raise AuthorityError("human_identity_required", "Sign in with a human account to join the discussion.")
        return authority.principal_id

    async def task(self, task_id, *, writing=False, lock=False):
        task = await self.db.scalar(select(Task).where(Task.id == task_id).execution_options(populate_existing=True))
        if task is None:
            raise ValueError("Task not found or inaccessible")
        require_project(self.db, task.project_id)
        authority = self.db.info.get("authority")
        if writing and authority and not any(authority.allows(task.project_id, action) for action in ("edit", "execute", "review")):
            raise AuthorityError()
        if lock:
            # Serialize comment/subscription CAS and task deletion on both dialects,
            # without reserving an execution or shared planning revision.
            with internal_authority(self.db):
                await self.db.execute(update(Task).where(Task.id == task_id).values(id=Task.id, updated_at=Task.updated_at)
                                      .execution_options(synchronize_session=False))
            return await self.task(task_id, writing=writing)
        return task

    async def mention_options(self, task_id, *, query="", limit=25, after_id=0):
        task = await self.task(task_id)
        if not 1 <= limit <= 50 or len(query) > 200 or after_id < 0:
            raise ValueError("Use a bounded mention query")
        from app.sql_semantics import portable_contains
        with internal_authority(self.db):
            project_members = select(ProjectMembership.principal_id).where(ProjectMembership.project_id == task.project_id)
            workspace_members = select(WorkspaceMembership.principal_id).where(WorkspaceMembership.role.in_(
                ["owner", "operator", *(["member"] if task.project_id is None else [])]))
            statement = select(Principal.id, Principal.display_name).where(Principal.kind == "human", Principal.enabled.is_(True),
                Principal.id > after_id, or_(Principal.id.in_(project_members), Principal.id.in_(workspace_members)))
            if query:
                statement = statement.where(portable_contains(Principal.display_name, query))
            rows = (await self.db.execute(statement.order_by(Principal.id).limit(limit + 1))).all()
        return {"items": [{"id": row.id, "name": row.display_name} for row in rows[:limit]],
            "has_more": len(rows) > limit, "next_after_id": rows[limit - 1].id if len(rows) > limit else None}

    async def recipient_authorized(self, principal_id, task_id):
        from app.services.identity_service import IdentityService
        with internal_authority(self.db):
            person = await self.db.get(Principal, principal_id, populate_existing=True)
            task = await self.db.scalar(select(Task).where(Task.id == task_id).execution_options(populate_existing=True))
            if person is None or not person.enabled or person.kind != "human" or task is None:
                return False
            authority = await IdentityService(self.db).context(person)
            return authority.allows(task.project_id, "read")

    @staticmethod
    def serialize(comment, author_name):
        return {"id": comment.id, "task_id": comment.original_task_id, "principal_id": comment.principal_id,
            "author_name": author_name, "body": "" if comment.deleted else comment.body,
            "mentions": [] if comment.deleted else comment.mentions, "version": comment.version,
            "deleted": comment.deleted, "created_at": comment.created_at, "updated_at": comment.updated_at}

    async def list(self, task_id, *, after_id=0, limit=50):
        await self.task(task_id)
        if not 1 <= limit <= 100 or after_id < 0:
            raise ValueError("Use a limit from 1 to 100 and a nonnegative cursor")
        rows = (await self.db.execute(select(TaskComment, Principal.display_name).join(Principal, Principal.id == TaskComment.principal_id)
            .where(TaskComment.original_task_id == task_id, TaskComment.id > after_id).order_by(TaskComment.id).limit(limit + 1))).all()
        return {"items": [self.serialize(comment, name) for comment, name in rows[:limit]], "has_more": len(rows) > limit,
            "next_after_id": rows[limit - 1][0].id if len(rows) > limit else None}

    async def history(self, task_id, comment_id, *, after_version=0, limit=50):
        await self.task(task_id)
        comment = await self.db.scalar(select(TaskComment).where(TaskComment.id == comment_id, TaskComment.original_task_id == task_id))
        if comment is None:
            raise ValueError("Comment not found or inaccessible")
        if not 1 <= limit <= 100 or after_version < 0:
            raise ValueError("Use a bounded history cursor")
        rows = (await self.db.scalars(select(TaskCommentRevision).where(TaskCommentRevision.comment_id == comment_id,
            TaskCommentRevision.version > after_version).order_by(TaskCommentRevision.version).limit(limit + 1))).all()
        return {"items": [{"version": row.version, "body": row.body, "mentions": row.mentions, "deleted": row.deleted,
            "principal_id": row.principal_id, "created_at": row.created_at} for row in rows[:limit]],
            "has_more": len(rows) > limit, "next_after_version": rows[limit - 1].version if len(rows) > limit else None}

    @atomic_command
    async def save(self, task_id, body, mentions, *, comment_id=None, expected_version=None, deleted=False):
        principal_id = self.principal_id()
        task = await self.task(task_id, writing=True, lock=True)
        body = body.strip()
        if not deleted and not body or len(body) > 12000 or len(mentions) > 25:
            raise ValueError("Use 1–12000 characters and at most 25 mentions")
        mentions = sorted(set(mentions))
        for recipient in mentions:
            if not await self.recipient_authorized(recipient, task_id):
                raise ValueError("A mentioned person is unavailable for this task")
        comment = await self.db.scalar(select(TaskComment).where(TaskComment.id == comment_id, TaskComment.original_task_id == task_id)
                                      .execution_options(populate_existing=True)) if comment_id else None
        if comment_id and comment is None:
            raise ValueError("Comment not found or inaccessible")
        if comment:
            authority = self.db.info["authority"]
            if comment.principal_id != principal_id and not (deleted and authority.allows(task.project_id, "manage")):
                raise AuthorityError("comment_author_required", "Only the author can edit this comment.")
            if expected_version != comment.version:
                raise PlanningConflict("comment_version_conflict", "This comment changed. Reload it before applying your draft.")
            if comment.deleted:
                raise PlanningConflict("comment_deleted", "This comment has been removed. Start a new comment.")
            comment.version += 1
        else:
            comment = TaskComment(task_id=task_id, original_task_id=task_id, principal_id=principal_id, version=1)
            self.db.add(comment)
        comment.task_id = task_id
        comment.body, comment.mentions, comment.deleted = ("", [], True) if deleted else (body, mentions, False)
        await self.db.flush()
        self.db.add(TaskCommentRevision(comment_id=comment.id, original_task_id=task_id, principal_id=principal_id,
            version=comment.version, body=comment.body, mentions=comment.mentions, deleted=comment.deleted))
        await self.db.flush()
        if not deleted:
            await self.enqueue(task_id, "discussion", f"comment:{comment.id}:{comment.version}", mentions=mentions)
        name = await self.db.scalar(select(Principal.display_name).where(Principal.id == comment.principal_id))
        return self.serialize(comment, name)

    async def subscription(self, task_id):
        principal_id = self.principal_id()
        await self.task(task_id)
        row = await self.db.get(TaskSubscription, (task_id, principal_id))
        return {"enabled": row.enabled if row else False, "events": row.events if row else sorted(EVENTS), "version": row.version if row else 0}

    @atomic_command
    async def subscribe(self, task_id, enabled, events, expected_version):
        principal_id = self.principal_id()
        await self.task(task_id, lock=True)
        if not set(events) <= EVENTS:
            raise ValueError("Unsupported subscription event")
        row = await self.db.get(TaskSubscription, (task_id, principal_id), populate_existing=True)
        if expected_version != (row.version if row else 0):
            raise PlanningConflict("subscription_version_conflict", "Subscription changed. Reload before saving.")
        if row is None:
            row = TaskSubscription(task_id=task_id, principal_id=principal_id, version=1)
            self.db.add(row)
        else:
            row.version += 1
        row.enabled, row.events = enabled, sorted(set(events))
        await self.db.flush()
        return await self.subscription(task_id)

    async def enqueue(self, task_id, kind, key, *, mentions=()):
        """Write worker intents only; dispatch rechecks access, preferences and task existence."""
        sender = getattr(self.db.info.get("authority"), "principal_id", None)
        with internal_authority(self.db):
            recipients = {row.principal_id: row for row in (await self.db.scalars(select(TaskSubscription).where(
                TaskSubscription.task_id == task_id))).all()}
            candidates = set(recipients) | set(mentions)
            if not candidates - {sender}:
                return
            event_key = sha256(f"discussion:{key}:{kind}".encode()).hexdigest()
            if await self.db.scalar(select(OutboundWebhookEvent.id).where(OutboundWebhookEvent.event_id == event_key)):
                return
            event = OutboundWebhookEvent(event_id=event_key, event_type=f"task.{kind}", entity_type="task", entity_id=task_id,
                payload_json={"task_id": task_id, "kind": kind})
            self.db.add(event)
            await self.db.flush()
            for principal_id in sorted(candidates - {sender}):
                event_kind = "mention" if principal_id in mentions else kind
                subscription = recipients.get(principal_id)
                if subscription and (not subscription.enabled or event_kind not in subscription.events):
                    continue
                if subscription is None and event_kind != "mention":
                    continue
                if not await self.recipient_authorized(principal_id, task_id):
                    continue
                self.db.add(OutboundWebhookDelivery(event_id=event.id, target_name="Personal inbox", target_url=f"inbox:{principal_id}",
                    channel="inbox", payload_json={"principal_id": principal_id, "task_id": task_id, "kind": event_kind}, max_attempts=5))
            await self.db.flush()

    async def deliver(self, delivery):
        """Idempotent local inbox sink; no external recipient messaging occurs here."""
        from app.services.outbound_webhook_service import OutboundDeliveryAttemptError
        payload = delivery.payload_json
        principal_id, task_id, kind = payload["principal_id"], payload["task_id"], payload["kind"]
        with internal_authority(self.db):
            if not await self.recipient_authorized(principal_id, task_id):
                raise OutboundDeliveryAttemptError("Recipient access is unavailable; notification stopped", retryable=False)
            subscription = await self.db.get(TaskSubscription, (task_id, principal_id), populate_existing=True)
            if subscription and (not subscription.enabled or kind not in subscription.events) or subscription is None and kind != "mention":
                raise OutboundDeliveryAttemptError("Subscription is disabled; notification stopped", retryable=False)
            if await self.db.scalar(select(InboxNotification.id).where(InboxNotification.delivery_id == delivery.id)):
                return
            self.db.add(InboxNotification(task_id=task_id, principal_id=principal_id, delivery_id=delivery.id, event_type=kind))
            await self.db.flush()

    async def inbox(self, *, after_id=0, limit=50):
        principal_id = self.principal_id()
        if not 1 <= limit <= 100 or after_id < 0:
            raise ValueError("Use a bounded inbox cursor")
        rows = (await self.db.execute(select(InboxNotification, Task.title).join(Task, Task.id == InboxNotification.task_id)
            .where(InboxNotification.principal_id == principal_id, InboxNotification.id > after_id)
            .order_by(InboxNotification.id).limit(limit + 1))).all()
        return {"items": [{"id": row.id, "task_id": row.task_id, "title": title, "event_type": row.event_type,
            "read": row.read, "created_at": row.created_at} for row, title in rows[:limit]],
            "has_more": len(rows) > limit, "next_after_id": rows[limit - 1][0].id if len(rows) > limit else None}

    @atomic_command
    async def mark_read(self, notification_id, read):
        principal_id = self.principal_id()
        row = await self.db.scalar(select(InboxNotification).where(InboxNotification.id == notification_id,
            InboxNotification.principal_id == principal_id))
        if row is None:
            raise ValueError("Notification not found or inaccessible")
        await self.task(row.task_id)
        row.read = read
        await self.db.flush()
        return {"id": row.id, "read": row.read}

    async def delivery_status(self, *, after_id=0, limit=50):
        principal_id = self.principal_id()
        if not 1 <= limit <= 100 or after_id < 0:
            raise ValueError("Use a bounded delivery cursor")
        query = select(OutboundWebhookDelivery, Task.title).join(Task,
            Task.id == OutboundWebhookDelivery.payload_json["task_id"].as_integer()).where(
                OutboundWebhookDelivery.channel == "inbox", OutboundWebhookDelivery.id > after_id,
                OutboundWebhookDelivery.payload_json["principal_id"].as_integer() == principal_id)
        rows = (await self.db.execute(query.order_by(OutboundWebhookDelivery.id).limit(limit + 1))).all()
        return {"items": [{"id": row.id, "task_id": row.payload_json["task_id"], "title": title,
            "status": "suppressed" if row.last_error in SUPPRESSED_DELIVERY_ERRORS else row.status, "attempt_count": row.attempt_count, "max_attempts": row.max_attempts,
            "next_retry_at": row.next_retry_at} for row, title in rows[:limit]],
            "has_more": len(rows) > limit, "next_after_id": rows[limit - 1][0].id if len(rows) > limit else None}

    @atomic_command
    async def retry(self, delivery_id):
        from app.utils.time import utc_now
        principal_id = self.principal_id()
        row = await self.db.scalar(select(OutboundWebhookDelivery).where(OutboundWebhookDelivery.id == delivery_id,
            OutboundWebhookDelivery.channel == "inbox", OutboundWebhookDelivery.payload_json["principal_id"].as_integer() == principal_id).with_for_update())
        if row is None:
            raise ValueError("Delivery not found or inaccessible")
        await self.task(row.payload_json["task_id"])
        if row.status != "failed":
            raise PlanningConflict("notification_retry_unavailable", "Only a failed delivery can be retried.")
        with internal_authority(self.db):
            row.status, row.attempt_count, row.next_retry_at, row.terminal_at = "pending", 0, utc_now(), None
            row.last_error = None
            await self.db.flush()
        return {"id": row.id, "status": row.status}
