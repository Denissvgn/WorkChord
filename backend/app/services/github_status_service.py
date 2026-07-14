"""GitHub pull request status refresh service."""
from datetime import datetime, timezone
import logging
from typing import Any, Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.external_link import ExternalLink, ExternalLinkEntityType
from app.services.external_link_service import (
    ExternalLinkService,
    ExternalLinkValidationError,
)
from app.services.task_context_revision_service import reserve_task_context_revision
from app.utils.url_policy import normalize_provider_api_url


logger = logging.getLogger(__name__)


class GitHubStatusService:
    """Refresh cached GitHub pull request metadata for external links."""

    def __init__(
        self,
        db: AsyncSession,
        settings_override=None,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ):
        settings = settings_override or get_settings()
        self.db = db
        self.api_url = normalize_provider_api_url(settings.github_api_url).rstrip("/")
        self.token = settings.github_token
        self.timeout_seconds = settings.github_request_timeout_seconds
        self.transport = transport
        self.link_service = ExternalLinkService(db)

    @classmethod
    async def from_runtime(
        cls,
        db: AsyncSession,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> "GitHubStatusService":
        """Construct the service from DB-backed runtime GitHub settings."""
        from app.services.system_settings_service import RuntimeSettingsService

        settings = await RuntimeSettingsService(db).get_github_settings()
        return cls(db, settings_override=settings, transport=transport)

    def _now_iso(self) -> str:
        """Return an API-friendly UTC timestamp."""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _headers(self) -> dict[str, str]:
        """Build GitHub request headers."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "workchord",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _pr_metadata(self, link: ExternalLink) -> tuple[str, str, int]:
        """Extract GitHub PR identity from external link metadata."""
        metadata = link.metadata_json or {}
        if (
            link.provider != "github"
            or metadata.get("github_type") != "pull_request"
        ):
            raise ExternalLinkValidationError(
                "Only GitHub pull request links can be refreshed"
            )

        owner = metadata.get("owner")
        repo = metadata.get("repo")
        number = metadata.get("number")
        if isinstance(number, str) and number.isdigit():
            number = int(number)

        if not isinstance(owner, str) or not isinstance(repo, str) or not isinstance(number, int):
            raise ExternalLinkValidationError(
                "GitHub pull request link is missing owner, repo, or number metadata"
            )

        return owner, repo, number

    def status_from_payload(self, payload: dict[str, Any]) -> str:
        """Normalize GitHub PR state into the external link status field."""
        if payload.get("draft") is True:
            return "draft"
        if payload.get("merged") is True or payload.get("merged_at"):
            return "merged"
        if payload.get("state") == "closed":
            return "closed"
        return "open"

    async def _fetch_pull_request(
        self,
        owner: str,
        repo: str,
        number: int,
    ) -> dict[str, Any]:
        """Fetch one pull request payload from GitHub."""
        url = f"{self.api_url}/repos/{owner}/{repo}/pulls/{number}"
        client_kwargs: dict[str, Any] = {"timeout": self.timeout_seconds}
        if self.transport is not None:
            client_kwargs["transport"] = self.transport

        async with httpx.AsyncClient(**client_kwargs) as client:
            response = await client.get(url, headers=self._headers())

        if response.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"GitHub returned {response.status_code}",
                request=response.request,
                response=response,
            )

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("GitHub response was not a JSON object")
        return payload

    def _provider_error_message(self, error: Exception) -> str:
        """Convert provider exceptions into a safe cached message."""
        if isinstance(error, httpx.TimeoutException):
            return "GitHub request timed out"
        if isinstance(error, httpx.HTTPStatusError):
            return f"GitHub returned {error.response.status_code}"
        if isinstance(error, httpx.RequestError):
            return "GitHub request failed"
        return str(error) or "GitHub refresh failed"

    async def _save_link(self, link: ExternalLink) -> ExternalLink:
        """Persist changed link fields."""
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def _reserve_task_context_revision(
        self,
        link: ExternalLink,
        *,
        outcome: str,
    ) -> None:
        """Fence a task assignment before provider data dirties its linked context."""
        if link.entity_type != ExternalLinkEntityType.TASK.value:
            return
        await reserve_task_context_revision(
            self.db,
            link.entity_id,
            context_kind="external_link",
            action="github_status_refresh",
            details={"external_link_id": link.id, "outcome": outcome},
        )

    async def refresh_pull_request_status(self, link_id: int) -> Optional[ExternalLink]:
        """Refresh a GitHub PR link and cache status metadata.

        Provider failures are cached on the link and returned as a successful
        response so task loading and link display remain resilient.
        """
        link = await self.link_service.get_by_id(link_id)
        if not link:
            return None

        owner, repo, number = self._pr_metadata(link)
        metadata = dict(link.metadata_json or {})
        refreshed_at = self._now_iso()

        try:
            payload = await self._fetch_pull_request(owner, repo, number)
        except Exception as error:
            # GitHub availability must not make linked tasks unreadable. Cache a
            # redacted provider error and retain the prior link status.
            logger.warning(
                "GitHub pull-request refresh failed",
                exc_info=True,
                extra={"link_id": link_id, "owner": owner, "repo": repo, "number": number},
            )
            await self._reserve_task_context_revision(link, outcome="provider_error")
            metadata["status_refreshed_at"] = refreshed_at
            metadata["status_refresh_error"] = self._provider_error_message(error)
            link.metadata_json = metadata
            return await self._save_link(link)

        status = self.status_from_payload(payload)
        await self._reserve_task_context_revision(link, outcome="refreshed")
        title = payload.get("title")
        if isinstance(title, str) and title:
            link.title = title
        link.status = status

        metadata.update({
            "github_state": payload.get("state"),
            "draft": payload.get("draft"),
            "merged": payload.get("merged"),
            "mergeable": payload.get("mergeable"),
            "mergeable_state": payload.get("mergeable_state"),
            "github_updated_at": payload.get("updated_at"),
            "status_refreshed_at": refreshed_at,
        })
        metadata.pop("status_refresh_error", None)
        link.metadata_json = metadata

        return await self._save_link(link)
