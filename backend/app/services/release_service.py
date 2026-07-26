"""Release service for project-scoped shipping records."""
from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.agent import TaskEvent
from app.models.project import Project
from app.models.release import Release, ReleaseStatus
from app.models.task import Task
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.release import ReleaseCreateRequest, ReleaseUpdateRequest
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_service import TaskService
from app.utils.time import utc_now


RELEASE_SHIPPED_EVENT_TYPE = "release_shipped"


class ReleaseService:
    """Service for release CRUD and task link validation."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _release_options(self) -> tuple:
        """Return release relationship loading options used by responses."""
        return (selectinload(Release.tasks),)

    def _is_shipped(self, release: Release) -> bool:
        """Return whether a release is currently in shipped state."""
        return release.status == ReleaseStatus.SHIPPED.value

    def _release_shipped_idempotency_key(self, release_id: int, task_id: int) -> str:
        """Build the stable idempotency key for one release/task shipped signal."""
        return f"release-shipped:{release_id}:{task_id}"

    async def _event_exists(self, idempotency_key: str) -> bool:
        """Return whether a task event idempotency key has already been recorded."""
        result = await self.db.execute(
            select(TaskEvent.id).where(TaskEvent.idempotency_key == idempotency_key)
        )
        return result.scalar_one_or_none() is not None

    def _release_shipped_payload(self, release: Release) -> dict:
        """Build the task timeline payload for a shipped release."""
        return {
            "summary": f"Release shipped: {release.name}",
            "release_id": release.id,
            "release_name": release.name,
            "project_id": release.project_id,
            "version": release.version,
            "environment": release.environment,
            "target_date": release.target_date.isoformat() if release.target_date else None,
            "shipped_at": release.shipped_at.isoformat() if release.shipped_at else None,
        }

    async def _emit_release_shipped_events(self, release: Release) -> None:
        """Emit missing shipped events for linked release tasks."""
        if not self._is_shipped(release):
            return

        if release.shipped_at is None:
            release.shipped_at = utc_now()

        await self.db.flush()
        task_service = TaskService(self.db)
        for task in release.tasks:
            idempotency_key = self._release_shipped_idempotency_key(release.id, task.id)
            if await self._event_exists(idempotency_key):
                continue
            await task_service.record_task_event(
                task.id,
                RELEASE_SHIPPED_EVENT_TYPE,
                self._release_shipped_payload(release),
                actor_type="user",
                idempotency_key=idempotency_key,
            )

    async def _project_exists(self, project_id: int) -> bool:
        """Return whether a project exists."""
        result = await self.db.execute(select(Project.id).where(Project.id == project_id))
        return result.scalar_one_or_none() is not None

    async def get_by_id(self, release_id: int) -> Optional[Release]:
        """Get a release with linked tasks loaded."""
        result = await self.db.execute(
            select(Release)
            .options(*self._release_options())
            .where(Release.id == release_id)
        )
        return result.scalar_one_or_none()

    async def list_for_project(self, project_id: int) -> Optional[Sequence[Release]]:
        """List releases for a project in project-release order."""
        if not await self._project_exists(project_id):
            return None

        result = await self.db.execute(
            select(Release)
            .options(*self._release_options())
            .where(Release.project_id == project_id)
            .order_by(
                Release.target_date.asc().nulls_last(),
                Release.id.asc(),
            )
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        releases = list(result.scalars().all())
        if len(releases) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "project release list",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return releases

    async def _validate_task_ids(
        self,
        project_id: int,
        task_ids: Sequence[int],
    ) -> list[Task]:
        """Validate that all task IDs exist once and belong to the release project."""
        if not task_ids:
            return []

        seen: set[int] = set()
        duplicates = sorted({task_id for task_id in task_ids if task_id in seen or seen.add(task_id)})
        if duplicates:
            duplicate_text = ", ".join(str(task_id) for task_id in duplicates)
            raise ValueError(f"Duplicate task IDs are not allowed: {duplicate_text}")

        result = await self.db.execute(select(Task).where(Task.id.in_(task_ids)))
        tasks = result.scalars().all()
        tasks_by_id = {task.id: task for task in tasks}
        missing_ids = [task_id for task_id in task_ids if task_id not in tasks_by_id]
        if missing_ids:
            missing_text = ", ".join(str(task_id) for task_id in missing_ids)
            raise ValueError(f"Task IDs not found: {missing_text}")

        invalid_project_ids = [
            task_id
            for task_id in task_ids
            if tasks_by_id[task_id].project_id != project_id
        ]
        if invalid_project_ids:
            invalid_text = ", ".join(str(task_id) for task_id in invalid_project_ids)
            raise ValueError(
                f"Task IDs must belong to project {project_id}: {invalid_text}"
            )

        return [tasks_by_id[task_id] for task_id in task_ids]

    async def create_for_project(
        self,
        project_id: int,
        data: ReleaseCreateRequest,
    ) -> Optional[Release]:
        """Create a release for a project."""
        if not await self._project_exists(project_id):
            return None

        tasks = await self._validate_task_ids(project_id, data.task_ids)
        release = Release(
            project_id=project_id,
            name=data.name,
            description=data.description,
            status=self._enum_value(data.status),
            target_date=data.target_date,
            shipped_at=data.shipped_at,
            version=data.version,
            environment=data.environment,
        )
        release.tasks = tasks
        self.db.add(release)
        try:
            await self._emit_release_shipped_events(release)
            await self.db.flush()
            event_data = {
                "release_id": release.id,
                "project_id": release.project_id,
                "name": release.name,
                "status": release.status,
                "version": release.version,
                "environment": release.environment,
                "task_ids": [task.id for task in release.tasks],
            }
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="release.created",
                entity_type="release",
                entity_id=release.id,
                data=event_data,
            )
            if self._is_shipped(release):
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="release.shipped",
                    entity_type="release",
                    entity_id=release.id,
                    data={
                        **event_data,
                        "shipped_at": release.shipped_at.isoformat() if release.shipped_at else None,
                    },
                )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(release.id)

    async def update(
        self,
        release_id: int,
        data: ReleaseUpdateRequest,
    ) -> Optional[Release]:
        """Apply a partial release update."""
        release = await self.get_by_id(release_id)
        if not release:
            return None

        old_status = release.status
        update_data = data.model_dump(exclude_unset=True)
        if "task_ids" in update_data:
            release.tasks = await self._validate_task_ids(
                release.project_id,
                update_data.pop("task_ids") or [],
            )

        for field, value in update_data.items():
            setattr(release, field, self._enum_value(value))

        try:
            await self._emit_release_shipped_events(release)
            event_data = {
                "release_id": release.id,
                "project_id": release.project_id,
                "name": release.name,
                "status": release.status,
                "version": release.version,
                "environment": release.environment,
                "task_ids": [task.id for task in release.tasks],
                "changes": {
                    field: self._enum_value(value)
                    for field, value in update_data.items()
                },
            }
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="release.updated",
                entity_type="release",
                entity_id=release.id,
                data=event_data,
            )
            if old_status != ReleaseStatus.SHIPPED.value and self._is_shipped(release):
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="release.shipped",
                    entity_type="release",
                    entity_id=release.id,
                    data={
                        **event_data,
                        "from_status": old_status,
                        "shipped_at": release.shipped_at.isoformat() if release.shipped_at else None,
                    },
                )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(release.id)
