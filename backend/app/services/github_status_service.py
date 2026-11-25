"""GitHub pull request status refresh service."""

from app.commands import commit_or_flush
from datetime import datetime, timezone
import logging
import re
from typing import Any, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.external_link import ExternalLink, ExternalLinkEntityType
from app.services.external_link_service import (
    ExternalLinkService,
    ExternalLinkValidationError,
)
from app.models.agent import TaskEvent
from app.services.task_context_revision_service import reserve_task_context_revision
from app.utils.url_policy import normalize_provider_api_url


logger = logging.getLogger(__name__)

_FAILED_CONCLUSIONS = {"failure", "timed_out", "cancelled", "action_required", "startup_failure", "stale"}


def parse_github_time(value: Any) -> Optional[datetime]:
    """Parse a GitHub ISO timestamp, or None when it is absent or malformed."""
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def payload_merged(payload: dict[str, Any]) -> bool:
    """Whether a pull request payload describes a merged pull request."""
    return bool(payload.get("merged") or payload.get("merged_at"))


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

    @staticmethod
    def observation_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
        """The head, target and closure facts a pull request payload states.

        GitHub fills ``merge_commit_sha`` with a provisional test merge for an
        open pull request, so it counts only once the pull request is merged.
        """
        head = payload.get("head") if isinstance(payload.get("head"), dict) else {}
        base = payload.get("base") if isinstance(payload.get("base"), dict) else {}
        merged = payload_merged(payload)
        return {
            "head_sha": head.get("sha"),
            "head_ref": head.get("ref"),
            "base_ref": base.get("ref"),
            "merged": merged,
            "merge_commit_sha": payload.get("merge_commit_sha") if merged else None,
            "merged_at": payload.get("merged_at"),
            "closed_at": payload.get("closed_at"),
            "github_updated_at": payload.get("updated_at"),
        }

    @staticmethod
    def is_stale_observation(metadata: dict[str, Any], payload: dict[str, Any]) -> bool:
        """Whether a payload is older than what the link already records.

        Deliveries can repeat or arrive out of order. A merge never reverts, and
        a payload last updated before the recorded state must not replace it.
        """
        if metadata.get("merged") and not payload_merged(payload):
            return True
        recorded = parse_github_time(metadata.get("github_updated_at"))
        incoming = parse_github_time(payload.get("updated_at"))
        return bool(recorded and incoming and incoming < recorded)

    @staticmethod
    def checks_from_runs(runs_payload: Any) -> dict[str, Any]:
        """Summarize the check runs GitHub reports for one commit."""
        runs = runs_payload.get("check_runs") if isinstance(runs_payload, dict) else None
        if not isinstance(runs, list):
            return {"checks_state": "unknown", "checks_total": None}
        if not runs:
            return {"checks_state": "none", "checks_total": 0}
        if any(run.get("status") != "completed" for run in runs):
            state = "pending"
        elif any(run.get("conclusion") in _FAILED_CONCLUSIONS for run in runs):
            state = "failure"
        else:
            state = "success"
        return {"checks_state": state, "checks_total": len(runs)}

    async def observe_checks(self, owner: str, repo: str, head_sha: Any) -> dict[str, Any]:
        """Read the checks of the observed head; a read failure is recorded, not raised."""
        if not isinstance(head_sha, str) or not head_sha:
            return {"checks_state": "unknown", "checks_total": None, "checks_sha": None}
        try:
            runs = await self._fetch_resource(
                f"{self.api_url}/repos/{owner}/{repo}/commits/{head_sha}/check-runs?per_page=100"
            )
        except Exception as error:
            return {
                "checks_state": "unknown",
                "checks_total": None,
                "checks_sha": head_sha,
                "checks_error": self._provider_error_message(error),
            }
        return {**self.checks_from_runs(runs), "checks_sha": head_sha, "checks_error": None}

    @staticmethod
    def observed_closure_key(link_id: int, status: str, observation: dict[str, Any]) -> str:
        """The identity of one merge or unmerged closure of a linked pull request."""
        marker = observation.get("merge_commit_sha") or observation.get("closed_at") or status
        return f"github-observed:{link_id}:{status}:{marker}"

    async def lock_link_after_task(self, link_id: int) -> Optional[ExternalLink]:
        """Re-read a link under a row lock, discarding any cached copy.

        Callers take the task context lock first (iteration, task, then link,
        the order link edits use), so concurrent catch-ups and webhooks for one
        link see each other's committed status and closure events.
        """
        return await self.db.scalar(
            select(ExternalLink)
            .where(ExternalLink.id == link_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )

    async def _record_observed_closure(self, link: ExternalLink, status: str, observation: dict[str, Any]) -> None:
        """Record a merge or unmerged closure seen by catch-up as a GitHub task event, once."""
        if link.entity_type != ExternalLinkEntityType.TASK.value or status not in {"merged", "closed"}:
            return
        key = self.observed_closure_key(link.id, status, observation)
        if await self.db.scalar(select(TaskEvent.id).where(TaskEvent.idempotency_key == key)):
            return
        from app.services.task_service import TaskService

        number = (link.metadata_json or {}).get("number")
        await TaskService(self.db).record_task_event(
            link.entity_id,
            "github_pr_merged" if status == "merged" else "github_pr_closed",
            {
                "summary": f"GitHub PR #{number} {'merged' if status == 'merged' else 'closed without merging'} (observed by refresh)",
                "provider": "github",
                "github_event": "pull_request",
                "observed_by": "refresh",
                "status": status,
                "pr_number": number,
                "url": link.url,
                "head_sha": observation.get("head_sha"),
                "merge_commit_sha": observation.get("merge_commit_sha"),
                "external_link_id": link.id,
                "artifact_links": [link.url] if link.url else [],
            },
            actor_type="github",
            idempotency_key=key,
        )

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
    def _check_review_commits(commits, count, expected_sha, attributed_commits, failure_context=None):
        if len(commits) != count or not commits or commits[-1].get("sha") != expected_sha:
            return "verification_candidate_stale"
        seen = set()
        for item in commits:
            sha = item.get("sha")
            if not isinstance(sha, str) or re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", sha) is None:
                return "verification_candidate_unverifiable"
            if sha in seen or not attributed_commits.get(sha):
                if failure_context is not None:
                    failure_context.update(offending_sha=sha, attribution_gap="commit_attribution")
                return "verification_contributors_unverifiable"
            seen.add(sha)
            message = item.get("commit", {}).get("message")
            if not isinstance(message, str) or any(line.strip().casefold().startswith("co-authored-by:") for line in message.splitlines()):
                if failure_context is not None:
                    failure_context.update(offending_sha=sha, attribution_gap="coauthor_trailer" if isinstance(message, str) else "commit_metadata")
                return "verification_contributors_unverifiable"
        return None

    async def verify_review_range(self, base, head, attributed_commits, *, failure_context=None):
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
                return self._check_review_commits(commits, count, head.sha, attributed_commits, failure_context)
        return "verification_candidate_unverifiable"

    async def verify_review_head(self, pr, expected_sha, attributed_commits, *, expected_repository=None, failure_context=None):
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
        blocker = self._check_review_commits(commits, count, expected_sha, attributed_commits, failure_context)
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

        observation = self.observation_from_payload(payload)
        checks = await self.observe_checks(owner, repo, observation["head_sha"])
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
        if self.is_stale_observation(metadata, payload):
            # A webhook already recorded something newer; keep it and note the check.
            metadata["status_refreshed_at"] = refreshed_at
            metadata["observed_at"] = refreshed_at
            link.metadata_json = metadata
            return await self._save_link(link)
        await self._reserve_task_context_revision(link, outcome="refreshed")
        # Another catch-up or a webhook may have recorded this observation while
        # this one waited for the lock; decide from what it committed.
        link = await self.lock_link_after_task(link_id)
        if link is None:
            await self.db.rollback()
            return None
        if self._pr_metadata(link) != (owner, repo, number):
            raise ExternalLinkValidationError(
                "GitHub pull request link changed during refresh"
            )
        metadata = dict(link.metadata_json or {})
        if self.is_stale_observation(metadata, payload):
            metadata["status_refreshed_at"] = refreshed_at
            metadata["observed_at"] = refreshed_at
            link.metadata_json = metadata
            return await self._save_link(link)
        previous_status = link.status
        title = payload.get("title")
        if isinstance(title, str) and title:
            link.title = title
        link.status = status

        metadata.update({
            "github_state": payload.get("state"),
            "draft": payload.get("draft"),
            "mergeable": payload.get("mergeable"),
            "mergeable_state": payload.get("mergeable_state"),
            "status_refreshed_at": refreshed_at,
            "observed_at": refreshed_at,
            "observation_source": "refresh",
            **observation,
            **checks,
        })
        metadata.pop("status_refresh_error", None)
        link.metadata_json = metadata
        if previous_status != status:
            await self._record_observed_closure(link, status, observation)

        return await self._save_link(link)
