"""External link service."""

from app.authority import require_project
from app.commands import commit_or_flush
from typing import Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.external_link import ExternalLink, ExternalLinkEntityType as ModelExternalLinkEntityType
from app.models.release import Release
from app.models.task import Task
from app.schemas.external_link import (
    ExternalLinkCreate,
    ExternalLinkEntityType,
    ExternalLinkProvider,
    ExternalLinkResponse,
    ExternalLinkUpdate,
    TaskExternalLinkCreate,
    normalize_link_url,
)
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_context_revision_service import reserve_task_context_revision
from app.utils.github_links import GitHubLinkError, ParsedGitHubLink, parse_github_url


class ExternalLinkValidationError(ValueError):
    """Raised when a provider-specific link cannot be parsed."""


class ExternalLinkConflictError(Exception):
    """Raised when a provider-specific link already exists for an entity."""


class ExternalLinkService:
    """Service for generic external links and task-scoped link operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def parse_github_url(self, raw_url: str) -> ParsedGitHubLink:
        """Parse GitHub pull request, issue, branch, commit, and tag URLs."""
        try:
            return parse_github_url(raw_url)
        except GitHubLinkError as exc:
            raise ExternalLinkValidationError(str(exc)) from exc

    async def task_exists(self, task_id: int) -> bool:
        """Return whether a task exists."""
        result = await self.db.execute(select(Task.id).where(Task.id == task_id))
        return result.scalar_one_or_none() is not None

    async def list_for_entity(
        self,
        entity_type: str,
        entity_id: int,
    ) -> Sequence[ExternalLink]:
        """List links for a generic entity."""
        result = await self.db.execute(
            select(ExternalLink)
            .where(
                ExternalLink.entity_type == entity_type,
                ExternalLink.entity_id == entity_id,
            )
            .order_by(ExternalLink.created_at, ExternalLink.id)
        )
        return result.scalars().all()

    async def list_task_links(
        self,
        task_id: int,
    ) -> Optional[Sequence[ExternalLink]]:
        """List persisted external links for a task."""
        if not await self.task_exists(task_id):
            return None
        return await self.list_for_entity(ModelExternalLinkEntityType.TASK.value, task_id)

    async def get_by_id(self, link_id: int) -> Optional[ExternalLink]:
        """Get an external link by ID."""
        result = await self.db.execute(
            select(ExternalLink).where(ExternalLink.id == link_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        data: ExternalLinkCreate,
        *,
        commit: bool = True,
    ) -> ExternalLink:
        """Create a generic external link.

        An agdash session link with an external key is created once per entity:
        repeating it returns the existing link, so a retried publish never adds
        duplicates.
        """
        entity_type = self._enum_value(data.entity_type)
        provider = self._enum_value(data.provider)
        if provider == ExternalLinkProvider.AGDASH.value and data.external_key:
            existing = await self.db.scalar(select(ExternalLink).where(
                ExternalLink.entity_type == entity_type,
                ExternalLink.entity_id == data.entity_id,
                ExternalLink.provider == provider,
                ExternalLink.external_key == data.external_key,
            ).order_by(ExternalLink.id).limit(1))
            if existing is not None:
                return existing
        if entity_type == ModelExternalLinkEntityType.TASK.value:
            await reserve_task_context_revision(
                self.db,
                data.entity_id,
                context_kind="external_link",
                action="create",
            )
        link = ExternalLink(
            entity_type=entity_type,
            entity_id=data.entity_id,
            provider=self._enum_value(data.provider),
            external_key=data.external_key,
            url=data.url,
            title=data.title,
            status=data.status,
            metadata_json=data.metadata_json,
        )
        self.db.add(link)
        try:
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="external_link.created",
                entity_type=link.entity_type,
                entity_id=link.entity_id,
                data={
                    "external_link_id": link.id,
                    "entity_type": link.entity_type,
                    "entity_id": link.entity_id,
                    "provider": link.provider,
                    "external_key": link.external_key,
                    "url": link.url,
                },
            )
            if commit:
                await commit_or_flush(self.db)
                await self.db.refresh(link)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return link

    async def create_task_link(
        self,
        task_id: int,
        data: TaskExternalLinkCreate,
        *,
        commit: bool = True,
    ) -> Optional[ExternalLink]:
        """Create an external link for a task."""
        if not await self.task_exists(task_id):
            return None

        return await self.create(
            ExternalLinkCreate(
                entity_type=ExternalLinkEntityType.TASK,
                entity_id=task_id,
                provider=data.provider,
                external_key=data.external_key,
                url=data.url,
                title=data.title,
                status=data.status,
                metadata_json=data.metadata_json,
            ),
            commit=commit,
        )

    async def github_link_exists(
        self,
        task_id: int,
        parsed: ParsedGitHubLink,
        *,
        entity_type: str = ModelExternalLinkEntityType.TASK.value,
    ) -> bool:
        """Return whether the normalized GitHub link already exists for an entity."""
        result = await self.db.execute(
            select(ExternalLink.id).where(
                ExternalLink.entity_type == entity_type,
                ExternalLink.entity_id == task_id,
                ExternalLink.provider == ExternalLinkProvider.GITHUB.value,
                (
                    (ExternalLink.url == parsed.url)
                    | (ExternalLink.external_key == parsed.external_key)
                ),
            ).limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def _emit_github_created(
        self,
        link: ExternalLink,
        parsed: ParsedGitHubLink,
    ) -> None:
        data = {
            "external_link_id": link.id,
            "github_type": parsed.github_type,
            "repo_full_name": parsed.repo_full_name,
            "number": parsed.number,
            "branch": parsed.branch,
            "url": parsed.url,
        }
        if link.entity_type == ModelExternalLinkEntityType.TASK.value:
            data["task_id"] = link.entity_id
        else:
            data["entity_type"] = link.entity_type
            data["entity_id"] = link.entity_id
        await emit_outbound_webhook_event(
            self.db,
            commit=False,
            event_type="external_link.github_created",
            entity_type=link.entity_type,
            entity_id=link.entity_id,
            data=data,
        )

    async def create_release_github_link(
        self,
        release_id: int,
        url: str,
        *,
        commit: bool = True,
    ) -> Optional[ExternalLink]:
        """Parse and link a GitHub pull request, commit, branch, or tag to a release."""
        row = (await self.db.execute(select(Release.id, Release.project_id).where(Release.id == release_id))).first()
        if row is None:
            return None
        require_project(self.db, row.project_id, "edit")
        parsed = self.parse_github_url(url)
        release_type = ModelExternalLinkEntityType.RELEASE.value
        if await self.github_link_exists(release_id, parsed, entity_type=release_type):
            raise ExternalLinkConflictError("GitHub link already exists for this release")
        try:
            link = await self.create(
                ExternalLinkCreate(
                    entity_type=ExternalLinkEntityType.RELEASE,
                    entity_id=release_id,
                    provider=ExternalLinkProvider.GITHUB,
                    external_key=parsed.external_key,
                    url=parsed.url,
                    title=parsed.title,
                    status=None,
                    metadata_json=parsed.metadata_json,
                ),
                commit=False,
            )
            await self._emit_github_created(link, parsed)
            if commit:
                await commit_or_flush(self.db)
                await self.db.refresh(link)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return link

    async def record_work_github_links(
        self,
        task_id: int,
        urls: Sequence[str],
    ) -> list[ExternalLink]:
        """Link a worker's GitHub branch, commits, and pull request to its task.

        Runs inside a begin or submit command, which already validated the
        worker's fence and reserved the new task version, so recording the links
        reserves no other version and the worker's execute permission covers
        them. A URL already linked to the task is skipped, so a repeated submit
        adds nothing.
        """
        created: list[ExternalLink] = []
        for url in urls:
            parsed = self.parse_github_url(url)
            if await self.github_link_exists(task_id, parsed):
                continue
            link = ExternalLink(
                entity_type=ModelExternalLinkEntityType.TASK.value,
                entity_id=task_id,
                provider=ExternalLinkProvider.GITHUB.value,
                external_key=parsed.external_key,
                url=parsed.url,
                title=parsed.title,
                status=None,
                metadata_json=parsed.metadata_json,
            )
            self.db.info.setdefault("work_link_authorizations", set()).add((task_id, parsed.url))
            self.db.add(link)
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="external_link.created",
                entity_type=link.entity_type,
                entity_id=link.entity_id,
                data={
                    "external_link_id": link.id,
                    "entity_type": link.entity_type,
                    "entity_id": link.entity_id,
                    "provider": link.provider,
                    "external_key": link.external_key,
                    "url": link.url,
                },
            )
            await self._emit_github_created(link, parsed)
            created.append(link)
        return created

    async def create_task_github_link(
        self,
        task_id: int,
        url: str,
        *,
        commit: bool = True,
    ) -> Optional[ExternalLink]:
        """Parse and create a manual GitHub link for a task."""
        if not await self.task_exists(task_id):
            return None

        parsed = self.parse_github_url(url)
        if await self.github_link_exists(task_id, parsed):
            raise ExternalLinkConflictError("GitHub link already exists for this task")

        try:
            link = await self.create_task_link(
                task_id,
                TaskExternalLinkCreate(
                    provider=ExternalLinkProvider.GITHUB,
                    external_key=parsed.external_key,
                    url=parsed.url,
                    title=parsed.title,
                    status=None,
                    metadata_json=parsed.metadata_json,
                ),
                commit=False,
            )
            if link is None:
                return None
            await self._emit_github_created(link, parsed)
            if commit:
                await commit_or_flush(self.db)
                await self.db.refresh(link)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return link

    async def update(
        self,
        link_id: int,
        data: ExternalLinkUpdate,
    ) -> Optional[ExternalLink]:
        """Apply a partial external link update."""
        link = await self.get_by_id(link_id)
        if not link:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "provider" in update_data or "url" in update_data:
            # The URL rule depends on the provider, so check the resulting pair.
            provider = self._enum_value(update_data.get("provider", link.provider))
            try:
                normalize_link_url(update_data.get("url", link.url), provider)
            except ValueError as exc:
                raise ExternalLinkValidationError(str(exc)) from exc
        if update_data and link.entity_type == ModelExternalLinkEntityType.TASK.value:
            await reserve_task_context_revision(
                self.db,
                link.entity_id,
                context_kind="external_link",
                action="update",
                details={"external_link_id": link.id},
            )
        for field, value in update_data.items():
            setattr(link, field, self._enum_value(value))

        try:
            if update_data:
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="external_link.updated",
                    entity_type=link.entity_type,
                    entity_id=link.entity_id,
                    data={
                        "external_link_id": link.id,
                        "entity_type": link.entity_type,
                        "entity_id": link.entity_id,
                        "provider": link.provider,
                        "changes": {
                            field: self._enum_value(value)
                            for field, value in update_data.items()
                        },
                    },
                )
            await commit_or_flush(self.db)
            await self.db.refresh(link)
        except Exception:
            await self.db.rollback()
            raise
        return link

    async def delete_link(self, link_id: int, *, commit: bool = True) -> bool:
        """Delete an external link by ID."""
        link = await self.get_by_id(link_id)
        if not link:
            return False

        if link.entity_type == ModelExternalLinkEntityType.TASK.value:
            await reserve_task_context_revision(
                self.db,
                link.entity_id,
                context_kind="external_link",
                action="delete",
                details={"external_link_id": link.id},
            )

        event_data = {
            "external_link_id": link.id,
            "entity_type": link.entity_type,
            "entity_id": link.entity_id,
            "provider": link.provider,
            "external_key": link.external_key,
            "url": link.url,
        }
        await self.db.delete(link)
        try:
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="external_link.deleted",
                entity_type=event_data["entity_type"],
                entity_id=event_data["entity_id"],
                data=event_data,
            )
            if commit:
                await commit_or_flush(self.db)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return True

    async def delete_for_entity(self, entity_type: str, entity_id: int) -> None:
        """Delete all links for an entity."""
        await self.db.execute(
            delete(ExternalLink).where(
                ExternalLink.entity_type == entity_type,
                ExternalLink.entity_id == entity_id,
            )
        )

    def link_to_response(self, link: ExternalLink) -> ExternalLinkResponse:
        """Convert a persisted link into a response schema."""
        return ExternalLinkResponse(
            id=link.id,
            entity_type=link.entity_type,
            entity_id=link.entity_id,
            provider=link.provider,
            external_key=link.external_key,
            url=link.url,
            title=link.title,
            status=link.status,
            metadata_json=link.metadata_json or {},
            is_legacy=False,
            created_at=link.created_at,
            updated_at=link.updated_at,
        )

    def legacy_task_link_response(self, task: Task) -> Optional[ExternalLinkResponse]:
        """Represent legacy task source fields as one read-only external link."""
        if not (task.external_key or task.source_url or task.source):
            return None

        return ExternalLinkResponse(
            id=None,
            entity_type=ModelExternalLinkEntityType.TASK.value,
            entity_id=task.id,
            provider=task.source or "custom",
            external_key=task.external_key,
            url=task.source_url,
            title=task.external_key or task.source,
            status=None,
            metadata_json={},
            is_legacy=True,
            created_at=None,
            updated_at=None,
        )

    def task_links_to_response(
        self,
        task: Task,
        persisted_links: Sequence[ExternalLink],
    ) -> list[ExternalLinkResponse]:
        """Build task external link response list with legacy compatibility."""
        links = [self.link_to_response(link) for link in persisted_links]
        legacy_link = self.legacy_task_link_response(task)
        if legacy_link is not None:
            links.insert(0, legacy_link)
        return links
