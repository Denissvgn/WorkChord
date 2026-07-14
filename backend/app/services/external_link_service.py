"""External link service."""
from dataclasses import dataclass
from typing import Any, Optional, Sequence
from urllib.parse import urlparse

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.external_link import ExternalLink, ExternalLinkEntityType as ModelExternalLinkEntityType
from app.models.task import Task
from app.schemas.external_link import (
    ExternalLinkCreate,
    ExternalLinkEntityType,
    ExternalLinkProvider,
    ExternalLinkResponse,
    ExternalLinkUpdate,
    TaskExternalLinkCreate,
)
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_context_revision_service import reserve_task_context_revision


class ExternalLinkValidationError(ValueError):
    """Raised when a provider-specific link cannot be parsed."""


class ExternalLinkConflictError(Exception):
    """Raised when a provider-specific link already exists for an entity."""


@dataclass(frozen=True)
class ParsedGitHubLink:
    """Normalized GitHub link details ready for persistence."""

    github_type: str
    owner: str
    repo: str
    repo_full_name: str
    number: Optional[int]
    branch: Optional[str]
    external_key: str
    url: str
    title: str

    @property
    def metadata_json(self) -> dict[str, Any]:
        """Return the public metadata stored with the external link."""
        metadata: dict[str, Any] = {
            "github_type": self.github_type,
            "owner": self.owner,
            "repo": self.repo,
            "repo_full_name": self.repo_full_name,
        }
        if self.number is not None:
            metadata["number"] = self.number
        if self.branch is not None:
            metadata["branch"] = self.branch
        return metadata


class ExternalLinkService:
    """Service for generic external links and task-scoped link operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _enum_value(self, value):
        """Normalize enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def parse_github_url(self, raw_url: str) -> ParsedGitHubLink:
        """Parse common GitHub PR, issue, and branch URLs."""
        url = raw_url.strip()
        if not url:
            raise ExternalLinkValidationError("GitHub URL is required")

        parsed = urlparse(url if "://" in url else f"https://{url}")
        hostname = (parsed.hostname or "").lower()
        if parsed.scheme not in {"http", "https"} or hostname not in {
            "github.com",
            "www.github.com",
        }:
            raise ExternalLinkValidationError(
                "Only GitHub PR, issue, and branch URLs are supported"
            )

        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) < 4:
            raise ExternalLinkValidationError(
                "Only GitHub PR, issue, and branch URLs are supported"
            )

        owner, repo, link_type = parts[0], parts[1], parts[2]
        repo_full_name = f"{owner}/{repo}"

        if link_type == "pull" and parts[3].isdigit():
            number = int(parts[3])
            normalized_url = f"https://github.com/{repo_full_name}/pull/{number}"
            return ParsedGitHubLink(
                github_type="pull_request",
                owner=owner,
                repo=repo,
                repo_full_name=repo_full_name,
                number=number,
                branch=None,
                external_key=f"{repo_full_name}#{number}",
                url=normalized_url,
                title=f"{repo_full_name} PR #{number}",
            )

        if link_type == "issues" and parts[3].isdigit():
            number = int(parts[3])
            normalized_url = f"https://github.com/{repo_full_name}/issues/{number}"
            return ParsedGitHubLink(
                github_type="issue",
                owner=owner,
                repo=repo,
                repo_full_name=repo_full_name,
                number=number,
                branch=None,
                external_key=f"{repo_full_name}#{number}",
                url=normalized_url,
                title=f"{repo_full_name} issue #{number}",
            )

        if link_type == "tree":
            branch = "/".join(parts[3:]).strip("/")
            if branch:
                normalized_url = f"https://github.com/{repo_full_name}/tree/{branch}"
                return ParsedGitHubLink(
                    github_type="branch",
                    owner=owner,
                    repo=repo,
                    repo_full_name=repo_full_name,
                    number=None,
                    branch=branch,
                    external_key=f"{repo_full_name}@{branch}",
                    url=normalized_url,
                    title=f"{repo_full_name} branch {branch}",
                )

        raise ExternalLinkValidationError(
            "Only GitHub PR, issue, and branch URLs are supported"
        )

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
        """Create a generic external link."""
        entity_type = self._enum_value(data.entity_type)
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
                await self.db.commit()
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
    ) -> bool:
        """Return whether the normalized GitHub link already exists for a task."""
        result = await self.db.execute(
            select(ExternalLink.id).where(
                ExternalLink.entity_type == ModelExternalLinkEntityType.TASK.value,
                ExternalLink.entity_id == task_id,
                ExternalLink.provider == ExternalLinkProvider.GITHUB.value,
                (
                    (ExternalLink.url == parsed.url)
                    | (ExternalLink.external_key == parsed.external_key)
                ),
            )
        )
        return result.scalar_one_or_none() is not None

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
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="external_link.github_created",
                entity_type="task",
                entity_id=task_id,
                data={
                    "external_link_id": link.id,
                    "task_id": task_id,
                    "github_type": parsed.github_type,
                    "repo_full_name": parsed.repo_full_name,
                    "number": parsed.number,
                    "branch": parsed.branch,
                    "url": parsed.url,
                },
            )
            if commit:
                await self.db.commit()
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
            await self.db.commit()
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
                await self.db.commit()
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
