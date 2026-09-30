"""Discussion is attributable, versioned, private and independent from execution."""

from dataclasses import replace

import pytest
from sqlalchemy import delete, select, update

from app.authority import Authority, AuthorityError, internal_authority
from app.commands import PlanningConflict, command_transaction
from app.config import get_settings
from app.models.capacity import PlanningState
from app.models.discussion import InboxNotification, TaskCommentRevision
from app.models.identity import ProjectMembership
from app.models.outbound_webhook import OutboundWebhookDelivery
from app.schemas.task import TaskCreate
from app.services.discussion_service import DiscussionService
from app.services.outbound_webhook_service import OutboundWebhookService
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context


async def context(db, scenario, monkeypatch):
    authority, reviewer = await human_context(db, scenario.projects[0])
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    db.info["authority"] = authority
    task = await TaskService(db).create(None, TaskCreate(title="Discuss this delivery", project_id=scenario.projects[0]))
    return authority, reviewer, task


async def test_comment_versions_preserve_execution_and_history(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, reviewer, task = await context(db, scenario, monkeypatch)
        task_id, version = task.id, task.version
        revision = await db.scalar(select(PlanningState.revision))
        service = DiscussionService(db)
        comment = await service.save(task_id, "<script>plain text</script>", [reviewer])
        assert comment["body"] == "<script>plain text</script>"
        edited = await service.save(task_id, "Updated note", [], comment_id=comment["id"], expected_version=1)
        assert edited["version"] == 2
        assert len((await service.history(task_id, comment["id"]))["items"]) == 2
        await db.refresh(task)
        assert task.version == version
        assert await db.scalar(select(PlanningState.revision)) == revision
        with pytest.raises(PlanningConflict, match="comment changed"):
            await service.save(task_id, "Stale draft", [], comment_id=comment["id"], expected_version=1)
        with pytest.raises(ValueError, match="append-only"):
            await db.execute(update(TaskCommentRevision).values(body="Rewrite history"))
        await db.rollback()
    get_settings.cache_clear()


async def test_comment_authority_mentions_and_tombstone(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, reviewer, task = await context(db, scenario, monkeypatch)
        task_id = task.id
        service = DiscussionService(db)
        with pytest.raises(ValueError, match="mentioned person"):
            await service.save(task_id, "Invalid mention", [999999])
        comment = await service.save(task_id, "Review question", [reviewer])
        db.info["authority"] = Authority(reviewer, "human", projects={scenario.projects[0]: "reviewer"})
        with pytest.raises(AuthorityError, match="Only the author"):
            await service.save(task_id, "Impersonated edit", [], comment_id=comment["id"], expected_version=1)
        db.info["authority"] = author
        removed = await service.save(task_id, "", [], comment_id=comment["id"], expected_version=1, deleted=True)
        assert removed["deleted"] and removed["body"] == ""
        assert (await service.history(task_id, comment["id"]))["items"][0]["body"] == "Review question"
        db.info["authority"] = Authority(reviewer, "human", projects={scenario.projects[1]: "reviewer"})
        with pytest.raises(ValueError, match="inaccessible"):
            await service.list(task_id)
    get_settings.cache_clear()


@pytest.mark.parametrize("revoke", [False, True])
async def test_worker_rechecks_unsubscribe_or_revocation(delivery_store, monkeypatch, revoke):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, reviewer, task = await context(db, scenario, monkeypatch)
        task_id = task.id
        service = DiscussionService(db)
        db.info["authority"] = Authority(reviewer, "human", projects={scenario.projects[0]: "reviewer"})
        await service.subscribe(task_id, True, ["discussion"], 0)
        db.info["authority"] = author
        await service.save(task_id, "Please inspect the result", [])
        db.info["authority"] = Authority(reviewer, "human", projects={scenario.projects[0]: "reviewer"})
        if revoke:
            with internal_authority(db):
                await db.execute(delete(ProjectMembership).where(ProjectMembership.principal_id == reviewer))
                await db.commit()
        else:
            await service.subscribe(task_id, False, ["discussion"], 1)
        db.info.pop("authority")
        assert await OutboundWebhookService(db).run_due_jobs(limit=50) >= 1
        assert (await db.scalars(select(InboxNotification))).all() == []
        delivery = await db.scalar(select(OutboundWebhookDelivery).where(OutboundWebhookDelivery.channel == "inbox"))
        assert delivery.status == "failed" and delivery.delivered_at is None
        assert delivery.terminal_at is not None and delivery.next_retry_at is None
    get_settings.cache_clear()


async def test_inbox_retry_idempotency_and_read_state_are_separate(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        author, reviewer, task = await context(db, scenario, monkeypatch)
        task_id = task.id
        service = DiscussionService(db)
        await service.save(task_id, "A question for you", [reviewer])
        db.info.pop("authority")
        worker = OutboundWebhookService(db)
        assert await worker.run_due_jobs(limit=50) >= 1
        rows = (await db.scalars(select(InboxNotification))).all()
        assert len(rows) == 1
        delivery = await db.get(OutboundWebhookDelivery, rows[0].delivery_id)
        await service.deliver(delivery)
        await db.commit()
        assert len((await db.scalars(select(InboxNotification))).all()) == 1
        db.info["authority"] = Authority(reviewer, "human", projects={scenario.projects[0]: "reviewer"})
        inbox = await service.inbox()
        assert inbox["items"][0]["event_type"] == "mention"
        await service.mark_read(rows[0].id, True)
        assert (await service.inbox())["items"][0]["read"]
        assert (await service.delivery_status())["items"][0]["status"] == "delivered"
    get_settings.cache_clear()


async def test_delivery_failure_is_bounded_and_retry_does_not_duplicate_receipts(delivery_store, monkeypatch):
    from datetime import timedelta
    from app.utils.time import utc_now
    factory, scenario, _ = delivery_store
    async with factory() as db:
        _, reviewer, task = await context(db, scenario, monkeypatch)
        await DiscussionService(db).save(task.id, "Please review this discussion", [reviewer])
        db.info.pop("authority")
        original = DiscussionService.deliver

        async def unavailable(self, delivery):
            raise RuntimeError("Disposable inbox sink unavailable")

        monkeypatch.setattr(DiscussionService, "deliver", unavailable)
        worker = OutboundWebhookService(db)
        await worker.run_due_jobs(limit=50)
        delivery = await db.scalar(select(OutboundWebhookDelivery).where(OutboundWebhookDelivery.channel == "inbox"))
        assert delivery.status == "pending" and delivery.attempt_count == 1
        assert delivery.next_retry_at is not None
        monkeypatch.setattr(DiscussionService, "deliver", original)
        await worker.run_due_jobs(limit=50, now=utc_now() + timedelta(hours=1))
        await db.refresh(delivery)
        assert delivery.status == "delivered" and delivery.attempt_count == 2
        assert len((await db.scalars(select(InboxNotification))).all()) == 1
    get_settings.cache_clear()


async def test_comment_rechecks_task_scope_after_acquiring_its_write_lock(delivery_store, monkeypatch):
    from sqlalchemy.sql.dml import Update
    from app.models.task import Task
    from app.models.discussion import TaskComment
    factory, scenario, _ = delivery_store
    async with factory() as db:
        _, _, task = await context(db, scenario, monkeypatch)
        task_id = task.id
        execute = db.execute
        moved = False

        async def move_before_lock(statement, *args, **kwargs):
            nonlocal moved
            if not moved and isinstance(statement, Update) and statement.table.name == "tasks":
                moved = True
                async with factory() as other:
                    await other.execute(update(Task).where(Task.id == task_id).values(project_id=scenario.projects[1]))
                    await other.commit()
            return await execute(statement, *args, **kwargs)

        monkeypatch.setattr(db, "execute", move_before_lock)
        with pytest.raises(ValueError, match="inaccessible"):
            await DiscussionService(db).save(task_id, "A draft for the former project", [])
    async with factory() as db:
        assert (await db.scalars(select(TaskComment))).all() == []
    get_settings.cache_clear()


async def test_discussion_history_reappears_with_the_restored_task_identity(delivery_store, monkeypatch):
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        _, _, task = await context(db, scenario, monkeypatch)
        task_id = task.id
        comment = await DiscussionService(db).save(task_id, "Keep this coordination history", [])
        snapshot = await BacklogSnapshotService(db).capture(scenario.projects[0], "before_removal")
        await TaskService(db).delete(task_id)
        await BacklogSnapshotService(db).restore(scenario.projects[0], snapshot, {}, reason="Recover the same task and its history")
        listed = await DiscussionService(db).list(task_id)
        assert listed["items"][0]["id"] == comment["id"]
        assert listed["items"][0]["body"] == "Keep this coordination history"
        updated = await DiscussionService(db).save(task_id, "Continue after recovery", [], comment_id=comment["id"], expected_version=1)
        assert updated["version"] == 2
        assert len((await DiscussionService(db).history(task_id, comment["id"]))["items"]) == 2
    get_settings.cache_clear()
