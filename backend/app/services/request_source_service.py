"""Helpers for request source traceability."""
from typing import Optional, Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.request_source import RequestSource, RequestSourceLink, RequestSourceType
from app.models.task import Task
from app.models.triage import TriageItem
from app.schemas.request_source import (
    RequestSourceCreate,
    RequestSourceLinkCreateRequest,
    RequestSourceTargetType,
)
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_context_revision_service import reserve_task_context_revision
from app.sql_semantics import portable_contains


class RequestSourceValidationError(ValueError):
    """Raised when request-source input is invalid."""


class RequestSourceNotFoundError(LookupError):
    """Raised when a request source or link cannot be found."""


class RequestSourceTargetNotFoundError(LookupError):
    """Raised when a requested link target cannot be found."""


class RequestSourceConflictError(ValueError):
    """Raised when a source is already linked to the target."""


class RequestSourceService:
    """Small service for direct request-source link counts."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _normalize_target_type(
        self,
        target_type: RequestSourceTargetType | str,
    ) -> RequestSourceTargetType:
        """Convert API target type strings to the request-source target enum."""
        if isinstance(target_type, RequestSourceTargetType):
            return target_type
        try:
            return RequestSourceTargetType(target_type)
        except ValueError as exc:
            raise RequestSourceValidationError(f"Unsupported target type: {target_type}") from exc

    def _target_model_and_field(
        self,
        target_type: RequestSourceTargetType | str,
    ):
        """Return the ORM model and link column for a target type."""
        normalized = self._normalize_target_type(target_type)
        if normalized == RequestSourceTargetType.TASK:
            return Task, RequestSourceLink.task_id
        if normalized == RequestSourceTargetType.PROJECT:
            return Project, RequestSourceLink.project_id
        if normalized == RequestSourceTargetType.TRIAGE_ITEM:
            return TriageItem, RequestSourceLink.triage_item_id
        raise RequestSourceValidationError(f"Unsupported target type: {target_type}")

    async def _require_target_exists(
        self,
        target_type: RequestSourceTargetType | str,
        target_id: int,
    ) -> None:
        """Validate that a requested link target exists."""
        model, _ = self._target_model_and_field(target_type)
        result = await self.db.execute(select(model.id).where(model.id == target_id))
        if result.scalar_one_or_none() is None:
            raise RequestSourceTargetNotFoundError(
                f"{self._normalize_target_type(target_type).value} with id {target_id} not found"
            )

    async def _get_source_or_raise(self, request_source_id: int) -> RequestSource:
        """Load an existing request source or raise a 404-mapped error."""
        result = await self.db.execute(
            select(RequestSource).where(RequestSource.id == request_source_id)
        )
        source = result.scalar_one_or_none()
        if source is None:
            raise RequestSourceNotFoundError(
                f"Request source with id {request_source_id} not found"
            )
        return source

    def _source_from_payload(self, data: RequestSourceCreate) -> RequestSource:
        """Build a request source model from API data."""
        return RequestSource(
            title=data.title.strip(),
            description=data.description,
            source_type=self._enum_value(data.source_type),
            source_name=data.source_name,
            source_url=data.source_url,
            external_key=data.external_key,
            priority_hint=data.priority_hint,
        )

    def _source_type_from_triage(self, item: TriageItem) -> str:
        """Choose a request-source type for a triage-originated request."""
        source = (item.source or "").strip().lower().replace("-", "_")
        allowed = {source_type.value for source_type in RequestSourceType}
        return source if source in allowed else RequestSourceType.IMPORT.value

    def _source_from_triage_item(self, item: TriageItem) -> RequestSource:
        """Build a request source from a triage item."""
        return RequestSource(
            title=item.title,
            description=item.description,
            source_type=self._source_type_from_triage(item),
            source_name=item.source,
            source_url=item.source_url,
            external_key=item.external_key,
            priority_hint=item.priority_hint,
        )

    async def search_sources(
        self,
        q: Optional[str] = None,
        source_type: Optional[str] = None,
        limit: int = 20,
    ) -> Sequence[RequestSource]:
        """Search existing request sources for linking."""
        query = select(RequestSource)
        if q and q.strip():
            query = query.where(
                or_(
                    portable_contains(RequestSource.title, q),
                    portable_contains(RequestSource.description, q),
                    portable_contains(RequestSource.source_name, q),
                    portable_contains(RequestSource.source_url, q),
                    portable_contains(RequestSource.external_key, q),
                )
            )
        if source_type:
            normalized_source_type = self._enum_value(source_type)
            if normalized_source_type not in {source_type.value for source_type in RequestSourceType}:
                raise RequestSourceValidationError(
                    f"Unsupported source type: {normalized_source_type}"
                )
            query = query.where(RequestSource.source_type == normalized_source_type)

        result = await self.db.execute(
            query.order_by(RequestSource.created_at.desc(), RequestSource.id.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_link(self, link_id: int) -> Optional[RequestSourceLink]:
        """Load a request-source link with embedded source data."""
        result = await self.db.execute(
            select(RequestSourceLink)
            .options(selectinload(RequestSourceLink.request_source))
            .where(RequestSourceLink.id == link_id)
        )
        return result.scalar_one_or_none()

    async def list_links_for_target(
        self,
        target_type: RequestSourceTargetType | str,
        target_id: int,
    ) -> Sequence[RequestSourceLink]:
        """List request-source links for a target."""
        await self._require_target_exists(target_type, target_id)
        _, target_field = self._target_model_and_field(target_type)
        result = await self.db.execute(
            select(RequestSourceLink)
            .options(selectinload(RequestSourceLink.request_source))
            .where(target_field == target_id)
            .order_by(RequestSourceLink.created_at.desc(), RequestSourceLink.id.desc())
        )
        return result.scalars().all()

    async def create_link(
        self,
        data: RequestSourceLinkCreateRequest,
        *,
        commit: bool = True,
    ) -> RequestSourceLink:
        """Create a link from an existing or new request source."""
        await self._require_target_exists(data.target_type, data.target_id)
        _, target_field = self._target_model_and_field(data.target_type)
        if self._normalize_target_type(data.target_type) == RequestSourceTargetType.TASK:
            await reserve_task_context_revision(
                self.db,
                data.target_id,
                context_kind="request_source",
                action="link",
            )

        if data.request_source_id is not None:
            await self._get_source_or_raise(data.request_source_id)
            request_source_id = data.request_source_id
        elif data.request_source is not None:
            source = self._source_from_payload(data.request_source)
            self.db.add(source)
            await self.db.flush()
            request_source_id = source.id
        else:
            raise RequestSourceValidationError(
                "Set exactly one of request_source_id or request_source"
            )

        link = RequestSourceLink(request_source_id=request_source_id)
        setattr(link, target_field.key, data.target_id)
        self.db.add(link)

        try:
            await self.db.flush()
            link_id = link.id
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="request_source.linked",
                entity_type="request_source",
                entity_id=link.request_source_id,
                data={
                    "request_source_id": link.request_source_id,
                    "request_source_link_id": link_id,
                    "target_type": self._normalize_target_type(data.target_type).value,
                    "target_id": data.target_id,
                },
            )
            if not commit:
                return link
            await self.db.commit()
            loaded_link = await self.get_link(link_id)
            if loaded_link is None:
                raise RequestSourceNotFoundError(
                    f"Request source link with id {link_id} not found"
                )
            return loaded_link
        except IntegrityError as exc:
            if commit:
                await self.db.rollback()
            raise RequestSourceConflictError(
                "Request source is already linked to this target"
            ) from exc
        except Exception:
            if commit:
                await self.db.rollback()
            raise

    async def unlink(self, link_id: int, *, commit: bool = True) -> bool:
        """Remove a request-source link without deleting the source."""
        link = await self.get_link(link_id)
        if link is None:
            return False
        target_type = "task" if link.task_id else "project" if link.project_id else "triage_item"
        target_id = link.task_id or link.project_id or link.triage_item_id
        request_source_id = link.request_source_id
        if link.task_id is not None:
            await reserve_task_context_revision(
                self.db,
                link.task_id,
                context_kind="request_source",
                action="unlink",
                details={"request_source_link_id": link_id},
            )
        await self.db.delete(link)
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="request_source.unlinked",
                entity_type="request_source",
                entity_id=request_source_id,
                data={
                    "request_source_id": request_source_id,
                    "request_source_link_id": link_id,
                    "target_type": target_type,
                    "target_id": target_id,
                },
            )
            if commit:
                await self.db.commit()
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return True

    async def link_triage_item_as_task_request(
        self,
        item: TriageItem,
        task_id: int,
    ) -> RequestSourceLink:
        """Create a new request source from triage intake and link it to a task."""
        await reserve_task_context_revision(
            self.db,
            task_id,
            context_kind="request_source",
            action="link_from_triage",
            details={"triage_item_id": item.id},
        )
        source = self._source_from_triage_item(item)
        self.db.add(source)
        await self.db.flush()
        link = RequestSourceLink(request_source_id=source.id, task_id=task_id)
        self.db.add(link)
        await self.db.flush()
        return link

    async def copy_triage_links_to_task(self, triage_item_id: int, task_id: int) -> int:
        """Copy request-source links from a triage item to a newly converted task."""
        result = await self.db.execute(
            select(RequestSourceLink.request_source_id).where(
                RequestSourceLink.triage_item_id == triage_item_id,
            )
        )
        source_ids = [row[0] for row in result.fetchall()]
        if not source_ids:
            return 0

        existing_result = await self.db.execute(
            select(RequestSourceLink.request_source_id).where(
                RequestSourceLink.task_id == task_id,
                RequestSourceLink.request_source_id.in_(source_ids),
            )
        )
        existing_source_ids = {row[0] for row in existing_result.fetchall()}
        copied = 0
        if any(source_id not in existing_source_ids for source_id in source_ids):
            await reserve_task_context_revision(
                self.db,
                task_id,
                context_kind="request_source",
                action="copy_from_triage",
                details={"triage_item_id": triage_item_id},
            )
        for source_id in source_ids:
            if source_id in existing_source_ids:
                continue
            self.db.add(RequestSourceLink(request_source_id=source_id, task_id=task_id))
            copied += 1
        if copied:
            await self.db.flush()
        return copied

    async def count_for_task(self, task_id: int) -> int:
        """Count request sources directly linked to a task."""
        result = await self.db.execute(
            select(func.count(RequestSourceLink.id)).where(
                RequestSourceLink.task_id == task_id,
            )
        )
        return int(result.scalar() or 0)

    async def count_for_project(self, project_id: int) -> int:
        """Count request sources directly linked to a project."""
        result = await self.db.execute(
            select(func.count(RequestSourceLink.id)).where(
                RequestSourceLink.project_id == project_id,
            )
        )
        return int(result.scalar() or 0)

    async def count_for_triage_item(self, triage_item_id: int) -> int:
        """Count request sources directly linked to a triage item."""
        result = await self.db.execute(
            select(func.count(RequestSourceLink.id)).where(
                RequestSourceLink.triage_item_id == triage_item_id,
            )
        )
        return int(result.scalar() or 0)
