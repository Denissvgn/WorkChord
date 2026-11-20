"""GitHub pull request status refresh service."""

from app.commands import commit_or_flush
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
        payload = await self._fetch_pr_resource(owner, repo, number)
        if not isinstance(payload, dict):
            raise ValueError("GitHub response was not a JSON object")
        return payload

    async def _fetch_pr_resource(self, owner, repo, number, suffix=""):
        url = f"{self.api_url}/repos/{owner}/{repo}/pulls/{number}{suffix}"
        return await self._fetch_resource(url)

    async def _fetch_resource(self, url):
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

        return response.json()

    @staticmethod
    def _check_review_commits(commits, count, expected_sha, attributed_commits):
        if len(commits) != count or not commits or commits[-1].get("sha") != expected_sha:
            return "verification_candidate_stale"
        seen = set()
        for item in commits:
            sha = item.get("sha")
            if sha in seen or not attributed_commits.get(sha):
                return "verification_contributors_unverifiable"
            seen.add(sha)
            message = item.get("commit", {}).get("message")
            if not isinstance(message, str) or any(line.strip().casefold().startswith("co-authored-by:") for line in message.splitlines()):
                return "verification_contributors_unverifiable"
        return None

    async def verify_review_range(self, base, head, attributed_commits):
        """Verify every commit after the submitted immutable base."""
        endpoint = f"{self.api_url}/repos/{head.owner}/{head.repo}/compare/{base.sha}...{head.sha}"
        commits = []
        expected_count = None
        for page in range(1, 4):
            comparison = await self._fetch_resource(f"{endpoint}?per_page=100&page={page}")
            count = comparison.get("total_commits")
            if (comparison.get("status") != "ahead" or comparison.get("base_commit", {}).get("sha") != base.sha
                    or comparison.get("merge_base_commit", {}).get("sha") != base.sha
                    or type(count) is not int or not 0 < count <= 250
                    or expected_count is not None and expected_count != count):
                return "verification_candidate_unverifiable"
            expected_count = count
            batch = comparison.get("commits")
            if not isinstance(batch, list):
                return "verification_candidate_unverifiable"
            commits.extend(batch)
            if len(commits) >= count:
                return self._check_review_commits(commits, count, head.sha, attributed_commits)
        return "verification_candidate_unverifiable"

    async def verify_review_head(self, pr, expected_sha, attributed_commits, *, expected_repository=None):
        """Observe the exact PR candidate and flag additional, unbound authors."""
        pull = await self._fetch_pull_request(pr.owner, pr.repo, pr.number)
        if pull.get("head", {}).get("sha") != expected_sha:
            return "verification_candidate_stale"
        if expected_repository and expected_repository.casefold() != pr.repo_full_name.casefold():
            if (pull.get("head", {}).get("repo") or {}).get("full_name", "").casefold() != expected_repository.casefold():
                return "verification_candidate_stale"
        count = pull.get("commits")
        if type(count) is not int or not 0 < count <= 250:
            return "verification_contributors_unverifiable"
        commits = []
        for page in range(1, (count + 99) // 100 + 1):
            batch = await self._fetch_pr_resource(pr.owner, pr.repo, pr.number, f"/commits?per_page=100&page={page}")
            if not isinstance(batch, list):
                return "verification_candidate_unverifiable"
            commits.extend(batch)
        blocker = self._check_review_commits(commits, count, expected_sha, attributed_commits)
        if blocker:
            return blocker
        current = await self._fetch_pull_request(pr.owner, pr.repo, pr.number)
        return None if current.get("head", {}).get("sha") == expected_sha else "verification_candidate_stale"

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
        await commit_or_flush(self.db)
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
        refreshed_at = self._now_iso()
        # The provider request needs only immutable plain values. Release the
        # read transaction before crossing the network boundary.
        await self.db.rollback()

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
            link = await self.link_service.get_by_id(link_id)
            if link is None:
                return None
            metadata = dict(link.metadata_json or {})
            await self._reserve_task_context_revision(link, outcome="provider_error")
            metadata["status_refreshed_at"] = refreshed_at
            metadata["status_refresh_error"] = self._provider_error_message(error)
            link.metadata_json = metadata
            return await self._save_link(link)

        link = await self.link_service.get_by_id(link_id)
        if link is None:
            return None
        # Revalidate the target after the external wait so a concurrent edit
        # cannot redirect the fetched payload onto a different link.
        if self._pr_metadata(link) != (owner, repo, number):
            raise ExternalLinkValidationError(
                "GitHub pull request link changed during refresh"
            )
        metadata = dict(link.metadata_json or {})
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
