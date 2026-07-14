"""GitHub webhook intake service."""
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.agent import TaskEvent
from app.models.external_link import ExternalLink, ExternalLinkEntityType
from app.models.triage import TriageItem
from app.schemas.github import GitHubWebhookResponse
from app.services.github_status_automation_service import GitHubStatusAutomationService
from app.schemas.triage import TriageItemCreate
from app.services.github_status_service import GitHubStatusService
from app.services.language_service import LanguageCode, localized, resolve_runtime_ui_language
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.task_context_revision_service import reserve_task_context_revision
from app.services.task_service import TaskService
from app.services.triage_service import TriageService


SUPPORTED_PULL_REQUEST_ACTIONS = {
    "opened",
    "edited",
    "reopened",
    "synchronize",
    "ready_for_review",
    "converted_to_draft",
    "closed",
}


class GitHubWebhookConfigurationError(RuntimeError):
    """Raised when webhook processing is not configured."""


class GitHubWebhookSignatureError(ValueError):
    """Raised when a webhook signature is missing or invalid."""


class GitHubWebhookPayloadError(ValueError):
    """Raised when a webhook payload cannot be processed."""


class GitHubWebhookService:
    """Verify and process GitHub webhook deliveries."""

    def __init__(self, db: AsyncSession, settings_override=None):
        settings = settings_override or get_settings()
        self.db = db
        self.webhook_secret = settings.github_webhook_secret
        self.create_triage_for_unmatched = settings.github_webhook_create_triage_for_unmatched
        self.task_service = TaskService(db)
        self.triage_service = TriageService(db)
        self.status_service = GitHubStatusService(db, settings_override=settings)
        self.automation_service = GitHubStatusAutomationService(db)

    @classmethod
    async def from_runtime(cls, db: AsyncSession) -> "GitHubWebhookService":
        """Construct the service from DB-backed runtime GitHub settings."""
        from app.services.system_settings_service import RuntimeSettingsService

        settings = await RuntimeSettingsService(db).get_github_settings()
        return cls(db, settings_override=settings)

    def verify_signature(self, body: bytes, signature_header: Optional[str]) -> None:
        """Verify the GitHub HMAC SHA-256 signature."""
        if not self.webhook_secret:
            raise GitHubWebhookConfigurationError("GitHub webhook secret is not configured")
        if not signature_header or not signature_header.startswith("sha256="):
            raise GitHubWebhookSignatureError("Missing GitHub webhook signature")

        digest = hmac.new(
            self.webhook_secret.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()
        expected = f"sha256={digest}"
        if not hmac.compare_digest(expected, signature_header):
            raise GitHubWebhookSignatureError("Invalid GitHub webhook signature")

    def parse_payload(self, body: bytes) -> dict[str, Any]:
        """Parse a JSON webhook body."""
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GitHubWebhookPayloadError("GitHub webhook payload must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise GitHubWebhookPayloadError("GitHub webhook payload must be a JSON object")
        return payload

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _repository_full_name(self, payload: dict[str, Any]) -> str:
        repo = payload.get("repository")
        if not isinstance(repo, dict):
            raise GitHubWebhookPayloadError("GitHub pull request payload is missing repository")

        full_name = repo.get("full_name")
        if isinstance(full_name, str) and "/" in full_name:
            return full_name

        owner = repo.get("owner")
        owner_login = owner.get("login") if isinstance(owner, dict) else None
        repo_name = repo.get("name")
        if isinstance(owner_login, str) and isinstance(repo_name, str):
            return f"{owner_login}/{repo_name}"

        raise GitHubWebhookPayloadError("GitHub pull request payload is missing repository full_name")

    def _pull_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        pr = payload.get("pull_request")
        if not isinstance(pr, dict):
            raise GitHubWebhookPayloadError("GitHub payload is missing pull_request")
        return pr

    def _pull_request_number(self, pr: dict[str, Any]) -> int:
        number = pr.get("number")
        if not isinstance(number, int):
            raise GitHubWebhookPayloadError("GitHub pull request payload is missing number")
        return number

    def _external_key(self, repo_full_name: str, number: int) -> str:
        return f"{repo_full_name}#{number}"

    def _sender_login(self, payload: dict[str, Any]) -> Optional[str]:
        sender = payload.get("sender")
        login = sender.get("login") if isinstance(sender, dict) else None
        return login if isinstance(login, str) else None

    def _pull_request_url(self, pr: dict[str, Any], repo_full_name: str, number: int) -> str:
        url = pr.get("html_url")
        return url if isinstance(url, str) and url else f"https://github.com/{repo_full_name}/pull/{number}"

    def _event_type(self, action: str, status: str) -> str:
        if action == "closed" and status == "merged":
            return "github_pr_merged"
        return f"github_pr_{action}"

    async def _matching_link(self, repo_full_name: str, number: int) -> Optional[ExternalLink]:
        external_key = self._external_key(repo_full_name, number)
        result = await self.db.execute(
            select(ExternalLink).where(
                ExternalLink.entity_type == ExternalLinkEntityType.TASK.value,
                ExternalLink.provider == "github",
                ExternalLink.external_key == external_key,
            ).order_by(ExternalLink.id)
        )
        for link in result.scalars().all():
            metadata = link.metadata_json or {}
            if metadata.get("github_type") == "pull_request":
                return link

        fallback_result = await self.db.execute(
            select(ExternalLink).where(
                ExternalLink.entity_type == ExternalLinkEntityType.TASK.value,
                ExternalLink.provider == "github",
            ).order_by(ExternalLink.id)
        )
        for link in fallback_result.scalars().all():
            metadata = link.metadata_json or {}
            if (
                metadata.get("github_type") == "pull_request"
                and metadata.get("repo_full_name") == repo_full_name
                and metadata.get("number") == number
            ):
                return link
        return None

    async def _event_exists(self, delivery_id: Optional[str]) -> bool:
        if not delivery_id:
            return False
        result = await self.db.execute(
            select(TaskEvent.id).where(TaskEvent.idempotency_key == delivery_id)
        )
        return result.scalar_one_or_none() is not None

    def _event_payload(
        self,
        *,
        action: str,
        delivery_id: Optional[str],
        repo_full_name: str,
        number: int,
        url: str,
        title: str,
        status: str,
        sender: Optional[str],
        link_id: int,
        pr: dict[str, Any],
        ui_language: LanguageCode,
    ) -> dict[str, Any]:
        action_label = action.replace("_", " ")
        summary = localized(
            ui_language,
            f"GitHub PR #{number} {action_label}: {title}",
            f"GitHub PR #{number}, событие {action_label}: {title}",
        )
        return {
            "summary": summary,
            "provider": "github",
            "github_event": "pull_request",
            "action": action,
            "repo": repo_full_name,
            "pr_number": number,
            "url": url,
            "status": status,
            "delivery_id": delivery_id,
            "sender": sender,
            "external_link_id": link_id,
            "github_updated_at": pr.get("updated_at"),
            "artifact_links": [url],
            "artifact_label": f"PR #{number}",
        }

    async def _update_link_from_pr(
        self,
        link: ExternalLink,
        *,
        action: str,
        delivery_id: Optional[str],
        repo_full_name: str,
        pr: dict[str, Any],
        sender: Optional[str],
    ) -> str:
        await reserve_task_context_revision(
            self.db,
            link.entity_id,
            context_kind="external_link",
            action="github_webhook_update",
            details={
                "external_link_id": link.id,
                "delivery_id": delivery_id,
                "webhook_action": action,
            },
        )
        status = self.status_service.status_from_payload(pr)
        title = pr.get("title")
        if isinstance(title, str) and title:
            link.title = title
        link.status = status

        metadata = dict(link.metadata_json or {})
        metadata.update({
            "github_type": "pull_request",
            "repo_full_name": repo_full_name,
            "owner": repo_full_name.split("/", 1)[0],
            "repo": repo_full_name.split("/", 1)[1],
            "number": pr.get("number"),
            "github_state": pr.get("state"),
            "draft": pr.get("draft"),
            "merged": pr.get("merged") or bool(pr.get("merged_at")),
            "mergeable": pr.get("mergeable"),
            "mergeable_state": pr.get("mergeable_state"),
            "github_updated_at": pr.get("updated_at"),
            "webhook_delivery_id": delivery_id,
            "webhook_action": action,
            "webhook_sender": sender,
            "webhook_received_at": self._now_iso(),
        })
        metadata.pop("status_refresh_error", None)
        link.metadata_json = metadata
        return status

    async def _existing_triage_item(self, external_key: str) -> Optional[TriageItem]:
        result = await self.db.execute(
            select(TriageItem).where(
                TriageItem.source == "github-webhook",
                TriageItem.external_key == external_key,
            ).order_by(TriageItem.id)
        )
        return result.scalars().first()

    async def _create_or_get_triage_item(
        self,
        *,
        external_key: str,
        repo_full_name: str,
        number: int,
        title: str,
        url: str,
        action: str,
        status: str,
        sender: Optional[str],
    ) -> TriageItem:
        existing = await self._existing_triage_item(external_key)
        if existing:
            return existing

        ui_language = await resolve_runtime_ui_language(self.db)
        description = localized(
            ui_language,
            (
                f"Unmatched GitHub pull request webhook for {repo_full_name}#{number}.\n\n"
                f"Action: {action}\n"
                f"Status: {status}\n"
                f"Sender: {sender or 'unknown'}\n"
                f"URL: {url}"
            ),
            (
                f"Непривязанный GitHub pull request webhook для {repo_full_name}#{number}.\n\n"
                f"Action: {action}\n"
                f"Status: {status}\n"
                f"Sender: {sender or 'unknown'}\n"
                f"URL: {url}"
            ),
        )
        return await self.triage_service.create(
            TriageItemCreate(
                title=title,
                description=description,
                source="github-webhook",
                source_url=url,
                external_key=external_key,
                labels=["github", "pull-request"],
            ),
            commit=False,
        )

    async def process(
        self,
        event: str,
        delivery_id: Optional[str],
        payload: dict[str, Any],
    ) -> GitHubWebhookResponse:
        """Process one verified GitHub webhook payload."""
        if event == "ping":
            return GitHubWebhookResponse(
                accepted=True,
                event=event,
                action="ping",
                matched=False,
                ignored_reason="ping",
            )

        if event != "pull_request":
            return GitHubWebhookResponse(
                accepted=True,
                event=event,
                action=str(payload.get("action")) if payload.get("action") else None,
                matched=False,
                ignored_reason="unsupported_event",
            )

        action = payload.get("action")
        action = action if isinstance(action, str) else ""
        if action not in SUPPORTED_PULL_REQUEST_ACTIONS:
            return GitHubWebhookResponse(
                accepted=True,
                event=event,
                action=action or None,
                matched=False,
                ignored_reason="unsupported_action",
            )

        pr = self._pull_request(payload)
        repo_full_name = self._repository_full_name(payload)
        number = self._pull_request_number(pr)
        external_key = self._external_key(repo_full_name, number)
        raw_title = pr.get("title")
        title: str = (
            raw_title
            if isinstance(raw_title, str) and raw_title.strip()
            else f"{repo_full_name} PR #{number}"
        )
        url = self._pull_request_url(pr, repo_full_name, number)
        sender = self._sender_login(payload)
        status = self.status_service.status_from_payload(pr)
        ui_language = await resolve_runtime_ui_language(self.db)

        link = await self._matching_link(repo_full_name, number)
        if not link:
            if not self.create_triage_for_unmatched:
                return GitHubWebhookResponse(
                    accepted=True,
                    event=event,
                    action=action,
                    matched=False,
                    ignored_reason="no_matching_external_link",
                )

            try:
                item = await self._create_or_get_triage_item(
                    external_key=external_key,
                    repo_full_name=repo_full_name,
                    number=number,
                    title=title,
                    url=url,
                    action=action,
                    status=status,
                    sender=sender,
                )
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type=f"github.pr_{action}",
                    entity_type="triage_item",
                    entity_id=item.id,
                    data={
                        "triage_item_id": item.id,
                        "repo": repo_full_name,
                        "pr_number": number,
                        "url": url,
                        "action": action,
                        "status": status,
                        "sender": sender,
                        "matched": False,
                    },
                )
                await self.db.commit()
                await self.db.refresh(item)
            except Exception:
                await self.db.rollback()
                raise
            return GitHubWebhookResponse(
                accepted=True,
                event=event,
                action=action,
                matched=False,
                triage_item_id=item.id,
            )

        try:
            status = await self._update_link_from_pr(
                link,
                action=action,
                delivery_id=delivery_id,
                repo_full_name=repo_full_name,
                pr=pr,
                sender=sender,
            )

            event_type = self._event_type(action, status)
            event_already_recorded = await self._event_exists(delivery_id)
            if not event_already_recorded:
                await self.task_service.record_task_event(
                    link.entity_id,
                    event_type,
                    self._event_payload(
                        action=action,
                        delivery_id=delivery_id,
                        repo_full_name=repo_full_name,
                        number=number,
                        url=url,
                        title=title,
                        status=status,
                        sender=sender,
                        link_id=link.id,
                        pr=pr,
                        ui_language=ui_language,
                    ),
                    actor_type="github",
                    idempotency_key=delivery_id,
                )

            automation_results = await self.automation_service.apply_rules(
                task_id=link.entity_id,
                github_event_type=event_type,
                delivery_id=delivery_id,
                context={
                    "action": action,
                    "repo": repo_full_name,
                    "pr_number": number,
                    "pr_title": title,
                    "url": url,
                    "status": status,
                    "sender": sender,
                    "external_link_id": link.id,
                },
                commit=False,
            )

            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type=event_type.replace("github_pr_", "github.pr_"),
                entity_type="task",
                entity_id=link.entity_id,
                data={
                    "task_id": link.entity_id,
                    "external_link_id": link.id,
                    "repo": repo_full_name,
                    "pr_number": number,
                    "url": url,
                    "action": action,
                    "status": status,
                    "sender": sender,
                    "matched": True,
                    "automation_results": [
                        result.model_dump(mode="json")
                        if hasattr(result, "model_dump")
                        else dict(result)
                        for result in automation_results
                    ],
                },
            )
            await self.db.commit()
            await self.db.refresh(link)
        except Exception:
            await self.db.rollback()
            raise
        return GitHubWebhookResponse(
            accepted=True,
            event=event,
            action=action,
            matched=True,
            external_link_id=link.id,
            task_id=link.entity_id,
            automation_results=automation_results,
        )
