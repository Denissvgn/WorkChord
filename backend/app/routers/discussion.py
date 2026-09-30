"""Task discussion and a personal inbox, separate from execution evidence."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.task_domain import domain_result
from app.services.discussion_service import DiscussionService

router = APIRouter()
DiscussionDatabase = Annotated[AsyncSession, Depends(get_db, scope="function")]


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=12000)
    mentions: list[PositiveInt] = Field(default_factory=list, max_length=25)


class CommentUpdate(CommentCreate):
    expected_version: int = Field(gt=0)
    deleted: bool = False


class SubscriptionInput(BaseModel):
    expected_version: int = Field(ge=0)
    enabled: bool
    events: list[Literal["discussion", "mention", "review", "block"]] = Field(default_factory=lambda: ["discussion", "mention", "review", "block"], max_length=4)


class NotificationRead(BaseModel):
    read: bool


@router.get("/tasks/{task_id}/comments")
async def list_task_comments(task_id: int, db: DiscussionDatabase, after_id: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(DiscussionService(db).list(task_id, after_id=after_id, limit=limit))


@router.get("/tasks/{task_id}/mention-options")
async def task_mention_options(task_id: int, db: DiscussionDatabase, q: str = Query(default="", max_length=200), after_id: int = Query(default=0, ge=0), limit: int = Query(default=25, ge=1, le=50)):
    return await domain_result(DiscussionService(db).mention_options(task_id, query=q, limit=limit, after_id=after_id))


@router.post("/tasks/{task_id}/comments", status_code=201)
async def create_task_comment(task_id: int, data: CommentCreate, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).save(task_id, data.body, data.mentions))


@router.put("/tasks/{task_id}/comments/{comment_id}")
async def update_task_comment(task_id: int, comment_id: int, data: CommentUpdate, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).save(task_id, data.body, data.mentions, comment_id=comment_id,
        expected_version=data.expected_version, deleted=data.deleted))


@router.get("/tasks/{task_id}/comments/{comment_id}/history")
async def task_comment_history(task_id: int, comment_id: int, db: DiscussionDatabase, after_version: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(DiscussionService(db).history(task_id, comment_id, after_version=after_version, limit=limit))


@router.get("/tasks/{task_id}/subscription")
async def get_task_subscription(task_id: int, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).subscription(task_id))


@router.put("/tasks/{task_id}/subscription")
async def set_task_subscription(task_id: int, data: SubscriptionInput, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).subscribe(task_id, data.enabled, data.events, data.expected_version))


@router.get("/notifications")
async def personal_inbox(db: DiscussionDatabase, after_id: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(DiscussionService(db).inbox(after_id=after_id, limit=limit))


@router.get("/notifications/deliveries")
async def personal_notification_deliveries(db: DiscussionDatabase, after_id: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    return await domain_result(DiscussionService(db).delivery_status(after_id=after_id, limit=limit))


@router.post("/notifications/deliveries/{delivery_id}/retry")
async def retry_personal_notification(delivery_id: int, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).retry(delivery_id))


@router.put("/notifications/{notification_id}")
async def mark_notification_read(notification_id: int, data: NotificationRead, db: DiscussionDatabase):
    return await domain_result(DiscussionService(db).mark_read(notification_id, data.read))
